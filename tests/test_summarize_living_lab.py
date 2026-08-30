from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "summarize_living_lab",
    SCRIPTS / "summarize_living_lab.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LivingLabSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        observation_dir = ROOT / "research" / "living-lab" / "observations"
        cls.records = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(observation_dir.glob("*.json"))
        ]

    def test_public_observations_summarize_without_scoring(self) -> None:
        summary = MODULE.summarize(self.records)
        self.assertIn("not KPIs", summary["interpretation_note"])
        self.assertEqual(summary["inventory"]["activation_scopes"], {"non_activation": 1})
        self.assertEqual(summary["inventory"]["event_types"], {"useful_nonuse": 1})
        self.assertEqual(summary["rounds"][0]["round_id"], "round-2026-08-30-001")
        self.assertEqual(summary["rounds"][0]["events"][0]["event_type"], "useful_nonuse")

    def test_summary_requires_a_closed_record_set(self) -> None:
        event_only = [record for record in self.records if "event_id" in record]
        with self.assertRaises(MODULE.ValidationError):
            MODULE.summarize(event_only)


if __name__ == "__main__":
    unittest.main()
