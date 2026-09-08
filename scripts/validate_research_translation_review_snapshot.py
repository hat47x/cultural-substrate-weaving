#!/usr/bin/env python3
"""Validate that bilingual semantic-review source bytes have not drifted."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"


def _safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_review_snapshot(root: Path, status: dict) -> list[str]:
    errors: list[str] = []
    scope = status.get("scope_files")
    blobs = status.get("reviewed_source_blobs")
    if not isinstance(scope, list) or not scope or not all(isinstance(x, str) and x for x in scope):
        return ["translation review snapshot requires nonempty scope_files"]
    if len(scope) != len(set(scope)):
        errors.append("translation review snapshot scope_files must not contain duplicates")
    if not isinstance(blobs, dict):
        return errors + ["translation review snapshot requires reviewed_source_blobs"]
    if set(blobs) != set(scope):
        errors.append("reviewed_source_blobs must cover exactly scope_files")

    for relative in scope:
        if not _safe_relative(relative):
            errors.append(f"unsafe translation review source path: {relative!r}")
            continue
        expected = blobs.get(relative)
        if not isinstance(expected, str) or len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
            errors.append(f"invalid reviewed source blob SHA: {relative}")
            continue
        source = root / "src" / "ja-JP" / relative
        if not source.is_file():
            errors.append(f"reviewed Japanese source missing: src/ja-JP/{relative}")
            continue
        current = _git_blob_sha(source)
        if current != expected:
            errors.append(
                f"Japanese source changed after bilingual semantic review: {relative} "
                f"({expected} -> {current})"
            )

    invariants = status.get("invariants")
    joined = "\n".join(x for x in invariants if isinstance(x, str)) if isinstance(invariants, list) else ""
    if "reviewed_source_blobs pins the exact Japanese source bytes" not in joined:
        errors.append("translation review snapshot invariant is missing")
    return errors


def main() -> int:
    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research translation review snapshot validation failed: {exc}", file=sys.stderr)
        return 1
    errors = validate_review_snapshot(ROOT, status)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Research translation review source snapshot validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
