#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

DATE = r"\d{4}-\d{2}-\d{2}"
UNRELEASED_HEADING = "## Unreleased"


def release_headings(text: str, version: str) -> list[str]:
    pattern = re.compile(rf"^## {re.escape(version)} — {DATE}$")
    return [line for line in text.splitlines() if pattern.fullmatch(line)]


def check_release_heading(text: str, version: str) -> None:
    lines = text.splitlines()
    matches = release_headings(text, version)
    if not matches:
        raise ValueError(
            f"CHANGELOG release boundary missing: expected '## {version} — YYYY-MM-DD'"
        )
    if len(matches) > 1:
        raise ValueError(
            f"CHANGELOG release boundary duplicated for version {version}: {len(matches)} headings"
        )

    release_date = matches[0].rsplit(" — ", 1)[1]
    try:
        date.fromisoformat(release_date)
    except ValueError as exc:
        raise ValueError(
            f"CHANGELOG release boundary has an invalid calendar date: {release_date}"
        ) from exc

    unreleased_indexes = [
        index for index, line in enumerate(lines) if line == UNRELEASED_HEADING
    ]
    if len(unreleased_indexes) != 1:
        raise ValueError(
            "CHANGELOG must keep exactly one '## Unreleased' heading after freezing the release boundary; "
            f"found {len(unreleased_indexes)}"
        )

    unreleased_index = unreleased_indexes[0]
    release_index = lines.index(matches[0])
    if unreleased_index > release_index:
        raise ValueError(
            "CHANGELOG '## Unreleased' must precede the frozen release boundary"
        )

    unreleased_body = lines[unreleased_index + 1 : release_index]
    if any(line.strip() for line in unreleased_body):
        raise ValueError(
            "CHANGELOG '## Unreleased' must be empty after freezing the release boundary; "
            "move release contents into the dated release section before publication"
        )

    next_section_index = next(
        (
            index
            for index in range(release_index + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    release_body = lines[release_index + 1 : next_section_index]
    if not any(line.strip() for line in release_body):
        raise ValueError(
            "CHANGELOG dated release section must contain release contents before publication"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Require one valid non-empty dated CHANGELOG section for a release version, "
            "with exactly one empty Unreleased section reserved for subsequent development."
        )
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
