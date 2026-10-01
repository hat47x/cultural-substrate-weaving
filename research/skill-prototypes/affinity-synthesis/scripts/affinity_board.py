from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from validate_map import validate


SECTIONS = {
    "source": ("sources", "S"),
    "card": ("cards", "C"),
    "group": ("groups", "G"),
    "resonance": ("resonances", "X"),
    "relation": ("relations", "R"),
    "narrative": ("narratives", "N"),
    "residual": ("residuals", "U"),
    "question": ("questions", "Q"),
}


def load_map(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("top-level affinity map must be an object")
    return value


def save_map(path: Path, data: dict[str, Any]) -> list[str]:
    errors, warnings = validate(data)
    if errors:
        raise ValueError("map would be invalid:\n- " + "\n- ".join(errors))
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return warnings


def objects(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.setdefault(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be an array")
    if any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{key} must contain objects")
    return value


def all_ids(data: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for section, _prefix in SECTIONS.values():
        for item in objects(data, section):
            item_id = str(item.get("id", "")).strip()
            if item_id:
                result.add(item_id)
    return result


def next_id(data: dict[str, Any], kind: str) -> str:
    section, prefix = SECTIONS[kind]
    highest = 0
    for item in objects(data, section):
        item_id = str(item.get("id", ""))
        if item_id.startswith(prefix) and item_id[len(prefix) :].isdigit():
            highest = max(highest, int(item_id[len(prefix) :]))
    return f"{prefix}{highest + 1:03d}"


def choose_id(data: dict[str, Any], kind: str, requested: str | None) -> str:
    item_id = requested.strip() if requested else next_id(data, kind)
    if not item_id:
        raise ValueError("id must not be empty")
    if item_id in all_ids(data):
        raise ValueError(f"id already exists: {item_id}")
    return item_id


def find_item(data: dict[str, Any], kind: str, item_id: str) -> dict[str, Any]:
    section, _prefix = SECTIONS[kind]
    for item in objects(data, section):
        if str(item.get("id", "")) == item_id:
            return item
    raise ValueError(f"{kind} does not exist: {item_id}")


def semantic_nodes(data: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for section in ("cards", "groups")
        for item in objects(data, section)
        if item.get("id")
    }


def positionable_ids(data: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for section in ("cards", "groups", "narratives", "residuals", "questions")
        for item in objects(data, section)
        if item.get("id")
    }


def layout_positions(
    data: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    layout = data.setdefault("layout", {})
    if not isinstance(layout, dict):
        raise ValueError("layout must be an object")
    positions = layout.setdefault("positions", {})
    if not isinstance(positions, dict):
        raise ValueError("layout positions must be an object")
    return layout, positions


def warn_lines(warnings: list[str]) -> None:
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)


def mutate(path: Path, operation) -> None:
    data = load_map(path)
    operation(data)
    warnings = save_map(path, data)
    warn_lines(warnings)


def cmd_init(args: argparse.Namespace) -> None:
    path: Path = args.map
    if path.exists() and not args.force:
        raise ValueError(f"refusing to overwrite existing map: {path}")
    data: dict[str, Any] = {
        "format": "affinity-map",
        "version": "0.1",
        "subject": {
            "question": args.question or "",
            "scope": args.scope or "",
        },
        "sources": [],
        "cards": [],
        "groups": [],
        "resonances": [],
        "relations": [],
        "narratives": [],
        "residuals": [],
        "questions": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    warnings = save_map(path, data)
    warn_lines(warnings)
    print(path)


def cmd_add_source(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item = {
            "id": choose_id(data, "source", args.id),
            "ref": args.ref,
        }
        for key, value in (
            ("provenance", args.provenance),
            ("discovery_route", args.discovery_route),
            ("input_status", args.status),
            ("independence_note", args.independence_note),
        ):
            if value:
                item[key] = value
        objects(data, "sources").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_add_card(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "card", args.id),
            "text": args.text,
        }
        if args.source:
            item["source_refs"] = list(dict.fromkeys(args.source))
        if args.preservation_note:
            item["preservation_note"] = args.preservation_note
        if args.derived_from:
            item["derivation_refs"] = list(dict.fromkeys(args.derived_from))
        if args.status:
            item["input_status"] = args.status
        objects(data, "cards").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_trace_card(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        if not any(
            value is not None
            for value in (
                args.framework,
                args.operation,
                args.location,
                args.yield_kind,
                args.target_response,
                args.target_response_ref,
                args.as_if,
                args.note,
            )
        ):
            raise ValueError(
                "trace-card requires framework, operation, location, yield-kind, target-response, target-response-ref, as-if, or note"
            )

        card = find_item(data, "card", args.card)
        trace = card.setdefault("catalytic_trace", {})
        if not isinstance(trace, dict):
            raise ValueError(
                f"card catalytic_trace must be an object: {args.card}"
            )

        for key, values in (
            ("frameworks", args.framework),
            ("operations", args.operation),
            ("locations", args.location),
            ("yield_kinds", args.yield_kind),
            ("target_responses", args.target_response),
            ("target_response_refs", args.target_response_ref),
        ):
            if values is None:
                continue
            existing = trace.get(key, [])
            if not isinstance(existing, list):
                raise ValueError(
                    f"card catalytic_trace {key} must be an array: {args.card}"
                )
            trace[key] = list(
                dict.fromkeys([str(value) for value in existing] + values)
            )

        if not trace.get("frameworks") or not trace.get("operations"):
            raise ValueError(
                "trace-card requires at least one framework and one operation"
            )
        if trace.get("target_response_refs") and not trace.get("target_responses"):
            raise ValueError(
                "target-response-ref requires at least one target-response"
            )

        if args.as_if is not None:
            trace["as_if"] = args.as_if
        if args.note is not None:
            trace["note"] = args.note

        print(args.card)

    mutate(args.map, op)


def cmd_audit_return(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        card = find_item(data, "card", args.card)
        if str(card.get("input_status", "")) != "framework_generated":
            raise ValueError(
                f"audit-return requires input_status=framework_generated: {args.card}"
            )

        trace = card.get("catalytic_trace")
        if not (
            isinstance(trace, dict)
            and trace.get("frameworks")
            and trace.get("operations")
        ):
            raise ValueError(
                f"audit-return requires a complete catalytic trace first: {args.card}"
            )

        audits = trace.setdefault("target_return_audits", [])
        if not isinstance(audits, list):
            raise ValueError(
                f"card catalytic target_return_audits must be an array: {args.card}"
            )

        audit: dict[str, Any] = {
            "state": args.state,
            "basis_refs": list(dict.fromkeys(args.basis_ref)),
        }
        if args.note:
            audit["note"] = args.note
        if args.next_check:
            audit["next_checks"] = list(dict.fromkeys(args.next_check))
        audits.append(audit)
        print(args.card)

    mutate(args.map, op)


def cmd_trace_cross_field(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        card = find_item(data, "card", args.card)
        if str(card.get("input_status", "")) != "cross_field_emergent":
            raise ValueError(
                f"cross-field trace requires input_status=cross_field_emergent: {args.card}"
            )

        trace = card.setdefault("cross_field_trace", {})
        if not isinstance(trace, dict):
            raise ValueError(
                f"card cross_field_trace must be an object: {args.card}"
            )

        for key, values in (
            ("target_refs", args.target_ref),
            ("framework_refs", args.framework_ref),
            ("preserved_from_target", args.preserved_target),
            ("preserved_from_framework", args.preserved_framework),
            ("negated_or_revised", args.negated_or_revised),
            ("newly_recomposed", args.newly_recomposed),
        ):
            if values is None:
                continue
            existing = trace.get(key, [])
            if not isinstance(existing, list):
                raise ValueError(
                    f"card cross_field_trace {key} must be an array: {args.card}"
                )
            trace[key] = list(
                dict.fromkeys([str(value) for value in existing] + values)
            )

        if not trace.get("target_refs") or not trace.get("framework_refs"):
            raise ValueError(
                "trace-cross-field requires at least one target-ref and one framework-ref"
            )

        if args.note is not None:
            trace["note"] = args.note

        print(args.card)

    mutate(args.map, op)


def cmd_add_group(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "group", args.id),
            "label": args.label,
            "members": list(dict.fromkeys(args.member or [])),
        }
        if args.display_label:
            item["display_label"] = args.display_label
        if args.preserved_difference:
            item["preserved_differences"] = list(args.preserved_difference)
        objects(data, "groups").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_audit_group(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        group = find_item(data, "group", args.group)
        updates = {
            "inherited": args.inherited,
            "emergent": args.emergent,
            "residual": args.residual,
        }
        if (
            not any(values is not None for values in updates.values())
            and args.preserved_difference is None
        ):
            raise ValueError(
                "audit-group requires at least one transformation audit "
                "or preserved difference"
            )

        audit_updates = {
            key: values
            for key, values in updates.items()
            if values is not None
        }
        if audit_updates:
            audit = group.setdefault("transformation_audit", {})
            if not isinstance(audit, dict):
                raise ValueError(
                    f"group {args.group} transformation_audit must be an object"
                )
            for key, values in audit_updates.items():
                audit[key] = list(dict.fromkeys(values))

        if args.preserved_difference is not None:
            group["preserved_differences"] = list(
                dict.fromkeys(args.preserved_difference)
            )

    mutate(args.map, op)


def cmd_group_add(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        group = find_item(data, "group", args.group)
        members = group.setdefault("members", [])
        for ref in args.member:
            if ref in members:
                raise ValueError(f"{ref} is already a member of {args.group}")
            members.append(ref)

    mutate(args.map, op)


def cmd_group_remove(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        group = find_item(data, "group", args.group)
        members = group.setdefault("members", [])
        for ref in args.member:
            if ref not in members:
                raise ValueError(f"{ref} is not a member of {args.group}")
        group["members"] = [ref for ref in members if ref not in set(args.member)]

    mutate(args.map, op)


def cmd_move_card(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        find_item(data, "card", args.card)
        target = find_item(data, "group", args.to)
        for group in objects(data, "groups"):
            members = list(group.get("members", []))
            if args.card in members:
                group["members"] = [ref for ref in members if ref != args.card]
        target_members = target.setdefault("members", [])
        if args.card not in target_members:
            target_members.append(args.card)

    mutate(args.map, op)


def cmd_add_resonance(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "resonance", args.id),
            "from": args.source,
            "to": args.to,
            "note": args.note,
        }
        objects(data, "resonances").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_add_relation(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        nodes = semantic_nodes(data)
        for ref in (args.source, args.to):
            if ref not in nodes:
                raise ValueError(f"relation endpoint is not a card/group: {ref}")
        item: dict[str, Any] = {
            "id": choose_id(data, "relation", args.id),
            "from": args.source,
            "to": args.to,
            "direction": args.direction,
            "predicate": args.predicate,
        }
        if args.state:
            item["state"] = args.state
        if args.basis:
            item["basis"] = list(dict.fromkeys(args.basis))
        objects(data, "relations").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_add_narrative(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "narrative", args.id),
            "text": args.text,
        }
        if args.basis:
            item["basis"] = list(dict.fromkeys(args.basis))
        if args.state:
            item["state"] = args.state
        if args.display_label:
            item["display_label"] = args.display_label

        audit: dict[str, list[str]] = {}
        for key, values in (
            ("inherited", args.inherited),
            ("emergent", args.emergent),
            ("residual", args.residual),
        ):
            if values:
                audit[key] = list(dict.fromkeys(values))
        if audit:
            item["transformation_audit"] = audit

        objects(data, "narratives").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_add_residual(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "residual", args.id),
            "text": args.text,
        }
        if args.ref:
            item["refs"] = list(dict.fromkeys(args.ref))
        if args.handling:
            item["handling"] = args.handling
        objects(data, "residuals").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_add_question(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        item: dict[str, Any] = {
            "id": choose_id(data, "question", args.id),
            "text": args.text,
        }
        if args.arises_from:
            item["arises_from"] = list(dict.fromkeys(args.arises_from))
        if args.between:
            item["candidate_relation_between"] = args.between
        if args.would_clarify:
            item["would_clarify_refs"] = list(dict.fromkeys(args.would_clarify))
        if args.handling:
            item["handling"] = args.handling
        if args.state:
            item["state"] = args.state
        objects(data, "questions").append(item)
        print(item["id"])

    mutate(args.map, op)


def cmd_promote_question(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        question = find_item(data, "question", args.question)
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

        nodes = semantic_nodes(data)
        for ref in endpoints:
            if ref not in nodes:
                raise ValueError(
                    f"question candidate relation endpoint is not a card/group: {ref}"
                )

        relation_id = choose_id(data, "relation", args.id)
        relation: dict[str, Any] = {
            "id": relation_id,
            "from": endpoints[0],
            "to": endpoints[1],
            "direction": args.direction,
            "predicate": args.predicate,
        }
        if args.basis:
            relation["basis"] = list(dict.fromkeys(args.basis))
        if args.state:
            relation["state"] = args.state

        objects(data, "relations").append(relation)
        question["state"] = "promoted-after-return-check"
        question["handling"] = f"promoted to {relation_id}"
        print(relation_id)

    mutate(args.map, op)


def cmd_revise_relation(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        relation = find_item(data, "relation", args.relation)
        relation["predicate"] = args.predicate
        relation["direction"] = args.direction
        if args.basis is not None:
            if args.basis:
                relation["basis"] = list(dict.fromkeys(args.basis))
            else:
                relation.pop("basis", None)
        if args.state:
            relation["state"] = args.state
        if args.note:
            relation["note"] = args.note

    mutate(args.map, op)


def cmd_demote_relation(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        relation = find_item(data, "relation", args.relation)
        source = relation.get("from")
        target = relation.get("to")
        predicate = relation.get("predicate")
        if not isinstance(source, str) or not source:
            raise ValueError(f"relation source is invalid: {args.relation}")
        if not isinstance(target, str) or not target:
            raise ValueError(f"relation target is invalid: {args.relation}")
        if not isinstance(predicate, str) or not predicate.strip():
            raise ValueError(f"relation predicate is invalid: {args.relation}")

        question_id = choose_id(data, "question", args.id)
        question: dict[str, Any] = {
            "id": question_id,
            "text": args.text,
            "arises_from": [source, target],
            "candidate_relation_between": [source, target],
            "handling": (
                args.handling
                or (
                    f"demoted from {args.relation} after return-check; "
                    f"prior predicate: {predicate}"
                )
            ),
            "state": args.state or "unresolved",
        }
        if args.would_clarify:
            question["would_clarify_refs"] = list(
                dict.fromkeys(args.would_clarify)
            )

        objects(data, "relations").remove(relation)
        for prior_question in objects(data, "questions"):
            if prior_question.get("handling") == f"promoted to {args.relation}":
                prior_question["state"] = "relation-demoted-after-return-check"
                prior_question["handling"] = (
                    f"relation {args.relation} demoted to {question_id} "
                    "after return-check"
                )
        objects(data, "questions").append(question)
        print(question_id)

    mutate(args.map, op)


def cmd_update_handoff(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        updates = {
            "semantic_refs": args.semantic_ref,
            "residual_refs": args.residual_ref,
            "source_refs_to_preserve": args.source_ref,
            "do_not_assume": args.do_not_assume,
        }
        if not any(value is not None for value in updates.values()):
            raise ValueError(
                "update-handoff requires at least one handoff field"
            )

        handoff = data.setdefault("handoff", {})
        if not isinstance(handoff, dict):
            raise ValueError("handoff must be an object")
        for key, values in updates.items():
            if values is not None:
                handoff[key] = list(dict.fromkeys(values))

    mutate(args.map, op)


def cmd_handoff_add_check(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        handoff = data.setdefault("handoff", {})
        if not isinstance(handoff, dict):
            raise ValueError("handoff must be an object")
        candidates = handoff.setdefault("next_check_candidates", [])
        if not isinstance(candidates, list):
            raise ValueError("handoff next_check_candidates must be an array")

        item: dict[str, Any] = {"text": args.text}
        if args.ref:
            item["refs"] = list(dict.fromkeys(args.ref))
        if args.status:
            item["status"] = args.status
        candidates.append(item)

    mutate(args.map, op)


def cmd_set_position(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        if args.ref not in positionable_ids(data):
            raise ValueError(
                "layout position ref must resolve to card/group/narrative/residual/question: "
                f"{args.ref}"
            )
        if not 0 <= args.x <= 1 or not 0 <= args.y <= 1:
            raise ValueError("layout coordinates must be between 0 and 1")
        layout, positions = layout_positions(data)
        positions[args.ref] = {"x": args.x, "y": args.y}
        if args.projection:
            layout["projection"] = args.projection

    mutate(args.map, op)


def cmd_clear_position(args: argparse.Namespace) -> None:
    def op(data: dict[str, Any]) -> None:
        _layout, positions = layout_positions(data)
        if args.ref not in positions:
            raise ValueError(f"layout position does not exist: {args.ref}")
        del positions[args.ref]

    mutate(args.map, op)


def focus_payload(data: dict[str, Any], ref: str) -> dict[str, Any]:
    matches: list[tuple[str, dict[str, Any]]] = []
    for candidate_kind, (section, _prefix) in SECTIONS.items():
        for item in objects(data, section):
            if str(item.get("id", "")) == ref:
                matches.append((candidate_kind, item))

    if not matches:
        raise ValueError(f"semantic ref does not exist: {ref}")
    if len(matches) > 1:
        namespaces = ", ".join(kind for kind, _item in matches)
        raise ValueError(
            f"semantic ref is ambiguous across namespaces: {ref} ({namespaces})"
        )

    kind, artifact = matches[0]

    member_of_groups = [
        str(group.get("id"))
        for group in objects(data, "groups")
        if ref in [str(member) for member in group.get("members", [])]
    ]
    endpoint_relations = [
        item
        for item in objects(data, "relations")
        if ref in {str(item.get("from", "")), str(item.get("to", ""))}
    ]
    basis_relations = [
        item
        for item in objects(data, "relations")
        if ref in [str(value) for value in item.get("basis", [])]
        and item not in endpoint_relations
    ]
    resonances = [
        item
        for item in objects(data, "resonances")
        if ref in {str(item.get("from", "")), str(item.get("to", ""))}
    ]
    narratives = [
        item
        for item in objects(data, "narratives")
        if ref in [str(value) for value in item.get("basis", [])]
    ]
    residuals = [
        item
        for item in objects(data, "residuals")
        if ref in [str(value) for value in item.get("refs", [])]
    ]
    questions = [
        item
        for item in objects(data, "questions")
        if (
            ref in [str(value) for value in item.get("arises_from", [])]
            or ref in [
                str(value)
                for value in item.get("candidate_relation_between", [])
            ]
            or ref in [
                str(value)
                for value in item.get("would_clarify_refs", [])
            ]
        )
    ]
    cross_field_cards = [
        card
        for card in objects(data, "cards")
        if isinstance(card.get("cross_field_trace"), dict)
        and (
            ref in [
                str(value)
                for value in card["cross_field_trace"].get("target_refs", [])
            ]
            or ref in [
                str(value)
                for value in card["cross_field_trace"].get("framework_refs", [])
            ]
        )
    ]

    target_return_audits: list[dict[str, Any]] = []
    if kind == "card":
        catalytic_trace = artifact.get("catalytic_trace")
        if isinstance(catalytic_trace, dict):
            audits = catalytic_trace.get("target_return_audits", [])
            if isinstance(audits, list):
                target_return_audits = [
                    item for item in audits if isinstance(item, dict)
                ]

    source_refs: list[str] = []
    sources: list[dict[str, Any]] = []
    cards_from_source: list[dict[str, Any]] = []
    if kind == "card":
        source_refs = [str(value) for value in artifact.get("source_refs", [])]
        source_ref_set = set(source_refs)
        sources = [
            item
            for item in objects(data, "sources")
            if str(item.get("id", "")) in source_ref_set
        ]
    elif kind == "source":
        cards_from_source = [
            item
            for item in objects(data, "cards")
            if ref in [str(value) for value in item.get("source_refs", [])]
        ]

    handoff_context: dict[str, Any] = {
        "semantic_ref": False,
        "residual_ref": False,
        "source_ref_to_preserve": False,
        "next_check_candidates": [],
        "do_not_assume": [],
    }
    handoff = data.get("handoff")
    if isinstance(handoff, dict):
        semantic_refs = handoff.get("semantic_refs", [])
        residual_refs = handoff.get("residual_refs", [])
        source_refs_to_preserve = handoff.get("source_refs_to_preserve", [])
        candidates = handoff.get("next_check_candidates", [])
        if isinstance(semantic_refs, list):
            handoff_context["semantic_ref"] = ref in [
                str(value) for value in semantic_refs
            ]
        if isinstance(residual_refs, list):
            handoff_context["residual_ref"] = ref in [
                str(value) for value in residual_refs
            ]
        if isinstance(source_refs_to_preserve, list):
            handoff_context["source_ref_to_preserve"] = ref in [
                str(value) for value in source_refs_to_preserve
            ]
        if isinstance(candidates, list):
            handoff_context["next_check_candidates"] = [
                candidate
                for candidate in candidates
                if isinstance(candidate, dict)
                and ref in [
                    str(value)
                    for value in candidate.get("refs", [])
                ]
            ]

        is_locally_carried = bool(
            handoff_context["semantic_ref"]
            or handoff_context["residual_ref"]
            or handoff_context["source_ref_to_preserve"]
            or handoff_context["next_check_candidates"]
        )
        guardrails = handoff.get("do_not_assume", [])
        if is_locally_carried and isinstance(guardrails, list):
            handoff_context["do_not_assume"] = [
                str(value)
                for value in guardrails
                if isinstance(value, str)
            ]

    layout_position = None
    layout = data.get("layout")
    if isinstance(layout, dict):
        positions = layout.get("positions")
        if isinstance(positions, dict):
            position = positions.get(ref)
            if isinstance(position, dict):
                layout_position = position

    return {
        "ref": ref,
        "kind": kind,
        "artifact": artifact,
        "member_of_groups": member_of_groups,
        "endpoint_relations": endpoint_relations,
        "basis_relations": basis_relations,
        "resonances": resonances,
        "narratives": narratives,
        "residuals": residuals,
        "questions": questions,
        "cross_field_cards": cross_field_cards,
        "source_refs": source_refs,
        "sources": sources,
        "cards_from_source": cards_from_source,
        "target_return_audits": target_return_audits,
        "handoff": handoff_context,
        "layout_position": layout_position,
    }


def cmd_focus(args: argparse.Namespace) -> None:
    data = load_map(args.map)
    errors, warnings = validate(data)
    if errors:
        raise ValueError("map is invalid:\n- " + "\n- ".join(errors))
    warn_lines(warnings)
    print(
        json.dumps(
            focus_payload(data, args.ref),
            ensure_ascii=False,
            indent=2,
        )
    )


def _items_by_id(data: dict[str, Any], section: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in objects(data, section):
        item_id = str(item.get("id", "")).strip()
        if item_id:
            result[item_id] = item
    return result


def _changed_fields(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    keys = (set(before) | set(after)) - {"id"}
    return sorted(key for key in keys if before.get(key) != after.get(key))


def diff_payload(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    total_added = 0
    total_removed = 0
    total_changed = 0

    for kind, (section, _prefix) in SECTIONS.items():
        before_items = _items_by_id(before, section)
        after_items = _items_by_id(after, section)
        before_ids = set(before_items)
        after_ids = set(after_items)
        added = sorted(after_ids - before_ids)
        removed = sorted(before_ids - after_ids)
        changed: dict[str, Any] = {}

        for item_id in sorted(before_ids & after_ids):
            old = before_items[item_id]
            new = after_items[item_id]
            if old == new:
                continue
            detail: dict[str, Any] = {"fields": _changed_fields(old, new)}
            if kind == "group" and old.get("members") != new.get("members"):
                old_members = [str(value) for value in old.get("members", [])]
                new_members = [str(value) for value in new.get("members", [])]
                detail["members_added"] = [
                    value for value in new_members if value not in old_members
                ]
                detail["members_removed"] = [
                    value for value in old_members if value not in new_members
                ]
                detail["member_order_changed"] = (
                    set(old_members) == set(new_members)
                    and old_members != new_members
                )
            changed[item_id] = detail

        sections[kind] = {
            "added": added,
            "removed": removed,
            "changed": changed,
        }
        total_added += len(added)
        total_removed += len(removed)
        total_changed += len(changed)

    before_layout = before.get("layout")
    after_layout = after.get("layout")
    before_positions = (
        before_layout.get("positions", {})
        if isinstance(before_layout, dict)
        and isinstance(before_layout.get("positions", {}), dict)
        else {}
    )
    after_positions = (
        after_layout.get("positions", {})
        if isinstance(after_layout, dict)
        and isinstance(after_layout.get("positions", {}), dict)
        else {}
    )
    layout_refs = set(before_positions) | set(after_positions)

    return {
        "format": "affinity-map-diff",
        "version": "0.1",
        "sections": sections,
        "subject_changed": before.get("subject") != after.get("subject"),
        "handoff_changed": before.get("handoff") != after.get("handoff"),
        "representation": {
            "layout_changed": before_layout != after_layout,
            "layout_changed_refs": sorted(
                ref
                for ref in layout_refs
                if before_positions.get(ref) != after_positions.get(ref)
            ),
        },
        "summary": {
            "added": total_added,
            "removed": total_removed,
            "changed": total_changed,
        },
        "interpretation_boundary": (
            "This is a mechanical stable-ID/field diff. It does not decide whether "
            "a wording change is semantic, whether an untouched artifact was checked, "
            "or whether a changed field is justified by the material."
        ),
    }


def cmd_diff(args: argparse.Namespace) -> None:
    before = load_map(args.before)
    after = load_map(args.after)
    before_errors, before_warnings = validate(before)
    after_errors, after_warnings = validate(after)
    if before_errors:
        raise ValueError("before map is invalid:\n- " + "\n- ".join(before_errors))
    if after_errors:
        raise ValueError("after map is invalid:\n- " + "\n- ".join(after_errors))
    warn_lines([f"before: {warning}" for warning in before_warnings])
    warn_lines([f"after: {warning}" for warning in after_warnings])
    print(json.dumps(diff_payload(before, after), ensure_ascii=False, indent=2))


def status_payload(data: dict[str, Any]) -> dict[str, Any]:
    cards = objects(data, "cards")
    groups = objects(data, "groups")
    memberships: Counter[str] = Counter()
    for group in groups:
        for member in group.get("members", []):
            if str(member).startswith("C"):
                memberships[str(member)] += 1

    card_ids = [str(card.get("id")) for card in cards if card.get("id")]
    source_statuses = Counter(
        str(item.get("input_status", "")).strip() or "(unspecified)"
        for item in objects(data, "sources")
    )
    card_statuses = Counter(
        str(item.get("input_status", "")).strip() or "(unspecified)"
        for item in cards
    )
    traced_cards = [
        card
        for card in cards
        if isinstance(card.get("catalytic_trace"), dict)
        and bool(card["catalytic_trace"].get("frameworks"))
        and bool(card["catalytic_trace"].get("operations"))
    ]
    framework_counts: Counter[str] = Counter()
    operation_counts: Counter[str] = Counter()
    yield_kind_counts: Counter[str] = Counter()
    target_response_counts: Counter[str] = Counter()
    for card in traced_cards:
        trace = card["catalytic_trace"]
        for framework in trace.get("frameworks", []):
            framework_counts[str(framework)] += 1
        for operation in trace.get("operations", []):
            operation_counts[str(operation)] += 1
        for yield_kind in trace.get("yield_kinds", []):
            yield_kind_counts[str(yield_kind)] += 1
        for target_response in trace.get("target_responses", []):
            target_response_counts[str(target_response)] += 1
    untraced_framework_generated = [
        str(card.get("id"))
        for card in cards
        if card.get("id")
        and str(card.get("input_status", "")) == "framework_generated"
        and not (
            isinstance(card.get("catalytic_trace"), dict)
            and bool(card["catalytic_trace"].get("frameworks"))
            and bool(card["catalytic_trace"].get("operations"))
        )
    ]
    framework_generated_without_yield_kind = [
        str(card.get("id"))
        for card in cards
        if card.get("id")
        and str(card.get("input_status", "")) == "framework_generated"
        and isinstance(card.get("catalytic_trace"), dict)
        and bool(card["catalytic_trace"].get("frameworks"))
        and bool(card["catalytic_trace"].get("operations"))
        and not bool(card["catalytic_trace"].get("yield_kinds"))
    ]
    target_response_without_refs = [
        str(card.get("id"))
        for card in traced_cards
        if card.get("id")
        and bool(card["catalytic_trace"].get("target_responses"))
        and not bool(card["catalytic_trace"].get("target_response_refs"))
    ]
    target_return_state_counts: Counter[str] = Counter()
    for card in traced_cards:
        audits = card["catalytic_trace"].get("target_return_audits", [])
        if isinstance(audits, list):
            for audit in audits:
                if isinstance(audit, dict):
                    state = str(audit.get("state", "")).strip()
                    if state:
                        target_return_state_counts[state] += 1
    framework_generated_without_return_audit = [
        str(card.get("id"))
        for card in traced_cards
        if card.get("id")
        and str(card.get("input_status", "")) == "framework_generated"
        and not bool(card["catalytic_trace"].get("target_return_audits"))
    ]
    cross_field_traced = [
        card
        for card in cards
        if str(card.get("input_status", "")) == "cross_field_emergent"
        and isinstance(card.get("cross_field_trace"), dict)
        and bool(card["cross_field_trace"].get("target_refs"))
        and bool(card["cross_field_trace"].get("framework_refs"))
    ]
    untraced_cross_field = [
        str(card.get("id"))
        for card in cards
        if card.get("id")
        and str(card.get("input_status", "")) == "cross_field_emergent"
        and card not in cross_field_traced
    ]

    return {
        "format": data.get("format"),
        "version": data.get("version"),
        "input_status_counts": {
            "sources": dict(sorted(source_statuses.items())),
            "cards": dict(sorted(card_statuses.items())),
        },
        "catalytic_trace": {
            "traced_cards": len(traced_cards),
            "frameworks": dict(sorted(framework_counts.items())),
            "operations": dict(sorted(operation_counts.items())),
            "yield_kinds": dict(sorted(yield_kind_counts.items())),
            "target_responses": dict(sorted(target_response_counts.items())),
            "untraced_framework_generated_cards": untraced_framework_generated,
            "framework_generated_cards_without_yield_kind": (
                framework_generated_without_yield_kind
            ),
            "target_response_cards_without_refs": target_response_without_refs,
            "target_return_states": dict(sorted(target_return_state_counts.items())),
            "framework_generated_cards_without_return_audit": (
                framework_generated_without_return_audit
            ),
        },
        "cross_field_trace": {
            "traced_cards": len(cross_field_traced),
            "untraced_cross_field_emergent_cards": untraced_cross_field,
        },
        "counts": {
            key: len(objects(data, section))
            for key, (section, _prefix) in SECTIONS.items()
        },
        "ungrouped_cards": [cid for cid in card_ids if memberships[cid] == 0],
        "multiply_grouped_cards": [cid for cid in card_ids if memberships[cid] > 1],
        "singleton_groups": [
            str(group.get("id"))
            for group in groups
            if len(group.get("members", [])) == 1
        ],
        "groups_without_transformation_audit": [
            str(group.get("id"))
            for group in groups
            if group.get("id")
            and not (
                isinstance(group.get("transformation_audit"), dict)
                and any(
                    isinstance(group["transformation_audit"].get(key), list)
                    and bool(group["transformation_audit"].get(key))
                    for key in ("inherited", "emergent", "residual")
                )
            )
        ],
        "narrative_refs": [
            str(item.get("id"))
            for item in objects(data, "narratives")
            if item.get("id")
        ],
        "residual_refs": [
            str(item.get("id"))
            for item in objects(data, "residuals")
            if item.get("id")
        ],
        "question_refs": [
            str(item.get("id"))
            for item in objects(data, "questions")
            if item.get("id")
        ],
        "layout": (
            {
                "present": True,
                "projection": data["layout"].get("projection"),
                "position_count": len(data["layout"].get("positions", {}))
                if isinstance(data["layout"].get("positions", {}), dict)
                else 0,
            }
            if isinstance(data.get("layout"), dict)
            else {"present": False}
        ),
        "handoff": (
            {
                "present": True,
                "semantic_refs": len(data["handoff"].get("semantic_refs", [])),
                "residual_refs": len(data["handoff"].get("residual_refs", [])),
                "source_refs_to_preserve": len(
                    data["handoff"].get("source_refs_to_preserve", [])
                ),
                "next_check_candidates": len(
                    data["handoff"].get("next_check_candidates", [])
                ),
                "do_not_assume": len(data["handoff"].get("do_not_assume", [])),
            }
            if isinstance(data.get("handoff"), dict)
            else {"present": False}
        ),
    }


def cmd_status(args: argparse.Namespace) -> None:
    data = load_map(args.map)
    errors, warnings = validate(data)
    payload = status_payload(data)
    payload["validation"] = {
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    counts = payload["counts"]
    print(
        " ".join(
            f"{name}={counts[name]}"
            for name in (
                "source",
                "card",
                "group",
                "resonance",
                "relation",
                "narrative",
                "residual",
                "question",
            )
        )
    )
    print("ungrouped:", ", ".join(payload["ungrouped_cards"]) or "-")
    print("multi-membership:", ", ".join(payload["multiply_grouped_cards"]) or "-")
    print("singleton-groups:", ", ".join(payload["singleton_groups"]) or "-")
    print(
        "group-audit-missing:",
        ", ".join(payload["groups_without_transformation_audit"]) or "-",
    )
    print("narratives:", ", ".join(payload["narrative_refs"]) or "-")
    print("residuals:", ", ".join(payload["residual_refs"]) or "-")
    print("questions:", ", ".join(payload["question_refs"]) or "-")
    layout = payload["layout"]
    if layout["present"]:
        print(
            "layout:",
            f"projection={layout['projection'] or '-'} "
            f"positions={layout['position_count']}",
        )
    else:
        print("layout: -")
    handoff = payload["handoff"]
    if handoff["present"]:
        print(
            "handoff:",
            " ".join(
                f"{key}={handoff[key]}"
                for key in (
                    "semantic_refs",
                    "residual_refs",
                    "source_refs_to_preserve",
                    "next_check_candidates",
                    "do_not_assume",
                )
            ),
        )
    else:
        print("handoff: -")
    source_status = payload["input_status_counts"]["sources"]
    card_status = payload["input_status_counts"]["cards"]
    print(
        "source-status:",
        ", ".join(f"{key}={value}" for key, value in source_status.items()) or "-",
    )
    print(
        "card-status:",
        ", ".join(f"{key}={value}" for key, value in card_status.items()) or "-",
    )
    catalytic = payload["catalytic_trace"]
    print(
        "catalytic-trace:",
        f"cards={catalytic['traced_cards']} "
        f"frameworks={len(catalytic['frameworks'])} "
        f"operations={len(catalytic['operations'])}",
    )
    print(
        "catalytic-untraced-framework-generated:",
        ", ".join(catalytic["untraced_framework_generated_cards"]) or "-",
    )
    print(
        "catalytic-return-states:",
        ", ".join(
            f"{key}={value}"
            for key, value in catalytic["target_return_states"].items()
        )
        or "-",
    )
    print(
        "catalytic-return-pending:",
        ", ".join(catalytic["framework_generated_cards_without_return_audit"])
        or "-",
    )
    print(
        "catalytic-yield-kinds:",
        ", ".join(
            f"{key}={value}"
            for key, value in catalytic["yield_kinds"].items()
        )
        or "-",
    )
    print(
        "catalytic-target-responses:",
        ", ".join(
            f"{key}={value}"
            for key, value in catalytic["target_responses"].items()
        )
        or "-",
    )
    print(
        "catalytic-framework-generated-without-yield-kind:",
        ", ".join(
            catalytic["framework_generated_cards_without_yield_kind"]
        )
        or "-",
    )
    print(
        "catalytic-target-response-without-refs:",
        ", ".join(catalytic["target_response_cards_without_refs"]) or "-",
    )
    cross_field = payload["cross_field_trace"]
    print(
        "cross-field-trace:",
        f"cards={cross_field['traced_cards']}",
    )
    print(
        "cross-field-untraced:",
        ", ".join(cross_field["untraced_cross_field_emergent_cards"]) or "-",
    )
    print(f"validation: errors={len(errors)} warnings={len(warnings)}")


def add_common_id(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--id")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Explicitly manage an affinity-map working board without inferring "
            "grouping or semantic relations."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create an empty affinity-map working board")
    init.add_argument("map", type=Path)
    init.add_argument("--question")
    init.add_argument("--scope")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    source = sub.add_parser("add-source", help="register a source/provenance handle")
    source.add_argument("map", type=Path)
    add_common_id(source)
    source.add_argument("--ref", required=True)
    source.add_argument("--provenance")
    source.add_argument("--discovery-route")
    source.add_argument("--status")
    source.add_argument("--independence-note")
    source.set_defaults(func=cmd_add_source)

    card = sub.add_parser("add-card", help="add one meaning-bearing card")
    card.add_argument("map", type=Path)
    add_common_id(card)
    card.add_argument("text")
    card.add_argument("--source", action="append")
    card.add_argument("--status")
    card.add_argument("--preservation-note")
    card.add_argument("--derived-from", action="append")
    card.set_defaults(func=cmd_add_card)

    trace_card = sub.add_parser(
        "trace-card",
        help=(
            "attach cultural-framework catalytic provenance to a card without "
            "changing grouping or epistemic status"
        ),
    )
    trace_card.add_argument("map", type=Path)
    trace_card.add_argument("card")
    trace_card.add_argument("--framework", action="append", default=None)
    trace_card.add_argument("--operation", action="append", default=None)
    trace_card.add_argument("--location", action="append", default=None)
    trace_card.add_argument("--yield-kind", action="append", default=None)
    trace_card.add_argument("--target-response", action="append", default=None)
    trace_card.add_argument("--target-response-ref", action="append", default=None)
    trace_card.add_argument("--as-if")
    trace_card.add_argument("--note")
    trace_card.set_defaults(func=cmd_trace_card)

    audit_return = sub.add_parser(
        "audit-return",
        help=(
            "append a target-return audit to a traced framework-generated card "
            "without changing its epistemic status or synthesis authority"
        ),
    )
    audit_return.add_argument("map", type=Path)
    audit_return.add_argument("card")
    audit_return.add_argument("--state", required=True)
    audit_return.add_argument("--basis-ref", action="append", required=True)
    audit_return.add_argument("--note")
    audit_return.add_argument("--next-check", action="append", default=None)
    audit_return.set_defaults(func=cmd_audit_return)

    trace_cross_field = sub.add_parser(
        "trace-cross-field",
        help=(
            "preserve target/framework lineage for a cross_field_emergent card "
            "without promoting it to a privileged synthesis"
        ),
    )
    trace_cross_field.add_argument("map", type=Path)
    trace_cross_field.add_argument("card")
    trace_cross_field.add_argument("--target-ref", action="append", default=None)
    trace_cross_field.add_argument("--framework-ref", action="append", default=None)
    trace_cross_field.add_argument("--preserved-target", action="append", default=None)
    trace_cross_field.add_argument("--preserved-framework", action="append", default=None)
    trace_cross_field.add_argument("--negated-or-revised", action="append", default=None)
    trace_cross_field.add_argument("--newly-recomposed", action="append", default=None)
    trace_cross_field.add_argument("--note")
    trace_cross_field.set_defaults(func=cmd_trace_cross_field)

    group = sub.add_parser("add-group", help="create an explicit group")
    group.add_argument("map", type=Path)
    add_common_id(group)
    group.add_argument("--label", required=True)
    group.add_argument("--display-label")
    group.add_argument("--member", action="append")
    group.add_argument("--preserved-difference", action="append")
    group.set_defaults(func=cmd_add_group)

    audit_group = sub.add_parser(
        "audit-group",
        help=(
            "record inherited/emergent/residual transformation audit after grouping"
        ),
    )
    audit_group.add_argument("map", type=Path)
    audit_group.add_argument("group")
    audit_group.add_argument("--inherited", action="append", default=None)
    audit_group.add_argument("--emergent", action="append", default=None)
    audit_group.add_argument("--residual", action="append", default=None)
    audit_group.add_argument(
        "--preserved-difference",
        action="append",
        default=None,
    )
    audit_group.set_defaults(func=cmd_audit_group)

    group_add = sub.add_parser("group-add", help="add explicit members to a group")
    group_add.add_argument("map", type=Path)
    group_add.add_argument("group")
    group_add.add_argument("member", nargs="+")
    group_add.set_defaults(func=cmd_group_add)

    group_remove = sub.add_parser("group-remove", help="remove explicit members from a group")
    group_remove.add_argument("map", type=Path)
    group_remove.add_argument("group")
    group_remove.add_argument("member", nargs="+")
    group_remove.set_defaults(func=cmd_group_remove)

    move_card = sub.add_parser(
        "move-card",
        help="move one card to one primary group by removing its other direct memberships",
    )
    move_card.add_argument("map", type=Path)
    move_card.add_argument("card")
    move_card.add_argument("--to", required=True)
    move_card.set_defaults(func=cmd_move_card)

    resonance = sub.add_parser(
        "add-resonance",
        help="record secondary resonance without changing membership",
    )
    resonance.add_argument("map", type=Path)
    add_common_id(resonance)
    resonance.add_argument("--from", dest="source", required=True)
    resonance.add_argument("--to", required=True)
    resonance.add_argument("--note", required=True)
    resonance.set_defaults(func=cmd_add_resonance)

    relation = sub.add_parser(
        "add-relation",
        help="record an explicit readable relation; no relation is inferred automatically",
    )
    relation.add_argument("map", type=Path)
    add_common_id(relation)
    relation.add_argument("--from", dest="source", required=True)
    relation.add_argument("--to", required=True)
    relation.add_argument(
        "--direction",
        choices=("directed", "reciprocal", "unspecified"),
        default="unspecified",
    )
    relation.add_argument("--predicate", required=True)
    relation.add_argument("--state")
    relation.add_argument("--basis", action="append")
    relation.set_defaults(func=cmd_add_relation)

    narrative = sub.add_parser(
        "add-narrative",
        help="record narrative synthesis from explicit map refs without inventing relations",
    )
    narrative.add_argument("map", type=Path)
    add_common_id(narrative)
    narrative.add_argument("text")
    narrative.add_argument("--basis", action="append", required=True)
    narrative.add_argument("--state")
    narrative.add_argument("--display-label")
    narrative.add_argument("--inherited", action="append")
    narrative.add_argument("--emergent", action="append")
    narrative.add_argument("--residual", action="append")
    narrative.set_defaults(func=cmd_add_narrative)

    residual = sub.add_parser("add-residual", help="keep an unresolved difference visible")
    residual.add_argument("map", type=Path)
    add_common_id(residual)
    residual.add_argument("text")
    residual.add_argument("--ref", action="append")
    residual.add_argument("--handling")
    residual.set_defaults(func=cmd_add_residual)

    question = sub.add_parser(
        "add-question",
        help="externalize a gap/question without promoting it to a relation",
    )
    question.add_argument("map", type=Path)
    add_common_id(question)
    question.add_argument("text")
    question.add_argument("--arises-from", action="append")
    question.add_argument("--between", nargs=2)
    question.add_argument("--would-clarify", action="append")
    question.add_argument("--handling")
    question.add_argument("--state")
    question.set_defaults(func=cmd_add_question)

    promote = sub.add_parser(
        "promote-question",
        help=(
            "promote an explicit relation candidate only after a return-to-source "
            "check has justified a readable relation"
        ),
    )
    promote.add_argument("map", type=Path)
    promote.add_argument("question")
    add_common_id(promote)
    promote.add_argument("--predicate", required=True)
    promote.add_argument(
        "--direction",
        choices=("directed", "reciprocal", "unspecified"),
        required=True,
    )
    promote.add_argument("--basis", action="append")
    promote.add_argument("--state")
    promote.set_defaults(func=cmd_promote_question)

    revise_relation = sub.add_parser(
        "revise-relation",
        help=(
            "restate an existing relation after return-to-source without changing "
            "its endpoints"
        ),
    )
    revise_relation.add_argument("map", type=Path)
    revise_relation.add_argument("relation")
    revise_relation.add_argument("--predicate", required=True)
    revise_relation.add_argument(
        "--direction",
        choices=("directed", "reciprocal", "unspecified"),
        required=True,
    )
    revise_relation.add_argument("--basis", action="append", default=None)
    revise_relation.add_argument("--state")
    revise_relation.add_argument("--note")
    revise_relation.set_defaults(func=cmd_revise_relation)

    demote_relation = sub.add_parser(
        "demote-relation",
        help=(
            "withdraw an explicit relation after return-check and preserve it as "
            "an unresolved question candidate"
        ),
    )
    demote_relation.add_argument("map", type=Path)
    demote_relation.add_argument("relation")
    add_common_id(demote_relation)
    demote_relation.add_argument("text")
    demote_relation.add_argument("--would-clarify", action="append")
    demote_relation.add_argument("--handling")
    demote_relation.add_argument("--state")
    demote_relation.set_defaults(func=cmd_demote_relation)

    update_handoff = sub.add_parser(
        "update-handoff",
        help=(
            "update selected handoff capsule fields without starting another round"
        ),
    )
    update_handoff.add_argument("map", type=Path)
    update_handoff.add_argument("--semantic-ref", action="append", default=None)
    update_handoff.add_argument("--residual-ref", action="append", default=None)
    update_handoff.add_argument("--source-ref", action="append", default=None)
    update_handoff.add_argument("--do-not-assume", action="append", default=None)
    update_handoff.set_defaults(func=cmd_update_handoff)

    handoff_check = sub.add_parser(
        "handoff-add-check",
        help=(
            "append a possible next check to the handoff capsule without "
            "executing or prioritizing it"
        ),
    )
    handoff_check.add_argument("map", type=Path)
    handoff_check.add_argument("text")
    handoff_check.add_argument("--ref", action="append")
    handoff_check.add_argument("--status")
    handoff_check.set_defaults(func=cmd_handoff_add_check)

    set_position = sub.add_parser(
        "set-position",
        help=(
            "set an explicit normalized layout position without inferring "
            "semantic relations"
        ),
    )
    set_position.add_argument("map", type=Path)
    set_position.add_argument("ref")
    set_position.add_argument("x", type=float)
    set_position.add_argument("y", type=float)
    set_position.add_argument("--projection")
    set_position.set_defaults(func=cmd_set_position)

    clear_position = sub.add_parser(
        "clear-position",
        help="remove one explicit layout position without changing semantics",
    )
    clear_position.add_argument("map", type=Path)
    clear_position.add_argument("ref")
    clear_position.set_defaults(func=cmd_clear_position)

    focus = sub.add_parser(
        "focus",
        help=(
            "show the one-hop semantic neighborhood of one stable ref without "
            "reopening the whole map"
        ),
    )
    focus.add_argument("map", type=Path)
    focus.add_argument("ref")
    focus.set_defaults(func=cmd_focus)

    diff = sub.add_parser(
        "diff",
        help=(
            "compare two affinity-map snapshots by stable ID without inferring "
            "semantic justification or touched-but-unchanged state"
        ),
    )
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.set_defaults(func=cmd_diff)

    status = sub.add_parser(
        "status",
        help="show working-board counts, ungrouped cards, residuals, and validation",
    )
    status.add_argument("map", type=Path)
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
