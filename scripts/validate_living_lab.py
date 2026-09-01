#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "0.1"

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
    "material_delta_refs",
    "invocation",
    "unloaded_framework_candidates",
    "kj_snapshot_refs",
    "comparison",
    "notes",
}
ENVIRONMENT_REQUIRED: set[str] = set()
ENVIRONMENT_ALLOWED = {"platform", "model_label", "product_mode", "tools", "notes"}
TASK_REQUIRED = {"summary"}
TASK_ALLOWED = {"summary", "domain", "source_refs", "preservation_set"}
CANDIDATE_REQUIRED = {"framework", "reason", "disposition"}
CANDIDATE_ALLOWED = CANDIDATE_REQUIRED | {"stop_reason"}
CONTACT_REQUIRED = {"framework", "depth", "use"}
CONTACT_ALLOWED = CONTACT_REQUIRED | {"notes"}
COMPARISON_REQUIRED = {"baseline_chat_ref", "treatment_chat_ref"}
COMPARISON_ALLOWED = COMPARISON_REQUIRED | {
    "evaluator_chat_ref",
    "run_order",
    "difference_notes",
}

EVENT_REQUIRED = {
    "schema_version",
    "event_id",
    "round_id",
    "event_type",
    "observation_mode",
    "recorded_at",
    "summary",
    "evidence_refs",
}
EVENT_ALLOWED = EVENT_REQUIRED | {
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
    "decision_change",
    "delayed_reactivation",
    "repeated_transfer",
    "useful_nonuse",
    "harm_detected",
}
OBSERVATION_MODES = {"prospective", "retrospective"}
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
    if "preservation_set" in task:
        _check_string_list(task["preservation_set"], "round.task.preservation_set")

    for field in ("material_delta_refs", "kj_snapshot_refs", "artifacts"):
        if field in data:
            _check_string_list(data[field], f"round.{field}", unique=True)
    _check_string_list(data["residuals"], "round.residuals")
    _check_string_list(data["reopening_conditions"], "round.reopening_conditions")

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

    if data["activation_scope"] == "non_activation" and contacts:
        raise ValidationError("non_activation rounds must not contain framework_contacts")

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
        if "difference_notes" in comparison:
            _check_string_list(
                comparison["difference_notes"], "round.comparison.difference_notes"
            )

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
    _require_nonempty_string(data["summary"], "event.summary")
    _check_string_list(data["evidence_refs"], "event.evidence_refs", nonempty=True, unique=True)
    for field in ("artifact_refs", "framework_refs"):
        if field in data:
            _check_string_list(data[field], f"event.{field}", unique=True)
    for field in ("reopening_condition", "notes"):
        if field in data:
            _require_string(data[field], f"event.{field}")


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
    """Validate identifiers and event-to-round references inside one supplied record set.

    This is intentionally separate from single-record validation: an event file may be
    checked on its own when its round lives elsewhere, while a declared record set is
    expected to be internally connected.
    """
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
