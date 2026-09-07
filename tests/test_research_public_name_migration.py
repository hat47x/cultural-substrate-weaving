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

from validate_research_public_name_migration import (  # noqa: E402
    validate_public_name_migration,
)

CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
)


class ResearchPublicNameMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, contract: dict, fragment: str) -> None:
        errors = validate_public_name_migration(ROOT, contract)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_contract_is_valid(self) -> None:
        self.assertEqual(validate_public_name_migration(ROOT, self.contract), [])

    def test_mapping_must_match_production_descriptor(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["research_to_production_name"]["affinity-synthesis"] = "affinity-synthesis"
        self.assert_has_error(contract, "must exactly match production descriptor")

    def test_layer1_public_name_cannot_silently_revert(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["research_to_production_name"]["affinity-synthesis"] = "affinity-synthesis"
        self.assert_has_error(contract, "affinity-synthesis -> material-led-synthesis")

    def test_research_history_policy_must_remain_stable(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["policy"]["research_history_is_not_renamed"] = False
        self.assert_has_error(contract, "research_history_is_not_renamed must remain True")

    def test_production_explicit_handoffs_use_public_name(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["policy"]["production_explicit_skill_references_use_production_name"] = False
        self.assert_has_error(
            contract,
            "production_explicit_skill_references_use_production_name must remain True",
        )

    def test_filesystem_sibling_paths_are_forbidden_in_production_runtime(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["forbidden_production_reference_prefixes"] = [
            "research/skill-prototypes/"
        ]
        self.assert_has_error(
            contract,
            "must protect research paths and sibling filesystem paths",
        )

    def test_display_terms_remain_separate_from_installable_names(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["display_terms"]["affinity-synthesis"]["en"] = "material-led-synthesis"
        self.assert_has_error(contract, "English display term must remain Affinity Synthesis")

    def test_alias_directory_is_not_created_by_default(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["policy"]["compatibility_alias_directory_is_not_created_by_default"] = False
        self.assert_has_error(
            contract,
            "compatibility_alias_directory_is_not_created_by_default must remain True",
        )


if __name__ == "__main__":
    unittest.main()
