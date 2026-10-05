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

from plan_production_adapter_metadata_promotion import (  # noqa: E402
    _bundle_catalog_source,
    _bundle_distribution_names,
    _openai_profile_names,
    plan_production_adapter_metadata_promotion,
    validate_production_adapter_metadata_promotion_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"


class ResearchProductionAdapterMetadataAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
        cls.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        catalog_source = _bundle_catalog_source(cls.adapter_plan)
        cls.locale_catalog = json.loads((ROOT / catalog_source).read_text(encoding="utf-8"))

    def test_current_plan_is_valid_with_adapter_plan_as_authority(self) -> None:
        plan = plan_production_adapter_metadata_promotion(
            self.adapter_plan,
            self.descriptor,
            self.locale_catalog,
        )
        errors = validate_production_adapter_metadata_promotion_plan(
            plan,
            self.descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertEqual(errors, [])

        profiles = _openai_profile_names(self.adapter_plan)
        expected_count = sum(
            len(skill_metadata) * len(profiles)
            for skill_metadata in self.adapter_plan["distributions"]["openai_skill"]["skills"].values()
        )
        self.assertEqual(len(plan["openai_profile_promotions"]), expected_count)

    def test_openai_profiles_come_from_adapter_plan_not_python_tuple(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["profiles"]["batch-review"] = {
            "expected_allow_implicit_invocation": False
        }
        self.assertIn("batch-review", _openai_profile_names(adapter_plan))

    def test_locale_bundle_distribution_set_comes_from_adapter_plan_scope(self) -> None:
        expected = tuple(
            name
            for name, config in self.adapter_plan["distributions"].items()
            if config.get("scope") == "locale_bundle"
        )
        self.assertEqual(_bundle_distribution_names(self.adapter_plan), expected)

    def test_locale_bundle_catalog_must_have_one_declared_source(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["codex_plugin"]["source"] = "adapters/other/locales.json"
        with self.assertRaisesRegex(ValueError, "must share one production catalog"):
            _bundle_catalog_source(adapter_plan)

    def test_existing_openai_metadata_route_preserves_declared_source_mode(self) -> None:
        plan = plan_production_adapter_metadata_promotion(
            self.adapter_plan, self.descriptor, self.locale_catalog,
        )
        core = [item for item in plan["openai_profile_promotions"] if item["research_id"] == "cultural-substrate-weaving"]
        self.assertEqual(len(core), 4)
        self.assertTrue(all(item["state"] == "existing-production-source" for item in core))
        self.assertTrue(all(item["content_operation"] == "keep-existing-production-metadata" for item in core))


if __name__ == "__main__":
    unittest.main()
