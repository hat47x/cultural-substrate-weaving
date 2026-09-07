#!/usr/bin/env python3
"""Validate the research-stage complete-checkout execution gate."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
EXPECTED_BLOCKED_EVIDENCE = (
    "research/skill-prototypes/"
    "P4-COMPLETE-CHECKOUT-EXECUTION-STATUS-2026-09-07.md"
)
EXPECTED_COMMANDS = [
    "make update-en-hashes",
    "make research-skill-check",
    "make build",
    "make check",
]
ALLOWED_STATUS = {"blocked-not-run", "passed"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _existing_file(root: Path, value: object) -> Path | None:
    if not _safe_repo_relative(value):
        return None
    path = root / str(value)
    return path if path.is_file() else None


def _current_checkout_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip().lower()
    return value if HEX40.fullmatch(value) else None


def validate_complete_checkout_gate(
    root: Path,
    descriptor: dict,
    *,
    current_commit: str | None = None,
) -> list[str]:
    errors: list[str] = []
    gate = descriptor.get("complete_checkout_validation")
    if not isinstance(gate, dict):
        return ["production descriptor must declare complete_checkout_validation"]

    status = gate.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("complete_checkout_validation.status must be blocked-not-run or passed")

    commands = gate.get("required_commands")
    if commands != EXPECTED_COMMANDS:
        errors.append(
            "complete_checkout_validation.required_commands must remain the canonical command set"
        )

    evidence = gate.get("evidence")
    evidence_path = _existing_file(root, evidence)
    if evidence_path is None:
        errors.append("complete-checkout execution evidence is missing or unsafe")
    else:
        text = evidence_path.read_text(encoding="utf-8")
        if status == "blocked-not-run":
            if evidence != EXPECTED_BLOCKED_EVIDENCE:
                errors.append(
                    "blocked-not-run complete-checkout gate must reference the canonical blocked execution record"
                )
            for marker in (
                "Status: **blocked / not run**",
                "translation-manifest hash refresh:       NOT RUN",
                "translation research state transition:  NOT RUN",
                "complete-checkout research-skill-check: NOT RUN",
                "production build regeneration:          NOT RUN",
                "full repository make check:             NOT RUN",
                "production promotion authorization:     NO",
            ):
                if marker not in text:
                    errors.append(
                        f"blocked complete-checkout evidence missing required marker: {marker}"
                    )
        elif status == "passed":
            for marker in (
                "execution commit:",
                "make update-en-hashes: PASS",
                "translation research state transition: PASS",
                "make research-skill-check: PASS",
                "make build: PASS",
                "make check: PASS",
            ):
                if marker not in text:
                    errors.append(
                        f"passed complete-checkout evidence missing required marker: {marker}"
                    )
            commit_line = next(
                (line for line in text.splitlines() if line.startswith("execution commit:")),
                "",
            )
            commit = commit_line.partition(":")[2].strip().lower()
            if commit and not HEX40.fullmatch(commit):
                errors.append("passed complete-checkout execution commit must be a 40-char SHA")
            elif HEX40.fullmatch(commit):
                if current_commit is None:
                    errors.append(
                        "passed complete-checkout validation requires the current checkout HEAD"
                    )
                elif not HEX40.fullmatch(current_commit.lower()):
                    errors.append("current checkout HEAD must be a 40-char SHA")
                elif commit != current_commit.lower():
                    errors.append(
                        "passed complete-checkout execution commit must match current checkout HEAD"
                    )

    if gate.get("production_promotion_authorized") is not False:
        errors.append(
            "complete-checkout gate must not authorize production promotion by itself"
        )

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"complete-checkout gate validation failed: {exc}", file=sys.stderr)
        return 1

    gate = descriptor.get("complete_checkout_validation")
    current_commit = None
    if isinstance(gate, dict) and gate.get("status") == "passed":
        current_commit = _current_checkout_head(ROOT)

    errors = validate_complete_checkout_gate(
        ROOT,
        descriptor,
        current_commit=current_commit,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research complete-checkout execution gate validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
