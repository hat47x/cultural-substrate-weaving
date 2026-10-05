from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from plan_production_suite_manifest import (  # noqa: E402
    project_production_suite_manifest,
    validate_projected_production_suite,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


class ResearchProductionSuiteRenameAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    @staticmethod
    def renamed_skill(descriptor: dict) -> dict:
        return next(
            item
            for item in descriptor["skills"]
            if item["research_id"] != item["proposed_installable_name"]
        )

    def test_undeclared_research_identity_cannot_replace_suite_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        self.renamed_skill(descriptor)["research_id"] = "legacy-material-research"
        with self.assertRaisesRegex(ValueError, "exactly the three research suite Skills"):
            project_production_suite_manifest(descriptor)

    def test_declared_renamed_research_id_cannot_reenter_production_ids(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        renamed = self.renamed_skill(descriptor)
        projected = project_production_suite_manifest(descriptor)

        projected_skill = next(
            item
            for item in projected["skills"]
            if item["id"] == renamed["proposed_installable_name"]
        )
        projected_skill["id"] = renamed["research_id"]

        errors = validate_projected_production_suite(projected, descriptor)
        self.assertTrue(
            any(
                f"renamed research ID {renamed['research_id']} must not become a production Skill id"
                in error
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
