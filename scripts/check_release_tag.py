#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from check_release_changelog import check_release_heading
from common import git_head

VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")


def validate_tag_against_version(tag: str, version: str) -> list[str]:
    errors: list[str] = []
    version = version.strip()

    if not VERSION_PATTERN.fullmatch(version):
        errors.append(f"VERSION must be X.Y.Z: {version!r}")
        return errors

    expected_tag = f"v{version}"
    if not TAG_PATTERN.fullmatch(tag):
        errors.append(f"release tag must be vX.Y.Z: {tag!r}")
    if tag != expected_tag:
        errors.append(f"release tag mismatch: {tag} != {expected_tag}")
    return errors


def validate_release_tag(tag: str, version: str, manifest_version: str) -> list[str]:
    version = version.strip()
    manifest_version = manifest_version.strip()
    errors = validate_tag_against_version(tag, version)
    if manifest_version != version:
        errors.append(
            f"release manifest version mismatch: {manifest_version} != {version}"
        )
    return errors


def validate_release_publication(
    tag: str,
    version: str,
    manifest_version: str,
    manifest_source_commit: str,
    current_head: str,
    changelog_text: str,
) -> list[str]:
    """Validate the publication-time tag contract against the exact local release commit."""
    version = version.strip()
    errors = validate_release_tag(tag, version, manifest_version)
    if manifest_source_commit != current_head:
        errors.append(
            "release manifest source_commit mismatch at tag gate: "
            f"{manifest_source_commit} != {current_head}"
        )
    try:
        check_release_heading(changelog_text, version)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def read_manifest_version(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("release manifest must be a JSON object")
    value = data.get("version")
    if not isinstance(value, str) or not value:
        raise ValueError("release manifest version must be a non-empty string")
    return value


def read_manifest_source_commit(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("release manifest must be a JSON object")
    value = data.get("source_commit")
    if not isinstance(value, str) or not value:
        raise ValueError("release manifest source_commit must be a non-empty string")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that a release tag matches VERSION and the final release manifest, "
            "that the manifest was produced from the current HEAD, and that CHANGELOG "
            "has a dated boundary for the release version."
        )
    )
    parser.add_argument("--tag", required=True, help="Release tag to validate, for example v0.5.0")
    parser.add_argument(
        "--version-file",
        type=Path,
        default=Path("VERSION"),
        help="Path to VERSION (default: VERSION)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("dist/release-manifest.json"),
        help="Path to the final release manifest",
    )
    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
        help="Path to CHANGELOG.md (default: CHANGELOG.md)",
    )
    args = parser.parse_args()

    try:
        version = args.version_file.read_text(encoding="utf-8")
        manifest_version = read_manifest_version(args.manifest)
        manifest_source_commit = read_manifest_source_commit(args.manifest)
        current_head = git_head()
        changelog_text = args.changelog.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = validate_release_publication(
        args.tag,
        version,
        manifest_version,
        manifest_source_commit,
        current_head,
        changelog_text,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Release tag {args.tag} matches VERSION and the final release manifest, "
        "the manifest source_commit matches the current HEAD, and the CHANGELOG "
        "release boundary is frozen."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
