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
    plan_production_adapter_metadata_promotion,
    validate_production_adapter_metadata_promotion_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
LOCALE_CATALOG_PATH = ROOT / "adapters" / "claude-code" / "locales.json"


class ResearchProductionAdapterMetadataPromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.locale_catalog = json.loads(LOCALE_CATALOG_PATH.read_text(encoding="utf-8"))
        self.plan = plan_production_adapter_metadata_promotion(
            self.adapter_plan,
            self.descriptor,
            self.locale_catalog,
        )

    def errors(self, plan: dict | None = None) -> list[str]:
        return validate_production_adapter_metadata_promotion_plan(
            self.plan if plan is None else plan,
            self.descriptor,
            self.locale_catalog,
        )

    def openai_item(self, research_id: str, locale: str, profile: str, plan: dict | None = None) -> dict:
        source = self.plan if plan is None else plan
        return next(
            item
            for item in source["openai_profile_promotions"]
            if item["research_id"] == research_id
            and item["locale"] == locale
            and item["profile"] == profile
        )

    def bundle_item(self, locale: str, plan: dict | None = None) -> dict:
        source = self.plan if plan is None else plan
        return next(item for item in source["locale_bundle_promotions"] if item["locale"] == locale)

    def test_current_adapter_promotion_plan_is_valid(self) -> None:
        self.assertEqual(self.errors(), [])
        self.assertFalse(self.plan["writes_production_metadata"])
        self.assertEqual(len(self.plan["openai_profile_promotions"]), 12)
        self.assertEqual(len(self.plan["locale_bundle_promotions"]), 2)

    def test_claude_and_codex_research_bundle_sources_are_shared_per_locale(self) -> None:
        distributions = self.adapter_plan["distributions"]
        claude = distributions["claude_plugin"]
        codex = distributions["codex_plugin"]
        self.assertEqual(claude["source"], codex["source"])
        for locale in ("ja-JP", "en-US"):
            self.assertEqual(
                claude["locales"][locale]["prototype_source"],
                codex["locales"][locale]["prototype_source"],
            )

    def test_layer1_openai_metadata_uses_public_name_path_and_byte_identical_content(self) -> None:
        for locale in ("ja-JP", "en-US"):
            for profile in ("interactive", "metered"):
                item = self.openai_item("affinity-synthesis", locale, profile)
                self.assertEqual(item["production_name"], "material-led-synthesis")
                self.assertIn(f"/{locale}/material-led-synthesis/", item["target"])
                self.assertNotIn("/affinity-synthesis/", item["target"])
                self.assertEqual(item["content_operation"], "copy-byte-identical")
                self.assertEqual(len(item["sha256"]), 64)

    def test_iterative_openai_metadata_keeps_same_public_id_and_byte_identical_content(self) -> None:
        item = self.openai_item("iterative-inquiry-synthesis", "en-US", "interactive")
        self.assertEqual(item["production_name"], "iterative-inquiry-synthesis")
        self.assertIn("/iterative-inquiry-synthesis/", item["target"])
        self.assertEqual(item["content_operation"], "copy-byte-identical")

    def test_csw_openai_metadata_remains_existing_production_source(self) -> None:
        item = self.openai_item("cultural-substrate-weaving", "ja-JP", "interactive")
        self.assertEqual(item["state"], "existing-production-source")
        self.assertEqual(item["source"], "adapters/openai-skill/ja-JP/openai.interactive.yaml")
        self.assertEqual(item["target"], item["source"])

    def test_bundle_promotion_preserves_identity_and_updates_description_only(self) -> None:
        for locale in ("ja-JP", "en-US"):
            item = self.bundle_item(locale)
            current = self.locale_catalog[locale]
            self.assertEqual(
                item["preserve"],
                {
                    "plugin_name": current["plugin_name"],
                    "skill_name": current["skill_name"],
                    "display": current["display"],
                },
            )
            self.assertEqual(set(item["update"]), {"description"})
            self.assertNotEqual(item["update"]["description"], "")
            self.assertEqual(item["shared_by"], ["claude_plugin", "codex_plugin"])

    def test_bundle_research_composition_maps_to_public_production_composition(self) -> None:
        expected_public = [
            "cultural-substrate-weaving",
            "material-led-synthesis",
            "iterative-inquiry-synthesis",
        ]
        for locale in ("ja-JP", "en-US"):
            item = self.bundle_item(locale)
            self.assertEqual(
                set(item["prototype_research_contains"]),
                {
                    "cultural-substrate-weaving",
                    "affinity-synthesis",
                    "iterative-inquiry-synthesis",
                },
            )
            self.assertEqual(item["production_suite_contains"], expected_public)
            self.assertIn("contains", item["drop_prototype_fields_from_host_catalog"])
            self.assertIn("status", item["drop_prototype_fields_from_host_catalog"])

    def test_layer1_research_id_cannot_leak_into_openai_production_target(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "ja-JP", "interactive", plan)
        item["target"] = "adapters/openai-skill/ja-JP/affinity-synthesis/openai.interactive.yaml"
        errors = self.errors(plan)
        self.assertTrue(any("must use material-led-synthesis" in error for error in errors), errors)

    def test_sibling_openai_metadata_cannot_gain_content_rewrite(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "en-US", "metered", plan)
        item["content_operation"] = "rewrite-display-name"
        errors = self.errors(plan)
        self.assertTrue(any("promote byte-identically" in error for error in errors), errors)

    def test_bundle_identity_cannot_be_replaced_by_prototype_identity(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("ja-JP", plan)
        item["preserve"]["plugin_name"] = "new-suite-plugin"
        errors = self.errors(plan)
        self.assertTrue(any("preserve existing locale/plugin identity" in error for error in errors), errors)

    def test_bundle_host_catalog_cannot_store_research_id_composition(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("en-US", plan)
        item["production_suite_contains"] = item["prototype_research_contains"]
        errors = self.errors(plan)
        self.assertTrue(any("must use public Skill identities" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
