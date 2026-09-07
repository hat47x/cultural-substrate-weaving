from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_skill_tree import (  # noqa: E402
    _safe_output_root,
    materialize_skill_tree,
)


class ResearchSkillTreeMaterializerTests(unittest.TestCase):
    def materialize(
        self,
        locale: str,
        distribution: str,
        *,
        allow_partial: bool = False,
    ) -> tuple[Path, dict, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "tree"
        result = materialize_skill_tree(
            locale=locale,
            distribution_name=distribution,
            output_root=output,
            root=ROOT,
            allow_partial=allow_partial,
        )
        return output, result, temp

    def test_ja_openai_materializes_three_standalone_skill_trees(self) -> None:
        output, result, temp = self.materialize("ja-JP", "openai_skill")
        self.addCleanup(temp.cleanup)

        self.assertFalse(result["partial"])
        for skill_name in (
            "cultural-substrate-weaving",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
        ):
            self.assertTrue((output / skill_name / "SKILL.md").is_file())

        csw = (output / "cultural-substrate-weaving" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        affinity = (output / "affinity-synthesis" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        iterative = (output / "iterative-inquiry-synthesis" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: cultural-substrate-weaving", csw)
        self.assertIn("name: affinity-synthesis", affinity)
        self.assertIn("name: iterative-inquiry-synthesis", iterative)
        self.assertNotIn("disable-model-invocation:", csw)
        self.assertNotIn("disable-model-invocation:", affinity)
        self.assertNotIn("disable-model-invocation:", iterative)

        self.assertTrue(
            (output / "cultural-substrate-weaving" / "references" / "10-integration.md").is_file()
        )
        self.assertTrue(
            (output / "affinity-synthesis" / "references" / "METHOD.md").is_file()
        )
        self.assertTrue(
            (output / "affinity-synthesis" / "evidence" / "dossier.md").is_file()
        )
        self.assertTrue(
            (
                output
                / "iterative-inquiry-synthesis"
                / "references"
                / "ROUND-TEMPLATE.md"
            ).is_file()
        )
        self.assertNotIn("../affinity-synthesis/", iterative)

    def test_ja_claude_materializes_shared_skill_tree_with_explicit_invocation(self) -> None:
        output, result, temp = self.materialize("ja-JP", "claude_plugin")
        self.addCleanup(temp.cleanup)

        self.assertFalse(result["partial"])
        for skill_name in ("weave", "affinity-synthesis", "iterative-inquiry-synthesis"):
            entry = (output / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"name: {skill_name}", entry)
            self.assertEqual(entry.count("disable-model-invocation: true"), 1)

        self.assertTrue(
            (output / "skills" / "weave" / "references" / "00-iteration.md").is_file()
        )
        self.assertTrue(
            (
                output
                / "skills"
                / "affinity-synthesis"
                / "references"
                / "REPRESENTATION.md"
            ).is_file()
        )

    def test_ja_codex_uses_same_shared_skill_tree_entry_policy(self) -> None:
        output, result, temp = self.materialize("ja-JP", "codex_plugin")
        self.addCleanup(temp.cleanup)

        self.assertFalse(result["partial"])
        weave = (output / "skills" / "weave" / "SKILL.md").read_text(encoding="utf-8")
        affinity = (output / "skills" / "affinity-synthesis" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("disable-model-invocation: true", weave)
        self.assertIn("disable-model-invocation: true", affinity)

    def test_en_openai_requires_explicit_partial_probe(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "allow_partial=True"):
                materialize_skill_tree(
                    locale="en-US",
                    distribution_name="openai_skill",
                    output_root=Path(temp_dir) / "blocked",
                    root=ROOT,
                )

        output, result, temp = self.materialize(
            "en-US",
            "openai_skill",
            allow_partial=True,
        )
        self.addCleanup(temp.cleanup)
        self.assertTrue(result["partial"])
        self.assertTrue((output / "cultural-substrate-weaving" / "SKILL.md").is_file())
        self.assertFalse((output / "affinity-synthesis").exists())
        self.assertFalse((output / "iterative-inquiry-synthesis").exists())

    def test_en_claude_partial_probe_still_requires_bundle_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "bundle metadata is not materializable"):
                materialize_skill_tree(
                    locale="en-US",
                    distribution_name="claude_plugin",
                    output_root=Path(temp_dir) / "tree",
                    root=ROOT,
                    allow_partial=True,
                )

    def test_materializer_refuses_output_inside_repository(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            _safe_output_root(ROOT / "research" / "materializer-output", ROOT)

    def test_materializer_refuses_nonempty_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "tree"
            output.mkdir()
            (output / "existing.txt").write_text("do not overwrite", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must be empty"):
                materialize_skill_tree(
                    locale="ja-JP",
                    distribution_name="openai_skill",
                    output_root=output,
                    root=ROOT,
                )

    def test_composite_agent_distribution_is_not_materialized_as_skill_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "unsupported Skill-tree materialization"):
                materialize_skill_tree(
                    locale="ja-JP",
                    distribution_name="chatgpt_gpt",
                    output_root=Path(temp_dir) / "tree",
                    root=ROOT,
                )


if __name__ == "__main__":
    unittest.main()
