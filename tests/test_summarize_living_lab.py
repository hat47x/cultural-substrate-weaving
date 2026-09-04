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
            summary["record_ids"],
            {
                "rounds": ["round-2026-08-30-001", "round-2026-09-04-002"],
                "events": ["event-2026-09-04-002"],
            },
        )
        self.assertEqual(
            summary["inventory"]["task_domains"],
            {
                "creative writing revision and KJ integration": 1,
                "software and research-method repository operations": 1,
            },
        )
        self.assertEqual(
            summary["inventory"]["activation_scopes"],
            {"limited_use": 1, "non_activation": 1},
        )
        self.assertEqual(summary["inventory"]["event_types"], {"kj_reconfiguration": 1})
        self.assertEqual(summary["inventory"]["observation_modes"], {"retrospective": 1})
        self.assertEqual(summary["inventory"]["interpretation_source_types"], {"ai": 3})

        first, second = summary["rounds"]
        self.assertEqual(first["round_id"], "round-2026-08-30-001")
        self.assertEqual(
            first["task_domain"],
            "software and research-method repository operations",
        )
        self.assertEqual(first["events"], [])
        self.assertEqual(first["interpretations"][0]["source_type"], "ai")

        self.assertEqual(second["round_id"], "round-2026-09-04-002")
        self.assertEqual(second["task_domain"], "creative writing revision and KJ integration")
        self.assertEqual(second["activation_scope"], "limited_use")
        self.assertEqual(second["events"][0]["event_id"], "event-2026-09-04-002")
        self.assertEqual(second["events"][0]["event_type"], "kj_reconfiguration")
        self.assertEqual(second["events"][0]["observation_mode"], "retrospective")
        self.assertEqual(second["interpretations"][0]["source_type"], "ai")

    def test_summary_requires_event_round_references_to_resolve(self) -> None:
        with self.assertRaises(MODULE.ValidationError):
            MODULE.summarize([self.event_example])


if __name__ == "__main__":
    unittest.main()
