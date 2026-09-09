from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-COMPLETE-CHECKOUT-EXECUTION-STATUS-2026-09-08.md"
)


class ResearchCompleteCheckoutStatusSeparationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = STATUS_PATH.read_text(encoding="utf-8")

    def test_checked_in_translation_state_is_separate_from_execution_evidence(self) -> None:
        self.assertIn("Status: **blocked / not run**", self.text)
        self.assertIn(
            "checked-in translation refresh state: SYNCHRONIZED",
            self.text,
        )
        self.assertIn("checked-in expected_stale_files: []", self.text)
        self.assertIn("repository stateとcommand execution stateを混同しない", self.text)

    def test_canonical_translation_commands_remain_not_run(self) -> None:
        self.assertIn("translation V preparation:              NOT RUN", self.text)
        self.assertIn("translation-manifest hash refresh:       NOT RUN", self.text)
        self.assertIn("translation research state transition:  NOT RUN", self.text)
        self.assertIn(
            "checked-in treeが同期済みであることとは両立する",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
