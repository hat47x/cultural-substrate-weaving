#!/usr/bin/env python3
"""Mark the research translation refresh state synchronized after hash refresh.

Run only after reviewing the bilingual semantic edits and running
`make update-en-hashes`. The helper refuses to change state unless every tracked
Japanese hash is synchronized and all declared English semantic markers remain
present. It does not alter the translation manifest itself.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transition_to_synchronized(root: Path, status: dict, manifest: dict) -> tuple[dict, list[str]]:
    errors: list[str] = []
    if status.get("status") not in {"pending-review-hash-refresh", "synchronized"}:
        errors.append("translation refresh state is not transitionable")
        return status, errors

    scope = status.get("scope_files")
    if not isinstance(scope, list) or not scope:
        errors.append("translation refresh scope_files is missing")
        return status, errors

    files = manifest.get("files")
    if not isinstance(files, dict):
        errors.append("translation manifest files must be an object")
        return status, errors

    stale: list[str] = []
    for relative, entry in files.items():
        if not isinstance(entry, dict):
            errors.append(f"invalid translation manifest entry: {relative}")
            continue
        ja_path = root / "src" / "ja-JP" / relative
        if not ja_path.is_file():
            errors.append(f"canonical Japanese file missing: {relative}")
            continue
        current = _sha256(ja_path)
        if current != entry.get("ja_sha256") or current != entry.get("en_source_ja_sha256"):
            stale.append(relative)

    if stale:
        errors.append(
            "translation manifest is not synchronized; run/review make update-en-hashes first: "
            + ", ".join(sorted(stale))
        )

    markers = status.get("english_markers")
    if not isinstance(markers, dict) or set(markers) != set(scope):
        errors.append("english_markers must cover the persistent scope_files before synchronization")
    else:
        for relative, required in markers.items():
            en_path = root / "src" / "en-US" / relative
            if not en_path.is_file():
                errors.append(f"English scope file missing: {relative}")
                continue
            text = en_path.read_text(encoding="utf-8")
            for marker in required:
                if marker not in text:
                    errors.append(
                        f"English translation missing declared tension marker in {relative}: {marker}"
                    )

    if errors:
        return status, errors

    updated = dict(status)
    updated["status"] = "synchronized"
    updated["expected_stale_files"] = []
    return updated, []


def main() -> int:
    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        manifest_path = ROOT / str(status.get("manifest", ""))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"translation refresh state transition failed: {exc}", file=sys.stderr)
        return 1

    updated, errors = transition_to_synchronized(ROOT, status, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    STATUS_PATH.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Research translation refresh state marked synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
