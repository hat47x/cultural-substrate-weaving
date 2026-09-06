from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("top-level affinity map must be an object")
    return value


def objects(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def ids(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("id", "")) for item in items if item.get("id")]


def find_group_cycles(groups: list[dict[str, Any]]) -> list[list[str]]:
    group_ids = set(ids(groups))
    graph: dict[str, list[str]] = {}
    for group in groups:
        gid = str(group.get("id", ""))
        graph[gid] = [
            str(member)
            for member in group.get("members", [])
            if str(member) in group_ids
        ]

    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            try:
                start = stack.index(node)
            except ValueError:
                start = 0
            cycles.append(stack[start:] + [node])
            return
        visiting.add(node)
        stack.append(node)
        for target in graph.get(node, []):
            visit(target)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for gid in graph:
        visit(gid)
    return cycles


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if data.get("format") != "affinity-map":
        errors.append("format must be 'affinity-map'")

    sections = {
        "source": objects(data, "sources"),
        "card": objects(data, "cards"),
        "group": objects(data, "groups"),
        "resonance": objects(data, "resonances"),
        "relation": objects(data, "relations"),
        "residual": objects(data, "residuals"),
        "question": objects(data, "questions"),
    }

    all_ids: dict[str, str] = {}
    for namespace, items in sections.items():
        seen: set[str] = set()
        for item in items:
            item_id = str(item.get("id", "")).strip()
            if not item_id:
                errors.append(f"{namespace} item is missing id")
                continue
            if item_id in seen:
                errors.append(f"duplicate {namespace} id: {item_id}")
            seen.add(item_id)
            if item_id in all_ids:
                warnings.append(
                    f"id {item_id} is reused across namespaces "
                    f"({all_ids[item_id]} and {namespace}); globally unique IDs are recommended"
                )
            else:
                all_ids[item_id] = namespace

    source_ids = set(ids(sections["source"]))
    card_ids = set(ids(sections["card"]))
    group_ids = set(ids(sections["group"]))
    semantic_node_ids = card_ids | group_ids
    residual_ids = set(ids(sections["residual"]))
    question_ids = set(ids(sections["question"]))
    traceable_ids = source_ids | semantic_node_ids | residual_ids | question_ids

    for card in sections["card"]:
        cid = str(card.get("id", ""))
        for ref in card.get("source_refs", []):
            if str(ref) not in source_ids:
                errors.append(f"card {cid} source_ref does not resolve: {ref}")
        for ref in card.get("derivation_refs", []):
            if str(ref) not in traceable_ids:
                warnings.append(f"card {cid} derivation_ref does not resolve locally: {ref}")

    group_membership: dict[str, set[str]] = {}
    for group in sections["group"]:
        gid = str(group.get("id", ""))
        members = [str(value) for value in group.get("members", [])]
        duplicates = sorted({member for member in members if members.count(member) > 1})
        if duplicates:
            errors.append(f"group {gid} repeats member refs: {', '.join(duplicates)}")
        group_membership[gid] = set(members)
        for member in members:
            if member not in semantic_node_ids:
                errors.append(f"group {gid} member does not resolve to card/group: {member}")
            if member == gid:
                errors.append(f"group {gid} directly contains itself")

    for cycle in find_group_cycles(sections["group"]):
        errors.append("group membership cycle: " + " -> ".join(cycle))

    for resonance in sections["resonance"]:
        xid = str(resonance.get("id", ""))
        source = str(resonance.get("from", ""))
        target = str(resonance.get("to", ""))
        if source not in semantic_node_ids:
            errors.append(f"resonance {xid} source does not resolve: {source}")
        if target not in group_ids:
            errors.append(f"resonance {xid} target must resolve to a group: {target}")
        if target in group_membership and source in group_membership[target]:
            warnings.append(
                f"resonance {xid}: {source} is already a member of {target}; "
                "if this is meant as secondary resonance, the cross-link is redundant or misleading"
            )
        if not str(resonance.get("note", "")).strip():
            warnings.append(f"resonance {xid} has no explanatory note")

    for relation in sections["relation"]:
        rid = str(relation.get("id", ""))
        source = str(relation.get("from", ""))
        target = str(relation.get("to", ""))
        if source not in semantic_node_ids:
            errors.append(f"relation {rid} source does not resolve: {source}")
        if target not in semantic_node_ids:
            errors.append(f"relation {rid} target does not resolve: {target}")
        predicate = str(relation.get("predicate", "")).strip()
        if not predicate:
            errors.append(f"relation {rid} has no readable predicate")
        direction = str(relation.get("direction", ""))
        if direction not in {"directed", "reciprocal", "unspecified"}:
            errors.append(f"relation {rid} has invalid direction: {direction}")
        for ref in relation.get("basis", []):
            if str(ref) not in traceable_ids:
                warnings.append(f"relation {rid} basis ref does not resolve locally: {ref}")

    for residual in sections["residual"]:
        uid = str(residual.get("id", ""))
        for ref in residual.get("refs", []):
            if str(ref) not in traceable_ids:
                warnings.append(f"residual {uid} ref does not resolve locally: {ref}")

    for question in sections["question"]:
        qid = str(question.get("id", ""))
        for ref in question.get("arises_from", []):
            if str(ref) not in semantic_node_ids | residual_ids:
                warnings.append(f"question {qid} arises_from ref does not resolve locally: {ref}")

    layout = data.get("layout")
    if isinstance(layout, dict):
        positions = layout.get("positions", {})
        if isinstance(positions, dict):
            for ref, position in positions.items():
                if str(ref) not in semantic_node_ids | residual_ids | question_ids:
                    warnings.append(f"layout position refers to unknown semantic id: {ref}")
                if not isinstance(position, dict):
                    errors.append(f"layout position for {ref} must be an object")
                    continue
                for axis in ("x", "y"):
                    value = position.get(axis)
                    if not isinstance(value, (int, float)) or isinstance(value, bool):
                        errors.append(f"layout {ref}.{axis} must be numeric")
                    elif not 0 <= float(value) <= 1:
                        errors.append(f"layout {ref}.{axis} must be between 0 and 1")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate semantic cross-references in an affinity-map JSON file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    try:
        data = load(args.input)
        errors, warnings = validate(data)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors or (args.warnings_as_errors and warnings):
        raise SystemExit(1)

    print(f"Affinity map semantic validation passed ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
