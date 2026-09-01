#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys


class MainPushContractError(ValueError):
    pass


def parent_shas(parent_line: str) -> list[str]:
    return [value for value in parent_line.split() if value]


def check_main_push_parents(parent_line: str) -> None:
    parents = parent_shas(parent_line)
    if len(parents) < 2:
        raise MainPushContractError(
            "main push must point to a merge commit produced by a PR; "
            f"found {len(parents)} parent(s)"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reject direct single-parent pushes to main in the Git Flow repository contract."
    )
    parser.add_argument(
        "--parents",
        required=True,
        help="Whitespace-separated parent commit SHAs for the pushed main HEAD.",
    )
    args = parser.parse_args()

    try:
        check_main_push_parents(args.parents)
    except MainPushContractError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
