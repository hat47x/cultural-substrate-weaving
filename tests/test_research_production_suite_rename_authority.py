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

    def test_rename_check_follows_descriptor_pair_not_layer1_literals(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        renamed = self.renamed_skill(descriptor)
        renamed["research_id"] = "legacy-material-research"
        renamed["proposed_installable_name"] = "future-material-synthesis"

        projected = project_production_suite_manifest(descriptor)

        self.assertIn(
            "future-material-synthesis",
            [item["id"] for item in projected["skills"]],
        )
        self.assertEqual(validate_projected_production_suite(projected, descriptor), [])

    def test_declared_renamed_research_id_cannot_reenter_production_ids(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        renamed = self.renamed_skill(descriptor)
        renamed["research_id"] = "legacy-material-research"
        renamed["proposed_installable_name"] = "future-material-synthesis"
        projected = project_production_suite_manifest(descriptor)

        projected_skill = next(
            item
            for item in projected["skills"]
            if item["id"] == "future-material-synthesis"
        )
        projected_skill["id"] = "legacy-material-research"

        errors = validate_projected_production_suite(projected, descriptor)
        self.assertTrue(
            any(
                "renamed research ID legacy-material-research must not become a production Skill id"
                in error
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
