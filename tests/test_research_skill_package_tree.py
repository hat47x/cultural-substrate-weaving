from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
sys.path.insert(0, str(PLANNER_DIR))

from plan_package_tree import plan_package_trees  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchSkillPackageTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def tree(self, plan: dict, locale: str, distribution: str, skill_id: str) -> dict:
        return next(
            item
            for item in plan["locales"][locale]["distributions"][distribution]["skill_trees"]
            if item["skill_id"] == skill_id
        )

    def test_current_plan_has_no_target_path_collisions(self) -> None:
        plan, errors = plan_package_trees(self.manifest)
        self.assertEqual(errors, [])
        for locale in ("ja-JP", "en-US"):
            for distribution in ("openai_skill", "claude_plugin", "codex_plugin"):
                self.assertEqual(
                    plan["locales"][locale]["distributions"][distribution]["collisions"],
                    {},
                )

    def test_bundle_target_roots_are_distribution_specific(self) -> None:
        plan, _ = plan_package_trees(self.manifest)
        expected = {
            "cultural-substrate-weaving": "skills/weave",
            "affinity-synthesis": "skills/affinity-synthesis",
            "iterative-inquiry-synthesis": "skills/iterative-inquiry-synthesis",
        }
        for locale in ("ja-JP", "en-US"):
            for distribution in ("claude_plugin", "codex_plugin"):
                actual = {
                    item["skill_id"]: item["target_root"]
                    for item in plan["locales"][locale]["distributions"][distribution]["skill_trees"]
                }
                self.assertEqual(actual, expected)

    def test_english_runtime_projects_to_canonical_skill_filename(self) -> None:
        plan, _ = plan_package_trees(self.manifest)
        affinity = self.tree(plan, "en-US", "openai_skill", "affinity-synthesis")
        mapping = {item["source"]: item["target"] for item in affinity["files"]}
        self.assertEqual(
            mapping["research/skill-prototypes/affinity-synthesis/SKILL.en.md"],
            "SKILL.md",
        )
        self.assertEqual(
            mapping["research/skill-prototypes/affinity-synthesis/references/METHOD.en.md"],
            "references/METHOD.en.md",
        )

    def test_csw_canonical_manifest_projects_router_and_modules(self) -> None:
        plan, _ = plan_package_trees(self.manifest)
        csw = self.tree(plan, "ja-JP", "claude_plugin", "cultural-substrate-weaving")
        mapping = {item["source"]: item["target"] for item in csw["files"]}
        self.assertEqual(mapping["src/ja-JP/ROUTER.md"], "SKILL.md")
        self.assertEqual(
            mapping["src/ja-JP/methods/integration.md"],
            "references/10-integration.md",
        )

    def test_claude_and_codex_share_the_same_skill_subtree_shape(self) -> None:
        plan, _ = plan_package_trees(self.manifest)
        for locale in ("ja-JP", "en-US"):
            claude = plan["locales"][locale]["distributions"]["claude_plugin"]["skill_trees"]
            codex = plan["locales"][locale]["distributions"]["codex_plugin"]["skill_trees"]
            self.assertEqual(claude, codex)

    def test_composite_distributions_do_not_invent_sibling_skill_trees(self) -> None:
        plan, _ = plan_package_trees(self.manifest)
        for locale in ("ja-JP", "en-US"):
            for distribution in ("chatgpt_gpt", "microsoft_copilot"):
                self.assertEqual(
                    plan["locales"][locale]["distributions"][distribution]["skill_trees"],
                    [],
                )

    def test_runtime_projection_collision_fails_closed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["en-US"]["package_source"]["files"].append("SKILL.md")
        _, errors = plan_package_trees(manifest)
        self.assertTrue(any("target path collision" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
