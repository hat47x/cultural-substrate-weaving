#!/usr/bin/env python3
"""Run the complete-checkout research gate on one clean validation commit.

This runner does not mutate the production descriptor and does not create
repository evidence. It pins the current HEAD as validation commit V, executes
the four descriptor-required promotion commands plus one runner-owned
translation idempotence guard, refuses any step that changes repository identity
or leaves a non-ignored working-tree diff, and only then writes an ignored
`.tmp/` candidate record for the later evidence-only commit workflow.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
OUTPUT_DIR = ROOT / ".tmp" / "research-complete-checkout"

STATE_TRANSITION_LABEL = "translation research state transition"
REQUIRED_GATE_COMMANDS: tuple[str, ...] = (
    "make update-en-hashes",
    "make research-skill-check",
    "make build",
    "make check",
)

# The execution sequence contains one runner-owned idempotence guard that is
# deliberately not part of descriptor.required_commands. Its PASS marker is
# still required in durable execution evidence.
COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("make update-en-hashes", ("make", "update-en-hashes")),
    (
        STATE_TRANSITION_LABEL,
        (sys.executable, "scripts/mark_research_translation_refresh_synchronized.py"),
    ),
    ("make research-skill-check", ("make", "research-skill-check")),
    ("make build", ("make", "build")),
    ("make check", ("make", "check")),
)

RunCommand = Callable[[Path, Sequence[str]], int]
ReadText = Callable[[Path], str]


def _run_command(root: Path, argv: Sequence[str]) -> int:
    return subprocess.run(list(argv), cwd=root, check=False).returncode


def _git_text(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _head(root: Path) -> str:
    return _git_text(root, "rev-parse", "HEAD").lower()


def _status(root: Path) -> str:
    return _git_text(root, "status", "--porcelain", "--untracked-files=all")


def _descriptor(root: Path) -> dict:
    return json.loads((root / DESCRIPTOR_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))


def _valid_sha(value: str) -> bool:
    return len(value) == 40 and all(ch in "0123456789abcdef" for ch in value)


def candidate_record(execution_commit: str) -> str:
    return (
        "# P4 Complete-Checkout Execution Candidate\n\n"
        "Status: **candidate / not yet repository evidence**\n\n"
        f"execution commit: {execution_commit}\n"
        "make update-en-hashes: PASS\n"
        "translation research state transition: PASS\n"
        "make research-skill-check: PASS\n"
        "make build: PASS\n"
        "make check: PASS\n"
        "production promotion authorization: NO\n\n"
        "This file was generated under `.tmp/`. It is not durable evidence until "
        "reviewed and recorded through the evidence-only child commit contract.\n"
    )


def candidate_execution_commit(record: str) -> str | None:
    line = next(
        (line for line in record.splitlines() if line.startswith("execution commit:")),
        "",
    )
    value = line.partition(":")[2].strip().lower()
    return value if _valid_sha(value) else None


def validate_candidate_recording_state(
    record: str,
    current_head: str,
    current_status: str,
) -> list[str]:
    errors: list[str] = []
    normalized_head = current_head.lower()
    if not _valid_sha(normalized_head):
        errors.append("candidate recording requires a 40-character lowercase current HEAD")
    execution_commit = candidate_execution_commit(record)
    if execution_commit is None:
        errors.append("candidate record does not contain a valid execution commit")
    elif _valid_sha(normalized_head) and execution_commit != normalized_head:
        errors.append(
            "candidate record execution commit no longer matches current HEAD; "
            "repository identity changed after validation"
        )
    if current_status:
        errors.append(
            "candidate recording requires a clean working tree after validation"
        )
    return errors


def validate_candidate_recording_head(record: str, current_head: str) -> list[str]:
    """Backward-compatible helper for callers that only need HEAD binding."""

    return validate_candidate_recording_state(record, current_head, "")


def validate_preconditions(root: Path, descriptor: dict, *, head: str, status: str) -> list[str]:
    errors: list[str] = []
    if not _valid_sha(head):
        errors.append("current HEAD is not a 40-character lowercase commit SHA")
    if status:
        errors.append("complete-checkout runner requires a clean working tree")

    gate = descriptor.get("complete_checkout_validation")
    if not isinstance(gate, dict):
        errors.append("production descriptor must declare complete_checkout_validation")
        return errors
    if gate.get("status") != "blocked-not-run":
        errors.append("complete-checkout runner requires descriptor status blocked-not-run")

    required = gate.get("required_commands")
    if required != list(REQUIRED_GATE_COMMANDS):
        errors.append(
            "descriptor required_commands does not match declared promotion command authority"
        )

    return errors


def execute_gate(
    root: Path,
    *,
    run_command: RunCommand = _run_command,
    head_reader: ReadText = _head,
    status_reader: ReadText = _status,
    descriptor: dict | None = None,
) -> tuple[int, str | None, list[str]]:
    """Execute the declared commands plus guard and return (code, candidate, messages)."""

    messages: list[str] = []
    try:
        validation_commit = head_reader(root)
        initial_status = status_reader(root)
        descriptor_value = descriptor if descriptor is not None else _descriptor(root)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return 2, None, [f"complete-checkout preflight failed: {exc}"]

    errors = validate_preconditions(
        root,
        descriptor_value,
        head=validation_commit,
        status=initial_status,
    )
    if errors:
        return 2, None, errors

    for label, argv in COMMANDS:
        messages.append(f"RUN {label}")
        code = run_command(root, argv)
        if code != 0:
            messages.append(f"FAIL {label}: exit {code}")
            return code, None, messages

        try:
            current_head = head_reader(root)
            current_status = status_reader(root)
        except (OSError, subprocess.CalledProcessError) as exc:
            messages.append(f"FAIL {label}: repository state check failed: {exc}")
            return 2, None, messages

        if current_head != validation_commit:
            messages.append(
                f"FAIL {label}: HEAD changed during validation ({validation_commit} -> {current_head})"
            )
            return 2, None, messages
        if current_status:
            messages.append(
                f"FAIL {label}: command left repository changes; validated commit V is incomplete"
            )
            return 2, None, messages
        messages.append(f"PASS {label}")

    return 0, candidate_record(validation_commit), messages


def main() -> int:
    code, record, messages = execute_gate(ROOT)
    for message in messages:
        print(message)
    if code != 0 or record is None:
        return code or 2

    try:
        current_head = _head(ROOT)
        current_status = _status(ROOT)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL candidate recording: cannot re-read repository state: {exc}")
        return 2

    errors = validate_candidate_recording_state(record, current_head, current_status)
    if errors:
        for error in errors:
            print(f"FAIL candidate recording: {error}")
        return 2

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"P4-COMPLETE-CHECKOUT-PASS-{current_head[:12]}.md"
    output.write_text(record, encoding="utf-8")
    print(f"Candidate record written to {output.relative_to(ROOT)}")
    print("No descriptor or tracked execution evidence was modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
