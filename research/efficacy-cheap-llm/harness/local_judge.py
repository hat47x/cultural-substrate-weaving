"""SemIf-style local judge: read option probabilities off a frozen local LLM (ollama).

Everything that is identical within one task (material, key, signature, trap) comes
first and is processed once per task (`prefill`), because ollama keeps a recurrent-state
checkpoint only at the end of the previous prompt; Qwen3.5 cannot reuse an arbitrary
prefix otherwise. Decisions then reuse that checkpoint and only process the five
questions and the fixed option text. The answer is one letter; probabilities come from
the log-probabilities of the first generated token. The prompt is built in raw mode
with the Qwen chat markers, thinking switched off.
"""

import json
import math
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge  # noqa: E402

OLLAMA = "http://localhost:11434"
SYSTEM = "あなたは厳密で一貫した判定者です。指示された形式で、選択肢の記号1文字だけを答えます。"
INSTR = (
    "分析者の問いのうち、『鍵に到達する問いが調べるべき固有の要素』を直接調べているものがあるかを、厳しく判定する。"
    "要素を名指すか明確に前提とした問いだけを直接とする。典型的な説明を疑うだけの問い、一般的な原因探しの問い、"
    "隣接する話題の問いは直接としない。"
)
OPTIONS = {
    "A": "direct: 問いのいずれかが、固有の要素を直接調べている",
    "B": "partial: 固有の要素の一部に触れるか隣接する方向だが、要素そのものは調べていない",
    "C": "none: 該当する問いがない。典型的な説明の範囲の問いだけである",
}
LABEL_TO_SCORE = {"A": 2, "B": 1, "C": 0}

HEAD_TMPL = "<|im_start|>system\n" + SYSTEM + "<|im_end|>\n<|im_start|>user\n"
TAIL = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def prefix(task: dict) -> str:
    return (
        f"【状況】\n{task['material']}\n\n【鍵】\n{task['key']}\n\n"
        f"【鍵に到達する問いが調べるべき固有の要素】\n{task.get('signature', '')}\n\n"
        f"【典型的だが鍵に届かない説明】\n{task['trap']}\n\n"
    )


def suffix(qs: list[dict]) -> str:
    opts = "\n".join(f"{k}: {v}" for k, v in OPTIONS.items())
    return (
        f"【分析者の問い】\n{judge.fmt_questions(qs, with_basis=False)}\n\n"
        f"判定: {INSTR}\n\n選択肢:\n{opts}\n\nA、B、Cのどれか1文字だけで答えてください。"
    )


def _generate(model: str, prompt: str, n: int, timeout: int = 900) -> dict:
    body = {
        "model": model, "prompt": prompt, "raw": True, "stream": False, "think": False,
        "logprobs": True, "top_logprobs": 12, "keep_alive": "60m",
        "options": {"temperature": 0, "num_predict": n, "num_ctx": 6144},
    }
    req = urllib.request.Request(OLLAMA + "/api/generate", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def prefill(model: str, task: dict) -> float:
    """Process the per-task shared prefix once so its checkpoint can be reused."""
    t0 = time.time()
    _generate(model, HEAD_TMPL + prefix(task), 1)
    return time.time() - t0


def ask(model: str, task: dict, qs: list[dict]) -> dict:
    t0 = time.time()
    out = _generate(model, HEAD_TMPL + prefix(task) + suffix(qs) + TAIL, 1)
    secs = time.time() - t0
    lp = out.get("logprobs") or []
    cand = {}
    if lp:
        for t in lp[0].get("top_logprobs", []):
            tok = t["token"].strip().upper()
            if tok in OPTIONS:
                cand[tok] = max(cand.get(tok, -1e9), t["logprob"])
    base = {"secs": secs, "eval": out.get("prompt_eval_count"), "cached": out.get("prompt_eval_cached_count")}
    if not cand:
        return {"label": None, "p": {}, "text": out.get("response", ""), **base}
    z = sum(math.exp(v) for v in cand.values())
    p = {k: math.exp(v) / z for k, v in cand.items()}
    label = max(p, key=p.get)
    return {"label": label, "score": LABEL_TO_SCORE[label], "p": p, **base}
