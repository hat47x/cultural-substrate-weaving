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


class ResearchProductionSuiteManifestProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.projected = project_production_suite_manifest(self.descriptor)

    def assert_has_error(self, projected: dict, fragment: str) -> None:
        errors = validate_projected_production_suite(projected, self.descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def skill(self, public_id: str) -> dict:
        return next(skill for skill in self.projected["skills"] if skill["id"] == public_id)

    def test_current_projection_is_valid(self) -> None:
        self.assertEqual(
            validate_projected_production_suite(self.projected, self.descriptor),
            [],
        )

    def test_layer1_research_id_is_removed_from_production_skill_ids(self) -> None:
        ids = [skill["id"] for skill in self.projected["skills"]]
        self.assertIn("material-led-synthesis", ids)
        self.assertNotIn("affinity-synthesis", ids)

    def test_projection_contains_only_first_wave_skill_tree_distributions(self) -> None:
        self.assertEqual(
            set(self.projected["distributions"]),
            {"openai_skill", "claude_plugin", "codex_plugin"},
        )
        self.assertNotIn("chatgpt_gpt", self.projected["distributions"])
        self.assertNotIn("microsoft_copilot", self.projected["distributions"])

    def test_projection_strips_research_adapter_maturity_state(self) -> None:
        layer1 = self.skill("material-led-synthesis")
        openai = layer1["adapter_metadata"]["openai_skill"]
        self.assertEqual(openai["mode"], "per_locale_profile")
        self.assertNotIn("planned-promotion-from-research-prototype", json.dumps(layer1))

        claude = layer1["adapter_metadata"]["claude_plugin"]
        self.assertEqual(claude["mode"], "locale_catalog")

    def test_projection_rejects_reintroduced_research_id(self) -> None:
        projected = copy.deepcopy(self.projected)
        projected["skills"][1]["id"] = "affinity-synthesis"
        self.assert_has_error(projected, "must use descriptor public installable names")
        self.assert_has_error(projected, "must not become a production Skill id")

    def test_projection_rejects_research_promotion_adapter_mode(self) -> None:
        projected = copy.deepcopy(self.projected)
        layer1 = next(
            skill for skill in projected["skills"] if skill["id"] == "material-led-synthesis"
        )
        layer1["adapter_metadata"]["openai_skill"]["mode"] = (
            "planned-promotion-from-research-prototype"
        )
        self.assert_has_error(projected, "adapter metadata mismatch")
        self.assert_has_error(projected, "uses non-production adapter mode")

    def test_projection_rejects_research_path(self) -> None:
        projected = copy.deepcopy(self.projected)
        layer1 = next(
            skill for skill in projected["skills"] if skill["id"] == "material-led-synthesis"
        )
        layer1["source"]["root_pattern"] = (
            "research/skill-prototypes/affinity-synthesis/{locale}"
        )
        self.assert_has_error(projected, "source mismatch")
        self.assert_has_error(projected, "must not contain research path")

    def test_codex_projection_keeps_shared_claude_tree(self) -> None:
        codex = self.projected["distributions"]["codex_plugin"]
        self.assertEqual(codex["mode"], "reuse_claude_skill_tree")
        self.assertEqual(codex["shared_skill_tree_distribution"], "claude_plugin")


if __name__ == "__main__":
    unittest.main()
