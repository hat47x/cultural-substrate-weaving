from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
for path in (SCRIPTS_DIR, PLANNER_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_production_builder_generalization import plan_production_builder  # noqa: E402
from validate_research_production_builder_contract import (  # noqa: E402
    validate_production_builder_contract,
)

CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
)
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


class ResearchProductionBuilderContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(
        self,
        contract: dict,
        fragment: str,
        *,
        descriptor: dict | None = None,
    ) -> None:
        errors = validate_production_builder_contract(
            ROOT,
            contract,
            self.descriptor if descriptor is None else descriptor,
        )
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def skill(self, research_id: str, *, descriptor: dict | None = None) -> dict:
        source = self.descriptor if descriptor is None else descriptor
        return next(
            skill
            for skill in source["skills"]
            if skill["research_id"] == research_id
        )

    def test_current_contract_is_valid(self) -> None:
        self.assertEqual(
            validate_production_builder_contract(ROOT, self.contract, self.descriptor),
            [],
        )

    def test_contract_never_authorizes_promotion(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["production_promotion_authorized"] = True
        self.assert_has_error(contract, "must not authorize production promotion")

    def test_production_builder_boundary_cannot_move_into_research(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["production_files"]["builder"] = (
            "research/skill-prototypes/build_preview.py"
        )
        self.assert_has_error(contract, "production_files must keep the planned production boundary")

    def test_target_names_cannot_default_back_to_research_ids(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["target_name_source"] = "production_descriptor.skills[].research_id"
        self.assert_has_error(
            contract,
            "production target names must be sourced from production_descriptor.skills[].targets",
        )

    def test_locale_tree_package_purity_validation_cannot_be_disabled(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["validation_requirements"].pop("locale_tree_source_package_purity")
        self.assert_has_error(contract, "validation_requirements set has drifted")

    def test_locale_tree_cannot_gain_research_only_exclusion_filter(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["invariants"] = [
            item
            for item in contract["invariants"]
            if "without a research-only exclusion filter" not in item
        ]
        self.assert_has_error(contract, "missing invariant fragment: without a research-only exclusion filter")

    def test_sibling_descriptor_source_mode_must_remain_locale_tree(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = self.skill("affinity-synthesis", descriptor=descriptor)
        layer1["production_source"] = {
            "mode": "explicit_files",
            "root": "src/skills/material-led-synthesis/ja-JP",
            "files": ["SKILL.md"],
        }
        self.assert_has_error(
            self.contract,
            "production source must use locale_tree",
            descriptor=descriptor,
        )

    def test_openai_profiles_cannot_drop_metered(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["first_wave"]["openai_skill"]["profiles"] = ["interactive"]
        self.assert_has_error(contract, "profiles must remain interactive and metered")

    def test_codex_cannot_materialize_a_second_skill_tree(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["first_wave"]["codex_plugin"]["mode"] = "separate_locale_bundle"
        self.assert_has_error(contract, "Codex builder mode must reuse the Claude Skill tree")

    def test_deferred_composite_cannot_enter_first_builder_change(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["deferred_composite"]["microsoft_copilot"]["first_wave_builder_change"] = True
        self.assert_has_error(
            contract,
            "deferred composite microsoft_copilot must remain outside the first builder change",
        )

    def test_planner_projects_layer1_public_name_not_research_id(self) -> None:
        plan = plan_production_builder(self.descriptor, self.contract)
        for locale in self.descriptor["locales"]:
            for profile in ("interactive", "metered"):
                skills = plan["locales"][locale]["distributions"]["openai_skill"]["profiles"][profile]["skills"]
                layer1 = next(item for item in skills if item["research_id"] == "affinity-synthesis")
                self.assertEqual(layer1["target_name"], "material-led-synthesis")
                self.assertTrue(layer1["target_root"].endswith("/material-led-synthesis"))
                self.assertFalse(layer1["target_root"].endswith("/affinity-synthesis"))

    def test_planner_exposes_package_closed_locale_tree_semantics(self) -> None:
        plan = plan_production_builder(self.descriptor, self.contract)
        for locale in self.descriptor["locales"]:
            skills = plan["locales"][locale]["distributions"]["openai_skill"]["profiles"]["interactive"]["skills"]
            for item in skills:
                if item["research_id"] == "cultural-substrate-weaving":
                    continue
                source = item["source"]
                self.assertEqual(source["mode"], "locale_tree")
                self.assertEqual(source["copy_scope"], "entire_locale_tree")
                self.assertTrue(source["package_closed"])
                self.assertEqual(source["exclusion_filter"], "none")
                self.assertEqual(
                    source["operation"],
                    "copy_locale_tree_preserving_runtime_relative_paths",
                )

    def test_planner_preserves_existing_csw_target_identities(self) -> None:
        plan = plan_production_builder(self.descriptor, self.contract)
        for locale in self.descriptor["locales"]:
            openai_skills = plan["locales"][locale]["distributions"]["openai_skill"]["profiles"]["interactive"]["skills"]
            openai_csw = next(item for item in openai_skills if item["research_id"] == "cultural-substrate-weaving")
            self.assertEqual(openai_csw["target_name"], "cultural-substrate-weaving")

            claude_skills = plan["locales"][locale]["distributions"]["claude_plugin"]["skills"]
            claude_csw = next(item for item in claude_skills if item["research_id"] == "cultural-substrate-weaving")
            self.assertEqual(claude_csw["target_name"], "weave")

    def test_planner_reuses_exact_claude_tree_for_codex(self) -> None:
        plan = plan_production_builder(self.descriptor, self.contract)
        for locale in self.descriptor["locales"]:
            distributions = plan["locales"][locale]["distributions"]
            claude_roots = [item["target_root"] for item in distributions["claude_plugin"]["skills"]]
            codex_roots = [item["target_root"] for item in distributions["codex_plugin"]["skills"]]
            self.assertEqual(claude_roots, codex_roots)
            self.assertFalse(distributions["codex_plugin"]["new_release_zip_kind"])

    def test_planner_does_not_add_composites_to_first_wave_locale_distributions(self) -> None:
        plan = plan_production_builder(self.descriptor, self.contract)
        for locale in self.descriptor["locales"]:
            distributions = plan["locales"][locale]["distributions"]
            self.assertEqual(
                set(distributions),
                {"openai_skill", "claude_plugin", "codex_plugin"},
            )


if __name__ == "__main__":
    unittest.main()
