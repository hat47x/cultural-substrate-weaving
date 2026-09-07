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

    def test_japanese_affinity_preserves_explicit_relative_structure(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        affinity = self.subtree(
            self.distribution(plan, "ja-JP", "openai_skill"),
            "affinity-synthesis",
        )
        self.assertEqual(affinity["target_root"], "affinity-synthesis")
        self.assertEqual(affinity["source_mode"], "explicit_files")
        by_relative = {item["target_relative"]: item for item in affinity["mappings"]}
        declared = set(
            self.skill(self.manifest, "affinity-synthesis")
            ["locale_realizations"]["ja-JP"]["package_source"]["files"]
        )
        self.assertEqual(set(by_relative), declared)
        for relative, mapping in by_relative.items():
            self.assertEqual(mapping["operation"], "copy")
            self.assertEqual(mapping["target"], f"affinity-synthesis/{relative}")

    def test_english_runtime_source_projects_to_canonical_skill_entry_name(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
            subtree = self.subtree(
                self.distribution(plan, "en-US", "openai_skill"),
                skill_id,
            )
            entry = next(
                item for item in subtree["mappings"] if item["target_relative"] == "SKILL.md"
            )
            self.assertTrue(entry["source"].endswith("/SKILL.en.md"))
            self.assertEqual(entry["operation"], "copy")
            self.assertEqual(entry["target"], f"{skill_id}/SKILL.md")

    def test_bilingual_bundles_contain_three_skill_subtrees(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        expected_roots = {
            "cultural-substrate-weaving": "skills/weave",
            "affinity-synthesis": "skills/affinity-synthesis",
            "iterative-inquiry-synthesis": "skills/iterative-inquiry-synthesis",
        }
        for locale in ("ja-JP", "en-US"):
            for distribution_name in ("claude_plugin", "codex_plugin"):
                distribution = self.distribution(plan, locale, distribution_name)
                self.assertEqual(distribution["layout_state"], "buildable")
                self.assertEqual(distribution["subtree_state"], "planned")
                self.assertEqual(distribution["missing_skills"], [])
                self.assertEqual(
                    {item["skill_id"]: item["target_root"] for item in distribution["subtrees"]},
                    expected_roots,
                )

    def test_iterative_standalone_has_no_affinity_subtree_dependency(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        iterative = self.subtree(
            self.distribution(plan, "ja-JP", "openai_skill"),
            "iterative-inquiry-synthesis",
        )
        self.assertEqual(
            [item["target_relative"] for item in iterative["mappings"]],
            ["SKILL.md", "references/METHOD.md", "references/ROUND-TEMPLATE.md"],
        )
        self.assertTrue(
            all("affinity-synthesis" not in item["target"] for item in iterative["mappings"])
        )

    def test_csw_bundle_maps_router_and_manifest_modules_to_existing_shape(self) -> None:
        plan = plan_skill_subtrees(self.manifest, ROOT)
        csw = self.subtree(
            self.distribution(plan, "ja-JP", "claude_plugin"),
            "cultural-substrate-weaving",
        )
        self.assertEqual(csw["target_root"], "skills/weave")
        self.assertEqual(csw["source_mode"], "canonical_manifest")
        self.assertEqual(len(csw["mappings"]), 13)
        by_target = {item["target"]: item for item in csw["mappings"]}
        self.assertEqual(by_target["skills/weave/SKILL.md"]["operation"], "render_runtime_entry")
        self.assertEqual(by_target["skills/weave/SKILL.md"]["source"], "src/ja-JP/ROUTER.md")
        self.assertEqual(
            by_target["skills/weave/references/10-integration.md"]["source"],
            "src/ja-JP/methods/integration.md",
        )

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


if __name__ == "__main__":
    unittest.main()
