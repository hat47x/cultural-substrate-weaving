from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_tension_emergence import validate  # noqa: E402


class ResearchTensionEmergenceTests(unittest.TestCase):
    def test_current_tension_emergence_contract_is_valid(self) -> None:
        self.assertEqual(validate(), [])

    def test_fixture_preserves_non_synthesis_outcome(self) -> None:
        text = (
            ROOT
            / "research/skill-prototypes/evals/CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md"
        ).read_text(encoding="utf-8")
        self.assertIn("tension may end without synthesis", text)
        self.assertIn("cross_field_emergent: none yet", text)
        self.assertIn("第三構造を作れないことを失敗にしない", text)

    def test_fixture_rejects_clean_correspondence_as_automatic_success(self) -> None:
        text = (
            ROOT
            / "research/skill-prototypes/evals/CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md"
        ).read_text(encoding="utf-8")
        self.assertIn("clean correspondence is not automatically the most informative result", text)
        self.assertIn("対応の美しさより、対象からの抵抗によって読みが更新される", text)

    def test_layer1_runtime_does_not_own_sublation(self) -> None:
        ja = (
            ROOT / "research/skill-prototypes/affinity-synthesis/SKILL.md"
        ).read_text(encoding="utf-8")
        en = (
            ROOT / "research/skill-prototypes/affinity-synthesis/SKILL.en.md"
        ).read_text(encoding="utf-8")
        for marker in ("止揚", "アウフヘーベン", "正・反・合"):
            self.assertNotIn(marker, ja)
        for marker in ("sublation", "Aufhebung", "thesis-antithesis-synthesis"):
            self.assertNotIn(marker, en)

    def test_csw_handoff_preserves_generating_tension(self) -> None:
        ja = (ROOT / "src/ja-JP/methods/integration.md").read_text(encoding="utf-8")
        en = (ROOT / "src/en-US/methods/integration.md").read_text(encoding="utf-8")
        for text in (ja, en):
            self.assertIn("target_side_tension:", text)
            self.assertIn("framework_side_claim_or_operation:", text)
            self.assertIn("cross_field_candidate:", text)


if __name__ == "__main__":
    unittest.main()
