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
        "source_refs": source_refs,
        "sources": sources,
        "cards_from_source": cards_from_source,
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

    return {
        "format": data.get("format"),
        "version": data.get("version"),
        "input_status_counts": {
            "sources": dict(sorted(source_statuses.items())),
            "cards": dict(sorted(card_statuses.items())),
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
