from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
sys.path.insert(0, str(PLANNER_DIR))

from plan_suite_layout import plan_suite  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchSkillSuiteLayoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def realize_like_canonical(self, manifest: dict, skill_id: str, locale: str) -> None:
        skill = self.skill(manifest, skill_id)
        canonical = skill["locale_realizations"][manifest["canonical_locale"]]
        skill["locale_realizations"][locale] = {
            "status": "prototype",
            "runtime_entry": canonical["runtime_entry"],
            "package_source": copy.deepcopy(canonical["package_source"]),
        }

    def test_current_locale_buildability_is_explicit(self) -> None:
        plan = plan_suite(self.manifest)

        ja = plan["locales"]["ja-JP"]["distributions"]
        en = plan["locales"]["en-US"]["distributions"]

        self.assertEqual(ja["openai_skill"]["state"], "buildable")
        self.assertEqual(ja["claude_plugin"]["state"], "buildable")
        self.assertEqual(ja["codex_plugin"]["state"], "buildable")

        self.assertEqual(en["openai_skill"]["state"], "partial")
        self.assertEqual(en["claude_plugin"]["state"], "blocked")
        self.assertEqual(en["codex_plugin"]["state"], "blocked")
        self.assertEqual(
            en["claude_plugin"]["missing_skills"],
            ["affinity-synthesis", "iterative-inquiry-synthesis"],
        )

        self.assertEqual(en["chatgpt_gpt"]["state"], "buildable")
        self.assertEqual(en["microsoft_copilot"]["state"], "buildable")
        self.assertIn("primary realization", en["chatgpt_gpt"]["scope"])

    def test_openai_standalones_expose_package_sources(self) -> None:
        plan = plan_suite(self.manifest)
        ja_items = {
            item["skill_id"]: item
            for item in plan["locales"]["ja-JP"]["distributions"]["openai_skill"]["items"]
        }
        en_items = {
            item["skill_id"]: item
            for item in plan["locales"]["en-US"]["distributions"]["openai_skill"]["items"]
        }

        self.assertEqual(
            ja_items["affinity-synthesis"]["package_source"]["mode"],
            "explicit_files",
        )
        self.assertEqual(
            ja_items["cultural-substrate-weaving"]["package_source"]["mode"],
            "canonical_manifest",
        )
        self.assertEqual(en_items["cultural-substrate-weaving"]["state"], "buildable")
        self.assertEqual(en_items["affinity-synthesis"]["state"], "blocked")
        self.assertEqual(en_items["affinity-synthesis"]["status"], "planned")
        self.assertIsNone(en_items["affinity-synthesis"]["package_source"])
        self.assertEqual(en_items["iterative-inquiry-synthesis"]["state"], "blocked")

    def test_locale_bundle_unblocks_only_when_all_target_skills_are_realized(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
            self.realize_like_canonical(manifest, skill_id, "en-US")

        plan = plan_suite(manifest)
        en = plan["locales"]["en-US"]["distributions"]

        self.assertEqual(en["claude_plugin"]["state"], "buildable")
        self.assertEqual(en["claude_plugin"]["missing_skills"], [])
        self.assertEqual(en["codex_plugin"]["state"], "buildable")

    def test_runtime_entry_without_package_source_is_not_buildable(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"].pop("package_source")

        plan = plan_suite(manifest)
        ja_items = {
            item["skill_id"]: item
            for item in plan["locales"]["ja-JP"]["distributions"]["openai_skill"]["items"]
        }

        self.assertEqual(ja_items["affinity-synthesis"]["state"], "blocked")
        self.assertIsNone(ja_items["affinity-synthesis"]["package_source"])

    def test_bundle_reports_unknown_target_skill_as_missing(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["claude_plugin"]["contains"].append(
            "not-declared"
        )

        plan = plan_suite(manifest)
        claude = plan["locales"]["ja-JP"]["distributions"]["claude_plugin"]

        self.assertEqual(claude["state"], "blocked")
        self.assertIn("not-declared", claude["missing_skills"])

    def test_composite_blocks_when_primary_realization_is_planned(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        csw = self.skill(manifest, "cultural-substrate-weaving")
        csw["locale_realizations"]["en-US"] = {"status": "planned"}

        plan = plan_suite(manifest)
        en = plan["locales"]["en-US"]["distributions"]

        self.assertEqual(en["chatgpt_gpt"]["state"], "blocked")
        self.assertEqual(en["microsoft_copilot"]["state"], "blocked")

    def test_unknown_distribution_mode_is_not_silently_buildable(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["future_surface"] = {"mode": "future-mode"}

        plan = plan_suite(manifest)

        self.assertEqual(
            plan["locales"]["ja-JP"]["distributions"]["future_surface"]["state"],
            "unsupported",
        )


if __name__ == "__main__":
    unittest.main()
