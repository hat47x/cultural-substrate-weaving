#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSIONED_BRANCH = re.compile(r"^(develop|release)/v(?P<version>\d+\.\d+\.\d+)$")
VERSIONED_PREFIXES = ("develop/v", "release/v")


def expected_version(branch: str) -> str | None:
    """Return the version encoded by a versioned branch, or None when not applicable."""
    match = VERSIONED_BRANCH.fullmatch(branch)
    if match:
        return match.group("version")
    if branch.startswith(VERSIONED_PREFIXES):
        raise ValueError(
            f"Malformed version branch: {branch}; expected develop/vX.Y.Z or release/vX.Y.Z"
        )
    return None


def check_branch_version(branch: str, version: str) -> None:
    """Raise ValueError when a versioned branch and VERSION disagree."""
    expected = expected_version(branch)
    if expected is None:
        return

    actual = version.strip()
    if actual != expected:
        raise ValueError(
            f"VERSION mismatch: branch {branch} expects {expected}, found {actual}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that develop/vX.Y.Z or release/vX.Y.Z matches VERSION."
    )
    parser.add_argument("--ref", required=True, help="Git branch/ref name to validate")
    parser.add_argument(
        "--version-file",
        type=Path,
        default=Path("VERSION"),
        help="Path to VERSION file (default: VERSION)",
    )
    args = parser.parse_args()

    try:
        check_branch_version(
            args.ref,
            args.version_file.read_text(encoding="utf-8"),
        )
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
