#!/usr/bin/env python3
"""Validate the research-stage translation refresh state without updating hashes.

This gate intentionally distinguishes bilingual semantic editing from the later
translation-manifest refresh. In pending state it proves that the stale set is
explicit and bounded; in synchronized state it requires no stale files.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"
)
EXPECTED_SCHEMA = "csw.translation-refresh-status/v1"
ALLOWED_STATUS = {"pending-review-hash-refresh", "synchronized"}


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_translation_refresh_state(
    root: Path,
    status: dict,
    manifest: dict,
) -> list[str]:
    errors: list[str] = []

    if status.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"translation refresh schema must be {EXPECTED_SCHEMA}")

    state = status.get("status")
    if state not in ALLOWED_STATUS:
        errors.append(
            "translation refresh status must be pending-review-hash-refresh or synchronized"
        )

    if status.get("locale") != "en-US":
        errors.append("translation refresh locale must remain en-US")

    if status.get("production_promotion_authorized") is not False:
        errors.append("translation refresh state must not authorize production promotion")

    human_record = status.get("human_record")
    if not _safe_repo_relative(human_record) or not (root / str(human_record)).is_file():
        errors.append("translation refresh human_record must be an existing safe repository file")

    manifest_path_value = status.get("manifest")
    if manifest_path_value != "i18n/translation-manifest.json":
        errors.append("translation refresh state must point to i18n/translation-manifest.json")

    expected_stale_raw = status.get("expected_stale_files")
    if not isinstance(expected_stale_raw, list) or not all(
        isinstance(item, str) and item for item in expected_stale_raw
    ):
        errors.append("expected_stale_files must be a nonempty string list while pending")
        expected_stale: set[str] = set()
    else:
        if len(expected_stale_raw) != len(set(expected_stale_raw)):
            errors.append("expected_stale_files must not contain duplicates")
        expected_stale = set(expected_stale_raw)

    if state == "synchronized" and expected_stale:
        errors.append("synchronized translation refresh state must have no expected_stale_files")
    if state == "pending-review-hash-refresh" and not expected_stale:
        errors.append("pending translation refresh state must name at least one expected stale file")

    files = manifest.get("files")
    if not isinstance(files, dict):
        return errors + ["translation manifest files must be an object"]

    manifest_names = set(files)
    unknown_expected = expected_stale - manifest_names
    if unknown_expected:
        errors.append(
            "expected_stale_files contains files not tracked by translation manifest: "
            + ", ".join(sorted(unknown_expected))
        )

    stale: set[str] = set()
    for relative, entry in files.items():
        if not isinstance(relative, str) or not _safe_repo_relative(relative):
            errors.append(f"translation manifest contains unsafe file path: {relative!r}")
            continue
        if not isinstance(entry, dict):
            errors.append(f"translation manifest entry must be an object: {relative}")
            continue

        ja_path = root / "src" / "ja-JP" / relative
        en_path = root / "src" / "en-US" / relative
        if not ja_path.is_file():
            errors.append(f"canonical Japanese file missing: src/ja-JP/{relative}")
            continue
        if entry.get("en_present") is True and not en_path.is_file():
            errors.append(f"declared English translation missing: src/en-US/{relative}")

        current_ja = _sha256(ja_path)
        tracked_ja = entry.get("ja_sha256")
        tracked_en_source = entry.get("en_source_ja_sha256")
        if not isinstance(tracked_ja, str) or len(tracked_ja) != 64:
            errors.append(f"invalid ja_sha256 in translation manifest: {relative}")
            continue
        if not isinstance(tracked_en_source, str) or len(tracked_en_source) != 64:
            errors.append(f"invalid en_source_ja_sha256 in translation manifest: {relative}")
            continue

        if current_ja != tracked_ja:
            stale.add(relative)

        if relative not in expected_stale:
            if current_ja != tracked_en_source:
                errors.append(
                    f"unexpected English source-hash drift outside pending scope: {relative}"
                )
        elif state == "pending-review-hash-refresh":
            # Pending state should describe an old-but-coherent manifest snapshot,
            # not two conflicting historical hashes.
            if tracked_en_source != tracked_ja:
                errors.append(
                    f"pending stale entry has divergent tracked Japanese/source hashes: {relative}"
                )

    if stale != expected_stale:
        missing = expected_stale - stale
        extra = stale - expected_stale
        if missing:
            errors.append(
                "declared stale files are already synchronized or did not change: "
                + ", ".join(sorted(missing))
            )
        if extra:
            errors.append(
                "translation manifest has undeclared stale files: "
                + ", ".join(sorted(extra))
            )

    markers = status.get("english_markers")
    if not isinstance(markers, dict):
        errors.append("english_markers must be an object")
    else:
        if set(markers) != expected_stale:
            errors.append("english_markers must cover exactly expected_stale_files")
        for relative, required in markers.items():
            if not isinstance(required, list) or not required or not all(
                isinstance(marker, str) and marker for marker in required
            ):
                errors.append(f"English markers must be a nonempty string list: {relative}")
                continue
            en_path = root / "src" / "en-US" / relative
            if not en_path.is_file():
                continue
            text = en_path.read_text(encoding="utf-8")
            for marker in required:
                if marker not in text:
                    errors.append(
                        f"English translation missing declared tension marker in {relative}: {marker}"
                    )

    if status.get("refresh_command") != "make update-en-hashes":
        errors.append("translation refresh command must remain make update-en-hashes")

    followup = status.get("followup_commands")
    if followup != ["make research-skill-check", "make build", "make check"]:
        errors.append("translation refresh followup command sequence has drifted")

    invariants = status.get("invariants")
    if not isinstance(invariants, list):
        errors.append("translation refresh invariants must be a list")
    else:
        joined = "\n".join(item for item in invariants if isinstance(item, str))
        for fragment in (
            "do not guess or hand-enter translation hashes",
            "exact canonical files",
            "files outside expected_stale_files",
            "does not authorize production promotion",
        ):
            if fragment not in joined:
                errors.append(f"translation refresh invariant missing fragment: {fragment}")

    return errors


def main() -> int:
    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        manifest_path = ROOT / str(status.get("manifest", ""))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research translation refresh state validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_translation_refresh_state(ROOT, status, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research translation refresh state validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
