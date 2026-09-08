from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_map import validate  # noqa: E402


class ResearchAffinityMapValidationTests(unittest.TestCase):
    def fixture(self) -> dict:
        return {
            "format": "affinity-map",
            "version": "0.1",
            "sources": [{"id": "S01", "ref": "source A"}],
            "cards": [
                {"id": "C001", "text": "main card", "source_refs": ["S01"]},
                {"id": "C002", "text": "group member", "source_refs": ["S01"]},
            ],
            "groups": [
                {"id": "G01", "label": "primary group", "members": ["C002"]},
            ],
            "resonances": [
                {
                    "id": "X01",
                    "from": "C001",
                    "to": "G01",
                    "note": "C001 resonates with G01 without becoming its member",
                }
            ],
            "questions": [
                {
                    "id": "Q01",
                    "text": "What would clarify the resonance?",
                    "arises_from": ["X01"],
                }
            ],
        }

    def test_question_may_use_secondary_resonance_as_local_provenance(self) -> None:
        errors, warnings = validate(self.fixture())
        self.assertEqual(errors, [])
        self.assertFalse(
            any("question Q01 arises_from ref does not resolve locally" in warning for warning in warnings)
        )

    def test_unresolved_question_provenance_still_warns(self) -> None:
        data = self.fixture()
        data["questions"][0]["arises_from"] = ["X404"]
        errors, warnings = validate(data)
        self.assertEqual(errors, [])
        self.assertTrue(
            any("question Q01 arises_from ref does not resolve locally: X404" in warning for warning in warnings)
        )


if __name__ == "__main__":
    unittest.main()
