from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from validate_production_projection import (  # noqa: E402
    _load,
    main as production_projection_main,
    validate_projection,
)

SKILL_SET_PATH = ROOT / "src" / "skill-set.json"
PLAN_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"


class ResearchProductionProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_set = json.loads(SKILL_SET_PATH.read_text(encoding="utf-8"))
        self.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    def assert_has_error(
        self,
        skill_set: dict,
        plan: dict,
        fragment: str,
    ) -> None:
        errors = validate_projection(skill_set, plan)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_projection_is_consistent(self) -> None:
        self.assertEqual(validate_projection(self.skill_set, self.plan), [])

    def test_validator_rejects_non_object_roots_without_crashing(self) -> None:
        self.assertEqual(
            validate_projection([], self.plan),
            ["production Skill-set must be an object"],
        )
        self.assertEqual(
            validate_projection(self.skill_set, []),
            ["research inclusion plan must be an object"],
        )

    def test_validator_rejects_malformed_production_entries(self) -> None:
        skill_set = copy.deepcopy(self.skill_set)
        skill_set["skills"].append([])
        self.assert_has_error(
            skill_set,
            self.plan,
            "production Skill-set entry",
        )

        skill_set = copy.deepcopy(self.skill_set)
        skill_set["skills"][0]["id"] = {"id": "invalid"}
        self.assert_has_error(
            skill_set,
            self.plan,
            "id must be a non-empty string",
        )

    def test_validator_rejects_duplicate_production_skill_id(self) -> None:
        skill_set = copy.deepcopy(self.skill_set)
        skill_set["skills"].append(copy.deepcopy(skill_set["skills"][0]))
        self.assert_has_error(
            skill_set,
            self.plan,
            "contains duplicate Skill id",
        )

    def test_validator_rejects_malformed_inclusion_entries(self) -> None:
        plan = copy.deepcopy(self.plan)
        value = plan["skills"].pop("affinity-synthesis")
        plan["skills"][1] = value
        self.assert_has_error(
            self.skill_set,
            plan,
            "research inclusion plan skill ids must be non-empty strings",
        )

        plan = copy.deepcopy(self.plan)
        plan["skills"]["affinity-synthesis"] = []
        self.assert_has_error(
            self.skill_set,
            plan,
            "research inclusion plan entry must be an object",
        )

    def test_json_loader_rejects_non_object_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "array.json"
            path.write_text("[]\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must contain a JSON object"):
                _load(path)

    def test_cli_catches_non_object_json_root(self) -> None:
        with patch(
            "validate_production_projection._load",
            side_effect=ValueError("authority must contain a JSON object"),
        ):
            self.assertEqual(production_projection_main(), 1)


if __name__ == "__main__":
    unittest.main()
