from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from run_research_complete_checkout_gate import (  # noqa: E402
    COMMANDS,
    REQUIRED_GATE_COMMANDS,
    STATE_TRANSITION_LABEL,
    candidate_execution_commit,
    candidate_record,
    execute_gate,
    validate_candidate_recording_head,
    validate_candidate_recording_state,
    validate_preconditions,
)

HEAD = "0123456789abcdef0123456789abcdef01234567"
OTHER_HEAD = "89abcdef0123456789abcdef0123456789abcdef"


def descriptor(status: str = "blocked-not-run") -> dict:
    return {
        "complete_checkout_validation": {
            "status": status,
            "required_commands": list(REQUIRED_GATE_COMMANDS),
        }
    }


class ResearchCompleteCheckoutRunnerTests(unittest.TestCase):
    def test_candidate_record_contains_validator_markers_without_authorization(self) -> None:
        text = candidate_record(HEAD)
        for marker in (
            f"execution commit: {HEAD}",
            "make update-en-hashes: PASS",
            "translation research state transition: PASS",
            "make research-skill-check: PASS",
            "make build: PASS",
            "make check: PASS",
            "production promotion authorization: NO",
        ):
            self.assertIn(marker, text)
        self.assertIn("candidate / not yet repository evidence", text)
        self.assertEqual(candidate_execution_commit(text), HEAD)

    def test_runner_guard_is_not_a_descriptor_promotion_command(self) -> None:
        labels = [label for label, _ in COMMANDS]
        self.assertEqual(
            [label for label in labels if label != STATE_TRANSITION_LABEL],
            list(REQUIRED_GATE_COMMANDS),
        )
        self.assertNotIn(STATE_TRANSITION_LABEL, REQUIRED_GATE_COMMANDS)
        self.assertIn(STATE_TRANSITION_LABEL, labels)

    def test_candidate_recording_requires_same_head_after_validation(self) -> None:
        record = candidate_record(HEAD)
        self.assertEqual(validate_candidate_recording_head(record, HEAD), [])
        errors = validate_candidate_recording_head(record, OTHER_HEAD)
        self.assertTrue(any("no longer matches current HEAD" in error for error in errors), errors)

    def test_candidate_recording_requires_clean_tree_after_validation(self) -> None:
        record = candidate_record(HEAD)
        self.assertEqual(validate_candidate_recording_state(record, HEAD, ""), [])
        errors = validate_candidate_recording_state(
            record,
            HEAD,
            " M research/skill-prototypes/suite-manifest.json",
        )
        self.assertTrue(
            any("clean working tree after validation" in error for error in errors),
            errors,
        )

    def test_candidate_recording_requires_valid_execution_commit(self) -> None:
        errors = validate_candidate_recording_head(
            "execution commit: not-a-sha\n",
            HEAD,
        )
        self.assertTrue(any("valid execution commit" in error for error in errors), errors)

    def test_clean_blocked_preconditions_are_accepted(self) -> None:
        self.assertEqual(
            validate_preconditions(ROOT, descriptor(), head=HEAD, status=""),
            [],
        )

    def test_dirty_worktree_is_rejected(self) -> None:
        errors = validate_preconditions(
            ROOT,
            descriptor(),
            head=HEAD,
            status=" M src/ja-JP/ROUTER.md",
        )
        self.assertTrue(any("clean working tree" in error for error in errors))

    def test_passed_descriptor_is_rejected_for_new_candidate_run(self) -> None:
        errors = validate_preconditions(ROOT, descriptor("passed"), head=HEAD, status="")
        self.assertTrue(any("blocked-not-run" in error for error in errors))

    def test_descriptor_command_drift_is_rejected(self) -> None:
        value = descriptor()
        value["complete_checkout_validation"]["required_commands"] = ["make check"]
        errors = validate_preconditions(ROOT, value, head=HEAD, status="")
        self.assertTrue(any("promotion command authority" in error for error in errors))

    def test_success_runs_all_commands_and_returns_candidate(self) -> None:
        calls: list[tuple[str, ...]] = []

        def run_command(_root: Path, argv) -> int:
            calls.append(tuple(argv))
            return 0

        code, record, messages = execute_gate(
            ROOT,
            run_command=run_command,
            head_reader=lambda _root: HEAD,
            status_reader=lambda _root: "",
            descriptor=descriptor(),
        )

        self.assertEqual(code, 0)
        self.assertIsNotNone(record)
        self.assertEqual(calls, [argv for _, argv in COMMANDS])
        self.assertEqual(sum(message.startswith("PASS ") for message in messages), len(COMMANDS))

    def test_command_failure_stops_without_candidate(self) -> None:
        count = 0

        def run_command(_root: Path, _argv) -> int:
            nonlocal count
            count += 1
            return 7 if count == 2 else 0

        code, record, messages = execute_gate(
            ROOT,
            run_command=run_command,
            head_reader=lambda _root: HEAD,
            status_reader=lambda _root: "",
            descriptor=descriptor(),
        )

        self.assertEqual(code, 7)
        self.assertIsNone(record)
        self.assertEqual(count, 2)
        self.assertTrue(any("FAIL translation research state transition" in message for message in messages))

    def test_repository_diff_after_command_stops_without_candidate(self) -> None:
        statuses = iter(["", " M i18n/translation-manifest.json"])
        code, record, messages = execute_gate(
            ROOT,
            run_command=lambda _root, _argv: 0,
            head_reader=lambda _root: HEAD,
            status_reader=lambda _root: next(statuses),
            descriptor=descriptor(),
        )
        self.assertEqual(code, 2)
        self.assertIsNone(record)
        self.assertTrue(any("validated commit V is incomplete" in message for message in messages))

    def test_head_change_after_command_stops_without_candidate(self) -> None:
        heads = iter([HEAD, OTHER_HEAD])
        code, record, messages = execute_gate(
            ROOT,
            run_command=lambda _root, _argv: 0,
            head_reader=lambda _root: next(heads),
            status_reader=lambda _root: "",
            descriptor=descriptor(),
        )
        self.assertEqual(code, 2)
        self.assertIsNone(record)
        self.assertTrue(any("HEAD changed during validation" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
