#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from check_release_changelog import check_release_heading
from check_release_tag import read_manifest_version, validate_tag_against_version
from common import ROOT

TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")


def read_source_commit(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("release manifest must be a JSON object")
    value = data.get("source_commit")
    if not isinstance(value, str) or not value:
        raise ValueError("release manifest source_commit must be a non-empty string")
    return value


def _resolve_fetched_commit(repo: Path, what: str) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "FETCH_HEAD^{commit}"],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot resolve {what}: {exc}") from exc
    value = result.stdout.strip()
    if not value:
        raise RuntimeError(f"cannot resolve {what}: empty commit")
    return value


def resolve_remote_tag_commit(
    tag: str,
    remote: str = "origin",
    repo: Path = ROOT,
) -> str:
    if not TAG_PATTERN.fullmatch(tag):
        raise ValueError(f"release tag must be vX.Y.Z: {tag!r}")
    try:
        subprocess.run(
            ["git", "fetch", "--quiet", "--no-tags", remote, f"refs/tags/{tag}"],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot resolve remote release tag {tag}: {exc}") from exc
    return _resolve_fetched_commit(repo, f"remote release tag {tag}")


def resolve_remote_main_commit(
    remote: str = "origin",
    repo: Path = ROOT,
) -> str:
    try:
        subprocess.run(
            ["git", "fetch", "--quiet", "--no-tags", remote, "refs/heads/main"],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot resolve remote main: {exc}") from exc
    return _resolve_fetched_commit(repo, "remote main")


def validate_remote_tag_commit(expected_commit: str, actual_commit: str) -> list[str]:
    if expected_commit == actual_commit:
        return []
    return [
        "remote release tag commit mismatch: "
        f"{actual_commit} != manifest source_commit {expected_commit}"
    ]


def validate_remote_main_history(
    expected_commit: str,
    remote_main_commit: str,
    repo: Path = ROOT,
) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", expected_commit, remote_main_commit],
            cwd=repo,
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        raise RuntimeError(f"cannot validate remote main history: {exc}") from exc
    if result.returncode == 0:
        return []
    if result.returncode == 1:
        return [
            "manifest source_commit is not present in remote main history: "
            f"{expected_commit} is not an ancestor of {remote_main_commit}"
        ]
    detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
    raise RuntimeError(f"cannot validate remote main history: {detail}")


def validate_remote_release_tag(
    tag: str,
    manifest_version: str,
    expected_commit: str,
    actual_commit: str,
) -> list[str]:
    errors = validate_tag_against_version(tag, manifest_version)
    errors.extend(validate_remote_tag_commit(expected_commit, actual_commit))
    return errors


def validate_remote_release_boundary(
    tag: str,
    manifest_version: str,
    expected_commit: str,
    actual_commit: str,
    remote_main_commit: str,
    changelog_text: str,
    repo: Path = ROOT,
) -> list[str]:
    errors = validate_remote_release_tag(
        tag,
        manifest_version,
        expected_commit,
        actual_commit,
    )
    errors.extend(validate_remote_main_history(expected_commit, remote_main_commit, repo))
    try:
        check_release_heading(changelog_text, manifest_version)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve a remote release tag and verify its version, commit provenance, "
            "remote-main history, and frozen CHANGELOG boundary against the final release manifest."
        )
    )
    parser.add_argument("--tag", required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("dist/release-manifest.json"),
    )
    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
    )
    parser.add_argument("--remote", default="origin")
    args = parser.parse_args()

    try:
        manifest_version = read_manifest_version(args.manifest)
        expected_commit = read_source_commit(args.manifest)
        changelog_text = args.changelog.read_text(encoding="utf-8")
        actual_commit = resolve_remote_tag_commit(args.tag, args.remote)
        remote_main_commit = resolve_remote_main_commit(args.remote)
        errors = validate_remote_release_boundary(
            args.tag,
            manifest_version,
            expected_commit,
            actual_commit,
            remote_main_commit,
            changelog_text,
        )
    except (OSError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Remote release tag {args.tag} matches manifest version {manifest_version}, "
        f"resolves to manifest source commit {expected_commit}, that commit is present "
        "in remote main history, and the CHANGELOG release boundary is frozen."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
