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
AFFINITY_ENTRY = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "SKILL.md"
ITERATIVE_ENTRY = ROOT / "research" / "skill-prototypes" / "iterative-inquiry-synthesis" / "SKILL.md"


class ResearchSkillEntryTransformTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def entries(self, plan: dict, locale: str, distribution: str) -> dict[str, dict]:
        return {
            entry["skill_id"]: entry
            for entry in plan["locales"][locale]["distributions"][distribution]["entries"]
        }

    def test_current_entry_transform_policies_are_explicit(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)

        openai = self.entries(plan, "ja-JP", "openai_skill")
        claude = self.entries(plan, "ja-JP", "claude_plugin")
        codex = self.entries(plan, "ja-JP", "codex_plugin")

        self.assertFalse(openai["affinity-synthesis"]["disable_model_invocation"])
        self.assertEqual(
            openai["affinity-synthesis"]["transform_mode"],
            "normalize_explicit_skill_frontmatter",
        )
        self.assertTrue(claude["affinity-synthesis"]["disable_model_invocation"])
        self.assertTrue(codex["affinity-synthesis"]["disable_model_invocation"])
        self.assertEqual(
            claude["affinity-synthesis"]["entry_policy"],
            "claude_codex_shared_skill_tree",
        )
        self.assertEqual(
            codex["affinity-synthesis"]["entry_policy"],
            "claude_codex_shared_skill_tree",
        )

    def test_canonical_csw_keeps_existing_builder_render_boundary(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for distribution in ("openai_skill", "claude_plugin", "codex_plugin"):
            csw = self.entries(plan, "ja-JP", distribution)["cultural-substrate-weaving"]
            self.assertEqual(csw["input_operation"], "render_runtime_entry")
            self.assertEqual(csw["transform_mode"], "existing_canonical_builder_render")

    def test_composite_agent_surfaces_do_not_invent_skill_entry_transforms(self) -> None:
        plan = plan_skill_entry_transforms(self.manifest, ROOT)
        for distribution in ("chatgpt_gpt", "microsoft_copilot"):
            item = plan["locales"]["ja-JP"]["distributions"][distribution]
            self.assertEqual(item["state"], "not-applicable")
            self.assertEqual(item["entries"], [])

    def test_openai_explicit_entry_keeps_description_without_claude_flag(self) -> None:
        source = AFFINITY_ENTRY.read_text(encoding="utf-8")
        rendered = render_explicit_skill_entry(
            source,
            target_name="affinity-synthesis",
            explicit_invocation=False,
        )
        fields, body = split_skill_frontmatter(rendered)
        metadata = dict(fields)

        self.assertEqual(metadata["name"], "affinity-synthesis")
        self.assertIn("description", metadata)
        self.assertNotIn("disable-model-invocation", metadata)
        self.assertTrue(body.startswith("\n# Affinity Synthesis") or body.startswith("# Affinity Synthesis"))

    def test_claude_codex_entry_adds_explicit_invocation_flag_once(self) -> None:
        source = ITERATIVE_ENTRY.read_text(encoding="utf-8")
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

        self.assertEqual(metadata["name"], "iterative-inquiry-synthesis")
        self.assertEqual(metadata["disable-model-invocation"], "true")
        self.assertEqual(
            [key for key, _ in fields].count("disable-model-invocation"),
            1,
        )

    def test_target_name_is_taken_from_distribution_contract_not_source_frontmatter(self) -> None:
        source = AFFINITY_ENTRY.read_text(encoding="utf-8")
        rendered = render_explicit_skill_entry(
            source,
            target_name="renamed-affinity",
            explicit_invocation=False,
        )
        fields, _ = split_skill_frontmatter(rendered)
        self.assertEqual(dict(fields)["name"], "renamed-affinity")

    def test_scalar_frontmatter_parser_rejects_missing_description(self) -> None:
        with self.assertRaisesRegex(ValueError, "must declare description"):
            render_explicit_skill_entry(
                "---\nname: sample\n---\n\n# Sample\n",
                target_name="sample",
                explicit_invocation=False,
            )

    def test_scalar_frontmatter_parser_rejects_duplicate_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            split_skill_frontmatter(
                "---\nname: one\nname: two\ndescription: sample\n---\n\n# Sample\n"
            )


if __name__ == "__main__":
    unittest.main()
