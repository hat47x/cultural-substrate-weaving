from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_living_lab",
    ROOT / "scripts" / "validate_living_lab.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LivingLabValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.round_record = json.loads(
            (ROOT / "evals" / "living-lab-round.example.json").read_text(encoding="utf-8")
        )
        cls.paired_record = json.loads(
            (ROOT / "evals" / "living-lab-paired.example.json").read_text(encoding="utf-8")
        )
        cls.event_record = json.loads(
            (ROOT / "evals" / "living-lab-event.example.json").read_text(encoding="utf-8")
        )

    def test_examples_are_valid(self) -> None:
        self.assertEqual(MODULE.validate_record(self.round_record), "round")
        self.assertEqual(MODULE.validate_record(self.paired_record), "round")
        self.assertEqual(MODULE.validate_record(self.event_record), "event")
        MODULE.validate_record_set(
            [self.round_record, self.paired_record, self.event_record]
        )

    def test_paired_check_requires_comparison_refs(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["mode"] = "paired_check"
        record.pop("comparison", None)
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_non_activation_rejects_framework_contacts(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["activation_scope"] = "non_activation"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_event_requires_evidence_reference(self) -> None:
        record = copy.deepcopy(self.event_record)
        record["evidence_refs"] = []
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(record)

    def test_unknown_event_type_is_rejected(self) -> None:
        record = copy.deepcopy(self.event_record)
        record["event_type"] = "framework_count_increased"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(record)

    def test_record_set_rejects_orphan_event(self) -> None:
        event = copy.deepcopy(self.event_record)
        event["round_id"] = "round-missing-001"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_record_set([self.round_record, event])

    def test_record_set_rejects_duplicate_round_id(self) -> None:
        duplicate = copy.deepcopy(self.round_record)
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_record_set([self.round_record, duplicate])

    def test_single_event_can_still_be_validated_without_round_file(self) -> None:
        self.assertEqual(MODULE.validate_record(self.event_record), "event")


if __name__ == "__main__":
    unittest.main()
