#!/usr/bin/env python3
"""Run one fail-closed OpenRouter free-tier request for research use."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY_ENV = "OPENROUTER_API_KEY"
REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_REPO_DIRS = (REPO_ROOT / ".tmp", REPO_ROOT / ".living-lab")
TRACKED_PRIVATE_PATHS = {(REPO_ROOT / ".living-lab" / "README.md").resolve()}


def is_free_model(model: str) -> bool:
    """Return True only for explicit free model slugs accepted by this runner."""
    return model == "openrouter/free" or model.endswith(":free")


def validate_payload(payload: Any) -> dict[str, Any]:
    """Validate request fields without making a network request."""
    if not isinstance(payload, dict):
        raise ValueError("request JSON must be an object")

    forbidden = {
        "model": "set the model with --model so the free-only check cannot be bypassed",
        "models": "model fallback arrays are disabled for this research runner",
        "plugins": "plugins are disabled because they may add cost or another confound",
        "web_search_options": "web search is disabled because it may add cost or another confound",
    }
    for field, reason in forbidden.items():
        if field in payload:
            raise ValueError(f"request field {field!r} is not allowed: {reason}")

    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("request JSON must contain a non-empty messages array")

    return payload


def load_payload(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read request JSON: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"request JSON is invalid: {exc}") from exc
    return validate_payload(data)


def build_request_body(model: str, payload: dict[str, Any]) -> bytes:
    if not is_free_model(model):
        raise ValueError(
            "--model must be 'openrouter/free' or an explicit model slug ending in ':free'"
        )
    body = dict(payload)
    body["model"] = model
    return json.dumps(body, ensure_ascii=False).encode("utf-8")


def resolve_output_path(path: Path) -> Path:
    """Resolve output and reject repository paths that are not private-by-default."""
    resolved = path.resolve() if path.is_absolute() else (Path.cwd() / path).resolve()

    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        return resolved

    if resolved in TRACKED_PRIVATE_PATHS:
        raise ValueError(
            "raw response output must not overwrite a tracked file inside a private workspace"
        )

    for private_dir in PRIVATE_REPO_DIRS:
        try:
            resolved.relative_to(private_dir.resolve())
            return resolved
        except ValueError:
            continue

    raise ValueError(
        "raw response output inside this repository must be under .tmp/ or .living-lab/; "
        "publish only a separately reviewed anonymized/abstracted record"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Send one OpenRouter request only after validating that the selected model "
            "is explicitly free and that no fallback or paid plugin fields are present."
        )
    )
    parser.add_argument("--model", required=True, help="openrouter/free or a :free model slug")
    parser.add_argument(
        "--request",
        type=Path,
        required=True,
        help=(
            "request JSON without model/key; keep private natural-work requests in an "
            "untracked/private location such as .tmp/openrouter/"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "path for the raw API response JSON; repository-local output is allowed only "
            "under .tmp/ or ignored .living-lab/ paths"
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="network timeout in seconds (default: 120)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the free-only request without reading an API key or using the network",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        payload = load_payload(args.request)
        body = build_request_body(args.model, payload)
    except ValueError as exc:
        print(f"OpenRouter free-tier request rejected: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("ok: free-only OpenRouter request is valid")
        return 0

    if args.output is None:
        print("OpenRouter free-tier request rejected: --output is required", file=sys.stderr)
        return 2

    try:
        output_path = resolve_output_path(args.output)
    except ValueError as exc:
        print(f"OpenRouter free-tier request rejected: {exc}", file=sys.stderr)
        return 2

    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        print(
            f"OpenRouter free-tier request rejected: {API_KEY_ENV} is not set",
            file=sys.stderr,
        )
        return 2

    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            response_body = response.read()
            status = getattr(response, "status", 200)
    except urllib.error.HTTPError as exc:
        print(f"OpenRouter request returned HTTP {exc.code}; no fallback attempted", file=sys.stderr)
        return 3
    except urllib.error.URLError as exc:
        print(f"OpenRouter request failed before a usable response: {exc.reason}", file=sys.stderr)
        return 4
    except TimeoutError:
        print("OpenRouter request timed out before a usable response", file=sys.stderr)
        return 4

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response_body)
    print(f"ok: HTTP {status}; raw response saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
