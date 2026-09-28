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
    validate_source_promotion_authorities,
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
            suite=self.suite,
            migration=self.migration,
        )

    def test_current_plan_is_valid(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_validator_rejects_non_object_plan_without_crashing(self) -> None:
        errors = validate_production_source_promotion_plan(
            [],
            self.descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertEqual(
            errors,
            ["production source promotion plan must be an object"],
        )

    def test_validator_rejects_non_object_descriptor_without_crashing(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            [],
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("production promotion descriptor must be an object" in error for error in errors),
            errors,
        )

    def test_validator_rejects_non_object_suite_authority_without_crashing(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=[],
            migration=self.migration,
        )
        self.assertTrue(
            any("research suite authority must be an object" in error for error in errors),
            errors,
        )

    def test_validator_rejects_non_object_inventory_authority_without_crashing(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            [],
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("projection-inventory authority must be an object" in error for error in errors),
            errors,
        )

    def test_validator_rejects_non_object_migration_authority_without_crashing(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=self.suite,
            migration=[],
        )
        self.assertTrue(
            any("public-name migration authority must be an object" in error for error in errors),
            errors,
        )

    def test_validator_rejects_non_list_plan_skills_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"] = {"affinity-synthesis": self.skill("affinity-synthesis", plan)}
        errors = self.validate(plan)
        self.assertTrue(
            any("production source promotion plan Skills must be a list" in error for error in errors),
            errors,
        )

    def test_validator_rejects_non_object_locale_plan_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        self.skill("affinity-synthesis", plan)["locales"]["ja-JP"] = []
        errors = self.validate(plan)
        self.assertTrue(
            any(
                "production source plan locale entries must be objects: affinity-synthesis/ja-JP"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_reports_malformed_descriptor_skills_without_crashing(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"] = None
        errors = validate_production_source_promotion_plan(
            self.plan,
            descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("production promotion descriptor skills must be a list" in error for error in errors),
            errors,
        )

    def test_validator_composes_full_descriptor_status_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["status"] = "promotion-ready"
        errors = validate_production_source_promotion_plan(
            self.plan,
            descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "production promotion descriptor must remain status=design-only" in error
                for error in errors
            ),
            errors,
        )

    def test_validator_requires_research_suite_authority(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
        )
        self.assertTrue(
            any(
                "production source promotion validation requires research suite authority"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_reports_malformed_suite_skills_without_crashing(self) -> None:
        suite = copy.deepcopy(self.suite)
        suite["skills"] = None
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "research skill suite skills must be a non-empty list" in error
                for error in errors
            ),
            errors,
        )

    def test_validator_fallback_handles_non_list_plan_skills_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"] = None
        errors = validate_production_source_promotion_plan(
            plan,
            self.descriptor,
            self.inventory,
            migration=self.migration,
        )
        self.assertTrue(
            any("production source promotion plan Skills must be a list" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                "production source promotion validation requires research suite authority"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_composes_full_research_suite_authority(self) -> None:
        suite = copy.deepcopy(self.suite)
        suite["status"] = "production-ready"
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "research skill suite must remain marked research-only before promotion"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_composes_full_projection_inventory_authority(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["status"] = "promotion-ready"
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("projection inventory must remain status=design-only" in error for error in errors),
            errors,
        )

    def test_validator_requires_public_name_migration_authority(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=self.suite,
        )
        self.assertTrue(
            any(
                "production source promotion validation requires public-name migration authority"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_composes_full_public_name_migration_authority(self) -> None:
        migration = copy.deepcopy(self.migration)
        migration["policy"]["production_frontmatter_uses_production_name"] = False
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            self.inventory,
            suite=self.suite,
            migration=migration,
        )
        self.assertTrue(
            any(
                "production_frontmatter_uses_production_name must remain True"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_requires_projection_inventory_authority(self) -> None:
        errors = validate_production_source_promotion_plan(
            self.plan,
            self.descriptor,
            None,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "production source promotion validation requires projection-inventory authority"
                in error
                for error in errors
            ),
            errors,
        )


    def test_current_authorities_are_valid(self) -> None:
        self.assertEqual(
            validate_source_promotion_authorities(
                ROOT,
                self.suite,
                self.descriptor,
                self.migration,
                self.inventory,
            ),
            [],
        )

    def test_cli_authorities_reject_non_object_roots_without_crashing(self) -> None:
        errors = validate_source_promotion_authorities(
            ROOT,
            [],
            [],
            [],
            [],
        )
        for expected in (
            "research suite authority must be an object",
            "production promotion descriptor authority must be an object",
            "public-name migration authority must be an object",
            "projection-inventory authority must be an object",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_cli_authorities_reject_migration_policy_drift(self) -> None:
        migration = copy.deepcopy(self.migration)
        migration["policy"]["production_frontmatter_uses_production_name"] = False
        errors = validate_source_promotion_authorities(
            ROOT,
            self.suite,
            self.descriptor,
            migration,
            self.inventory,
        )
        self.assertTrue(
            any(
                "production_frontmatter_uses_production_name must remain True" in error
                for error in errors
            ),
            errors,
        )

    def test_cli_authorities_reject_projection_inventory_drift(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["content_projection"] = inventory["content_projection"][1:]
        errors = validate_source_promotion_authorities(
            ROOT,
            self.suite,
            self.descriptor,
            self.migration,
            inventory,
        )
        self.assertTrue(
            any(
                "missing promotion-critical content projection paths" in error
                for error in errors
            ),
            errors,
        )


    def test_planner_rejects_duplicate_suite_skill(self) -> None:
        suite = copy.deepcopy(self.suite)
        suite["skills"].append(copy.deepcopy(suite["skills"][0]))
        with self.assertRaisesRegex(ValueError, "research suite contains duplicate Skills"):
            plan_production_source_promotion(
                suite,
                self.descriptor,
                self.migration,
                self.inventory,
            )

    def test_planner_rejects_duplicate_descriptor_skill(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"].append(copy.deepcopy(descriptor["skills"][0]))
        with self.assertRaisesRegex(
            ValueError,
            "production descriptor contains duplicate research Skills",
        ):
            plan_production_source_promotion(
                self.suite,
                descriptor,
                self.migration,
                self.inventory,
            )

    def test_validator_rejects_duplicate_descriptor_skill(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"].append(copy.deepcopy(descriptor["skills"][0]))
        errors = validate_production_source_promotion_plan(
            self.plan,
            descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "production descriptor contains duplicate research Skills" in error
                for error in errors
            ),
            errors,
        )

    def test_suite_skill_set_must_match_production_descriptor(self) -> None:
        suite = copy.deepcopy(self.suite)
        suite["skills"] = [
            item
            for item in suite["skills"]
            if item["id"] != "iterative-inquiry-synthesis"
        ]
        with self.assertRaisesRegex(
            ValueError,
            "Skill set must match production descriptor",
        ):
            plan_production_source_promotion(
                suite,
                self.descriptor,
                self.migration,
                self.inventory,
            )

    def test_public_name_migration_skill_set_must_match_descriptor(self) -> None:
        migration = copy.deepcopy(self.migration)
        del migration["research_to_production_name"]["affinity-synthesis"]
        with self.assertRaisesRegex(
            ValueError,
            "public-name migration Skill set must match production descriptor",
        ):
            plan_production_source_promotion(
                self.suite,
                self.descriptor,
                migration,
                self.inventory,
            )

    def test_public_name_migration_name_must_match_descriptor(self) -> None:
        migration = copy.deepcopy(self.migration)
        migration["research_to_production_name"]["affinity-synthesis"] = (
            "stale-material-synthesis"
        )
        with self.assertRaisesRegex(
            ValueError,
            "public-name migration must match descriptor installable name",
        ):
            plan_production_source_promotion(
                self.suite,
                self.descriptor,
                migration,
                self.inventory,
            )

    def test_planner_rejects_duplicate_descriptor_locale(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["locales"].append("ja-JP")
        with self.assertRaisesRegex(
            ValueError,
            "production descriptor locales must be a non-empty unique string list",
        ):
            plan_production_source_promotion(
                self.suite,
                descriptor,
                self.migration,
                self.inventory,
            )

    def test_validator_rejects_non_string_descriptor_locale(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["locales"].append(None)
        errors = validate_production_source_promotion_plan(
            self.plan,
            descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any(
                "production descriptor locales must be a non-empty unique string list"
                in error
                for error in errors
            ),
            errors,
        )

    def test_suite_locales_must_match_production_descriptor(self) -> None:
        suite = copy.deepcopy(self.suite)
        layer1 = next(
            item for item in suite["skills"] if item["id"] == "affinity-synthesis"
        )
        del layer1["locale_realizations"]["en-US"]
        with self.assertRaisesRegex(
            ValueError,
            "locale realizations must match production descriptor",
        ):
            plan_production_source_promotion(
                suite,
                self.descriptor,
                self.migration,
                self.inventory,
            )

    def test_plan_cannot_repeat_descriptor_skill(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"].append(copy.deepcopy(self.skill("affinity-synthesis", plan)))
        errors = self.validate(plan)
        self.assertTrue(
            any("production source plan repeats descriptor Skills" in error for error in errors),
            errors,
        )

    def test_plan_locale_set_cannot_drop_declared_realization(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        del layer1["locales"]["en-US"]
        errors = self.validate(plan)
        self.assertTrue(
            any("production source plan locale set mismatch" in error for error in errors),
            errors,
        )

    def test_plan_source_snapshot_must_match_descriptor_authority(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        layer1["source"]["root_pattern"] = "src/skills/other/{locale}"
        errors = self.validate(plan)
        self.assertTrue(
            any("source snapshot mismatch" in error for error in errors),
            errors,
        )

    def test_planner_rejects_unsafe_research_package_file(self) -> None:
        suite = copy.deepcopy(self.suite)
        layer1 = next(
            item for item in suite["skills"] if item["id"] == "affinity-synthesis"
        )
        layer1["locale_realizations"]["ja-JP"]["package_source"]["files"].append(
            "../outside.md"
        )
        with self.assertRaisesRegex(ValueError, "research package files are unsafe"):
            plan_production_source_promotion(
                suite,
                self.descriptor,
                self.migration,
                self.inventory,
            )

    def test_validator_rejects_unsafe_mapping_paths(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "affinity-synthesis",
            "ja-JP",
            "/references/TEMPLATE.md",
            plan,
        )
        mapping["source"] = "research/skill-prototypes/affinity-synthesis/../outside.md"
        mapping["source_relative"] = "../outside.md"
        mapping["target_relative"] = "../outside.md"
        mapping["target"] = "src/skills/material-led-synthesis/ja-JP/../outside.md"

        errors = self.validate(plan)
        self.assertTrue(
            any("source path is unsafe" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("source_relative is unsafe" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("target_relative is unsafe" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("target path is unsafe" in error for error in errors),
            errors,
        )

    def test_planner_rejects_unsafe_descriptor_production_root(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        layer1["production_source"]["root_pattern"] = (
            "src/skills/material-led-synthesis/{locale}/../../research"
        )
        with self.assertRaisesRegex(ValueError, "production source root is unsafe"):
            plan_production_source_promotion(
                self.suite,
                descriptor,
                self.migration,
                self.inventory,
            )

    def test_validator_rejects_coordinated_unsafe_production_root(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor_skill = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        descriptor_skill["production_source"]["root_pattern"] = (
            "src/skills/material-led-synthesis/{locale}/../../research"
        )

        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        layer1["source"] = copy.deepcopy(descriptor_skill["production_source"])
        for locale, locale_plan in layer1["locales"].items():
            unsafe_root = descriptor_skill["production_source"]["root_pattern"].format(
                locale=locale
            )
            locale_plan["production_root"] = unsafe_root
            locale_plan["runtime_entry"] = f"{unsafe_root}/SKILL.md"
            for mapping in locale_plan["mappings"]:
                mapping["target"] = (
                    f"{unsafe_root}/{mapping['target_relative']}"
                )

        errors = validate_production_source_promotion_plan(
            plan,
            descriptor,
            self.inventory,
            suite=self.suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("production source root must be a safe path" in error for error in errors),
            errors,
        )

    def test_locale_plan_production_root_must_match_descriptor_authority(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        locale_plan = layer1["locales"]["ja-JP"]
        drifted_root = "src/skills/material-led-synthesis/ja-JP-drift"
        locale_plan["production_root"] = drifted_root
        locale_plan["runtime_entry"] = f"{drifted_root}/SKILL.md"
        for mapping in locale_plan["mappings"]:
            mapping["target"] = (
                f"{drifted_root}/{mapping['target_relative']}"
            )
        errors = self.validate(plan)
        self.assertTrue(
            any(
                "production source root does not match descriptor authority" in error
                for error in errors
            ),
            errors,
        )

    def test_locale_plan_research_package_mode_must_remain_explicit_files(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        layer1["locales"]["ja-JP"]["research_package_mode"] = "directory"
        errors = self.validate(plan)
        self.assertTrue(
            any("research package mode must remain explicit_files" in error for error in errors),
            errors,
        )

    def test_locale_plan_copy_scope_is_authoritative(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer1 = self.skill("affinity-synthesis", plan)
        layer1["locales"]["en-US"]["copy_scope"] = "all-research-files"
        errors = self.validate(plan)
        self.assertTrue(
            any("production source copy scope mismatch" in error for error in errors),
            errors,
        )

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

    def test_layer1_japanese_progressive_support_rewrites_installable_identifier(self) -> None:
        cases = self.mapping("affinity-synthesis", "ja-JP", "/evals/CASES.md")
        dossier = self.mapping("affinity-synthesis", "ja-JP", "/evidence/dossier.md")
        for item in (cases, dossier):
            self.assertIn("rewrite-explicit-installable-name", item["content_transforms"])

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

    def test_projection_mapping_cannot_add_undeclared_transform(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "affinity-synthesis",
            "ja-JP",
            "/references/TEMPLATE.md",
            plan,
        )
        self.assertEqual(mapping["content_transforms"], [])
        mapping["content_transforms"].append("normalize-locale-suffixed-filename")
        errors = self.validate(plan)
        self.assertTrue(
            any("content transforms do not match declared authorities" in error for error in errors),
            errors,
        )

    def test_projection_mapping_transform_order_is_authoritative(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "affinity-synthesis",
            "en-US",
            "/SKILL.en.md",
            plan,
        )
        self.assertGreaterEqual(len(mapping["content_transforms"]), 2)
        mapping["content_transforms"] = list(reversed(mapping["content_transforms"]))
        errors = self.validate(plan)
        self.assertTrue(
            any("content transforms do not match declared authorities" in error for error in errors),
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

    def test_non_projection_sensitive_package_source_cannot_be_dropped_from_plan(self) -> None:
        plan = copy.deepcopy(self.plan)
        locale_plan = self.skill("affinity-synthesis", plan)["locales"]["ja-JP"]
        locale_plan["mappings"] = [
            item
            for item in locale_plan["mappings"]
            if not item["source_relative"].endswith("references/TEMPLATE.md")
        ]
        errors = self.validate(plan)
        self.assertTrue(
            any("missing package-selected source mappings" in error for error in errors),
            errors,
        )

    def test_undeclared_package_source_cannot_be_added_to_plan(self) -> None:
        plan = copy.deepcopy(self.plan)
        locale_plan = self.skill("affinity-synthesis", plan)["locales"]["ja-JP"]
        injected = copy.deepcopy(locale_plan["mappings"][0])
        injected["source"] = (
            "research/skill-prototypes/affinity-synthesis/references/UNDECLARED.md"
        )
        injected["source_relative"] = "references/UNDECLARED.md"
        injected["target"] = (
            "src/skills/material-led-synthesis/ja-JP/references/UNDECLARED.md"
        )
        injected["target_relative"] = "references/UNDECLARED.md"
        locale_plan["mappings"].append(injected)
        errors = self.validate(plan)
        self.assertTrue(
            any("contains undeclared source mappings" in error for error in errors),
            errors,
        )

    def test_mapping_target_relative_must_follow_source_normalization(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "affinity-synthesis",
            "ja-JP",
            "/references/TEMPLATE.md",
            plan,
        )
        mapping["target_relative"] = "references/RENAMED.md"
        mapping["target"] = "src/skills/material-led-synthesis/ja-JP/references/RENAMED.md"
        errors = self.validate(plan)
        self.assertTrue(
            any("target_relative does not match source normalization" in error for error in errors),
            errors,
        )

    def test_mapping_target_must_stay_under_declared_production_root(self) -> None:
        plan = copy.deepcopy(self.plan)
        mapping = self.mapping(
            "affinity-synthesis",
            "ja-JP",
            "/references/TEMPLATE.md",
            plan,
        )
        mapping["target"] = "src/skills/other/ja-JP/references/TEMPLATE.md"
        errors = self.validate(plan)
        self.assertTrue(
            any("target does not match production root" in error for error in errors),
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

    def test_excluded_research_metadata_must_match_suite_authority(self) -> None:
        plan = copy.deepcopy(self.plan)
        layer2 = self.skill("iterative-inquiry-synthesis", plan)
        layer2["excluded_research_metadata"] = []
        errors = self.validate(plan)
        self.assertTrue(
            any("excluded research metadata mismatch" in error for error in errors),
            errors,
        )

    def test_false_collision_flag_cannot_hide_normalized_target_collision(self) -> None:
        suite = copy.deepcopy(self.suite)
        layer1 = next(
            item for item in suite["skills"] if item["id"] == "affinity-synthesis"
        )
        package_source = layer1["locale_realizations"]["en-US"]["package_source"]
        package_source["files"].append("SKILL.md")

        plan = plan_production_source_promotion(
            suite,
            self.descriptor,
            self.migration,
            self.inventory,
        )
        locale_plan = next(
            item for item in plan["skills"] if item["research_id"] == "affinity-synthesis"
        )["locales"]["en-US"]
        self.assertTrue(locale_plan["target_collision"])
        locale_plan["target_collision"] = False

        errors = validate_production_source_promotion_plan(
            plan,
            self.descriptor,
            self.inventory,
            suite=suite,
            migration=self.migration,
        )
        self.assertTrue(
            any("production source target collision detected" in error for error in errors),
            errors,
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
