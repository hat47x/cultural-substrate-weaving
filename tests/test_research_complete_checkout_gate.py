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
    DESCRIPTOR_RELATIVE,
    EXPECTED_BINDING_CONTRACT,
    validate_complete_checkout_gate,
)

DESCRIPTOR_PATH = ROOT / DESCRIPTOR_RELATIVE
BLOCKED_EVIDENCE = Path(
    "research/skill-prototypes/P4-COMPLETE-CHECKOUT-EXECUTION-STATUS-2026-09-07.md"
)
PASS_COMMIT = "0123456789abcdef0123456789abcdef01234567"
RECORD_COMMIT = "1111111111111111111111111111111111111111"
OTHER_COMMIT = "89abcdef0123456789abcdef0123456789abcdef"


class ResearchCompleteCheckoutGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(
        self,
        descriptor: dict,
        fragment: str,
        *,
        root: Path = ROOT,
        current_commit: str | None = None,
        current_first_parent: str | None = None,
        changed_paths_from_execution: set[str] | None = None,
        execution_descriptor: dict | None = None,
        evidence_existed_at_execution: bool | None = None,
    ) -> None:
        errors = validate_complete_checkout_gate(
            root,
            descriptor,
            current_commit=current_commit,
            current_first_parent=current_first_parent,
            changed_paths_from_execution=changed_paths_from_execution,
            execution_descriptor=execution_descriptor,
            evidence_existed_at_execution=evidence_existed_at_execution,
        )
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def prepare_binding_contract(self, root: Path) -> None:
        path = root / EXPECTED_BINDING_CONTRACT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "validated commit V\n"
            "evidence-only recording commit E\n"
            "Eのfirst parentはV\n"
            "translation hash/state transitionはevidence recording commitへ混ぜない\n"
            "production promotionを単独承認しない\n",
            encoding="utf-8",
        )

    def write_pass_record(self, root: Path) -> Path:
        self.prepare_binding_contract(root)
        evidence_relative = Path(
            "research/skill-prototypes/execution/P4-COMPLETE-CHECKOUT-PASS.md"
        )
        evidence_path = root / evidence_relative
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(
            f"execution commit: {PASS_COMMIT}\n"
            "make update-en-hashes: PASS\n"
            "translation research state transition: PASS\n"
            "make research-skill-check: PASS\n"
            "make build: PASS\n"
            "make check: PASS\n",
            encoding="utf-8",
        )
        return evidence_relative

    def passed_descriptor(self, evidence_relative: Path) -> dict:
        descriptor = copy.deepcopy(self.descriptor)
        gate = descriptor["complete_checkout_validation"]
        gate["status"] = "passed"
        gate["evidence"] = str(evidence_relative)
        return descriptor

    def evidence_only_context(self, evidence_relative: Path) -> dict:
        return {
            "current_commit": RECORD_COMMIT,
            "current_first_parent": PASS_COMMIT,
            "changed_paths_from_execution": {
                DESCRIPTOR_RELATIVE.as_posix(),
                str(evidence_relative),
            },
            "execution_descriptor": copy.deepcopy(self.descriptor),
            "evidence_existed_at_execution": False,
        }

    def test_current_gate_is_valid_and_explicitly_not_run(self) -> None:
        self.assertEqual(validate_complete_checkout_gate(ROOT, self.descriptor), [])
        gate = self.descriptor["complete_checkout_validation"]
        self.assertEqual(gate["status"], "blocked-not-run")
        self.assertEqual(gate["binding_contract"], EXPECTED_BINDING_CONTRACT)
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

    def test_binding_contract_cannot_be_removed(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"].pop("binding_contract")
        self.assert_has_error(
            descriptor,
            "must reference the canonical evidence-binding contract",
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

    def test_passed_status_accepts_transient_record_for_current_execution_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)

            self.assertEqual(
                validate_complete_checkout_gate(
                    root,
                    descriptor,
                    current_commit=PASS_COMMIT,
                ),
                [],
            )

    def test_passed_status_accepts_one_evidence_only_recording_child(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)

            self.assertEqual(
                validate_complete_checkout_gate(
                    root,
                    descriptor,
                    **self.evidence_only_context(evidence_relative),
                ),
                [],
            )

    def test_evidence_only_child_rejects_extra_changed_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            context = self.evidence_only_context(evidence_relative)
            context["changed_paths_from_execution"].add("src/ja-JP/ROUTER.md")

            self.assert_has_error(
                descriptor,
                "may change only the production descriptor and execution record",
                root=root,
                **context,
            )

    def test_evidence_only_child_rejects_non_direct_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            context = self.evidence_only_context(evidence_relative)
            context["current_first_parent"] = OTHER_COMMIT

            self.assert_has_error(
                descriptor,
                "must be the current HEAD or its direct first parent",
                root=root,
                **context,
            )

    def test_evidence_only_child_rejects_descriptor_changes_outside_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            descriptor["suite_id"] = "changed-during-evidence-recording"
            context = self.evidence_only_context(evidence_relative)

            self.assert_has_error(
                descriptor,
                "must not change production descriptor fields outside complete_checkout_validation",
                root=root,
                **context,
            )

    def test_evidence_only_child_rejects_other_gate_field_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            descriptor["complete_checkout_validation"]["required_commands"] = [
                "make update-en-hashes",
                "make build",
                "make check",
            ]
            context = self.evidence_only_context(evidence_relative)

            self.assert_has_error(
                descriptor,
                "may change only complete-checkout status and evidence path",
                root=root,
                **context,
            )

    def test_evidence_only_child_requires_new_execution_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            context = self.evidence_only_context(evidence_relative)
            context["evidence_existed_at_execution"] = True

            self.assert_has_error(
                descriptor,
                "execution record must be new",
                root=root,
                **context,
            )

    def test_passed_status_rejects_stale_execution_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            self.assert_has_error(
                descriptor,
                "must be the current HEAD or its direct first parent",
                root=root,
                current_commit=OTHER_COMMIT,
                current_first_parent=RECORD_COMMIT,
            )

    def test_passed_status_requires_current_checkout_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_relative = self.write_pass_record(root)
            descriptor = self.passed_descriptor(evidence_relative)
            self.assert_has_error(
                descriptor,
                "requires the current checkout HEAD",
                root=root,
            )

    def test_passed_status_requires_translation_state_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_binding_contract(root)
            evidence_relative = Path(
                "research/skill-prototypes/execution/P4-COMPLETE-CHECKOUT-PASS.md"
            )
            evidence_path = root / evidence_relative
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(
                f"execution commit: {PASS_COMMIT}\n"
                "make update-en-hashes: PASS\n"
                "make research-skill-check: PASS\n"
                "make build: PASS\n"
                "make check: PASS\n",
                encoding="utf-8",
            )
            descriptor = self.passed_descriptor(evidence_relative)
            errors = validate_complete_checkout_gate(
                root,
                descriptor,
                current_commit=PASS_COMMIT,
            )
            self.assertTrue(
                any("translation research state transition: PASS" in error for error in errors)
            )

    def test_passed_evidence_must_use_execution_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_binding_contract(root)
            evidence_relative = Path("research/skill-prototypes/PASS.md")
            evidence_path = root / evidence_relative
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(
                f"execution commit: {PASS_COMMIT}\n"
                "make update-en-hashes: PASS\n"
                "translation research state transition: PASS\n"
                "make research-skill-check: PASS\n"
                "make build: PASS\n"
                "make check: PASS\n",
                encoding="utf-8",
            )
            descriptor = self.passed_descriptor(evidence_relative)
            self.assert_has_error(
                descriptor,
                "must live under research/skill-prototypes/execution/",
                root=root,
                current_commit=PASS_COMMIT,
            )

    def test_blocked_status_requires_canonical_blocked_record(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"]["evidence"] = (
            "research/skill-prototypes/other-blocked-note.md"
        )
        self.assert_has_error(descriptor, "execution evidence is missing or unsafe")


if __name__ == "__main__":
    unittest.main()
