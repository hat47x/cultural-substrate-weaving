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
    DOCUMENT_RULES,
    validate_production_plan_consistency,
)

DESCRIPTOR_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
CONTRACT_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"


class ResearchProductionPlanConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.documents = {
            label: rules["path"].read_text(encoding="utf-8")
            for label, rules in DOCUMENT_RULES.items()
        }

    def assert_has_error(
        self,
        fragment: str,
        *,
        descriptor: dict | None = None,
        contract: dict | None = None,
        documents: dict[str, str] | None = None,
    ) -> None:
        errors = validate_production_plan_consistency(
            self.descriptor if descriptor is None else descriptor,
            self.contract if contract is None else contract,
            self.documents if documents is None else documents,
        )
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_plans_match_machine_readable_contracts(self) -> None:
        self.assertEqual(
            validate_production_plan_consistency(
                self.descriptor,
                self.contract,
                self.documents,
            ),
            [],
        )

    def test_old_explicit_files_sibling_sentence_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["promotion plan"] += (
            "\nSibling entryはproduction `src/skills/...` を指す `explicit_files` modeでよい。\n"
        )
        self.assert_has_error("stale-contract marker", documents=documents)

    def test_old_layer1_production_path_is_rejected_in_promotion_plan(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["promotion plan"] += "\nsrc/skills/affinity-synthesis/\n"
        self.assert_has_error("stale-contract marker", documents=documents)

    def test_old_layer1_production_path_is_rejected_in_consolidation(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["source contract consolidation"] += "\nsrc/skills/affinity-synthesis/\n"
        self.assert_has_error("stale-contract marker", documents=documents)

    def test_old_layer1_production_path_is_rejected_in_static_plan(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["builder static plan"] += "\nsrc/skills/affinity-synthesis/\n"
        self.assert_has_error("stale-contract marker", documents=documents)

    def test_package_closed_marker_cannot_disappear(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["promotion plan"] = documents["promotion plan"].replace(
            "package-closed source boundary", "source boundary"
        )
        self.assert_has_error("missing current-contract marker", documents=documents)

    def test_consolidation_locale_tree_marker_cannot_disappear(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents["source contract consolidation"] = documents[
            "source contract consolidation"
        ].replace("production source modeは二種類", "production source mode")
        self.assert_has_error("missing current-contract marker", documents=documents)

    def test_missing_document_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents.pop("builder static plan")
        self.assert_has_error("document is missing: builder static plan", documents=documents)

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

    def test_contract_package_purity_gate_cannot_disappear(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["validation_requirements"]["locale_tree_source_package_purity"] = False
        self.assert_has_error("package-purity validation enabled", contract=contract)

    def test_contract_exclusion_filter_invariant_cannot_disappear(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["invariants"] = [
            item
            for item in contract["invariants"]
            if "research-only exclusion filter" not in item
        ]
        self.assert_has_error("missing locale_tree package-closure invariant", contract=contract)


if __name__ == "__main__":
    unittest.main()
