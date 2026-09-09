from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_complete_checkout_gate import (  # noqa: E402
    DESCRIPTOR_RELATIVE,
    EXPECTED_BINDING_CONTRACT,
    EXPECTED_BLOCKED_EVIDENCE,
    validate_complete_checkout_gate,
)

DESCRIPTOR = json.loads((ROOT / DESCRIPTOR_RELATIVE).read_text(encoding="utf-8"))


class ResearchCompleteCheckoutTranslationStateMarkerTests(unittest.TestCase):
    def make_root(self, *, include_translation_state: bool = True) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)

        binding = root / EXPECTED_BINDING_CONTRACT
        binding.parent.mkdir(parents=True, exist_ok=True)
        binding.write_text(
            "validated commit V\n"
            "evidence-only recording commit E\n"
            "Eのfirst parentはV\n"
            "translation hash/state transitionはevidence recording commitへ混ぜない\n"
            "production promotionを単独承認しない\n",
            encoding="utf-8",
        )

        evidence = root / EXPECTED_BLOCKED_EVIDENCE
        evidence.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Status: **blocked / not run**",
            "translation-manifest hash refresh:       NOT RUN",
            "translation research state transition:  NOT RUN",
            "complete-checkout research-skill-check: NOT RUN",
            "production build regeneration:          NOT RUN",
            "full repository make check:             NOT RUN",
            "production promotion authorization:     NO",
        ]
        if include_translation_state:
            lines[1:1] = [
                "checked-in translation refresh state: SYNCHRONIZED",
                "checked-in expected_stale_files: []",
            ]
        evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return root

    def tearDown(self) -> None:
        if hasattr(self, "tmp"):
            self.tmp.cleanup()

    def test_blocked_evidence_accepts_checked_in_translation_state_markers(self) -> None:
        root = self.make_root(include_translation_state=True)
        self.assertEqual(validate_complete_checkout_gate(root, copy.deepcopy(DESCRIPTOR)), [])

    def test_blocked_evidence_rejects_missing_checked_in_translation_state_markers(self) -> None:
        root = self.make_root(include_translation_state=False)
        errors = validate_complete_checkout_gate(root, copy.deepcopy(DESCRIPTOR))
        self.assertTrue(
            any("checked-in translation refresh state: SYNCHRONIZED" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("checked-in expected_stale_files: []" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
