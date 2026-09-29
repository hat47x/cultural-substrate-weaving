from __future__ import annotations

import argparse
import copy
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable

from validate_map import load, validate


SECTIONS = (
    "sources",
    "cards",
    "groups",
    "resonances",
    "relations",
    "narratives",
    "residuals",
    "questions",
)


def _non_empty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _string_list(values: object, label: str) -> list[str]:
    if values is None:
        return []
    if not isinstance(values, list) or not all(
        isinstance(value, str) and value for value in values
    ):
        raise ValueError(f"{label} must be a string list")
    return list(values)


def _section(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.setdefault(key, [])
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"affinity map {key} must be a list of objects")
    return value


def _all_ids(data: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for section in SECTIONS:
        value = data.get(section, [])
        if not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id:
                    found.add(item_id)
    return found


def _require_new_id(data: dict[str, Any], item_id: str) -> None:
    _non_empty(item_id, "id")
    if item_id in _all_ids(data):
        raise ValueError(f"affinity map id already exists: {item_id}")


def _find(data: dict[str, Any], section: str, item_id: str) -> dict[str, Any]:
    for item in _section(data, section):
        if item.get("id") == item_id:
            return item
    raise ValueError(f"{section[:-1]} does not exist: {item_id}")


def _validated(
    edited: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    errors, warnings = validate(edited)
    if errors:
        preview = "; ".join(errors[:3])
        if len(errors) > 3:
            preview += f"; ... ({len(errors)} errors)"
        raise ValueError(f"edited affinity map is invalid: {preview}")
    return edited, warnings


def _edit(
    data: dict[str, Any],
    operation: Callable[[dict[str, Any]], None],
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(data, dict):
        raise ValueError("top-level affinity map must be an object")
    edited = copy.deepcopy(data)
    operation(edited)
    return _validated(edited)


def add_source(
    data: dict[str, Any],
    *,
    source_id: str,
    ref: str,
    provenance: str | None = None,
    discovery_route: str | None = None,
    independence_note: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _require_new_id(edited, source_id)
        item: dict[str, Any] = {
            "id": _non_empty(source_id, "source id"),
            "ref": _non_empty(ref, "source ref"),
        }
        for key, value in (
            ("provenance", provenance),
            ("discovery_route", discovery_route),
            ("independence_note", independence_note),
        ):
            if value is not None:
                item[key] = _non_empty(value, key)
        _section(edited, "sources").append(item)

    return _edit(data, operation)


def add_card(
    data: dict[str, Any],
    *,
    card_id: str,
    text: str,
    source_refs: list[str] | None = None,
    preservation_note: str | None = None,
    derivation_refs: list[str] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _require_new_id(edited, card_id)
        item: dict[str, Any] = {
            "id": _non_empty(card_id, "card id"),
            "text": _non_empty(text, "card text"),
        }
        refs = _string_list(source_refs, "source_refs")
        if refs:
            item["source_refs"] = refs
        derivations = _string_list(derivation_refs, "derivation_refs")
        if derivations:
            item["derivation_refs"] = derivations
        if preservation_note is not None:
            item["preservation_note"] = _non_empty(
                preservation_note,
                "preservation_note",
            )
        _section(edited, "cards").append(item)

    return _edit(data, operation)


def add_group(
    data: dict[str, Any],
    *,
    group_id: str,
    label: str,
    members: list[str] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _require_new_id(edited, group_id)
        item = {
            "id": _non_empty(group_id, "group id"),
            "label": _non_empty(label, "group label"),
            "members": _string_list(members, "group members"),
        }
        _section(edited, "groups").append(item)

    return _edit(data, operation)


def move_card(
    data: dict[str, Any],
    *,
    card_id: str,
    to_group: str,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _find(edited, "cards", _non_empty(card_id, "card id"))
        target = _find(edited, "groups", _non_empty(to_group, "target group id"))

        for group in _section(edited, "groups"):
            members = group.get("members")
            if not isinstance(members, list):
                raise ValueError(
                    f"group {group.get('id', '<unknown>')} members must be a list"
                )
            group["members"] = [
                member for member in members if member != card_id
            ]

        target_members = target.get("members")
        if not isinstance(target_members, list):
            raise ValueError(f"group {to_group} members must be a list")
        if card_id not in target_members:
            target_members.append(card_id)

    return _edit(data, operation)


def add_resonance(
    data: dict[str, Any],
    *,
    resonance_id: str,
    source: str,
    target_group: str,
    note: str,
    display_label: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _require_new_id(edited, resonance_id)
        source_id = _non_empty(source, "resonance source")
        target_id = _non_empty(target_group, "resonance target group")
        group = _find(edited, "groups", target_id)

        semantic_ids = {
            item.get("id")
            for section in ("cards", "groups")
            for item in _section(edited, section)
        }
        if source_id not in semantic_ids:
            raise ValueError(f"resonance source does not exist: {source_id}")

        members = group.get("members")
        if isinstance(members, list) and source_id in members:
            raise ValueError(
                "secondary resonance must not duplicate direct group membership: "
                f"{source_id} -> {target_id}"
            )

        item: dict[str, Any] = {
            "id": _non_empty(resonance_id, "resonance id"),
            "from": source_id,
            "to": target_id,
            "note": _non_empty(note, "resonance note"),
        }
        if display_label is not None:
            item["display_label"] = _non_empty(
                display_label,
                "resonance display_label",
            )
        _section(edited, "resonances").append(item)

    return _edit(data, operation)


def add_question(
    data: dict[str, Any],
    *,
    question_id: str,
    text: str,
    arises_from: list[str] | None = None,
    candidate_relation_between: list[str] | None = None,
    would_clarify_refs: list[str] | None = None,
    handling: str | None = None,
    state: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        _require_new_id(edited, question_id)
        item: dict[str, Any] = {
            "id": _non_empty(question_id, "question id"),
            "text": _non_empty(text, "question text"),
        }
        origins = _string_list(arises_from, "question arises_from")
        if origins:
            item["arises_from"] = origins
        endpoints = _string_list(
            candidate_relation_between,
            "candidate_relation_between",
        )
        if endpoints:
            if len(endpoints) != 2 or endpoints[0] == endpoints[1]:
                raise ValueError(
                    "candidate_relation_between must contain two distinct refs"
                )
            item["candidate_relation_between"] = endpoints
        clarify = _string_list(would_clarify_refs, "would_clarify_refs")
        if clarify:
            item["would_clarify_refs"] = clarify
        if handling is not None:
            item["handling"] = _non_empty(handling, "question handling")
        if state is not None:
            item["state"] = _non_empty(state, "question state")
        _section(edited, "questions").append(item)

    return _edit(data, operation)


def promote_question(
    data: dict[str, Any],
    *,
    question_id: str,
    relation_id: str,
    predicate: str,
    direction: str,
    basis: list[str] | None = None,
    state: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    def operation(edited: dict[str, Any]) -> None:
        question = _find(
            edited,
            "questions",
            _non_empty(question_id, "question id"),
        )
        endpoints = question.get("candidate_relation_between")
        if (
            not isinstance(endpoints, list)
            or len(endpoints) != 2
            or not all(isinstance(value, str) and value for value in endpoints)
            or endpoints[0] == endpoints[1]
        ):
            raise ValueError(
                "question must declare two candidate_relation_between endpoints "
                "before promotion"
            )

        _require_new_id(edited, relation_id)
        if direction not in {"directed", "reciprocal", "unspecified"}:
            raise ValueError(
                "relation direction must be directed, reciprocal, or unspecified"
            )

        item: dict[str, Any] = {
            "id": _non_empty(relation_id, "relation id"),
            "from": endpoints[0],
            "to": endpoints[1],
            "direction": direction,
            "predicate": _non_empty(predicate, "relation predicate"),
        }
        relation_basis = _string_list(basis, "relation basis")
        if relation_basis:
            item["basis"] = relation_basis
        if state is not None:
            item["state"] = _non_empty(state, "relation state")
        _section(edited, "relations").append(item)

        question["state"] = "promoted-after-return-check"
        question["handling"] = f"promoted to {relation_id}"

    return _edit(data, operation)


def write_map(data: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    try:
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Apply explicit, non-inferential edits to an affinity-map JSON file. "
            "Every edit is semantically validated before writing."
        )
    )
    parser.add_argument("input", type=Path)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("-o", "--output", type=Path)
    destination.add_argument("--in-place", action="store_true")

    subparsers = parser.add_subparsers(dest="operation", required=True)

    source = subparsers.add_parser("add-source")
    source.add_argument("--id", required=True)
    source.add_argument("--ref", required=True)
    source.add_argument("--provenance")
    source.add_argument("--discovery-route")
    source.add_argument("--independence-note")

    card = subparsers.add_parser("add-card")
    card.add_argument("--id", required=True)
    card.add_argument("--text", required=True)
    card.add_argument("--source-ref", action="append", default=[])
    card.add_argument("--derivation-ref", action="append", default=[])
    card.add_argument("--preservation-note")

    group = subparsers.add_parser("add-group")
    group.add_argument("--id", required=True)
    group.add_argument("--label", required=True)
    group.add_argument("--member", action="append", default=[])

    move = subparsers.add_parser("move-card")
    move.add_argument("--card", required=True)
    move.add_argument("--to", required=True)

    resonance = subparsers.add_parser("add-resonance")
    resonance.add_argument("--id", required=True)
    resonance.add_argument("--from", dest="source", required=True)
    resonance.add_argument("--to", dest="target_group", required=True)
    resonance.add_argument("--note", required=True)
    resonance.add_argument("--display-label")

    question = subparsers.add_parser("add-question")
    question.add_argument("--id", required=True)
    question.add_argument("--text", required=True)
    question.add_argument("--arises-from", action="append", default=[])
    question.add_argument(
        "--candidate-relation-between",
        nargs=2,
        metavar=("FROM", "TO"),
    )
    question.add_argument("--would-clarify-ref", action="append", default=[])
    question.add_argument("--handling")
    question.add_argument("--state")

    promote = subparsers.add_parser("promote-question")
    promote.add_argument("--question", required=True)
    promote.add_argument("--relation-id", required=True)
    promote.add_argument("--predicate", required=True)
    promote.add_argument(
        "--direction",
        choices=("directed", "reciprocal", "unspecified"),
        required=True,
    )
    promote.add_argument("--basis", action="append", default=[])
    promote.add_argument("--state")

    return parser


def main() -> int:
    parser = _parser()
    args = parser.parse_args()

    try:
        data = load(args.input)
        if args.operation == "add-source":
            edited, warnings = add_source(
                data,
                source_id=args.id,
                ref=args.ref,
                provenance=args.provenance,
                discovery_route=args.discovery_route,
                independence_note=args.independence_note,
            )
        elif args.operation == "add-card":
            edited, warnings = add_card(
                data,
                card_id=args.id,
                text=args.text,
                source_refs=args.source_ref,
                derivation_refs=args.derivation_ref,
                preservation_note=args.preservation_note,
            )
        elif args.operation == "add-group":
            edited, warnings = add_group(
                data,
                group_id=args.id,
                label=args.label,
                members=args.member,
            )
        elif args.operation == "move-card":
            edited, warnings = move_card(
                data,
                card_id=args.card,
                to_group=args.to,
            )
        elif args.operation == "add-resonance":
            edited, warnings = add_resonance(
                data,
                resonance_id=args.id,
                source=args.source,
                target_group=args.target_group,
                note=args.note,
                display_label=args.display_label,
            )
        elif args.operation == "add-question":
            edited, warnings = add_question(
                data,
                question_id=args.id,
                text=args.text,
                arises_from=args.arises_from,
                candidate_relation_between=args.candidate_relation_between,
                would_clarify_refs=args.would_clarify_ref,
                handling=args.handling,
                state=args.state,
            )
        elif args.operation == "promote-question":
            edited, warnings = promote_question(
                data,
                question_id=args.question,
                relation_id=args.relation_id,
                predicate=args.predicate,
                direction=args.direction,
                basis=args.basis,
                state=args.state,
            )
        else:
            parser.error(f"unsupported operation: {args.operation}")

        output = args.input if args.in_place else args.output
        assert isinstance(output, Path)
        write_map(edited, output)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
