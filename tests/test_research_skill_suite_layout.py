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

    def test_current_artifact_layout_is_buildable_in_both_locales(self) -> None:
        plan = plan_suite(self.manifest)
        expected_names = {"cultural-substrate-weaving": "weave", "affinity-synthesis": "affinity-synthesis", "iterative-inquiry-synthesis": "iterative-inquiry-synthesis"}
        for locale in ("ja-JP", "en-US"):
            distributions = plan["locales"][locale]["distributions"]
            for name in ("openai_skill", "claude_plugin", "codex_plugin", "chatgpt_gpt", "microsoft_copilot"):
                self.assertEqual(distributions[name]["state"], "buildable")
            self.assertEqual(distributions["claude_plugin"]["target_skill_names"], expected_names)
            self.assertEqual(distributions["codex_plugin"]["target_skill_names"], expected_names)
        self.assertIn("no sibling Skill-tree target name is required here", plan["locales"]["en-US"]["distributions"]["chatgpt_gpt"]["scope"])

    def test_english_draft_is_artifact_buildable_not_promotion_ready(self) -> None:
        plan = plan_suite(self.manifest)
        en_items = {item["skill_id"]: item for item in plan["locales"]["en-US"]["distributions"]["openai_skill"]["items"]}
        self.assertEqual(en_items["affinity-synthesis"]["state"], "buildable")
        self.assertEqual(en_items["affinity-synthesis"]["status"], "translated-draft")
        self.assertEqual(en_items["iterative-inquiry-synthesis"]["state"], "buildable")
        self.assertEqual(self.manifest["locales"]["en-US"]["status"], "translated-draft")

    def test_missing_distribution_target_blocks_only_that_distribution(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["en-US"]["package_targets"].pop("claude_plugin")
        plan = plan_suite(manifest)
        en = plan["locales"]["en-US"]["distributions"]
        self.assertEqual(en["openai_skill"]["state"], "buildable")
        self.assertEqual(en["claude_plugin"]["state"], "blocked")
        self.assertEqual(en["claude_plugin"]["missing_skills"], ["affinity-synthesis"])
        self.assertEqual(en["codex_plugin"]["state"], "buildable")

    def test_locale_bundle_blocks_when_skill_becomes_planned(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        self.skill(manifest, "affinity-synthesis")["locale_realizations"]["en-US"] = {"status": "planned"}
        plan = plan_suite(manifest)
        en = plan["locales"]["en-US"]["distributions"]
        self.assertEqual(en["openai_skill"]["state"], "partial")
        self.assertEqual(en["claude_plugin"]["state"], "blocked")
        self.assertEqual(en["codex_plugin"]["state"], "blocked")

    def test_bundle_reports_unknown_target_skill_as_missing(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["claude_plugin"]["contains"].append("not-declared")
        plan = plan_suite(manifest)
        self.assertIn("not-declared", plan["locales"]["ja-JP"]["distributions"]["claude_plugin"]["missing_skills"])

    def test_composite_blocks_when_primary_realization_is_planned(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        self.skill(manifest, "cultural-substrate-weaving")["locale_realizations"]["en-US"] = {"status": "planned"}
        plan = plan_suite(manifest)
        en = plan["locales"]["en-US"]["distributions"]
        self.assertEqual(en["chatgpt_gpt"]["state"], "blocked")
        self.assertEqual(en["microsoft_copilot"]["state"], "blocked")

    def test_unknown_distribution_mode_is_not_silently_buildable(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["future_surface"] = {"mode": "future-mode"}
        self.assertEqual(plan_suite(manifest)["locales"]["ja-JP"]["distributions"]["future_surface"]["state"], "unsupported")


if __name__ == "__main__":
    unittest.main()
