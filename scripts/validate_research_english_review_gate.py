#!/usr/bin/env python3
"""Validate the research-stage English sibling Skill independent-review gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
EXPECTED_PACKET = (
    "research/skill-prototypes/"
    "P4-ENGLISH-INDEPENDENT-REVIEW-PACKET-2026-09-07.md"
)
ALLOWED_STATUS = {"pending", "completed"}


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _existing_file(root: Path, value: object) -> Path | None:
    if not _safe_repo_relative(value):
        return None
    path = root / str(value)
    return path if path.is_file() else None


def validate_english_review_gate(root: Path, descriptor: dict) -> list[str]:
    errors: list[str] = []
    gate = descriptor.get("english_independent_review")
    if not isinstance(gate, dict):
        return ["production descriptor must declare english_independent_review"]

    status = gate.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("english_independent_review.status must be pending or completed")

    packet = gate.get("packet")
    if packet != EXPECTED_PACKET:
        errors.append(
            "english_independent_review.packet must reference the canonical review packet"
        )
    packet_path = _existing_file(root, packet)
    if packet_path is None:
        errors.append("English independent review packet is missing or unsafe")
    else:
        text = packet_path.read_text(encoding="utf-8")
        for marker in (
            "review not yet completed",
            "Layer 1 必須不変条件",
            "Layer 2 必須不変条件",
            "Cross-layer査読",
            "production promotion全体の承認ではない",
        ):
            if marker not in text:
                errors.append(f"English review packet missing required marker: {marker}")

    completed_review = gate.get("completed_review")
    if status == "pending":
        if completed_review is not None:
            errors.append(
                "pending English independent review must not declare completed_review"
            )
    elif status == "completed":
        review_path = _existing_file(root, completed_review)
        if review_path is None:
            errors.append(
                "completed English independent review must reference an existing safe review record"
            )
        elif review_path == packet_path:
            errors.append("completed review record must be separate from the review packet")
        else:
            review_text = review_path.read_text(encoding="utf-8")
            for marker in (
                "reviewer:",
                "review date:",
                "Layer 1:",
                "Layer 2:",
                "Cross-layer ownership:",
                "KJ lineage / naming:",
                "Promotion recommendation:",
                "Reviewed commit / blob refs:",
            ):
                if marker not in review_text:
                    errors.append(
                        f"completed English review record missing required marker: {marker}"
                    )

    if gate.get("production_promotion_authorized") is not False:
        errors.append(
            "English independent review gate must not authorize production promotion by itself"
        )

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"English independent review gate validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_english_review_gate(ROOT, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research English independent review gate validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
