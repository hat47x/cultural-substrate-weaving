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
        cls.event_example = json.loads(
            (ROOT / "evals" / "living-lab-event.example.json").read_text(encoding="utf-8")
        )

    def test_public_observations_summarize_without_scoring(self) -> None:
        summary = MODULE.summarize(self.records)
        self.assertIn("not KPIs", summary["interpretation_note"])
        self.assertIn("Activation state does not establish", summary["interpretation_note"])
        self.assertEqual(summary["schema_version"], "0.2")
        self.assertEqual(
            summary["inventory"]["task_domains"],
            {"software and research-method repository operations": 1},
        )
        self.assertEqual(summary["inventory"]["activation_scopes"], {"non_activation": 1})
        self.assertEqual(summary["inventory"]["event_types"], {})
        self.assertEqual(summary["inventory"]["interpretation_source_types"], {"ai": 1})
        self.assertEqual(summary["rounds"][0]["round_id"], "round-2026-08-30-001")
        self.assertEqual(
            summary["rounds"][0]["task_domain"],
            "software and research-method repository operations",
        )
        self.assertEqual(summary["rounds"][0]["events"], [])
        self.assertEqual(
            summary["rounds"][0]["interpretations"][0]["source_type"],
            "ai",
        )

    def test_summary_requires_event_round_references_to_resolve(self) -> None:
        with self.assertRaises(MODULE.ValidationError):
            MODULE.summarize([self.event_example])


if __name__ == "__main__":
    unittest.main()
