from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_openai_packages import materialize_openai_packages  # noqa: E402

METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"


class ResearchOpenAIPackageMaterializerTests(unittest.TestCase):
    def materialize(
        self,
        locale: str,
        *,
        allow_partial: bool = False,
    ) -> tuple[Path, dict, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "packages"
        result = materialize_openai_packages(
            locale=locale,
            output_root=output,
            root=ROOT,
            allow_partial=allow_partial,
        )
        return output, result, temp

    def test_ja_materializes_three_skills_for_both_profiles(self) -> None:
        output, result, temp = self.materialize("ja-JP")
        self.addCleanup(temp.cleanup)

        self.assertFalse(result["partial"])
        self.assertEqual(result["runtime_state"], "buildable")
        self.assertEqual(result["metadata_coverage"], "prototype-for-realized")
        self.assertEqual(len(result["packages"]), 6)

        for profile in ("interactive", "metered"):
            for skill_name in (
                "cultural-substrate-weaving",
                "affinity-synthesis",
                "iterative-inquiry-synthesis",
            ):
                package = output / profile / skill_name
                self.assertTrue((package / "SKILL.md").is_file())
                self.assertTrue((package / "agents" / "openai.yaml").is_file())
                entry = (package / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("disable-model-invocation:", entry)

    def test_profile_packages_share_identical_skill_tree_content(self) -> None:
        output, _, temp = self.materialize("ja-JP")
        self.addCleanup(temp.cleanup)

        for skill_name in (
            "cultural-substrate-weaving",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
        ):
            interactive = output / "interactive" / skill_name
            metered = output / "metered" / skill_name

            interactive_files = {
                path.relative_to(interactive).as_posix(): path.read_bytes()
                for path in interactive.rglob("*")
                if path.is_file()
                and path.relative_to(interactive).as_posix() != "agents/openai.yaml"
            }
            metered_files = {
                path.relative_to(metered).as_posix(): path.read_bytes()
                for path in metered.rglob("*")
                if path.is_file()
                and path.relative_to(metered).as_posix() != "agents/openai.yaml"
            }
            self.assertEqual(interactive_files, metered_files)

    def test_packaged_openai_metadata_is_byte_identical_to_declared_source(self) -> None:
        output, _, temp = self.materialize("ja-JP")
        self.addCleanup(temp.cleanup)
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        openai = metadata["distributions"]["openai_skill"]["skills"]

        for skill_id in (
            "cultural-substrate-weaving",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
        ):
            for profile in ("interactive", "metered"):
                source = ROOT / openai[skill_id]["ja-JP"][profile]["source"]
                packaged = output / profile / skill_id / "agents" / "openai.yaml"
                self.assertEqual(packaged.read_bytes(), source.read_bytes())

    def test_profile_invocation_policy_is_preserved_in_materialized_metadata(self) -> None:
        output, _, temp = self.materialize("ja-JP")
        self.addCleanup(temp.cleanup)

        for skill_name in (
            "cultural-substrate-weaving",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
        ):
            interactive = (
                output / "interactive" / skill_name / "agents" / "openai.yaml"
            ).read_text(encoding="utf-8")
            metered = (
                output / "metered" / skill_name / "agents" / "openai.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn("allow_implicit_invocation: true", interactive)
            self.assertIn("allow_implicit_invocation: false", metered)

    def test_en_requires_explicit_partial_probe_and_materializes_only_csw(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            blocked = Path(temp_dir) / "blocked"
            with self.assertRaisesRegex(ValueError, "allow_partial=True"):
                materialize_openai_packages(
                    locale="en-US",
                    output_root=blocked,
                    root=ROOT,
                )
            self.assertFalse(blocked.exists())

        output, result, temp = self.materialize("en-US", allow_partial=True)
        self.addCleanup(temp.cleanup)
        self.assertTrue(result["partial"])
        self.assertEqual(len(result["packages"]), 2)

        for profile in ("interactive", "metered"):
            self.assertTrue(
                (output / profile / "cultural-substrate-weaving" / "SKILL.md").is_file()
            )
            self.assertFalse((output / profile / "affinity-synthesis").exists())
            self.assertFalse((output / profile / "iterative-inquiry-synthesis").exists())

    def test_materializer_refuses_repository_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            materialize_openai_packages(
                locale="ja-JP",
                output_root=ROOT / "research" / "openai-package-output",
                root=ROOT,
            )


if __name__ == "__main__":
    unittest.main()
