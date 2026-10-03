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
        cls.round_example = json.loads(
            (ROOT / "evals" / "living-lab-round.example.json").read_text(encoding="utf-8")
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

    def test_summary_surfaces_artifact_provenance_without_scoring(self) -> None:
        summary = MODULE.summarize([self.round_example])
        self.assertEqual(
            summary["inventory"]["artifact_origins"],
            {"framework_generated": 1},
        )
        self.assertEqual(
            summary["inventory"]["target_return_states"],
            {"target_weakened": 1},
        )
        self.assertEqual(
            summary["inventory"]["user_dispositions"],
            {"modified": 1},
        )
        trace = summary["rounds"][0]["artifact_traces"][0]
        self.assertEqual(trace["artifact_ref"], "artifact:draft-v4")
        self.assertEqual(trace["framework_refs"], ["example-framework"])
        self.assertEqual(
            trace["selection_refs"],
            ["selection://example-round/framework-choice"],
        )
        self.assertEqual(
            summary["inventory"]["catalytic_delta_kinds"],
            {"question": 1},
        )
        self.assertEqual(
            summary["inventory"]["catalytic_delta_target_return_states"],
            {"target_weakened": 1},
        )
        self.assertEqual(
            summary["inventory"]["catalytic_delta_pre_contact_states"],
            {"reframed_existing": 1},
        )
        self.assertEqual(
            summary["inventory"]["catalytic_delta_user_dispositions"],
            {"modified": 1},
        )
        delta = summary["rounds"][0]["catalytic_deltas"][0]
        self.assertEqual(delta["delta_ref"], "delta:example-question-001")
        self.assertEqual(delta["kind"], "question")
        self.assertIn("not KPIs", summary["interpretation_note"])

    def test_summary_requires_event_round_references_to_resolve(self) -> None:
        with self.assertRaises(MODULE.ValidationError):
            MODULE.summarize([self.event_example])


if __name__ == "__main__":
    unittest.main()
