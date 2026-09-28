from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from plan_production_adapter_metadata_promotion import (  # noqa: E402
    main as adapter_promotion_main,
    plan_production_adapter_metadata_promotion,
    validate_adapter_promotion_authorities,
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

    def errors(
        self,
        plan: dict | None = None,
        adapter_plan: dict | None = None,
    ) -> list[str]:
        return validate_production_adapter_metadata_promotion_plan(
            self.plan if plan is None else plan,
            self.descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan if adapter_plan is None else adapter_plan,
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

    def test_cli_authorities_reject_non_object_roots_without_crashing(self) -> None:
        errors = validate_adapter_promotion_authorities(
            ROOT,
            [],
            [],
        )
        for expected in (
            "adapter metadata plan authority must be an object",
            "production promotion descriptor authority must be an object",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_cli_validates_authority_before_bundle_catalog_derivation(self) -> None:
        with patch(
            "plan_production_adapter_metadata_promotion.json.loads",
            side_effect=[[], self.descriptor],
        ), patch(
            "plan_production_adapter_metadata_promotion._bundle_catalog_source",
            side_effect=AssertionError("bundle catalog derivation must not run"),
        ):
            self.assertEqual(adapter_promotion_main(), 1)

    def test_validator_rejects_non_object_plan_without_crashing(self) -> None:
        errors = validate_production_adapter_metadata_promotion_plan(
            [],
            self.descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertEqual(
            errors,
            ["adapter metadata promotion plan must be an object"],
        )

    def test_validator_rejects_non_object_descriptor_without_crashing(self) -> None:
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            [],
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any("production promotion descriptor must be an object" in error for error in errors),
            errors,
        )

    def test_planner_rejects_non_object_locale_catalog(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "production locale catalog must be an object",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                self.descriptor,
                [],
            )

    def test_validator_rejects_non_object_locale_catalog_without_crashing(self) -> None:
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            self.descriptor,
            [],
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any("production locale catalog must be an object" in error for error in errors),
            errors,
        )

    def test_validator_reports_malformed_descriptor_skills_without_crashing(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"] = None
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any("production promotion descriptor skills must be a list" in error for error in errors),
            errors,
        )

    def test_validator_composes_full_descriptor_gate_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["complete_checkout_validation"][
            "production_promotion_authorized"
        ] = True
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any(
                "complete_checkout_validation.production_promotion_authorized must remain False"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_requires_adapter_plan_authority(self) -> None:
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            self.descriptor,
            self.locale_catalog,
        )
        self.assertTrue(
            any(
                "adapter metadata promotion validation requires adapter-plan authority"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_rejects_non_object_adapter_plan_authority_without_crashing(self) -> None:
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            self.descriptor,
            self.locale_catalog,
            adapter_plan=[],
        )
        self.assertTrue(
            any("adapter metadata plan authority must be an object" in error for error in errors),
            errors,
        )

    def test_validator_composes_full_adapter_metadata_authority(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["profiles"]["interactive"][
            "expected_allow_implicit_invocation"
        ] = "yes"
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            self.descriptor,
            self.locale_catalog,
            adapter_plan=adapter_plan,
        )
        self.assertTrue(
            any(
                "expected_allow_implicit_invocation must be boolean" in error
                for error in errors
            ),
            errors,
        )

    def test_current_adapter_promotion_plan_is_valid(self) -> None:
        self.assertEqual(self.errors(), [])
        self.assertFalse(self.plan["writes_production_metadata"])
        self.assertEqual(len(self.plan["openai_profile_promotions"]), 12)
        self.assertEqual(len(self.plan["locale_bundle_promotions"]), 2)

    def test_validator_rejects_non_string_openai_identity_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["openai_profile_promotions"][0]["locale"] = []
        errors = self.errors(plan)
        self.assertTrue(
            any(
                "OpenAI adapter promotion identity fields must be non-empty strings"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_rejects_non_string_bundle_locale_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["locale_bundle_promotions"][0]["locale"] = []
        errors = self.errors(plan)
        self.assertTrue(
            any(
                "bundle metadata promotion locale must be a non-empty string"
                in error
                for error in errors
            ),
            errors,
        )

    def test_openai_profiles_follow_adapter_plan_authority(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        openai = adapter_plan["distributions"]["openai_skill"]
        openai["profiles"]["audit"] = {"expected_allow_implicit_invocation": False}
        for research_id, skill_metadata in openai["skills"].items():
            for locale, locale_profiles in skill_metadata.items():
                audit = copy.deepcopy(locale_profiles["interactive"])
                if research_id == "cultural-substrate-weaving":
                    audit["source"] = f"adapters/openai-skill/{locale}/openai.audit.yaml"
                locale_profiles["audit"] = audit

        plan = plan_production_adapter_metadata_promotion(
            adapter_plan,
            self.descriptor,
            self.locale_catalog,
        )
        self.assertEqual(
            {item["profile"] for item in plan["openai_profile_promotions"]},
            {"interactive", "metered", "audit"},
        )
        self.assertEqual(len(plan["openai_profile_promotions"]), 18)
        self.assertEqual(self.errors(plan, adapter_plan), [])

    def test_locale_bundle_distributions_follow_adapter_plan_authority(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["future_plugin"] = copy.deepcopy(
            adapter_plan["distributions"]["claude_plugin"]
        )

        plan = plan_production_adapter_metadata_promotion(
            adapter_plan,
            self.descriptor,
            self.locale_catalog,
        )
        for item in plan["locale_bundle_promotions"]:
            self.assertEqual(
                item["shared_by"],
                ["claude_plugin", "codex_plugin", "future_plugin"],
            )
        self.assertEqual(self.errors(plan, adapter_plan), [])

    def test_planner_rejects_non_list_descriptor_skills(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"] = None
        with self.assertRaisesRegex(
            ValueError,
            "production promotion descriptor skills must be a list",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_malformed_descriptor_skill_entry(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"].append([])
        with self.assertRaisesRegex(
            ValueError,
            "production descriptor Skill entry must declare research_id",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_non_object_openai_profile_entry(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"][
            "affinity-synthesis"
        ]["ja-JP"]["interactive"] = []
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata entry affinity-synthesis/ja-JP/interactive must be an object",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_non_object_authority_roots(self) -> None:
        cases = (
            ("adapter_plan", [], self.descriptor, self.locale_catalog, "adapter metadata plan authority must be an object"),
            ("descriptor", self.adapter_plan, [], self.locale_catalog, "production promotion descriptor authority must be an object"),
            ("locale_catalog", self.adapter_plan, self.descriptor, [], "production locale catalog must be an object"),
        )
        for label, adapter_plan, descriptor, locale_catalog, expected in cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, expected):
                    plan_production_adapter_metadata_promotion(
                        adapter_plan,
                        descriptor,
                        locale_catalog,
                    )

    def test_planner_rejects_malformed_descriptor_adapter_metadata(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        affinity = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        affinity["adapter_metadata"] = None
        with self.assertRaisesRegex(
            ValueError,
            "skill affinity-synthesis adapter_metadata must be an object",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

        descriptor = copy.deepcopy(self.descriptor)
        affinity = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        affinity["adapter_metadata"]["openai_skill"] = []
        with self.assertRaisesRegex(
            ValueError,
            "skill affinity-synthesis OpenAI adapter_metadata must be an object",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_non_object_openai_skills_map(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"] = []
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata plan must declare a skills object",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_duplicate_descriptor_skill(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"].append(copy.deepcopy(descriptor["skills"][0]))
        with self.assertRaisesRegex(
            ValueError,
            "production descriptor contains duplicate research Skills",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_validator_rejects_duplicate_descriptor_skill(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["skills"].append(copy.deepcopy(descriptor["skills"][0]))
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any(
                "production descriptor contains duplicate research Skills" in error
                for error in errors
            ),
            errors,
        )

    def test_planner_rejects_duplicate_descriptor_locale(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["locales"].append("ja-JP")
        with self.assertRaisesRegex(
            ValueError,
            "production descriptor locales must be a non-empty unique string list",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_adapter_plan_schema_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["schema"] = "csw.research-adapter-metadata-plan/v0"
        with self.assertRaisesRegex(
            ValueError,
            "adapter metadata plan schema must remain",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_suite_manifest_pointer_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["suite_manifest"] = (
            "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
        )
        with self.assertRaisesRegex(
            ValueError,
            "adapter metadata suite_manifest must remain canonical",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_validator_rejects_suite_manifest_pointer_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["suite_manifest"] = (
            "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
        )
        errors = self.errors(self.plan, adapter_plan)
        self.assertTrue(
            any(
                "adapter metadata suite_manifest must remain canonical" in error
                for error in errors
            ),
            errors,
        )

    def test_planner_rejects_openai_scope_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["scope"] = "locale_bundle"
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata scope must remain per_skill_per_profile",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_missing_required_bundle_distribution(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["claude_plugin"]["scope"] = "standalone_per_skill"
        with self.assertRaisesRegex(
            ValueError,
            "missing required locale_bundle distributions",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_bundle_source_mode_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["codex_plugin"]["source_mode"] = "per_skill_files"
        with self.assertRaisesRegex(
            ValueError,
            "must use source_mode=locale_catalog",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_validator_rejects_bundle_source_mode_drift(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["codex_plugin"]["source_mode"] = "per_skill_files"
        errors = self.errors(self.plan, adapter_plan)
        self.assertTrue(
            any("must use source_mode=locale_catalog" in error for error in errors),
            errors,
        )

    def test_openai_skill_set_must_match_production_descriptor(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        del adapter_plan["distributions"]["openai_skill"]["skills"]["iterative-inquiry-synthesis"]
        with self.assertRaisesRegex(
            ValueError,
            "skill set must match production descriptor",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_openai_locales_must_match_production_descriptor(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        del adapter_plan["distributions"]["openai_skill"]["skills"]["affinity-synthesis"]["en-US"]
        with self.assertRaisesRegex(
            ValueError,
            "locales must match production descriptor",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_openai_profiles_must_match_declared_profiles(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        del adapter_plan["distributions"]["openai_skill"]["skills"]["affinity-synthesis"]["ja-JP"]["metered"]
        with self.assertRaisesRegex(
            ValueError,
            "profiles must match declared profiles",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_bundle_locales_must_match_production_descriptor(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        for distribution_name in ("claude_plugin", "codex_plugin"):
            del adapter_plan["distributions"][distribution_name]["locales"]["en-US"]
        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle metadata locales must match production descriptor",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_unsafe_openai_source_before_read(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"]["affinity-synthesis"][
            "ja-JP"
        ]["interactive"]["source"] = "../outside.yaml"
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata source is invalid",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_safe_but_wrong_prototype_source_class(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"][
            "iterative-inquiry-synthesis"
        ]["en-US"]["interactive"]["source"] = (
            "research/skill-prototypes/affinity-synthesis/SKILL.md"
        )
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata source is outside declared source class",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_existing_source_outside_production_adapter_tree(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["ja-JP"]["interactive"]["source"] = (
            "research/skill-prototypes/adapters/openai-skill/ja-JP/"
            "cultural-substrate-weaving/openai.interactive.yaml"
        )
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata source is outside declared source class",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_unsafe_openai_target(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item
            for item in descriptor["skills"]
            if item["research_id"] == "affinity-synthesis"
        )
        layer1["adapter_metadata"]["openai_skill"]["source_pattern"] = (
            "adapters/openai-skill/{locale}/../../outside/openai.{profile}.yaml"
        )
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI production metadata target is invalid",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_csw_openai_descriptor_path_drift(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        csw = next(
            item
            for item in descriptor["skills"]
            if item["research_id"] == "cultural-substrate-weaving"
        )
        csw["adapter_metadata"]["openai_skill"]["source_pattern"] = (
            "adapters/openai-skill/{locale}/cultural-substrate-weaving/"
            "openai.{profile}.yaml"
        )
        with self.assertRaisesRegex(
            ValueError,
            "OpenAI adapter metadata path mismatch",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_bundle_descriptor_source_drift(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item
            for item in descriptor["skills"]
            if item["research_id"] == "affinity-synthesis"
        )
        layer1["adapter_metadata"]["claude_plugin"]["source"] = (
            "adapters/claude-code/other-locales.json"
        )
        with self.assertRaisesRegex(
            ValueError,
            "locale-bundle adapter metadata source mismatch",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_bundle_descriptor_mode_drift(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        iterative = next(
            item
            for item in descriptor["skills"]
            if item["research_id"] == "iterative-inquiry-synthesis"
        )
        iterative["adapter_metadata"]["codex_plugin"]["mode"] = (
            "existing-locale-catalog-to-update"
        )
        with self.assertRaisesRegex(
            ValueError,
            "locale-bundle adapter metadata mode mismatch",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_bundle_prototype_outside_research_source_class(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        for distribution_name in ("claude_plugin", "codex_plugin"):
            adapter_plan["distributions"][distribution_name]["locales"]["ja-JP"][
                "prototype_source"
            ] = "research/skill-prototypes/adapter-metadata-plan.json"

        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle prototype source is outside research bundle source class",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_coordinated_noncanonical_bundle_catalog(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        descriptor = copy.deepcopy(self.descriptor)
        drifted_source = "adapters/claude-code/other-locales.json"
        for distribution_name in ("claude_plugin", "codex_plugin"):
            adapter_plan["distributions"][distribution_name]["source"] = drifted_source
        for skill in descriptor["skills"]:
            for distribution_name in ("claude_plugin", "codex_plugin"):
                skill["adapter_metadata"][distribution_name]["source"] = drifted_source

        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle production catalog must remain canonical",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_drifted_locale_catalog_snapshot(self) -> None:
        locale_catalog = copy.deepcopy(self.locale_catalog)
        locale_catalog["ja-JP"]["display"] = "drifted display"
        with self.assertRaisesRegex(
            ValueError,
            "locale catalog snapshot must match canonical production catalog source",
        ):
            plan_production_adapter_metadata_promotion(
                self.adapter_plan,
                self.descriptor,
                locale_catalog,
            )

    def test_validator_rejects_drifted_locale_catalog_snapshot(self) -> None:
        locale_catalog = copy.deepcopy(self.locale_catalog)
        locale_catalog["en-US"]["display"] = "drifted display"
        errors = validate_production_adapter_metadata_promotion_plan(
            self.plan,
            self.descriptor,
            locale_catalog,
            adapter_plan=self.adapter_plan,
        )
        self.assertTrue(
            any(
                "locale catalog snapshot must match canonical production catalog source"
                in error
                for error in errors
            ),
            errors,
        )

    def test_planner_rejects_unhashable_bundle_catalog_source(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        for distribution_name in ("claude_plugin", "codex_plugin"):
            adapter_plan["distributions"][distribution_name]["source"] = []
        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle production catalog path is invalid",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_planner_rejects_bundle_catalog_outside_production_source_class(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        for distribution_name in ("claude_plugin", "codex_plugin"):
            adapter_plan["distributions"][distribution_name]["source"] = (
                "research/skill-prototypes/adapter-metadata-plan.json"
            )

        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle production catalog is outside production adapter source class",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

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

    def test_bundle_drop_fields_must_match_prototype_source(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("en-US", plan)
        item["drop_prototype_fields_from_host_catalog"].remove("invocation_policy")
        errors = self.errors(plan)
        self.assertTrue(
            any("drop-field set must match prototype source" in error for error in errors),
            errors,
        )

    def test_bundle_host_visible_field_cannot_be_added_to_drop_fields(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("ja-JP", plan)
        item["drop_prototype_fields_from_host_catalog"].append("description")
        errors = self.errors(plan)
        self.assertTrue(
            any("drop-field set must match prototype source" in error for error in errors),
            errors,
        )

    def test_layer1_research_id_cannot_leak_into_openai_production_target(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "ja-JP", "interactive", plan)
        item["target"] = "adapters/openai-skill/ja-JP/affinity-synthesis/openai.interactive.yaml"
        errors = self.errors(plan)
        self.assertTrue(any("must use material-led-synthesis" in error for error in errors), errors)

    def test_renamed_openai_byte_identical_source_cannot_expose_research_id(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"]["affinity-synthesis"][
            "ja-JP"
        ]["interactive"]["source"] = "research/skill-prototypes/suite-manifest.json"
        with self.assertRaisesRegex(ValueError, "retains renamed research identity"):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_bundle_description_cannot_expose_renamed_research_id(self) -> None:
        real_loads = json.loads

        def loads_with_research_id(text: str, *args: object, **kwargs: object) -> object:
            value = real_loads(text, *args, **kwargs)
            if (
                isinstance(value, dict)
                and value.get("schema") == "csw.research-locale-bundle-metadata/v1"
            ):
                value = copy.deepcopy(value)
                value["description"] += " affinity-synthesis"
            return value

        with patch(
            "plan_production_adapter_metadata_promotion.json.loads",
            side_effect=loads_with_research_id,
        ):
            with self.assertRaisesRegex(ValueError, "retains renamed research identity"):
                plan_production_adapter_metadata_promotion(
                    self.adapter_plan,
                    self.descriptor,
                    self.locale_catalog,
                )

    def test_planned_promotion_requires_prototype_research_status(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"]["affinity-synthesis"][
            "ja-JP"
        ]["interactive"]["status"] = "existing"
        with self.assertRaisesRegex(
            ValueError,
            "status does not match production metadata mode",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

        errors = self.errors(self.plan, adapter_plan)
        self.assertTrue(
            any("status does not match production metadata mode" in error for error in errors),
            errors,
        )

    def test_existing_production_metadata_requires_existing_research_status(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["en-US"]["metered"]["status"] = "prototype"
        with self.assertRaisesRegex(
            ValueError,
            "status does not match production metadata mode",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

        errors = self.errors(self.plan, adapter_plan)
        self.assertTrue(
            any("status does not match production metadata mode" in error for error in errors),
            errors,
        )

    def test_sibling_openai_metadata_cannot_gain_content_rewrite(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "en-US", "metered", plan)
        item["content_operation"] = "rewrite-display-name"
        errors = self.errors(plan)
        self.assertTrue(any("promote byte-identically" in error for error in errors), errors)

    def test_sibling_openai_source_must_match_adapter_plan_authority(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "ja-JP", "interactive", plan)
        item["source"] = (
            "research/skill-prototypes/adapters/openai-skill/ja-JP/"
            "iterative-inquiry-synthesis/openai.interactive.yaml"
        )
        errors = self.errors(plan)
        self.assertTrue(
            any("OpenAI adapter promotion source mismatch" in error for error in errors),
            errors,
        )

    def test_sibling_openai_sha256_must_match_source_content(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.openai_item("affinity-synthesis", "en-US", "metered", plan)
        item["sha256"] = "0" * 64
        errors = self.errors(plan)
        self.assertTrue(
            any("OpenAI adapter promotion source sha256 mismatch" in error for error in errors),
            errors,
        )

    def test_bundle_locale_coverage_rejects_duplicate_that_hides_missing_locale(self) -> None:
        plan = copy.deepcopy(self.plan)
        en = self.bundle_item("en-US", plan)
        en["locale"] = "ja-JP"

        errors = self.errors(plan)
        self.assertTrue(
            any("duplicate locale-bundle promotion entry: ja-JP" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                "bundle metadata promotion plan is missing declared locales" in error
                and "en-US" in error
                for error in errors
            ),
            errors,
        )

    def test_bundle_locale_coverage_rejects_undeclared_locale(self) -> None:
        plan = copy.deepcopy(self.plan)
        en = self.bundle_item("en-US", plan)
        en["locale"] = "fr-FR"

        errors = self.errors(plan)
        self.assertTrue(
            any(
                "bundle metadata promotion plan has undeclared locales" in error
                and "fr-FR" in error
                for error in errors
            ),
            errors,
        )
        self.assertTrue(
            any(
                "bundle metadata promotion plan is missing declared locales" in error
                and "en-US" in error
                for error in errors
            ),
            errors,
        )

    def test_bundle_promotion_requires_prototype_status(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["claude_plugin"]["locales"]["ja-JP"][
            "status"
        ] = "reviewed"
        with self.assertRaisesRegex(
            ValueError,
            "must remain prototype",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_bundle_promotion_requires_multi_skill_review_gate(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["codex_plugin"][
            "review_required_for_multi_skill"
        ] = False
        with self.assertRaisesRegex(
            ValueError,
            "must require review for multi-Skill promotion",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_bundle_description_must_match_prototype_source(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("ja-JP", plan)
        item["update"]["description"] += " modified"
        errors = self.errors(plan)
        self.assertTrue(
            any("description must match prototype source" in error for error in errors),
            errors,
        )

    def test_bundle_research_composition_rejects_unhashable_values_without_crashing(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("ja-JP", plan)
        item["prototype_research_contains"] = [
            "cultural-substrate-weaving",
            "affinity-synthesis",
            {"id": "iterative-inquiry-synthesis"},
        ]
        errors = self.errors(plan)
        self.assertTrue(
            any("bundle prototype research composition mismatch" in error for error in errors),
            errors,
        )

    def test_bundle_research_composition_must_match_prototype_source(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("en-US", plan)
        item["prototype_research_contains"] = list(
            reversed(item["prototype_research_contains"])
        )
        errors = self.errors(plan)
        self.assertTrue(
            any("research composition must match prototype source" in error for error in errors),
            errors,
        )

    def test_bundle_promotion_state_must_match_wording_update_mode(self) -> None:
        plan = copy.deepcopy(self.plan)
        item = self.bundle_item("en-US", plan)
        item["state"] = "ready-for-production"
        errors = self.errors(plan)
        self.assertTrue(
            any("promotion state must match planned wording-update mode" in error for error in errors),
            errors,
        )

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
