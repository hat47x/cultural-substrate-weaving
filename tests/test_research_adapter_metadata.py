from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
SCRIPTS_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_adapter_metadata import plan_adapter_metadata  # noqa: E402
from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402

SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
RESEARCH_OPENAI = ROOT / "research" / "skill-prototypes" / "adapters" / "openai-skill"
RESEARCH_BUNDLE_ROOT = ROOT / "research" / "skill-prototypes" / "adapters" / "claude-codex"


class ResearchAdapterMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, metadata: dict, fragment: str) -> None:
        errors = validate_adapter_metadata(ROOT, metadata)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def openai_entry(self, skill_id: str, locale: str, profile: str) -> dict:
        return self.metadata["distributions"]["openai_skill"]["skills"][skill_id][
            locale
        ][profile]

    def interface_without_policy(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8")
        before_policy, separator, _ = text.partition("policy:\n")
        self.assertEqual(separator, "policy:\n")
        return before_policy

    def bundle_metadata(self, locale: str) -> dict:
        path = RESEARCH_BUNDLE_ROOT / locale / "bundle-metadata.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_current_adapter_metadata_descriptor_is_consistent(self) -> None:
        self.assertEqual(validate_adapter_metadata(ROOT, self.metadata), [])

    def test_openai_metadata_covers_all_suite_skills_and_locales(self) -> None:
        openai = self.metadata["distributions"]["openai_skill"]
        suite_skill_ids = {skill["id"] for skill in self.suite["skills"]}
        suite_locales = set(self.suite["locales"])

        self.assertEqual(set(openai["skills"]), suite_skill_ids)
        for skill in openai["skills"].values():
            self.assertEqual(set(skill), suite_locales)

    def test_planned_openai_metadata_cannot_claim_source(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "affinity-synthesis"
        ]["en-US"]["interactive"]
        entry["status"] = "planned"
        self.assertIn("source", entry)
        self.assert_has_error(metadata, "planned openai_skill metadata")

    def test_existing_openai_metadata_source_must_exist(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["ja-JP"]["interactive"]
        entry["source"] = "adapters/openai-skill/ja-JP/DOES-NOT-EXIST.yaml"
        self.assert_has_error(metadata, "metadata source is missing")

    def test_prototype_openai_metadata_source_must_exist(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "affinity-synthesis"
        ]["en-US"]["interactive"]
        entry["source"] = "research/skill-prototypes/DOES-NOT-EXIST.yaml"
        self.assert_has_error(metadata, "metadata source is missing")

    def test_openai_profile_policy_is_checked_against_source(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["ja-JP"]["interactive"]
        entry["source"] = "adapters/openai-skill/ja-JP/openai.metered.yaml"
        self.assert_has_error(metadata, "allow_implicit_invocation: true")

    def test_multi_skill_bundle_prototype_must_remain_review_required(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["distributions"]["claude_plugin"][
            "review_required_for_multi_skill"
        ] = False
        self.assert_has_error(metadata, "must require review")

    def test_locale_catalog_must_declare_required_fields(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["distributions"]["claude_plugin"]["source"] = (
            "research/skill-prototypes/adapter-metadata-plan.json"
        )
        self.assert_has_error(metadata, "locale catalog does not declare metadata")

    def test_bundle_prototype_source_must_exist(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["distributions"]["claude_plugin"]["locales"]["en-US"][
            "prototype_source"
        ] = "research/skill-prototypes/DOES-NOT-EXIST.json"
        self.assert_has_error(metadata, "prototype metadata source is missing")

    def test_bundle_prototype_skill_composition_must_match_suite(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["claude_plugin"]["locales"]["en-US"]
        entry["prototype_source"] = "research/skill-prototypes/suite-manifest.json"
        self.assert_has_error(metadata, "prototype metadata en-US schema")

    def test_companion_openai_metadata_is_prototype_in_both_locales(self) -> None:
        for locale in ("ja-JP", "en-US"):
            for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
                for profile in ("interactive", "metered"):
                    entry = self.openai_entry(skill_id, locale, profile)
                    self.assertEqual(entry["status"], "prototype")
                    self.assertTrue((ROOT / entry["source"]).is_file())

    def test_companion_profiles_differ_only_in_invocation_policy(self) -> None:
        for locale in ("ja-JP", "en-US"):
            for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
                root = RESEARCH_OPENAI / locale / skill_id
                interactive = root / "openai.interactive.yaml"
                metered = root / "openai.metered.yaml"
                self.assertEqual(
                    self.interface_without_policy(interactive),
                    self.interface_without_policy(metered),
                )
                self.assertIn(
                    "allow_implicit_invocation: true",
                    interactive.read_text(encoding="utf-8"),
                )
                self.assertIn(
                    "allow_implicit_invocation: false",
                    metered.read_text(encoding="utf-8"),
                )

    def test_affinity_default_prompt_stays_one_round_and_material_led(self) -> None:
        ja = (
            RESEARCH_OPENAI
            / "ja-JP"
            / "affinity-synthesis"
            / "openai.interactive.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("一回の親和統合", ja)
        self.assertIn("先に分類体系を置かず", ja)
        self.assertNotIn("前ラウンド", ja)
        self.assertNotIn("文化体系", ja)

        en = (
            RESEARCH_OPENAI
            / "en-US"
            / "affinity-synthesis"
            / "openai.interactive.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("one round of affinity synthesis", en)
        self.assertIn("avoid predefined categories", en)
        self.assertNotIn("previous round", en)
        self.assertNotIn("cultural framework", en.lower())

    def test_iterative_default_prompt_delegates_one_round_synthesis(self) -> None:
        ja = (
            RESEARCH_OPENAI
            / "ja-JP"
            / "iterative-inquiry-synthesis"
            / "openai.interactive.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("前ラウンドを上書きせず", ja)
        self.assertIn("一回統合は利用可能な互換realizationへ委ね", ja)
        self.assertIn("残差・次の問い・停止理由", ja)
        self.assertNotIn("文化体系", ja)

        en = (
            RESEARCH_OPENAI
            / "en-US"
            / "iterative-inquiry-synthesis"
            / "openai.interactive.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("Do not overwrite the previous round", en)
        self.assertIn("delegate any needed one-round synthesis", en)
        self.assertIn("the next inquiry", en)
        self.assertIn("stop or handoff reasons", en)
        self.assertNotIn("cultural framework", en.lower())

    def test_bundle_metadata_keeps_three_roles_distinct_in_both_locales(self) -> None:
        expected_skills = {
            "cultural-substrate-weaving",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
        }

        ja = self.bundle_metadata("ja-JP")
        self.assertEqual(ja["plugin_name"], "cultural-substrate-weaving-ja")
        self.assertEqual(ja["invocation_policy"], "explicit")
        self.assertEqual(set(ja["contains"]), expected_skills)
        ja_description = ja["description"]
        self.assertIn("文化的体系による探索", ja_description)
        self.assertIn("一回統合", ja_description)
        self.assertIn("複数ラウンド", ja_description)
        self.assertIn("3つのSkill", ja_description)
        self.assertIn("handoff", ja_description)
        self.assertIn("万能手順", ja_description)

        en = self.bundle_metadata("en-US")
        self.assertEqual(en["plugin_name"], "cultural-substrate-weaving-en")
        self.assertEqual(en["invocation_policy"], "explicit")
        self.assertEqual(set(en["contains"]), expected_skills)
        en_description = en["description"]
        self.assertIn("cultural-framework exploration", en_description)
        self.assertIn("one-round material-led synthesis", en_description)
        self.assertIn("multi-round inquiry continuation", en_description)
        self.assertIn("three distinct Skills", en_description)
        self.assertIn("handoffs", en_description)
        self.assertIn("universal procedure", en_description)

    def test_openai_coverage_is_prototype_for_realized_in_both_locales(self) -> None:
        plan = plan_adapter_metadata(self.suite, self.metadata, ROOT)
        for locale in ("ja-JP", "en-US"):
            openai = plan["locales"][locale]["distributions"]["openai_skill"]
            self.assertEqual(openai["runtime_state"], "buildable")
            self.assertEqual(openai["metadata_coverage"], "prototype-for-realized")
            items = {item["skill_id"]: item for item in openai["items"]}
            self.assertEqual(
                items["cultural-substrate-weaving"]["metadata_state"], "existing"
            )
            self.assertEqual(items["affinity-synthesis"]["metadata_state"], "prototype")
            self.assertEqual(
                items["iterative-inquiry-synthesis"]["metadata_state"], "prototype"
            )
            self.assertEqual(items["affinity-synthesis"]["runtime_state"], "buildable")
            self.assertEqual(
                items["iterative-inquiry-synthesis"]["runtime_state"], "buildable"
            )

    def test_bundle_metadata_is_prototype_not_reviewed_in_both_locales(self) -> None:
        plan = plan_adapter_metadata(self.suite, self.metadata, ROOT)
        for locale, plugin_name in (
            ("ja-JP", "cultural-substrate-weaving-ja"),
            ("en-US", "cultural-substrate-weaving-en"),
        ):
            distributions = plan["locales"][locale]["distributions"]
            for distribution_name in ("claude_plugin", "codex_plugin"):
                distribution = distributions[distribution_name]
                self.assertEqual(distribution["runtime_state"], "buildable")
                self.assertEqual(distribution["metadata_state"], "prototype")
                self.assertEqual(distribution["source_kind"], "research-prototype")
                self.assertEqual(
                    distribution["catalog_entry"]["plugin_name"], plugin_name
                )
                self.assertEqual(
                    set(distribution["catalog_entry"]["contains"]),
                    {
                        "cultural-substrate-weaving",
                        "affinity-synthesis",
                        "iterative-inquiry-synthesis",
                    },
                )


if __name__ == "__main__":
    unittest.main()
