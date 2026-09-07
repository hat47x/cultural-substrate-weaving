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

from materialize_claude_codex_plugin_core import (  # noqa: E402
    materialize_claude_codex_plugin_core,
)

BUNDLE_METADATA = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "adapters"
    / "claude-codex"
    / "ja-JP"
    / "bundle-metadata.json"
)


class ResearchClaudeCodexPluginCoreTests(unittest.TestCase):
    def materialize(
        self,
        locale: str = "ja-JP",
    ) -> tuple[Path, Path, dict, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "bundle"
        result = materialize_claude_codex_plugin_core(
            locale=locale,
            output_root=output,
            root=ROOT,
        )
        plugin_root = output / result["plugin_name"]
        return output, plugin_root, result, temp

    def test_ja_materializes_one_shared_three_skill_plugin_core(self) -> None:
        _, plugin_root, result, temp = self.materialize()
        self.addCleanup(temp.cleanup)

        self.assertTrue(result["shared_skill_tree"])
        self.assertEqual(result["metadata_state"], "prototype")
        self.assertEqual(result["claude_subtree_state"], "planned")
        self.assertEqual(result["codex_subtree_state"], "planned")

        self.assertEqual(
            {path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()},
            {"weave", "affinity-synthesis", "iterative-inquiry-synthesis"},
        )
        self.assertTrue((plugin_root / ".claude-plugin" / "plugin.json").is_file())
        self.assertTrue((plugin_root / ".codex-plugin" / "plugin.json").is_file())

    def test_all_shared_skill_entries_preserve_explicit_invocation(self) -> None:
        _, plugin_root, _, temp = self.materialize()
        self.addCleanup(temp.cleanup)

        for skill_name in ("weave", "affinity-synthesis", "iterative-inquiry-synthesis"):
            entry = (plugin_root / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(entry.count("disable-model-invocation: true"), 1)

    def test_host_manifests_use_same_bundle_prototype_wording(self) -> None:
        _, plugin_root, _, temp = self.materialize()
        self.addCleanup(temp.cleanup)
        prototype = json.loads(BUNDLE_METADATA.read_text(encoding="utf-8"))
        claude = json.loads(
            (plugin_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        codex = json.loads(
            (plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

        self.assertEqual(claude["name"], prototype["plugin_name"])
        self.assertEqual(codex["name"], prototype["plugin_name"])
        self.assertEqual(claude["description"], prototype["description"])
        self.assertEqual(codex["description"], prototype["description"])
        self.assertEqual(codex["interface"]["displayName"], prototype["display"])
        self.assertEqual(codex["interface"]["shortDescription"], prototype["description"])
        self.assertEqual(claude["version"], "0.5.0")
        self.assertEqual(codex["version"], "0.5.0")

    def test_plugin_core_intentionally_omits_unreviewed_outer_artifacts(self) -> None:
        _, plugin_root, _, temp = self.materialize()
        self.addCleanup(temp.cleanup)

        self.assertFalse((plugin_root / "README.md").exists())
        self.assertFalse((plugin_root / "marketplace.json").exists())
        self.assertFalse((plugin_root / ".claude-plugin" / "marketplace.json").exists())

    def test_en_bundle_is_blocked_and_leaves_requested_output_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "blocked"
            with self.assertRaisesRegex(ValueError, "not buildable"):
                materialize_claude_codex_plugin_core(
                    locale="en-US",
                    output_root=output,
                    root=ROOT,
                )
            self.assertFalse(output.exists())

    def test_materializer_refuses_repository_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            materialize_claude_codex_plugin_core(
                locale="ja-JP",
                output_root=ROOT / "research" / "claude-codex-plugin-core",
                root=ROOT,
            )


if __name__ == "__main__":
    unittest.main()
