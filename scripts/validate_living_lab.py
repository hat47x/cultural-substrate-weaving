#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

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
    "kj_snapshot_refs",
    "comparison",
    "notes",
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
DEPTHS = {"probe", "preview", "full", "enacted"}
USES = {"exploration", "attribution"}
ACTIVATION_SCOPES = {"non_activation", "limited_use", "exploratory_use"}
ROUND_MODES = {"natural_work", "paired_check"}
INVOCATIONS = {"none", "implicit", "explicit"}
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


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value


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
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{label} must be an ISO-8601 date-time") from exc


def _check_string_list(value: Any, label: str, *, nonempty: bool = False, unique: bool = False) -> None:
    items = _require_list(value, label)
    if nonempty and not items:
        raise ValidationError(f"{label} must contain at least one item")
    for index, item in enumerate(items):
        _require_nonempty_string(item, f"{label}[{index}]")
    if unique and len(items) != len(set(items)):
        raise ValidationError(f"{label} must not contain duplicates")


def validate_round(data: dict[str, Any]) -> None:
    _check_keys(data, ROUND_REQUIRED, ROUND_ALLOWED, "round")
    if data["schema_version"] != "0.1":
        raise ValidationError("round.schema_version must be 0.1")
    round_id = _require_nonempty_string(data["round_id"], "round.round_id")
    if not ID_RE.fullmatch(round_id) or not round_id.startswith("round-"):
        raise ValidationError("round.round_id must start with round-")
    _require_nonempty_string(data["case_id"], "round.case_id")
    _check_enum(data["mode"], ROUND_MODES, "round.mode")
    _check_datetime(data["observed_at"], "round.observed_at")
    _check_enum(data["activation_scope"], ACTIVATION_SCOPES, "round.activation_scope")

    if "invocation" in data:
        _check_enum(data["invocation"], INVOCATIONS, "round.invocation")

    task = _require_object(data["task"], "round.task")
    _require_nonempty_string(task.get("summary"), "round.task.summary")
    if "source_refs" in task:
        _check_string_list(task["source_refs"], "round.task.source_refs", unique=True)
    if "preservation_set" in task:
        _check_string_list(task["preservation_set"], "round.task.preservation_set")

    for field in ("material_delta_refs", "kj_snapshot_refs", "artifacts"):
        if field in data:
            _check_string_list(data[field], f"round.{field}", unique=True)
    _check_string_list(data["residuals"], "round.residuals")
    _check_string_list(data["reopening_conditions"], "round.reopening_conditions")

    contacts = _require_list(data["framework_contacts"], "round.framework_contacts")
    for index, raw in enumerate(contacts):
        contact = _require_object(raw, f"round.framework_contacts[{index}]")
        expected = {"framework", "depth", "use"}
        missing = expected - contact.keys()
        extra = contact.keys() - (expected | {"notes"})
        if missing:
            raise ValidationError(f"framework contact {index} missing: {', '.join(sorted(missing))}")
        if extra:
            raise ValidationError(f"framework contact {index} unknown fields: {', '.join(sorted(extra))}")
        _require_nonempty_string(contact["framework"], f"framework contact {index}.framework")
        _check_enum(contact["depth"], DEPTHS, f"framework contact {index}.depth")
        _check_enum(contact["use"], USES, f"framework contact {index}.use")

    if data["activation_scope"] == "non_activation" and contacts:
        raise ValidationError("non_activation rounds must not contain framework_contacts")

    comparison = data.get("comparison")
    if data["mode"] == "paired_check":
        comparison = _require_object(comparison, "round.comparison")
        _require_nonempty_string(comparison.get("baseline_chat_ref"), "round.comparison.baseline_chat_ref")
        _require_nonempty_string(comparison.get("treatment_chat_ref"), "round.comparison.treatment_chat_ref")
    elif comparison is not None:
        _require_object(comparison, "round.comparison")


def validate_event(data: dict[str, Any]) -> None:
    _check_keys(data, EVENT_REQUIRED, EVENT_ALLOWED, "event")
    if data["schema_version"] != "0.1":
        raise ValidationError("event.schema_version must be 0.1")
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


def validate_record(data: dict[str, Any]) -> str:
    if "event_id" in data:
        validate_event(data)
        return "event"
    if "round_id" in data:
        validate_round(data)
        return "round"
    raise ValidationError("record must contain round_id or event_id")


def load_and_validate(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top level must be an object")
    return validate_record(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Web Chat Living Lab round/event records.")
    parser.add_argument("paths", nargs="*", type=Path, help="JSON records to validate")
    args = parser.parse_args()
    paths = args.paths or [
        ROOT / "evals" / "living-lab-round.example.json",
        ROOT / "evals" / "living-lab-event.example.json",
    ]

    try:
        for path in paths:
            kind = load_and_validate(path)
            print(f"OK {kind}: {path}")
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Living Lab validation failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
