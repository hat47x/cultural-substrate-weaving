from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
sys.path.insert(0, str(PLANNER_DIR))

from plan_skill_entry_transforms import (  # noqa: E402
    plan_skill_entry_transforms,
    render_explicit_skill_entry,
    split_skill_frontmatter,
)

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
AFFINITY_JA = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "SKILL.md"
AFFINITY_EN = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "SKILL.en.md"
ITERATIVE_JA = ROOT / "research" / "skill-prototypes" / "iterative-inquiry-synthesis" / "SKILL.md"
ITERATIVE_EN = ROOT / "research" / "skill-prototypes" / "iterative-inquiry-synthesis" / "SKILL.en.md"


class ResearchSkillEntryTransformTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def entries(self, plan: dict, locale: str, distribution: str) -> dict[str, dict]:
        return {
            entry["skill_id"]: entry
            for entry in plan["locales"][locale]["distributions"][distribution]["entries"]
        }

    def test_bilingual_entry_transform_policies_are_explicit(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for locale in ("ja-JP", "en-US"):
            openai = self.entries(plan, locale, "openai_skill")
            claude = self.entries(plan, locale, "claude_plugin")
            codex = self.entries(plan, locale, "codex_plugin")
            for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
                self.assertEqual(
                    openai[skill_id]["transform_mode"],
                    "normalize_explicit_skill_frontmatter",
                )
                self.assertFalse(openai[skill_id]["disable_model_invocation"])
                self.assertTrue(claude[skill_id]["disable_model_invocation"])
                self.assertTrue(codex[skill_id]["disable_model_invocation"])
                self.assertEqual(
                    claude[skill_id]["entry_policy"],
                    "claude_codex_shared_skill_tree",
                )

    def test_english_entry_sources_are_skill_en_but_targets_are_skill_md(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for distribution in ("openai_skill", "claude_plugin", "codex_plugin"):
            entries = self.entries(plan, "en-US", distribution)
            for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
                entry = entries[skill_id]
                self.assertTrue(entry["source"].endswith("/SKILL.en.md"))
                self.assertTrue(entry["target"].endswith("/SKILL.md"))

    def test_canonical_csw_keeps_existing_builder_render_boundary_in_both_locales(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for locale in ("ja-JP", "en-US"):
            for distribution in ("openai_skill", "claude_plugin", "codex_plugin"):
                csw = self.entries(plan, locale, distribution)["cultural-substrate-weaving"]
                self.assertEqual(csw["input_operation"], "render_runtime_entry")
                self.assertEqual(csw["transform_mode"], "existing_canonical_builder_render")

    def test_composite_agent_surfaces_do_not_invent_skill_entry_transforms(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for locale in ("ja-JP", "en-US"):
            for distribution in ("chatgpt_gpt", "microsoft_copilot"):
                item = plan["locales"][locale]["distributions"][distribution]
                self.assertEqual(item["state"], "not-applicable")
                self.assertEqual(item["entries"], [])

    def test_openai_explicit_entries_keep_description_without_claude_flag(self) -> None:
        for source_path, target_name in (
            (AFFINITY_JA, "affinity-synthesis"),
            (AFFINITY_EN, "affinity-synthesis"),
            (ITERATIVE_JA, "iterative-inquiry-synthesis"),
            (ITERATIVE_EN, "iterative-inquiry-synthesis"),
        ):
            rendered = render_explicit_skill_entry(
                source_path.read_text(encoding="utf-8"),
                target_name=target_name,
                explicit_invocation=False,
            )
            fields, body = split_skill_frontmatter(rendered)
            metadata = dict(fields)
            self.assertEqual(metadata["name"], target_name)
            self.assertIn("description", metadata)
            self.assertNotIn("disable-model-invocation", metadata)
            self.assertTrue(body.lstrip().startswith("# "))

    def test_claude_codex_entry_adds_explicit_invocation_flag_once(self) -> None:
        source = ITERATIVE_EN.read_text(encoding="utf-8")
        source = source.replace(
            "description: Orchestrates",
            "disable-model-invocation: false\ndescription: Orchestrates",
            1,
        )
        rendered = render_explicit_skill_entry(
            source,
            target_name="iterative-inquiry-synthesis",
            explicit_invocation=True,
        )
        fields, _ = split_skill_frontmatter(rendered)
        metadata = dict(fields)
        self.assertEqual(metadata["disable-model-invocation"], "true")
        self.assertEqual([key for key, _ in fields].count("disable-model-invocation"), 1)

    def test_target_name_comes_from_distribution_contract(self) -> None:
        source = AFFINITY_EN.read_text(encoding="utf-8")
        rendered = render_explicit_skill_entry(
            source,
            target_name="renamed-affinity",
            explicit_invocation=False,
        )
        fields, _ = split_skill_frontmatter(rendered)
        self.assertEqual(dict(fields)["name"], "renamed-affinity")

    def test_scalar_frontmatter_parser_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "must declare description"):
            render_explicit_skill_entry(
                "---\nname: sample\n---\n\n# Sample\n",
                target_name="sample",
                explicit_invocation=False,
            )
        with self.assertRaisesRegex(ValueError, "duplicate"):
            split_skill_frontmatter(
                "---\nname: one\nname: two\ndescription: sample\n---\n\n# Sample\n"
            )


if __name__ == "__main__":
    unittest.main()
