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
        cls.round_schema = json.loads(
            (ROOT / "evals" / "living-lab-round.schema.json").read_text(encoding="utf-8")
        )
        cls.event_schema = json.loads(
            (ROOT / "evals" / "living-lab-event.schema.json").read_text(encoding="utf-8")
        )

    def test_examples_are_valid(self) -> None:
        self.assertEqual(MODULE.validate_record(self.round_record), "round")
        self.assertEqual(MODULE.validate_record(self.paired_record), "round")
        self.assertEqual(MODULE.validate_record(self.event_record), "event")
        MODULE.validate_record_set(
            [self.round_record, self.paired_record, self.event_record]
        )

    def test_public_observations_form_a_valid_closed_record_set(self) -> None:
        observation_dir = ROOT / "research" / "living-lab" / "observations"
        records = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(observation_dir.glob("*.json"))
        ]
        self.assertTrue(records, "public Living Lab observation set must not be empty")
        MODULE.validate_record_set(records)

    def test_validator_contract_matches_json_schemas(self) -> None:
        round_properties = self.round_schema["properties"]
        event_properties = self.event_schema["properties"]

        self.assertEqual(MODULE.SCHEMA_VERSION, round_properties["schema_version"]["const"])
        self.assertEqual(MODULE.SCHEMA_VERSION, event_properties["schema_version"]["const"])
        self.assertEqual(MODULE.ROUND_REQUIRED, set(self.round_schema["required"]))
        self.assertEqual(MODULE.ROUND_ALLOWED, set(round_properties))
        self.assertEqual(MODULE.EVENT_REQUIRED, set(self.event_schema["required"]))
        self.assertEqual(MODULE.EVENT_ALLOWED, set(event_properties))

        environment = round_properties["environment"]
        self.assertEqual(MODULE.ENVIRONMENT_REQUIRED, set(environment.get("required", [])))
        self.assertEqual(MODULE.ENVIRONMENT_ALLOWED, set(environment["properties"]))

        task = round_properties["task"]
        self.assertEqual(MODULE.TASK_REQUIRED, set(task["required"]))
        self.assertEqual(MODULE.TASK_ALLOWED, set(task["properties"]))

        contact = round_properties["framework_contacts"]["items"]
        self.assertEqual(MODULE.CONTACT_REQUIRED, set(contact["required"]))
        self.assertEqual(MODULE.CONTACT_ALLOWED, set(contact["properties"]))

        comparison = round_properties["comparison"]
        self.assertEqual(MODULE.COMPARISON_REQUIRED, set(comparison["required"]))
        self.assertEqual(MODULE.COMPARISON_ALLOWED, set(comparison["properties"]))

        self.assertEqual(MODULE.ROUND_MODES, set(round_properties["mode"]["enum"]))
        self.assertEqual(
            MODULE.ACTIVATION_SCOPES,
            set(round_properties["activation_scope"]["enum"]),
        )
        self.assertEqual(MODULE.INVOCATIONS, set(round_properties["invocation"]["enum"]))
        self.assertEqual(
            MODULE.DEPTHS,
            set(round_properties["framework_contacts"]["items"]["properties"]["depth"]["enum"]),
        )
        self.assertEqual(
            MODULE.USES,
            set(round_properties["framework_contacts"]["items"]["properties"]["use"]["enum"]),
        )
        self.assertEqual(MODULE.RUN_ORDERS, set(comparison["properties"]["run_order"]["enum"]))
        self.assertEqual(MODULE.EVENT_TYPES, set(event_properties["event_type"]["enum"]))
        self.assertEqual(
            MODULE.OBSERVATION_MODES,
            set(event_properties["observation_mode"]["enum"]),
        )

    def test_paired_check_requires_comparison_refs(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["mode"] = "paired_check"
        record.pop("comparison", None)
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_comparison_object_always_requires_both_chat_refs(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["comparison"] = {"baseline_chat_ref": "chat:baseline"}
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_invalid_comparison_run_order_is_rejected(self) -> None:
        record = copy.deepcopy(self.paired_record)
        record["comparison"]["run_order"] = "framework_first"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_unknown_nested_round_fields_are_rejected(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["task"]["unexpected"] = "value"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        record = copy.deepcopy(self.round_record)
        record["environment"]["unexpected"] = "value"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        record = copy.deepcopy(self.paired_record)
        record["comparison"]["unexpected"] = "value"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_nested_optional_fields_respect_schema_types(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["task"]["domain"] = ["not", "a", "string"]
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        record = copy.deepcopy(self.round_record)
        record["environment"]["notes"] = {"not": "a string"}
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        event = copy.deepcopy(self.event_record)
        event["reopening_condition"] = ["not", "a", "string"]
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(event)

    def test_datetime_requires_date_time_and_timezone(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["observed_at"] = "2026-08-30"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        event = copy.deepcopy(self.event_record)
        event["recorded_at"] = "2026-08-30T15:35:00"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(event)

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
