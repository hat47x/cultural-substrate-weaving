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
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
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

    def test_recheck_evidence_must_exist(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["recheck_evidence"] = (
            "research/skill-prototypes/DOES-NOT-EXIST-PUBLIC-NAME-RECHECK.md"
        )
        self.assert_has_error(contract, "public-name recheck evidence is missing")

    def test_recheck_evidence_must_match_descriptor(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["recheck_evidence"] = (
            "research/skill-prototypes/P4-PUBLIC-NAME-AUDIT-2026-09-07.md"
        )
        self.assert_has_error(
            contract,
            "public_name_recheck.evidence must match migration contract recheck_evidence",
        )

    def test_name_recheck_never_authorizes_production_promotion(self) -> None:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        descriptor["public_name_recheck"]["production_promotion_authorized"] = True

        original = DESCRIPTOR_PATH.read_text(encoding="utf-8")
        try:
            DESCRIPTOR_PATH.write_text(
                json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assert_has_error(
                self.contract,
                "public-name recheck must not authorize production promotion by itself",
            )
        finally:
            DESCRIPTOR_PATH.write_text(original, encoding="utf-8")

    def test_sibling_status_must_record_current_recheck(self) -> None:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        affinity = next(
            skill
            for skill in descriptor["skills"]
            if skill["research_id"] == "affinity-synthesis"
        )
        affinity["public_name_status"] = "pending-final-collision-recheck"

        original = DESCRIPTOR_PATH.read_text(encoding="utf-8")
        try:
            DESCRIPTOR_PATH.write_text(
                json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assert_has_error(
                self.contract,
                "affinity-synthesis public_name_status must record the current collision recheck",
            )
        finally:
            DESCRIPTOR_PATH.write_text(original, encoding="utf-8")

    def test_contract_note_must_keep_final_immediate_recheck(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["note"] = "Research IDs and history remain stable."
        self.assert_has_error(
            contract,
            "must preserve the final pre-promotion recheck",
        )


if __name__ == "__main__":
    unittest.main()
