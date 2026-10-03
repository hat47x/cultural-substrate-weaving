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

        round_statement = self.round_schema["$defs"]["sourced_statement"]
        event_statement = self.event_schema["$defs"]["sourced_statement"]
        self.assertEqual(MODULE.SOURCED_STATEMENT_REQUIRED, set(round_statement["required"]))
        self.assertEqual(MODULE.SOURCED_STATEMENT_ALLOWED, set(round_statement["properties"]))
        self.assertEqual(MODULE.SOURCED_STATEMENT_REQUIRED, set(event_statement["required"]))
        self.assertEqual(MODULE.SOURCED_STATEMENT_ALLOWED, set(event_statement["properties"]))

        measurement = self.round_schema["$defs"]["measurement"]
        self.assertEqual(MODULE.MEASUREMENT_REQUIRED, set(measurement["required"]))
        self.assertEqual(MODULE.MEASUREMENT_ALLOWED, set(measurement["properties"]))

        artifact_trace = self.round_schema["$defs"]["artifact_trace"]
        catalytic_delta = self.round_schema["$defs"]["catalytic_delta"]
        pre_contact_relation = self.round_schema["$defs"]["pre_contact_relation"]
        target_return = self.round_schema["$defs"]["target_return"]
        user_disposition = self.round_schema["$defs"]["user_disposition"]
        self.assertEqual(MODULE.ARTIFACT_TRACE_REQUIRED, set(artifact_trace["required"]))
        self.assertEqual(MODULE.ARTIFACT_TRACE_ALLOWED, set(artifact_trace["properties"]))
        self.assertEqual(MODULE.CATALYTIC_DELTA_REQUIRED, set(catalytic_delta["required"]))
        self.assertEqual(MODULE.CATALYTIC_DELTA_ALLOWED, set(catalytic_delta["properties"]))
        self.assertEqual(
            MODULE.PRE_CONTACT_RELATION_REQUIRED,
            set(pre_contact_relation["required"]),
        )
        self.assertEqual(
            MODULE.PRE_CONTACT_RELATION_ALLOWED,
            set(pre_contact_relation["properties"]),
        )
        self.assertEqual(MODULE.TARGET_RETURN_REQUIRED, set(target_return["required"]))
        self.assertEqual(MODULE.TARGET_RETURN_ALLOWED, set(target_return["properties"]))
        self.assertEqual(
            MODULE.USER_DISPOSITION_REQUIRED,
            set(user_disposition["required"]),
        )
        self.assertEqual(
            MODULE.USER_DISPOSITION_ALLOWED,
            set(user_disposition["properties"]),
        )

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
        self.assertEqual(
            MODULE.SOURCE_TYPES,
            set(round_statement["properties"]["source_type"]["enum"]),
        )
        self.assertEqual(
            MODULE.SOURCE_TYPES,
            set(event_statement["properties"]["source_type"]["enum"]),
        )
        self.assertEqual(
            MODULE.ARTIFACT_ORIGINS,
            set(artifact_trace["properties"]["origin"]["enum"]),
        )
        self.assertEqual(
            MODULE.CATALYTIC_DELTA_KINDS,
            set(catalytic_delta["properties"]["kind"]["enum"]),
        )
        self.assertEqual(
            MODULE.PRE_CONTACT_RELATION_STATES,
            set(pre_contact_relation["properties"]["state"]["enum"]),
        )
        self.assertEqual(
            MODULE.TARGET_RETURN_STATES,
            set(target_return["properties"]["state"]["enum"]),
        )
        self.assertEqual(
            MODULE.USER_DISPOSITIONS,
            set(user_disposition["properties"]["state"]["enum"]),
        )

        target_return_rules = target_return["allOf"]
        self.assertTrue(
            any(
                "evidence_refs" in rule.get("then", {}).get("properties", {})
                and rule["then"]["properties"]["evidence_refs"].get("minItems") == 1
                for rule in target_return_rules
            ),
            "evaluated target-return states must require evidence in JSON Schema",
        )

        disposition_rules = user_disposition["allOf"]
        self.assertTrue(
            any(
                "source_ref" in rule.get("then", {}).get("required", [])
                for rule in disposition_rules
            ),
            "observed user disposition must require a source_ref in JSON Schema",
        )

        artifact_trace_rules = artifact_trace["allOf"]
        self.assertTrue(
            any(
                "framework_refs" in rule.get("then", {}).get("required", [])
                and rule.get("then", {})
                .get("properties", {})
                .get("framework_refs", {})
                .get("minItems")
                == 1
                for rule in artifact_trace_rules
            ),
            "framework-derived artifact provenance must be required in JSON Schema",
        )

        semantic_rules = self.round_schema["allOf"]
        self.assertTrue(
            any(
                rule.get("if", {}).get("properties", {}).get("mode", {}).get("const")
                == "paired_check"
                and "comparison" in rule.get("then", {}).get("required", [])
                for rule in semantic_rules
            ),
            "round schema must require comparison for paired_check",
        )
        self.assertTrue(
            any(
                rule.get("if", {})
                .get("properties", {})
                .get("activation_scope", {})
                .get("const")
                == "non_activation"
                and rule.get("then", {})
                .get("properties", {})
                .get("framework_contacts", {})
                .get("maxItems")
                == 0
                for rule in semantic_rules
            ),
            "round schema must forbid framework contacts for non_activation",
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

    def test_sourced_statements_require_valid_source_type(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["task"]["constraints"][0]["source_type"] = "model_guess"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

        event = copy.deepcopy(self.event_record)
        event["interpretations"][0]["source_type"] = "model_guess"
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(event)

    def test_measurements_are_distinct_from_interpretations(self) -> None:
        record = copy.deepcopy(self.paired_record)
        measurement = record["comparison"]["measurements"][0]
        measurement.pop("source_ref")
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

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

    def test_non_activation_rejects_catalytic_deltas(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["activation_scope"] = "non_activation"
        record["framework_contacts"] = []
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must not contain catalytic_deltas",
        ):
            MODULE.validate_round(record)

    def test_artifact_trace_requires_declared_artifact(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["artifact_traces"][0]["artifact_ref"] = "artifact:not-declared"
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must also appear in round.artifacts",
        ):
            MODULE.validate_round(record)

    def test_framework_derived_artifact_trace_requires_framework_provenance(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["artifact_traces"][0]["framework_refs"] = []
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must identify provenance",
        ):
            MODULE.validate_round(record)

    def test_evaluated_target_return_requires_evidence(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["artifact_traces"][0]["target_return"]["evidence_refs"] = []
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must contain evidence",
        ):
            MODULE.validate_round(record)

    def test_observed_user_disposition_requires_source_ref(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["artifact_traces"][0]["user_disposition"].pop("source_ref")
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "source_ref is required",
        ):
            MODULE.validate_round(record)

    def test_duplicate_artifact_trace_is_rejected(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["artifact_traces"].append(copy.deepcopy(record["artifact_traces"][0]))
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must not repeat artifact_ref",
        ):
            MODULE.validate_round(record)

    def test_catalytic_delta_requires_framework_provenance(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["catalytic_deltas"][0]["framework_refs"] = []
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_round(record)

    def test_catalytic_delta_evaluated_pre_contact_relation_requires_evidence(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["catalytic_deltas"][0]["pre_contact_relation"]["evidence_refs"] = []
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "pre-contact relation was evaluated",
        ):
            MODULE.validate_round(record)

    def test_catalytic_delta_evaluated_return_requires_evidence(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["catalytic_deltas"][0]["target_return"]["evidence_refs"] = []
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must contain evidence",
        ):
            MODULE.validate_round(record)

    def test_duplicate_catalytic_delta_ref_is_rejected(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["catalytic_deltas"].append(
            copy.deepcopy(record["catalytic_deltas"][0])
        )
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must not repeat delta_ref",
        ):
            MODULE.validate_round(record)

    def test_catalytic_delta_artifact_refs_must_be_declared(self) -> None:
        record = copy.deepcopy(self.round_record)
        record["catalytic_deltas"][0]["artifact_refs"] = ["artifact:not-declared"]
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            "must reference round.artifacts",
        ):
            MODULE.validate_round(record)

    def test_event_requires_evidence_reference(self) -> None:
        record = copy.deepcopy(self.event_record)
        record["evidence_refs"] = []
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(record)

    def test_event_requires_observation_not_legacy_summary(self) -> None:
        record = copy.deepcopy(self.event_record)
        record["summary"] = record.pop("observation")
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate_event(record)

    def test_evaluative_event_types_are_rejected(self) -> None:
        for event_type in ("useful_nonuse", "harm_detected"):
            record = copy.deepcopy(self.event_record)
            record["event_type"] = event_type
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
