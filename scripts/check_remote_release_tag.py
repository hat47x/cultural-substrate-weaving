#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

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
        result = subprocess.run(
            ["git", "rev-parse", "FETCH_HEAD^{commit}"],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot resolve remote release tag {tag}: {exc}") from exc
    value = result.stdout.strip()
    if not value:
        raise RuntimeError(f"cannot resolve remote release tag {tag}: empty commit")
    return value


def validate_remote_tag_commit(expected_commit: str, actual_commit: str) -> list[str]:
    if expected_commit == actual_commit:
        return []
    return [
        "remote release tag commit mismatch: "
        f"{actual_commit} != manifest source_commit {expected_commit}"
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve a remote release tag to its commit and compare it with the final release manifest source commit."
        )
    )
    parser.add_argument("--tag", required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("dist/release-manifest.json"),
    )
    parser.add_argument("--remote", default="origin")
    args = parser.parse_args()

    try:
        expected_commit = read_source_commit(args.manifest)
        actual_commit = resolve_remote_tag_commit(args.tag, args.remote)
    except (OSError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = validate_remote_tag_commit(expected_commit, actual_commit)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Remote release tag {args.tag} resolves to manifest source commit {expected_commit}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
