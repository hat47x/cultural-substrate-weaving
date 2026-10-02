"""Thin cached LLM caller for the cheap-model CSW efficacy study.

Providers: DeepSeek direct API and OpenRouter. Tokens are read from local/ at call
time and never printed. Every call is cached on disk (keyed by request content plus
an explicit `tag`, so repeated samples use different tags). A hard USD budget guard
stops the run before it overspends.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "local"
WORK = LOCAL / "efficacy-cheap-llm"
CACHE = WORK / "cache"
LEDGER = WORK / "ledger.jsonl"

PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/chat/completions",
        "token_file": LOCAL / "DEEPSEEK_TOKEN.TXT",
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "token_file": LOCAL / "OPENROUTER_TOKEN.txt",
    },
}

# Conservative USD per million tokens (input, output). Real prices are lower for
# the flash models; over-estimating keeps the budget guard safe.
PRICE = {
    "deepseek-v4-flash": (0.30, 1.20),
    "deepseek-v4-pro": (0.60, 1.80),
}
FREE_SUFFIX = ":free"

import os
BUDGET_USD = float(os.environ.get("CSW_BUDGET_USD", "0.50"))  # per-process cap; raise explicitly
_lock = threading.Lock()
_spent = {"usd": 0.0}


def _token(provider: str) -> str:
    return PROVIDERS[provider]["token_file"].read_text(encoding="utf-8").strip()


def _cost(model: str, usage: dict) -> float:
    if model.endswith(FREE_SUFFIX):
        return 0.0
    pin, pout = PRICE.get(model, (1.0, 3.0))
    return (usage.get("prompt_tokens", 0) * pin + usage.get("completion_tokens", 0) * pout) / 1e6


def spent() -> float:
    return _spent["usd"]


def _key(provider: str, model: str, messages: list, params: dict, tag: str) -> str:
    blob = json.dumps([provider, model, messages, params, tag], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def call(
    provider: str,
    model: str,
    messages: list[dict],
    *,
    tag: str = "",
    max_tokens: int = 1500,
    temperature: float = 1.0,
    thinking: bool = False,
    json_mode: bool = False,
    retries: int = 6,
    timeout: int = 240,
) -> dict:
    """Return {text, usage, cached}. Raises RuntimeError after retries."""
    params = {"max_tokens": max_tokens, "temperature": temperature, "thinking": thinking, "json": json_mode}
    key = _key(provider, model, messages, params, tag)
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{key}.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cached"] = True
        return data

    with _lock:
        if _spent["usd"] >= BUDGET_USD:
            raise RuntimeError(f"budget guard: estimated spend {_spent['usd']:.3f} USD reached {BUDGET_USD}")

    body: dict = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    if provider == "deepseek":
        body["thinking"] = {"type": "enabled" if thinking else "disabled"}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    data_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")

    last = ""
    for attempt in range(retries):
        req = urllib.request.Request(
            PROVIDERS[provider]["url"],
            data=data_bytes,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_token(provider)}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                api = json.loads(r.read().decode("utf-8"))
            if "error" in api:
                raise urllib.error.URLError(json.dumps(api["error"], ensure_ascii=False)[:300])
            msg = api["choices"][0]["message"]
            text = msg.get("content") or ""
            usage = api.get("usage", {})
            out = {"text": text, "usage": usage, "model": api.get("model", model), "cached": False}
            cost = _cost(model, usage)
            with _lock:
                _spent["usd"] += cost
                with LEDGER.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"t": time.time(), "model": model, "usage": usage, "cost": cost}) + "\n")
            path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
            return out
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
            if e.code in (400, 401, 402, 403, 404):
                raise RuntimeError(last)
        except Exception as e:  # network, JSON, provider error payload
            last = f"{type(e).__name__}: {str(e)[:300]}"
        time.sleep(min(60, 3 * (2 ** attempt)))
    raise RuntimeError(f"call failed after {retries} tries: {last}")


def parse_json(text: str):
    """Extract the first JSON object/array from model text; None if impossible."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = text.find(opener), text.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(text[i : j + 1])
            except json.JSONDecodeError:
                continue
    return None
