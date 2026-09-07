from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_host_package import materialize_host_package  # noqa: E402


class ResearchHostPackageMaterializerTests(unittest.TestCase):
    def materialize(
        self,
        locale: str,
        distribution: str,
        *,
        profile: str | None = None,
    ) -> tuple[Path, dict, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "package"
        result = materialize_host_package(
            locale=locale,
            distribution_name=distribution,
            output_root=output,
            profile=profile,
            root=ROOT,
        )
        return output, result, temp

    def test_openai_interactive_materializes_agents_metadata_in_both_locales(self) -> None:
        for locale in ("ja-JP", "en-US"):
            output, result, temp = self.materialize(
                locale,
                "openai_skill",
                profile="interactive",
            )
            self.addCleanup(temp.cleanup)

            self.assertEqual(result["profile"], "interactive")
            self.assertEqual(len(result["host_files"]), 3)
            for skill_name in (
                "cultural-substrate-weaving",
                "affinity-synthesis",
                "iterative-inquiry-synthesis",
            ):
                agent = output / skill_name / "agents" / "openai.yaml"
                self.assertTrue(agent.is_file())
                text = agent.read_text(encoding="utf-8")
                self.assertIn("interface:", text)
                self.assertIn("allow_implicit_invocation: true", text)
                self.assertTrue((output / skill_name / "SKILL.md").is_file())

            self.assertFalse((output / ".claude-plugin").exists())
            self.assertFalse((output / ".codex-plugin").exists())

    def test_openai_metered_materializes_nonimplicit_agents_metadata(self) -> None:
        for locale in ("ja-JP", "en-US"):
            output, result, temp = self.materialize(
                locale,
                "openai_skill",
                profile="metered",
            )
            self.addCleanup(temp.cleanup)

            self.assertEqual(result["profile"], "metered")
            for skill_name in (
                "cultural-substrate-weaving",
                "affinity-synthesis",
                "iterative-inquiry-synthesis",
            ):
                text = (
                    output / skill_name / "agents" / "openai.yaml"
                ).read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: false", text)

    def test_openai_requires_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "requires profile"):
                materialize_host_package(
                    locale="ja-JP",
                    distribution_name="openai_skill",
                    output_root=Path(temp_dir) / "package",
                    root=ROOT,
                )

    def test_bundle_distribution_rejects_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "profile is only valid"):
                materialize_host_package(
                    locale="ja-JP",
                    distribution_name="claude_plugin",
                    output_root=Path(temp_dir) / "package",
                    profile="interactive",
                    root=ROOT,
                )

    def test_claude_plugin_manifest_and_skill_tree_in_both_locales(self) -> None:
        expected_names = {
            "ja-JP": "cultural-substrate-weaving-ja",
            "en-US": "cultural-substrate-weaving-en",
        }
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        for locale in ("ja-JP", "en-US"):
            output, result, temp = self.materialize(locale, "claude_plugin")
            self.addCleanup(temp.cleanup)

            manifest_path = output / ".claude-plugin" / "plugin.json"
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], expected_names[locale])
            self.assertEqual(manifest["version"], version)
            self.assertEqual(manifest["author"], {"name": "hat47x"})
            self.assertEqual(manifest["license"], "MIT")
            self.assertIn("description", manifest)

            for skill_name in ("weave", "affinity-synthesis", "iterative-inquiry-synthesis"):
                entry = output / "skills" / skill_name / "SKILL.md"
                self.assertTrue(entry.is_file())
                self.assertIn(
                    "disable-model-invocation: true",
                    entry.read_text(encoding="utf-8"),
                )

            self.assertEqual(result["profile"], None)
            self.assertFalse((output / ".claude-plugin" / "marketplace.json").exists())
            self.assertFalse((output / ".codex-plugin").exists())
            self.assertFalse((output / "README.md").exists())

    def test_codex_plugin_manifest_and_skill_tree_in_both_locales(self) -> None:
        expected_names = {
            "ja-JP": "cultural-substrate-weaving-ja",
            "en-US": "cultural-substrate-weaving-en",
        }
        expected_displays = {
            "ja-JP": "Cultural Substrate Weaving — 日本語",
            "en-US": "Cultural Substrate Weaving — English",
        }
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        for locale in ("ja-JP", "en-US"):
            output, result, temp = self.materialize(locale, "codex_plugin")
            self.addCleanup(temp.cleanup)

            manifest_path = output / ".codex-plugin" / "plugin.json"
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], expected_names[locale])
            self.assertEqual(manifest["version"], version)
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["interface"]["displayName"], expected_displays[locale])
            self.assertEqual(manifest["interface"]["developerName"], "hat47x")
            self.assertEqual(manifest["interface"]["category"], "Productivity")

            for skill_name in ("weave", "affinity-synthesis", "iterative-inquiry-synthesis"):
                self.assertTrue((output / "skills" / skill_name / "SKILL.md").is_file())

            self.assertEqual(result["profile"], None)
            self.assertFalse((output / ".claude-plugin").exists())
            self.assertFalse((output / ".agents").exists())
            self.assertFalse((output / "README.md").exists())

    def test_failed_host_metadata_step_leaves_no_partial_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            output = base / "package"
            with patch(
                "materialize_host_package._repository_version",
                side_effect=ValueError("forced metadata failure"),
            ):
                with self.assertRaisesRegex(ValueError, "forced metadata failure"):
                    materialize_host_package(
                        locale="ja-JP",
                        distribution_name="claude_plugin",
                        output_root=output,
                        root=ROOT,
                    )

            self.assertFalse(output.exists())
            self.assertEqual(list(base.iterdir()), [])

    def test_failed_host_metadata_step_preserves_preexisting_empty_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            output = base / "package"
            output.mkdir()
            with patch(
                "materialize_host_package._repository_version",
                side_effect=ValueError("forced metadata failure"),
            ):
                with self.assertRaisesRegex(ValueError, "forced metadata failure"):
                    materialize_host_package(
                        locale="ja-JP",
                        distribution_name="claude_plugin",
                        output_root=output,
                        root=ROOT,
                    )

            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])
            self.assertEqual(list(base.iterdir()), [output])

    def test_composite_agent_distribution_is_not_host_materialized(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "unsupported host-package distribution"):
                materialize_host_package(
                    locale="ja-JP",
                    distribution_name="chatgpt_gpt",
                    output_root=Path(temp_dir) / "package",
                    root=ROOT,
                )


if __name__ == "__main__":
    unittest.main()
