"""Render an unprimed requirements-review packet from frozen target material.

This is an input rendering aid, not a review engine or an efficacy test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


FORMAT = "csw.precontact-review-target/v1"
VISIBLE_KEYS = ("title", "context", "provided_information", "not_provided", "review_request")


def visible_target(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict) or raw.get("format") != FORMAT:
        raise ValueError(f"target format must be {FORMAT}")
    data: dict[str, Any] = {}
    for key in VISIBLE_KEYS:
        value = raw.get(key)
        if key in {"provided_information", "not_provided"}:
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                raise ValueError(f"{key} must be a nonempty list of nonempty strings")
        elif not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a nonempty string")
        data[key] = value
    return data


def fingerprint(visible: dict[str, Any]) -> str:
    stable_bytes = json.dumps(
        visible, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(stable_bytes).hexdigest()


def render_packet(raw: dict[str, Any]) -> str:
    visible = visible_target(raw)
    notes = "\n".join(f"- {item}" for item in visible["provided_information"])
    unknowns = "\n".join(f"- {item}" for item in visible["not_provided"])
    return (
        f"# {visible['title']}\n\n"
        "以下は初回レビュー用に与えられた情報です。記載された事項を実装確認済みの事実とみなさないでください。\n\n"
        f"{visible['context']}\n\n"
        f"## 事前に与えられた事項\n\n{notes}\n\n"
        f"## まだ提供されていない情報\n\n{unknowns}\n\n"
        f"## 依頼\n\n{visible['review_request']}\n\n"
        "最初に自然に選ぶ確認方法と、その方法を選んだ理由も明記してください。"
        "情報不足により確定できないこと、追加資料が必要なことは区別してください。"
        "この段階では方法を指定せず、対象側の根拠を創作しないでください。\n\n"
        f"入力指紋（SHA-256）: {fingerprint(visible)}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="frozen target JSON")
    parser.add_argument("--output", type=Path, help="write a stand-alone reviewer packet")
    args = parser.parse_args()
    target = json.loads(args.target.read_text(encoding="utf-8"))
    content = render_packet(target)
    if args.output is None:
        print(content, end="")
    else:
        args.output.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
