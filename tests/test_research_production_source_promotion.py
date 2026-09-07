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

from plan_production_source_promotion import (  # noqa: E402
    plan_production_source_promotion,
    validate_production_source_promotion_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
SUITE_PATH = BASE / "suite-manifest.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
MIGRATION_PATH = BASE / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
INVENTORY_PATH = BASE / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"


class ResearchProductionSourcePromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
        self.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        self.plan = plan_production_source_promotion(
            self.suite,
            self.descriptor,
            self.migration,
            self.inventory,
        )

    def skill(self, research_id: str, plan: dict | None = None) -> dict:
        source = self.plan if plan is None else plan
        return next(item for item in source["skills"] if item["research_id"] == research_id)

    def mapping(self, research_id: str, locale: str, source_suffix: str, plan: dict | None = None) -> dict:
        mappings = self.skill(research_id, plan)["locales"][locale]["mappings"]
        return next(item for item in mappings if item["source"].endswith(source_suffix))

    def validate(self, plan: dict | None = None) -> list[str]:
        return validate_production_source_promotion_plan(
            self.plan if plan is None else plan,
            self.descriptor,
            self.inventory,
        )

    def test_current_plan_is_valid(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_layer1_uses_public_name_and_never_research_id_in_production_root(self) -> None:
        layer1 = self.skill("affinity-synthesis")
        self.assertEqual(layer1["production_name"], "material-led-synthesis")
        for locale_plan in layer1["locales"].values():
            self.assertIn("src/skills/material-led-synthesis/", locale_plan["production_root"])
            self.assertNotIn("src/skills/affinity-synthesis/", locale_plan["production_root"])

    def test_layer1_runtime_frontmatter_projection_is_explicit(self) -> None:
        ja = self.mapping("affinity-synthesis", "ja-JP", "/SKILL.md")
        en = self.mapping("affinity-synthesis", "en-US", "/SKILL.en.md")
        self.assertIn("rewrite-frontmatter-name-only", ja["content_transforms"])
        self.assertIn("rewrite-frontmatter-name-only", en["content_transforms"])
        self.assertEqual(en["target_relative"], "SKILL.md")
        self.assertIn("normalize-locale-suffixed-filename", en["content_transforms"])

    def test_layer2_runtime_and_method_rewrite_explicit_layer1_installable_name(self) -> None:
        ja_skill = self.mapping("iterative-inquiry-synthesis", "ja-JP", "/SKILL.md")
        en_skill = self.mapping("iterative-inquiry-synthesis", "en-US", "/SKILL.en.md")
        ja_method = self.mapping(
            "iterative-inquiry-synthesis", "ja-JP", "/references/METHOD.md"
        )
        en_method = self.mapping(
            "iterative-inquiry-synthesis", "en-US", "/references/METHOD.en.md"
        )
        self.assertIn("rewrite-explicit-installable-name", ja_skill["content_transforms"])
        self.assertIn(
            "rewrite-explicit-installable-name-and-remove-sibling-filesystem-reference",
            en_skill["content_transforms"],
        )
        self.assertIn("rewrite-realization-identifier-not-method-role", ja_method["content_transforms"])
        self.assertIn("rewrite-realization-identifier-not-method-role", en_method["content_transforms"])
        self.assertEqual(en_method["target_relative"], "references/METHOD.md")

    def test_projection_inventory_action_cannot_be_silently_dropped_from_plan(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "iterative-inquiry-synthesis",
            "en-US",
            "/references/METHOD.en.md",
            plan,
        )
        mapping["content_transforms"].remove("rewrite-realization-identifier-not-method-role")
        errors = self.validate(plan)
        self.assertTrue(
            any("missing projection-inventory transform" in error for error in errors),
            errors,
        )

    def test_projection_inventory_source_cannot_be_silently_dropped_from_plan(self) -> None:
        plan = copy.deepcopy(self.plan)
        locale_plan = self.skill("iterative-inquiry-synthesis", plan)["locales"]["en-US"]
        locale_plan["mappings"] = [
            item
            for item in locale_plan["mappings"]
            if not item["source"].endswith("/references/METHOD.en.md")
        ]
        errors = self.validate(plan)
        self.assertTrue(
            any("promotion-sensitive source declared by projection inventory is missing" in error for error in errors),
            errors,
        )

    def test_english_locale_suffixes_are_normalized_in_canonical_targets(self) -> None:
        for research_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
            mappings = self.skill(research_id)["locales"]["en-US"]["mappings"]
            self.assertTrue(mappings)
            self.assertFalse(any(".en.md" in item["target_relative"] for item in mappings))
            self.assertTrue(
                any("normalize-locale-suffixed-filename" in item["content_transforms"] for item in mappings)
            )

    def test_layer1_japanese_progressive_support_is_promoted_but_not_forced_into_english(self) -> None:
        layer1 = self.skill("affinity-synthesis")
        ja_targets = {item["target_relative"] for item in layer1["locales"]["ja-JP"]["mappings"]}
        en_targets = {item["target_relative"] for item in layer1["locales"]["en-US"]["mappings"]}
        self.assertIn("evals/CASES.md", ja_targets)
        self.assertIn("evidence/dossier.md", ja_targets)
        self.assertNotIn("evals/CASES.md", en_targets)
        self.assertNotIn("evidence/dossier.md", en_targets)

    def test_layer2_external_loop_dossier_remains_research_only(self) -> None:
        layer2 = self.skill("iterative-inquiry-synthesis")
        excluded = layer2["excluded_research_metadata"]
        self.assertIn(
            "research/skill-prototypes/iterative-inquiry-synthesis/evidence/dossier.md",
            excluded,
        )
        for locale_plan in layer2["locales"].values():
            self.assertFalse(
                any(item["target_relative"].startswith("evidence/") for item in locale_plan["mappings"])
            )

    def test_target_collision_is_rejected(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        layer1["locales"]["ja-JP"]["target_collision"] = True
        errors = self.validate(plan)
        self.assertTrue(any("target collision" in error for error in errors))

    def test_research_id_leak_in_layer1_production_root_is_rejected(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        locale_plan = layer1["locales"]["ja-JP"]
        locale_plan["production_root"] = "src/skills/affinity-synthesis/ja-JP"
        locale_plan["runtime_entry"] = "src/skills/affinity-synthesis/ja-JP/SKILL.md"
        errors = self.validate(plan)
        self.assertTrue(any("research id leaked" in error for error in errors))

    def test_stale_descriptor_source_mode_is_rejected_by_planner(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        layer1["production_source"]["mode"] = "explicit_files"
        with self.assertRaisesRegex(ValueError, "production source is not locale_tree"):
            plan_production_source_promotion(
                self.suite,
                descriptor,
                self.migration,
                self.inventory,
            )


if __name__ == "__main__":
    unittest.main()
