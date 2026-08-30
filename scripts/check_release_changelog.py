#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DATE = r"\d{4}-\d{2}-\d{2}"


def release_headings(text: str, version: str) -> list[str]:
    pattern = re.compile(rf"^## {re.escape(version)} — {DATE}$")
    return [line for line in text.splitlines() if pattern.fullmatch(line)]


def check_release_heading(text: str, version: str) -> None:
    matches = release_headings(text, version)
    if not matches:
        raise ValueError(
            f"CHANGELOG release boundary missing: expected '## {version} — YYYY-MM-DD'"
        )
    if len(matches) > 1:
        raise ValueError(
            f"CHANGELOG release boundary duplicated for version {version}: {len(matches)} headings"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Require an explicit dated CHANGELOG heading for a release version."
    )
    parser.add_argument("--version", required=True, help="Release version without the v prefix")
    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
        help="Path to CHANGELOG.md (default: CHANGELOG.md)",
    )
    args = parser.parse_args()

    try:
        text = args.changelog.read_text(encoding="utf-8")
        check_release_heading(text, args.version)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
