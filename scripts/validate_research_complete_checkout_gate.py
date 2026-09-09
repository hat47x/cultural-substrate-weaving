#!/usr/bin/env python3
"""Validate the research-stage complete-checkout execution gate."""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_RELATIVE = Path(
    "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
DESCRIPTOR_PATH = ROOT / DESCRIPTOR_RELATIVE
EXPECTED_BLOCKED_EVIDENCE = (
    "research/skill-prototypes/"
    "P4-COMPLETE-CHECKOUT-EXECUTION-STATUS-2026-09-08.md"
)
EXPECTED_BINDING_CONTRACT = (
    "research/skill-prototypes/"
    "P4-COMPLETE-CHECKOUT-EVIDENCE-BINDING-2026-09-08.md"
)
EXECUTION_RECORD_PREFIX = PurePosixPath("research/skill-prototypes/execution")
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


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _current_checkout_head(root: Path) -> str | None:
    value = _run_git(root, "rev-parse", "HEAD")
    if value is None:
        return None
    value = value.lower()
    return value if HEX40.fullmatch(value) else None


def _current_checkout_first_parent(root: Path) -> str | None:
    value = _run_git(root, "rev-parse", "HEAD^1")
    if value is None:
        return None
    value = value.lower()
    return value if HEX40.fullmatch(value) else None


def _changed_paths(root: Path, execution_commit: str, current_commit: str) -> set[str] | None:
    value = _run_git(
        root,
        "diff",
        "--name-only",
        "--no-renames",
        execution_commit,
        current_commit,
        "--",
    )
    if value is None:
        return None
    return {line for line in value.splitlines() if line}


def _json_at_commit(root: Path, commit: str, relative: Path) -> dict | None:
    value = _run_git(root, "show", f"{commit}:{relative.as_posix()}")
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _path_exists_at_commit(root: Path, commit: str, relative: str) -> bool | None:
    if not _safe_repo_relative(relative):
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{commit}:{relative}"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode == 0:
        return True
    # The commit is independently proven by the parent relationship before this
    # value is used, so a nonzero result here means the path did not exist there.
    return False


def _execution_commit_from_record(text: str) -> str | None:
    line = next(
        (line for line in text.splitlines() if line.startswith("execution commit:")),
        "",
    )
    value = line.partition(":")[2].strip().lower()
    return value if HEX40.fullmatch(value) else None


def _is_execution_record_path(value: object) -> bool:
    if not _safe_repo_relative(value):
        return False
    path = PurePosixPath(str(value))
    prefix_parts = EXECUTION_RECORD_PREFIX.parts
    return (
        len(path.parts) > len(prefix_parts)
        and path.parts[: len(prefix_parts)] == prefix_parts
    )


def _validate_evidence_only_child(
    errors: list[str],
    *,
    descriptor: dict,
    execution_commit: str,
    evidence: str,
    current_first_parent: str | None,
    changed_paths_from_execution: set[str] | None,
    execution_descriptor: dict | None,
    evidence_existed_at_execution: bool | None,
) -> None:
    if current_first_parent is None:
        errors.append(
            "passed complete-checkout evidence requires the current checkout first parent"
        )
        return
    if current_first_parent.lower() != execution_commit:
        errors.append(
            "passed complete-checkout execution commit must be the current HEAD or its direct first parent"
        )
        return

    expected_paths = {DESCRIPTOR_RELATIVE.as_posix(), evidence}
    if changed_paths_from_execution is None:
        errors.append(
            "passed evidence-only child validation requires changed paths from execution commit"
        )
    elif changed_paths_from_execution != expected_paths:
        errors.append(
            "passed evidence-only recording commit may change only the production descriptor "
            f"and execution record; expected={sorted(expected_paths)!r}, "
            f"actual={sorted(changed_paths_from_execution)!r}"
        )

    if evidence_existed_at_execution is None:
        errors.append(
            "passed evidence-only child validation could not determine whether the execution record already existed"
        )
    elif evidence_existed_at_execution:
        errors.append(
            "passed execution record must be new in the evidence-only recording commit"
        )

    if not isinstance(execution_descriptor, dict):
        errors.append(
            "passed evidence-only child validation requires the production descriptor from the execution commit"
        )
        return

    previous = copy.deepcopy(execution_descriptor)
    current = copy.deepcopy(descriptor)
    previous_gate = previous.pop("complete_checkout_validation", None)
    current_gate = current.pop("complete_checkout_validation", None)

    if previous != current:
        errors.append(
            "evidence-only recording commit must not change production descriptor fields outside complete_checkout_validation"
        )

    if not isinstance(previous_gate, dict) or not isinstance(current_gate, dict):
        errors.append(
            "execution/current production descriptors must both declare complete_checkout_validation"
        )
        return

    if previous_gate.get("status") != "blocked-not-run":
        errors.append(
            "execution commit must retain complete_checkout_validation.status=blocked-not-run before evidence recording"
        )
    if previous_gate.get("evidence") != EXPECTED_BLOCKED_EVIDENCE:
        errors.append(
            "execution commit must retain the canonical blocked evidence before evidence recording"
        )

    normalized_current_gate = copy.deepcopy(current_gate)
    normalized_current_gate["status"] = previous_gate.get("status")
    normalized_current_gate["evidence"] = previous_gate.get("evidence")
    if normalized_current_gate != previous_gate:
        errors.append(
            "evidence-only recording commit may change only complete-checkout status and evidence path"
        )


def validate_complete_checkout_gate(
    root: Path,
    descriptor: dict,
    *,
    current_commit: str | None = None,
    current_first_parent: str | None = None,
    changed_paths_from_execution: set[str] | None = None,
    execution_descriptor: dict | None = None,
    evidence_existed_at_execution: bool | None = None,
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

    binding = gate.get("binding_contract")
    binding_path = _existing_file(root, binding)
    if binding != EXPECTED_BINDING_CONTRACT:
        errors.append(
            "complete_checkout_validation.binding_contract must reference the canonical evidence-binding contract"
        )
    if binding_path is None:
        errors.append("complete-checkout evidence-binding contract is missing or unsafe")
    else:
        binding_text = binding_path.read_text(encoding="utf-8")
        for marker in (
            "validated commit V",
            "evidence-only recording commit E",
            "Eのfirst parentはV",
            "translation hash/state transitionはevidence recording commitへ混ぜない",
            "production promotionを単独承認しない",
        ):
            if marker not in binding_text:
                errors.append(
                    f"complete-checkout evidence-binding contract missing required marker: {marker}"
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
                "checked-in translation refresh state: SYNCHRONIZED",
                "checked-in expected_stale_files: []",
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
            if not _is_execution_record_path(evidence):
                errors.append(
                    "passed complete-checkout evidence must live under research/skill-prototypes/execution/"
                )
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

            commit = _execution_commit_from_record(text)
            if commit is None:
                errors.append(
                    "passed complete-checkout execution commit must be a 40-char SHA"
                )
            elif current_commit is None:
                errors.append(
                    "passed complete-checkout validation requires the current checkout HEAD"
                )
            elif not HEX40.fullmatch(current_commit.lower()):
                errors.append("current checkout HEAD must be a 40-char SHA")
            elif commit != current_commit.lower():
                _validate_evidence_only_child(
                    errors,
                    descriptor=descriptor,
                    execution_commit=commit,
                    evidence=str(evidence),
                    current_first_parent=(
                        current_first_parent.lower()
                        if isinstance(current_first_parent, str)
                        else None
                    ),
                    changed_paths_from_execution=changed_paths_from_execution,
                    execution_descriptor=execution_descriptor,
                    evidence_existed_at_execution=evidence_existed_at_execution,
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
    current_first_parent = None
    changed_paths_from_execution = None
    execution_descriptor = None
    evidence_existed_at_execution = None

    if isinstance(gate, dict) and gate.get("status") == "passed":
        current_commit = _current_checkout_head(ROOT)
        evidence = gate.get("evidence")
        evidence_path = _existing_file(ROOT, evidence)
        execution_commit = None
        if evidence_path is not None:
            execution_commit = _execution_commit_from_record(
                evidence_path.read_text(encoding="utf-8")
            )

        if (
            current_commit is not None
            and execution_commit is not None
            and execution_commit != current_commit
        ):
            current_first_parent = _current_checkout_first_parent(ROOT)
            changed_paths_from_execution = _changed_paths(
                ROOT, execution_commit, current_commit
            )
            execution_descriptor = _json_at_commit(
                ROOT, execution_commit, DESCRIPTOR_RELATIVE
            )
            evidence_existed_at_execution = _path_exists_at_commit(
                ROOT, execution_commit, str(evidence)
            )

    errors = validate_complete_checkout_gate(
        ROOT,
        descriptor,
        current_commit=current_commit,
        current_first_parent=current_first_parent,
        changed_paths_from_execution=changed_paths_from_execution,
        execution_descriptor=execution_descriptor,
        evidence_existed_at_execution=evidence_existed_at_execution,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research complete-checkout execution gate validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
