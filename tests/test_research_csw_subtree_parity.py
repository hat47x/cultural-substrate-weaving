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

    def assert_materialized_csw_matches_tracked_plugin(self, distribution: str) -> None:
        tracked = ROOT / "plugins" / "cultural-substrate-weaving-ja" / "skills" / "weave"
        self.assertTrue(tracked.is_dir(), "tracked ja-JP production CSW subtree is missing")

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "tree"
            result = materialize_skill_tree(
                locale="ja-JP",
                distribution_name=distribution,
                output_root=output,
                root=ROOT,
            )
            self.assertFalse(result["partial"])

            materialized = output / "skills" / "weave"
            self.assertTrue(materialized.is_dir())
            self.assertEqual(
                self.snapshot_tree(materialized),
                self.snapshot_tree(tracked),
                f"research {distribution} CSW subtree diverged from tracked production output",
            )

    def test_ja_claude_research_csw_subtree_matches_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin("claude_plugin")

    def test_ja_codex_research_csw_subtree_matches_shared_tracked_production(self) -> None:
        self.assert_materialized_csw_matches_tracked_plugin("codex_plugin")


if __name__ == "__main__":
    unittest.main()
