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

from validate_research_production_suite_descriptor import (  # noqa: E402
    validate_production_suite_descriptor,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


class ResearchProductionSuiteDescriptorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, descriptor: dict, fragment: str) -> None:
        errors = validate_production_suite_descriptor(descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def skill(self, descriptor: dict, research_id: str) -> dict:
        return next(
            skill for skill in descriptor["skills"] if skill["research_id"] == research_id
        )

    def test_current_descriptor_is_valid(self) -> None:
        self.assertEqual(validate_production_suite_descriptor(self.descriptor), [])

    def test_research_id_and_layer1_public_name_are_intentionally_distinct(self) -> None:
        layer1 = self.skill(self.descriptor, "affinity-synthesis")
        self.assertEqual(layer1["research_id"], "affinity-synthesis")
        self.assertEqual(layer1["proposed_installable_name"], "material-led-synthesis")
        self.assertNotEqual(layer1["research_id"], layer1["proposed_installable_name"])

    def test_layer1_public_name_gate_cannot_silently_revert_to_affinity_synthesis(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = self.skill(descriptor, "affinity-synthesis")
        layer1["proposed_installable_name"] = "affinity-synthesis"
        layer1["targets"] = {
            "openai_skill": "affinity-synthesis",
            "claude_plugin": "affinity-synthesis",
            "codex_plugin": "affinity-synthesis",
        }
        self.assert_has_error(descriptor, "must remain material-led-synthesis")

    def test_sibling_production_source_cannot_point_back_into_research(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = self.skill(descriptor, "affinity-synthesis")
        layer1["production_source"]["root_pattern"] = (
            "research/skill-prototypes/affinity-synthesis/{locale}"
        )
        self.assert_has_error(descriptor, "must stay under src/skills/")

    def test_production_openai_metadata_cannot_use_research_adapter_source(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = self.skill(descriptor, "affinity-synthesis")
        layer1["adapter_metadata"]["openai_skill"]["source_pattern"] = (
            "research/skill-prototypes/adapters/openai-skill/{locale}/"
            "affinity-synthesis/openai.{profile}.yaml"
        )
        self.assert_has_error(descriptor, "must live under adapters/openai-skill/")

    def test_public_installable_names_must_be_unique(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        iterative = self.skill(descriptor, "iterative-inquiry-synthesis")
        iterative["proposed_installable_name"] = "material-led-synthesis"
        self.assert_has_error(descriptor, "proposed_installable_name values must be unique")

    def test_public_installable_name_must_follow_agent_skill_name_shape(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        iterative = self.skill(descriptor, "iterative-inquiry-synthesis")
        iterative["proposed_installable_name"] = "Iterative Inquiry"
        self.assert_has_error(descriptor, "lowercase letters, numbers, and single hyphens")

    def test_first_wave_must_not_absorb_composite_surfaces(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["first_wave_distributions"].append("chatgpt_gpt")
        self.assert_has_error(descriptor, "first_wave_distributions must contain exactly")

    def test_codex_does_not_become_a_new_release_zip_kind_in_first_wave(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["release_shape"]["add_new_codex_release_zip_kind"] = True
        self.assert_has_error(
            descriptor,
            "release_shape.add_new_codex_release_zip_kind must remain False",
        )

    def test_descriptor_must_remain_design_only(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["status"] = "production"
        self.assert_has_error(descriptor, "must remain status=design-only")


if __name__ == "__main__":
    unittest.main()
