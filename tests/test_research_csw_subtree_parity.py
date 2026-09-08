from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_skill_tree import materialize_skill_tree  # noqa: E402


class ResearchCswSubtreeParityTests(unittest.TestCase):
    def snapshot_tree(self, root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def assert_materialized_csw_matches_tracked_plugin(
        self,
        *,
        locale: str,
        plugin_name: str,
        distribution: str,
        allow_partial: bool,
    ) -> None:
        tracked = ROOT / "plugins" / plugin_name / "skills" / "weave"
        self.assertTrue(
            tracked.is_dir(),
            f"tracked {locale} production CSW subtree is missing",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "tree"
            materialize_skill_tree(
                locale=locale,
                distribution_name=distribution,
                output_root=output,
                root=ROOT,
                allow_partial=allow_partial,
            )

            materialized = output / "skills" / "weave"
            self.assertTrue(materialized.is_dir())
            self.assertEqual(
                self.snapshot_tree(materialized),
                self.snapshot_tree(tracked),
                (
                    f"research {distribution} CSW subtree diverged from tracked "
                    f"production output for {locale}"
                ),
            )

    def test_ja_claude_research_csw_subtree_matches_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin(
            locale="ja-JP",
            plugin_name="cultural-substrate-weaving-ja",
            distribution="claude_plugin",
            allow_partial=False,
        )

    def test_ja_codex_research_csw_subtree_matches_shared_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin(
            locale="ja-JP",
            plugin_name="cultural-substrate-weaving-ja",
            distribution="codex_plugin",
            allow_partial=False,
        )

    def test_en_claude_research_csw_subtree_matches_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin(
            locale="en-US",
            plugin_name="cultural-substrate-weaving-en",
            distribution="claude_plugin",
            allow_partial=True,
        )

    def test_en_codex_research_csw_subtree_matches_shared_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin(
            locale="en-US",
            plugin_name="cultural-substrate-weaving-en",
            distribution="codex_plugin",
            allow_partial=True,
        )


if __name__ == "__main__":
    unittest.main()
