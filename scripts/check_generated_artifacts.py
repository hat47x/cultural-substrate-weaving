#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import ROOT

GENERATED_PATHS = (".claude-plugin", ".agents", "plugins")


def generated_artifact_changes(repo: Path = ROOT) -> list[str]:
    try:
        result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                *GENERATED_PATHS,
            ],
            cwd=repo,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot inspect generated artifact status: {exc}") from exc
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    try:
        changes = generated_artifact_changes()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if changes:
        print(
            "ERROR: generated distribution artifacts are not synchronized with Git after build. "
            "Regenerate them, review the changes, and commit the resulting .claude-plugin, .agents, and plugins files.",
            file=sys.stderr,
        )
        for change in changes:
            print(f"  {change}", file=sys.stderr)
        return 1

    print("Generated distribution artifacts are synchronized with Git")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
