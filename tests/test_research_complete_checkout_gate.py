from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_complete_checkout_gate import (  # noqa: E402
    validate_complete_checkout_gate,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
BLOCKED_EVIDENCE = Path(
    "research/skill-prototypes/P4-COMPLETE-CHECKOUT-EXECUTION-STATUS-2026-09-07.md"
)


class ResearchCompleteCheckoutGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, descriptor: dict, fragment: str) -> None:
        errors = validate_complete_checkout_gate(ROOT, descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_gate_is_valid_and_explicitly_not_run(self) -> None:
        self.assertEqual(validate_complete_checkout_gate(ROOT, self.descriptor), [])
        gate = self.descriptor["complete_checkout_validation"]
        self.assertEqual(gate["status"], "blocked-not-run")
        self.assertEqual(
            gate["required_commands"],
            [
                "make update-en-hashes",
                "make research-skill-check",
                "make build",
                "make check",
            ],
        )
        self.assertFalse(gate["production_promotion_authorized"])

    def test_blocked_gate_cannot_authorize_promotion(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["production_promotion_authorized"] = True
        self.assert_has_error(
            descriptor,
            "must not authorize production promotion by itself",
        )

    def test_command_set_cannot_silently_drop_translation_refresh(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["required_commands"] = [
            "make research-skill-check",
            "make build",
            "make check",
        ]
        self.assert_has_error(descriptor, "must remain the canonical command set")

    def test_command_set_cannot_silently_drop_full_check(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["required_commands"] = [
            "make update-en-hashes",
            "make research-skill-check",
            "make build",
        ]
        self.assert_has_error(descriptor, "must remain the canonical command set")

    def test_passed_status_rejects_blocked_not_run_evidence(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["status"] = "passed"
        self.assert_has_error(
            descriptor,
            "passed complete-checkout evidence missing required marker",
        )

    def test_passed_status_accepts_structured_execution_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = Path(
                "research/skill-prototypes/execution/P4-COMPLETE-CHECKOUT-PASS.md"
            )
            evidence_path = root / evidence_relative
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(
                "execution commit: 0123456789abcdef0123456789abcdef01234567\n"
                "make update-en-hashes: PASS\n"
                "make research-skill-check: PASS\n"
                "make build: PASS\n"
                "make check: PASS\n",
                encoding="utf-8",
            )

            descriptor = copy.deepcopy(self.descriptor)
            gate = descriptor["complete_checkout_validation"]
            gate["status"] = "passed"
            gate["evidence"] = str(evidence_relative)

            self.assertEqual(validate_complete_checkout_gate(root, descriptor), [])

    def test_blocked_status_requires_canonical_blocked_record(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["evidence"] = (
            "research/skill-prototypes/other-blocked-note.md"
        )
        self.assert_has_error(descriptor, "execution evidence is missing or unsafe")


if __name__ == "__main__":
    unittest.main()
