#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "0.2"

ROUND_REQUIRED = {
    "schema_version",
    "round_id",
    "case_id",
    "mode",
    "observed_at",
    "task",
    "activation_scope",
    "framework_contacts",
    "artifacts",
    "residuals",
    "reopening_conditions",
}
ROUND_ALLOWED = ROUND_REQUIRED | {
    "environment",
    "catalytic_deltas",
    "material_delta_refs",
    "invocation",
    "unloaded_framework_candidates",
    "kj_snapshot_refs",
    "artifact_traces",
    "comparison",
    "interpretations",
    "notes",
}
ENVIRONMENT_REQUIRED: set[str] = set()
ENVIRONMENT_ALLOWED = {"platform", "model_label", "product_mode", "tools", "notes"}
TASK_REQUIRED = {"summary"}
TASK_ALLOWED = {"summary", "domain", "source_refs", "constraints"}
CANDIDATE_REQUIRED = {"framework", "reason", "disposition"}
CANDIDATE_ALLOWED = CANDIDATE_REQUIRED | {"stop_reason"}
CONTACT_REQUIRED = {"framework", "depth", "use"}
CONTACT_ALLOWED = CONTACT_REQUIRED | {"notes", "selection_ref", "operations"}
COMPARISON_REQUIRED = {"baseline_chat_ref", "treatment_chat_ref"}
COMPARISON_ALLOWED = COMPARISON_REQUIRED | {
    "evaluator_chat_ref",
    "run_order",
    "observed_differences",
    "measurements",
    "interpretations",
}
SOURCED_STATEMENT_REQUIRED = {"source_type", "statement"}
SOURCED_STATEMENT_ALLOWED = SOURCED_STATEMENT_REQUIRED | {"source_ref", "evidence_refs"}
MEASUREMENT_REQUIRED = {"label", "value", "source_ref"}
MEASUREMENT_ALLOWED = MEASUREMENT_REQUIRED | {"unit", "notes"}

ARTIFACT_TRACE_REQUIRED = {"artifact_ref", "origin", "target_return"}
ARTIFACT_TRACE_ALLOWED = ARTIFACT_TRACE_REQUIRED | {
    "framework_refs",
    "selection_refs",
    "operation_refs",
    "user_disposition",
    "notes",
}

CATALYTIC_DELTA_REQUIRED = {
    "delta_ref",
    "kind",
    "statement",
    "framework_refs",
    "target_return",
}
CATALYTIC_DELTA_ALLOWED = CATALYTIC_DELTA_REQUIRED | {
    "selection_refs",
    "operation_refs",
    "artifact_refs",
    "user_disposition",
    "notes",
}
TARGET_RETURN_REQUIRED = {"state", "source_type", "evidence_refs"}
TARGET_RETURN_ALLOWED = TARGET_RETURN_REQUIRED | {"statement"}
USER_DISPOSITION_REQUIRED = {"state"}
USER_DISPOSITION_ALLOWED = USER_DISPOSITION_REQUIRED | {"source_ref", "notes"}

EVENT_REQUIRED = {
    "schema_version",
    "event_id",
    "round_id",
    "event_type",
    "observation_mode",
    "recorded_at",
    "observation",
    "evidence_refs",
}
EVENT_ALLOWED = EVENT_REQUIRED | {
    "interpretations",
    "artifact_refs",
    "framework_refs",
    "reopening_condition",
    "notes",
}

CANDIDATE_DISPOSITIONS = {"rejected", "deferred"}
DEPTHS = {"probe", "preview", "full", "enacted"}
USES = {"exploration", "attribution"}
ACTIVATION_SCOPES = {"non_activation", "limited_use", "exploratory_use"}
ROUND_MODES = {"natural_work", "paired_check"}
INVOCATIONS = {"none", "implicit", "explicit"}
RUN_ORDERS = {"baseline_first", "treatment_first", "parallel_or_unknown"}
EVENT_TYPES = {
    "question_shift",
    "search_shift",
    "kj_reconfiguration",
    "artifact_adoption",
    "artifact_withdrawal",
    "decision_change",
    "delayed_reactivation",
    "repeated_transfer",
    "framework_contact_change",
}
OBSERVATION_MODES = {"prospective", "retrospective"}
SOURCE_TYPES = {"user", "ai", "external", "mixed", "unknown"}
ARTIFACT_ORIGINS = {
    "target_only",
    "framework_generated",
    "cross_field_emergent",
    "mixed",
}
FRAMEWORK_DERIVED_ARTIFACT_ORIGINS = {
    "framework_generated",
    "cross_field_emergent",
    "mixed",
}
TARGET_RETURN_STATES = {
    "not_checked",
    "unresolved",
    "target_supported",
    "target_weakened",
    "target_rejected",
    "not_applicable",
}
USER_DISPOSITIONS = {"not_observed", "adopted", "modified", "withdrawn"}
CATALYTIC_DELTA_KINDS = {
    "question",
    "distinction",
    "relation-or-transition",
    "falsifier-or-observation",
    "residual",
    "framework-specific-scaffold",
}
ID_RE = re.compile(r"^(round|event)-[A-Za-z0-9._-]+$")


class ValidationError(ValueError):
    pass


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{label} must be an array")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{label} must be a string")
    return value


def _require_nonempty_string(value: Any, label: str) -> str:
    text = _require_string(value, label)
    if not text.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return text


def _check_keys(data: dict[str, Any], required: set[str], allowed: set[str], label: str) -> None:
    missing = sorted(required - data.keys())
    if missing:
        raise ValidationError(f"{label} missing required fields: {', '.join(missing)}")
    extra = sorted(data.keys() - allowed)
    if extra:
        raise ValidationError(f"{label} has unknown fields: {', '.join(extra)}")


def _check_enum(value: Any, allowed: set[str], label: str) -> None:
    if value not in allowed:
        raise ValidationError(f"{label} must be one of: {', '.join(sorted(allowed))}")


def _check_datetime(value: Any, label: str) -> None:
    text = _require_nonempty_string(value, label)
    if "T" not in text:
        raise ValidationError(f"{label} must be an ISO-8601 date-time")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{label} must be an ISO-8601 date-time") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{label} must include a timezone offset")


def _check_string_list(
    value: Any,
    label: str,
    *,
    nonempty: bool = False,
    unique: bool = False,
    item_nonempty: bool = True,
) -> None:
    items = _require_list(value, label)
    if nonempty and not items:
        raise ValidationError(f"{label} must contain at least one item")
    for index, item in enumerate(items):
        if item_nonempty:
            _require_nonempty_string(item, f"{label}[{index}]")
        else:
            _require_string(item, f"{label}[{index}]")
    if unique and len(items) != len(set(items)):
        raise ValidationError(f"{label} must not contain duplicates")


def _validate_sourced_statement(value: Any, label: str) -> None:
    statement = _require_object(value, label)
    _check_keys(statement, SOURCED_STATEMENT_REQUIRED, SOURCED_STATEMENT_ALLOWED, label)
    _check_enum(statement["source_type"], SOURCE_TYPES, f"{label}.source_type")
    _require_nonempty_string(statement["statement"], f"{label}.statement")
    if "source_ref" in statement:
        _require_nonempty_string(statement["source_ref"], f"{label}.source_ref")
    if "evidence_refs" in statement:
        _check_string_list(
            statement["evidence_refs"], f"{label}.evidence_refs", unique=True
        )


def _check_sourced_statement_list(value: Any, label: str) -> None:
    items = _require_list(value, label)
    for index, item in enumerate(items):
        _validate_sourced_statement(item, f"{label}[{index}]")


def _validate_measurement(value: Any, label: str) -> None:
    measurement = _require_object(value, label)
    _check_keys(measurement, MEASUREMENT_REQUIRED, MEASUREMENT_ALLOWED, label)
    _require_nonempty_string(measurement["label"], f"{label}.label")
    if not isinstance(measurement["value"], (str, int, float, bool)):
        raise ValidationError(f"{label}.value must be a string, number, or boolean")
    _require_nonempty_string(measurement["source_ref"], f"{label}.source_ref")
    for field in ("unit", "notes"):
        if field in measurement:
            _require_string(measurement[field], f"{label}.{field}")


def _validate_target_return(value: Any, label: str) -> dict[str, Any]:
    target_return = _require_object(value, label)
    _check_keys(target_return, TARGET_RETURN_REQUIRED, TARGET_RETURN_ALLOWED, label)
    _check_enum(target_return["state"], TARGET_RETURN_STATES, f"{label}.state")
    _check_enum(target_return["source_type"], SOURCE_TYPES, f"{label}.source_type")
    _check_string_list(
        target_return["evidence_refs"],
        f"{label}.evidence_refs",
        unique=True,
    )
    if (
        target_return["state"]
        not in {"not_checked", "not_applicable"}
        and not target_return["evidence_refs"]
    ):
        raise ValidationError(
            f"{label}.evidence_refs must contain evidence when target return was evaluated"
        )
    if "statement" in target_return:
        _require_nonempty_string(target_return["statement"], f"{label}.statement")
    return target_return


def _validate_user_disposition(value: Any, label: str) -> dict[str, Any]:
    disposition = _require_object(value, label)
    _check_keys(disposition, USER_DISPOSITION_REQUIRED, USER_DISPOSITION_ALLOWED, label)
    _check_enum(disposition["state"], USER_DISPOSITIONS, f"{label}.state")
    if disposition["state"] != "not_observed":
        if "source_ref" not in disposition:
            raise ValidationError(
                f"{label}.source_ref is required for an observed user disposition"
            )
        _require_nonempty_string(disposition["source_ref"], f"{label}.source_ref")
    elif "source_ref" in disposition:
        _require_nonempty_string(disposition["source_ref"], f"{label}.source_ref")
    if "notes" in disposition:
        _require_string(disposition["notes"], f"{label}.notes")
    return disposition


def _validate_artifact_trace(value: Any, label: str) -> dict[str, Any]:
    trace = _require_object(value, label)
    _check_keys(trace, ARTIFACT_TRACE_REQUIRED, ARTIFACT_TRACE_ALLOWED, label)
    _require_nonempty_string(trace["artifact_ref"], f"{label}.artifact_ref")
    _check_enum(trace["origin"], ARTIFACT_ORIGINS, f"{label}.origin")

    framework_refs = trace.get("framework_refs", [])
    _check_string_list(framework_refs, f"{label}.framework_refs", unique=True)
    if trace["origin"] in FRAMEWORK_DERIVED_ARTIFACT_ORIGINS and not framework_refs:
        raise ValidationError(
            f"{label}.framework_refs must identify provenance for framework-derived artifacts"
        )

    _check_string_list(
        trace.get("selection_refs", []),
        f"{label}.selection_refs",
        unique=True,
    )
    _check_string_list(
        trace.get("operation_refs", []),
        f"{label}.operation_refs",
        unique=True,
    )
    _validate_target_return(trace["target_return"], f"{label}.target_return")
    if "user_disposition" in trace:
        _validate_user_disposition(
            trace["user_disposition"],
            f"{label}.user_disposition",
        )
    if "notes" in trace:
        _require_string(trace["notes"], f"{label}.notes")
    return trace


def _validate_catalytic_delta(value: Any, label: str) -> dict[str, Any]:
    delta = _require_object(value, label)
    _check_keys(delta, CATALYTIC_DELTA_REQUIRED, CATALYTIC_DELTA_ALLOWED, label)
    _require_nonempty_string(delta["delta_ref"], f"{label}.delta_ref")
    _check_enum(delta["kind"], CATALYTIC_DELTA_KINDS, f"{label}.kind")
    _require_nonempty_string(delta["statement"], f"{label}.statement")
    _check_string_list(
        delta["framework_refs"],
        f"{label}.framework_refs",
        nonempty=True,
        unique=True,
    )
    for field in ("selection_refs", "operation_refs", "artifact_refs"):
        _check_string_list(
            delta.get(field, []),
            f"{label}.{field}",
            unique=True,
        )
    _validate_target_return(delta["target_return"], f"{label}.target_return")
    if "user_disposition" in delta:
        _validate_user_disposition(
            delta["user_disposition"],
            f"{label}.user_disposition",
        )
    if "notes" in delta:
        _require_string(delta["notes"], f"{label}.notes")
    return delta


def validate_round(data: dict[str, Any]) -> None:
    _check_keys(data, ROUND_REQUIRED, ROUND_ALLOWED, "round")
    if data["schema_version"] != SCHEMA_VERSION:
        raise ValidationError(f"round.schema_version must be {SCHEMA_VERSION}")

    round_id = _require_nonempty_string(data["round_id"], "round.round_id")
    if not ID_RE.fullmatch(round_id) or not round_id.startswith("round-"):
        raise ValidationError("round.round_id must start with round-")
    _require_nonempty_string(data["case_id"], "round.case_id")
    _check_enum(data["mode"], ROUND_MODES, "round.mode")
    _check_datetime(data["observed_at"], "round.observed_at")
    _check_enum(data["activation_scope"], ACTIVATION_SCOPES, "round.activation_scope")

    if "environment" in data:
        environment = _require_object(data["environment"], "round.environment")
        _check_keys(environment, ENVIRONMENT_REQUIRED, ENVIRONMENT_ALLOWED, "round.environment")
        if "platform" in environment:
            _require_nonempty_string(environment["platform"], "round.environment.platform")
        for field in ("model_label", "product_mode", "notes"):
            if field in environment:
                _require_string(environment[field], f"round.environment.{field}")
        if "tools" in environment:
            _check_string_list(
                environment["tools"],
                "round.environment.tools",
                unique=True,
                item_nonempty=False,
            )

    if "invocation" in data:
        _check_enum(data["invocation"], INVOCATIONS, "round.invocation")

    task = _require_object(data["task"], "round.task")
    _check_keys(task, TASK_REQUIRED, TASK_ALLOWED, "round.task")
    _require_nonempty_string(task["summary"], "round.task.summary")
    if "domain" in task:
        _require_string(task["domain"], "round.task.domain")
    if "source_refs" in task:
        _check_string_list(task["source_refs"], "round.task.source_refs", unique=True)
    if "constraints" in task:
        _check_sourced_statement_list(task["constraints"], "round.task.constraints")

    for field in ("material_delta_refs", "kj_snapshot_refs", "artifacts"):
        if field in data:
            _check_string_list(data[field], f"round.{field}", unique=True)

    artifact_refs = set(data["artifacts"])
    artifact_traces = _require_list(data.get("artifact_traces", []), "round.artifact_traces")
    traced_artifacts: set[str] = set()
    for index, raw in enumerate(artifact_traces):
        label = f"round.artifact_traces[{index}]"
        trace = _validate_artifact_trace(raw, label)
        artifact_ref = trace["artifact_ref"]
        if artifact_ref not in artifact_refs:
            raise ValidationError(
                f"{label}.artifact_ref must also appear in round.artifacts: {artifact_ref}"
            )
        if artifact_ref in traced_artifacts:
            raise ValidationError(
                f"round.artifact_traces must not repeat artifact_ref: {artifact_ref}"
            )
        traced_artifacts.add(artifact_ref)

    catalytic_deltas = _require_list(
        data.get("catalytic_deltas", []),
        "round.catalytic_deltas",
    )
    seen_delta_refs: set[str] = set()
    for index, raw in enumerate(catalytic_deltas):
        label = f"round.catalytic_deltas[{index}]"
        delta = _validate_catalytic_delta(raw, label)
        delta_ref = delta["delta_ref"]
        if delta_ref in seen_delta_refs:
            raise ValidationError(
                f"round.catalytic_deltas must not repeat delta_ref: {delta_ref}"
            )
        seen_delta_refs.add(delta_ref)
        for artifact_ref in delta.get("artifact_refs", []):
            if artifact_ref not in artifact_refs:
                raise ValidationError(
                    f"{label}.artifact_refs must reference round.artifacts: {artifact_ref}"
                )

    _check_sourced_statement_list(data["residuals"], "round.residuals")
    _check_sourced_statement_list(data["reopening_conditions"], "round.reopening_conditions")

    candidates = _require_list(
        data.get("unloaded_framework_candidates", []),
        "round.unloaded_framework_candidates",
    )
    for index, raw in enumerate(candidates):
        label = f"round.unloaded_framework_candidates[{index}]"
        candidate = _require_object(raw, label)
        _check_keys(candidate, CANDIDATE_REQUIRED, CANDIDATE_ALLOWED, label)
        _require_nonempty_string(candidate["framework"], f"{label}.framework")
        _require_nonempty_string(candidate["reason"], f"{label}.reason")
        _check_enum(
            candidate["disposition"],
            CANDIDATE_DISPOSITIONS,
            f"{label}.disposition",
        )
        if "stop_reason" in candidate:
            _require_string(candidate["stop_reason"], f"{label}.stop_reason")

    contacts = _require_list(data["framework_contacts"], "round.framework_contacts")
    for index, raw in enumerate(contacts):
        label = f"round.framework_contacts[{index}]"
        contact = _require_object(raw, label)
        _check_keys(contact, CONTACT_REQUIRED, CONTACT_ALLOWED, label)
        _require_nonempty_string(contact["framework"], f"{label}.framework")
        _check_enum(contact["depth"], DEPTHS, f"{label}.depth")
        _check_enum(contact["use"], USES, f"{label}.use")
        if "notes" in contact:
            _require_string(contact["notes"], f"{label}.notes")
        if "selection_ref" in contact:
            _require_nonempty_string(contact["selection_ref"], f"{label}.selection_ref")
        if "operations" in contact:
            _check_string_list(
                contact["operations"],
                f"{label}.operations",
                unique=True,
            )

    if data["activation_scope"] == "non_activation" and contacts:
        raise ValidationError("non_activation rounds must not contain framework_contacts")
    if data["activation_scope"] == "non_activation" and catalytic_deltas:
        raise ValidationError("non_activation rounds must not contain catalytic_deltas")

    comparison = data.get("comparison")
    if data["mode"] == "paired_check" and comparison is None:
        raise ValidationError("paired_check rounds must contain comparison")
    if comparison is not None:
        comparison = _require_object(comparison, "round.comparison")
        _check_keys(comparison, COMPARISON_REQUIRED, COMPARISON_ALLOWED, "round.comparison")
        _require_nonempty_string(
            comparison["baseline_chat_ref"], "round.comparison.baseline_chat_ref"
        )
        _require_nonempty_string(
            comparison["treatment_chat_ref"], "round.comparison.treatment_chat_ref"
        )
        if "evaluator_chat_ref" in comparison:
            _require_string(
                comparison["evaluator_chat_ref"], "round.comparison.evaluator_chat_ref"
            )
        if "run_order" in comparison:
            _check_enum(comparison["run_order"], RUN_ORDERS, "round.comparison.run_order")
        if "observed_differences" in comparison:
            _check_string_list(
                comparison["observed_differences"], "round.comparison.observed_differences"
            )
        if "measurements" in comparison:
            measurements = _require_list(
                comparison["measurements"], "round.comparison.measurements"
            )
            for index, measurement in enumerate(measurements):
                _validate_measurement(
                    measurement, f"round.comparison.measurements[{index}]"
                )
        if "interpretations" in comparison:
            _check_sourced_statement_list(
                comparison["interpretations"], "round.comparison.interpretations"
            )

    if "interpretations" in data:
        _check_sourced_statement_list(data["interpretations"], "round.interpretations")
    if "notes" in data:
        _require_string(data["notes"], "round.notes")


def validate_event(data: dict[str, Any]) -> None:
    _check_keys(data, EVENT_REQUIRED, EVENT_ALLOWED, "event")
    if data["schema_version"] != SCHEMA_VERSION:
        raise ValidationError(f"event.schema_version must be {SCHEMA_VERSION}")

    event_id = _require_nonempty_string(data["event_id"], "event.event_id")
    round_id = _require_nonempty_string(data["round_id"], "event.round_id")
    if not ID_RE.fullmatch(event_id) or not event_id.startswith("event-"):
        raise ValidationError("event.event_id must start with event-")
    if not ID_RE.fullmatch(round_id) or not round_id.startswith("round-"):
        raise ValidationError("event.round_id must start with round-")
    _check_enum(data["event_type"], EVENT_TYPES, "event.event_type")
    _check_enum(data["observation_mode"], OBSERVATION_MODES, "event.observation_mode")
    _check_datetime(data["recorded_at"], "event.recorded_at")
    _require_nonempty_string(data["observation"], "event.observation")
    _check_string_list(data["evidence_refs"], "event.evidence_refs", nonempty=True, unique=True)
    if "interpretations" in data:
        _check_sourced_statement_list(data["interpretations"], "event.interpretations")
    for field in ("artifact_refs", "framework_refs"):
        if field in data:
            _check_string_list(data[field], f"event.{field}", unique=True)
    if "reopening_condition" in data:
        _validate_sourced_statement(data["reopening_condition"], "event.reopening_condition")
    if "notes" in data:
        _require_string(data["notes"], "event.notes")


def validate_record(data: dict[str, Any]) -> str:
    if "event_id" in data:
        validate_event(data)
        return "event"
    if "round_id" in data:
        validate_round(data)
        return "round"
    raise ValidationError("record must contain round_id or event_id")


def load_record(path: Path) -> tuple[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top level must be an object")
    return validate_record(data), data


def load_and_validate(path: Path) -> str:
    kind, _ = load_record(path)
    return kind


def validate_record_set(records: list[dict[str, Any]]) -> None:
    """Validate identifiers and event-to-round references inside one supplied record set."""
    round_ids: set[str] = set()
    event_ids: set[str] = set()
    events: list[dict[str, Any]] = []

    for data in records:
        kind = validate_record(data)
        if kind == "round":
            identifier = data["round_id"]
            if identifier in round_ids:
                raise ValidationError(f"duplicate round_id in record set: {identifier}")
            round_ids.add(identifier)
        else:
            identifier = data["event_id"]
            if identifier in event_ids:
                raise ValidationError(f"duplicate event_id in record set: {identifier}")
            event_ids.add(identifier)
            events.append(data)

    for event in events:
        if event["round_id"] not in round_ids:
            raise ValidationError(
                f"event {event['event_id']} references missing round_id: {event['round_id']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Web Chat Living Lab round/event records.")
    parser.add_argument("paths", nargs="*", type=Path, help="JSON records to validate")
    parser.add_argument(
        "--record-set",
        action="store_true",
        help="Also require unique IDs and event round_id references to resolve within the supplied files.",
    )
    args = parser.parse_args()
    use_default_set = not args.paths
    paths = args.paths or [
        ROOT / "evals" / "living-lab-round.example.json",
        ROOT / "evals" / "living-lab-paired.example.json",
        ROOT / "evals" / "living-lab-event.example.json",
    ]

    try:
        loaded: list[dict[str, Any]] = []
        for path in paths:
            kind, data = load_record(path)
            loaded.append(data)
            print(f"OK {kind}: {path}")
        if args.record_set or use_default_set:
            validate_record_set(loaded)
            print(f"OK record-set: {len(loaded)} records")
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Living Lab validation failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
