from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
sys.path.insert(0, str(PLANNER_DIR))

from plan_skill_subtrees import plan_skill_subtrees  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchSkillSubtreePlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def distribution(self, plan: dict, locale: str, name: str) -> dict:
        return plan["locales"][locale]["distributions"][name]

    def subtree(self, distribution: dict, skill_id: str) -> dict:
        return next(item for item in distribution["subtrees"] if item["skill_id"] == skill_id)

    def test_affinity_explicit_files_preserve_relative_structure(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        openai = self.distribution(plan, "ja-JP", "openai_skill")
        affinity = self.subtree(openai, "affinity-synthesis")

        self.assertEqual(affinity["target_root"], "affinity-synthesis")
        self.assertEqual(affinity["source_mode"], "explicit_files")

        mapping_by_relative = {
            mapping["target_relative"]: mapping for mapping in affinity["mappings"]
        }
        declared = set(
            self.skill(self.manifest, "affinity-synthesis")["locale_realizations"]["ja-JP"]
            ["package_source"]["files"]
        )
        self.assertEqual(set(mapping_by_relative), declared)

        for relative, mapping in mapping_by_relative.items():
            self.assertEqual(mapping["operation"], "copy")
            self.assertEqual(mapping["target"], f"affinity-synthesis/{relative}")

    def test_iterative_standalone_has_no_sibling_subtree(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        openai = self.distribution(plan, "ja-JP", "openai_skill")
        iterative = self.subtree(openai, "iterative-inquiry-synthesis")

        self.assertEqual(
            [mapping["target_relative"] for mapping in iterative["mappings"]],
            ["SKILL.md", "references/METHOD.md", "references/ROUND-TEMPLATE.md"],
        )
        self.assertTrue(
            all("affinity-synthesis" not in mapping["target"] for mapping in iterative["mappings"])
        )

    def test_csw_bundle_maps_router_and_manifest_modules_to_existing_shape(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        claude = self.distribution(plan, "ja-JP", "claude_plugin")
        csw = self.subtree(claude, "cultural-substrate-weaving")

        self.assertEqual(csw["target_root"], "skills/weave")
        self.assertEqual(csw["source_mode"], "canonical_manifest")
        self.assertEqual(len(csw["mappings"]), 13)

        by_target = {mapping["target"]: mapping for mapping in csw["mappings"]}
        self.assertEqual(
            by_target["skills/weave/SKILL.md"],
            {
                "source": "src/ja-JP/ROUTER.md",
                "target_relative": "SKILL.md",
                "operation": "render_runtime_entry",
                "target": "skills/weave/SKILL.md",
            },
        )
        self.assertEqual(
            by_target["skills/weave/references/10-integration.md"]["source"],
            "src/ja-JP/methods/integration.md",
        )
        self.assertEqual(
            by_target["skills/weave/references/00-iteration.md"]["source"],
            "src/ja-JP/core/iteration.md",
        )

    def test_csw_openai_uses_existing_installable_target_root(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        openai = self.distribution(plan, "ja-JP", "openai_skill")
        csw = self.subtree(openai, "cultural-substrate-weaving")

        self.assertEqual(csw["target_root"], "cultural-substrate-weaving")
        self.assertEqual(csw["mappings"][0]["target"], "cultural-substrate-weaving/SKILL.md")

    def test_blocked_english_bundle_still_exposes_available_csw_subtree(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        claude = self.distribution(plan, "en-US", "claude_plugin")

        self.assertEqual(claude["layout_state"], "blocked")
        self.assertEqual(claude["subtree_state"], "partial")
        self.assertEqual(
            claude["missing_skills"],
            ["affinity-synthesis", "iterative-inquiry-synthesis"],
        )
        self.assertEqual(
            [subtree["skill_id"] for subtree in claude["subtrees"]],
            ["cultural-substrate-weaving"],
        )
        self.assertEqual(claude["subtrees"][0]["target_root"], "skills/weave")

    def test_target_collision_is_visible_in_pure_subtree_plan(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"]["package_targets"]["claude_plugin"][
            "skill_name"
        ] = "weave"

        plan = plan_skill_subtrees(manifest, ROOT)
        claude = self.distribution(plan, "ja-JP", "claude_plugin")

        self.assertEqual(claude["subtree_state"], "collision")
        self.assertIn(
            {
                "target": "skills/weave/SKILL.md",
                "skill_ids": ["cultural-substrate-weaving", "affinity-synthesis"],
            },
            claude["collisions"],
        )

    def test_composite_surfaces_do_not_invent_sibling_skill_subtrees(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        for locale in ("ja-JP", "en-US"):
            for distribution_name in ("chatgpt_gpt", "microsoft_copilot"):
                distribution = self.distribution(plan, locale, distribution_name)
                self.assertEqual(distribution["subtree_state"], "not-applicable")
                self.assertEqual(distribution["subtrees"], [])
                self.assertIn("does not yet declare", distribution["reason"])


if __name__ == "__main__":
    unittest.main()
