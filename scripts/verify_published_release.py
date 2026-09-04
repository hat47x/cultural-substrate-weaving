from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from check_release_tag import read_manifest_version, validate_tag_against_version


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path, label: str, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {label}: {exc}")
        return None


def _normalize_markdown(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def expected_assets(manifest_path: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    data = _read_json(manifest_path, "release manifest", errors)
    if not isinstance(data, dict):
        if data is not None:
            errors.append("release manifest must be a JSON object")
        return {}

    raw_files = data.get("files")
    if not isinstance(raw_files, list):
        errors.append("release manifest files must be an array")
        raw_files = []

    file_entries: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_files):
        if not isinstance(raw, dict):
            errors.append(f"release manifest files[{index}] must be an object")
            continue
        relative = raw.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append(f"release manifest files[{index}].path must be a non-empty string")
            continue
        file_entries[relative] = raw

    raw_assets = data.get("release_assets")
    if not isinstance(raw_assets, list):
        errors.append("release manifest release_assets must be an array")
        return {}

    dist = manifest_path.parent
    expected: dict[str, dict[str, Any]] = {}
    for index, relative in enumerate(raw_assets):
        if not isinstance(relative, str) or not relative:
            errors.append(f"release_assets[{index}] must be a non-empty string")
            continue
        if "\\" in relative:
            errors.append(f"release asset path must use POSIX separators: {relative}")
            continue
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts:
            errors.append(f"release asset path must stay inside the release root: {relative}")
            continue

        name = posix.name
        if not name:
            errors.append(f"release asset path must name a file: {relative}")
            continue
        if name in expected:
            errors.append(f"release asset basenames must be unique: {name}")
            continue

        if relative == "release-manifest.json":
            path = dist / relative
            if not path.is_file():
                errors.append(f"release manifest asset is missing locally: {relative}")
                continue
            expected[name] = {
                "bytes": path.stat().st_size,
                "digest": f"sha256:{file_sha256(path)}",
            }
            continue

        entry = file_entries.get(relative)
        if entry is None:
            errors.append(f"release asset has no manifest file entry: {relative}")
            continue
        byte_count = entry.get("bytes")
        sha256 = entry.get("sha256")
        if not isinstance(byte_count, int) or byte_count < 0:
            errors.append(f"release asset manifest byte count is invalid: {relative}")
            continue
        if not isinstance(sha256, str) or len(sha256) != 64:
            errors.append(f"release asset manifest sha256 is invalid: {relative}")
            continue
        expected[name] = {"bytes": byte_count, "digest": f"sha256:{sha256}"}

    return expected


def validate_published_release(
    manifest_path: Path,
    release_json_path: Path,
    expected_tag: str,
    expected_validation_note: str,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest_version = read_manifest_version(manifest_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"cannot validate release tag against manifest version: {exc}")
    else:
        errors.extend(validate_tag_against_version(expected_tag, manifest_version))

    expected = expected_assets(manifest_path, errors)
    release = _read_json(release_json_path, "published release JSON", errors)
    if not isinstance(release, dict):
        if release is not None:
            errors.append("published release JSON must be an object")
        return errors

    if release.get("tag_name") != expected_tag:
        errors.append(
            f"published release tag mismatch: {release.get('tag_name')} != {expected_tag}"
        )

    if release.get("draft") is not False:
        errors.append(f"published release must not be a draft: {release.get('draft')}")
    if release.get("prerelease") is not False:
        errors.append(f"published release must not be a prerelease: {release.get('prerelease')}")

    validation_note = _normalize_markdown(expected_validation_note)
    if not validation_note:
        errors.append("expected release validation note must not be empty")
    else:
        body = release.get("body")
        if not isinstance(body, str):
            errors.append("published release body must be a string")
        elif validation_note not in _normalize_markdown(body):
            errors.append("published release is missing the required validation disclosure note")

    raw_assets = release.get("assets")
    if not isinstance(raw_assets, list):
        errors.append("published release assets must be an array")
        return errors

    actual: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_assets):
        if not isinstance(raw, dict):
            errors.append(f"published release assets[{index}] must be an object")
            continue
        name = raw.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"published release assets[{index}].name must be a non-empty string")
            continue
        if name in actual:
            errors.append(f"duplicate published release asset name: {name}")
            continue
        actual[name] = raw

    expected_names = set(expected)
    actual_names = set(actual)
    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    if missing:
        errors.append(f"published release is missing manifest-declared assets: {missing}")
    if extra:
        errors.append(f"published release contains undeclared assets: {extra}")

    for name in sorted(expected_names & actual_names):
        wanted = expected[name]
        found = actual[name]
        if found.get("state") != "uploaded":
            errors.append(f"published release asset is not uploaded: {name}: {found.get('state')}")
        if found.get("size") != wanted["bytes"]:
            errors.append(
                f"published release asset size mismatch: {name}: {found.get('size')} != {wanted['bytes']}"
            )
        if found.get("digest") != wanted["digest"]:
            errors.append(
                f"published release asset digest mismatch: {name}: {found.get('digest')} != {wanted['digest']}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a published GitHub Release against the final release manifest and disclosure contract."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--release-json", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument(
        "--validation-note",
        type=Path,
        default=Path(".github/release-validation-note.md"),
        help="Required release disclosure note (default: .github/release-validation-note.md)",
    )
    args = parser.parse_args()

    try:
        validation_note = args.validation_note.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read release validation note: {exc}", file=sys.stderr)
        return 1

    errors = validate_published_release(
        args.manifest,
        args.release_json,
        args.tag,
        validation_note,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Published release {args.tag} matches the final release manifest and disclosure contract."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
