from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_production_plan_consistency import (  # noqa: E402
    validate_production_plan_consistency,
)

DESCRIPTOR_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
CONTRACT_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
PLAN_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SOURCE-AND-BUILDER-PROMOTION-PLAN-2026-09-07.md"


class ResearchProductionPlanConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.plan_text = PLAN_PATH.read_text(encoding="utf-8")

    def assert_has_error(
        self,
        fragment: str,
        *,
        descriptor: dict | None = None,
        contract: dict | None = None,
        plan_text: str | None = None,
    ) -> None:
        errors = validate_production_plan_consistency(
            self.descriptor if descriptor is None else descriptor,
            self.contract if contract is None else contract,
            self.plan_text if plan_text is None else plan_text,
        )
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_plan_matches_machine_readable_contracts(self) -> None:
        self.assertEqual(
            validate_production_plan_consistency(
                self.descriptor,
                self.contract,
                self.plan_text,
            ),
            [],
        )

    def test_old_explicit_files_sibling_sentence_is_rejected(self) -> None:
        plan_text = self.plan_text + (
            "\nSibling entryはproduction `src/skills/...` を指す `explicit_files` modeでよい。\n"
        )
        self.assert_has_error("stale-contract marker", plan_text=plan_text)

    def test_old_layer1_production_path_is_rejected(self) -> None:
        plan_text = self.plan_text + "\nsrc/skills/affinity-synthesis/\n"
        self.assert_has_error("stale-contract marker", plan_text=plan_text)

    def test_package_closed_marker_cannot_disappear(self) -> None:
        plan_text = self.plan_text.replace("package-closed source boundary", "source boundary")
        self.assert_has_error("missing current-contract marker", plan_text=plan_text)

    def test_sibling_descriptor_mode_cannot_drift_from_locale_tree(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        sibling = next(
            skill for skill in descriptor["skills"] if skill["research_id"] == "affinity-synthesis"
        )
        sibling["production_source"]["mode"] = "explicit_files"
        self.assert_has_error("descriptor sibling source mode must remain locale_tree", descriptor=descriptor)

    def test_contract_locale_tree_copy_operation_cannot_drift(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["source_mode_operations"]["locale_tree"] = "copy_selected_files"
        self.assert_has_error("must define locale_tree copy semantics", contract=contract)


if __name__ == "__main__":
    unittest.main()
