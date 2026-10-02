from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


SEARCH_FIELDS = {
    "name": ("names",),
    "operation": ("cognitive_operations",),
    "primitive": ("structural_primitives",),
    "useful": ("useful_for",),
    "all": ("names", "cognitive_operations", "structural_primitives", "useful_for"),
}


def load_inventory(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("inventory must be a JSON object")
    if data.get("schema") != "csw.framework-candidate-inventory/v1":
        raise ValueError("unsupported framework candidate inventory schema")
    rows = data.get("candidates")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("inventory.candidates must be an array of objects")
    seen: set[str] = set()
    for row in rows:
        item_id = str(row.get("id", "")).strip()
        if not item_id:
            raise ValueError("every candidate requires a non-empty id")
        if item_id in seen:
            raise ValueError(f"duplicate candidate id: {item_id}")
        seen.add(item_id)
    return data


def candidates(data: dict[str, Any]) -> list[dict[str, Any]]:
    return list(data.get("candidates", []))


def by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["id"]): row for row in candidates(data)}


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, (str, int, float))]
    return []


def _norm(value: str) -> str:
    return " ".join(value.casefold().split())


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    sources = row.get("sources", [])
    source_kinds = sorted({
        str(source.get("kind"))
        for source in sources
        if isinstance(source, dict) and source.get("kind")
    })
    result: dict[str, Any] = {
        "id": row["id"],
        "names": list(row.get("names", [])),
        "readiness": row.get("readiness"),
        "cognitive_operations": list(row.get("cognitive_operations", [])),
        "structural_primitives": list(row.get("structural_primitives", [])),
        "useful_for": list(row.get("useful_for", [])),
        "do_not_assume": list(row.get("do_not_assume", [])),
        "source_basis": {
            "count": len(sources) if isinstance(sources, list) else 0,
            "kinds": source_kinds,
        },
    }
    for key in ("adoption_hold", "profile_path", "runtime_path", "source_packet_path"):
        if row.get(key):
            result[key] = row[key]
    return result


def _matches(row: dict[str, Any], term: str, field: str) -> dict[str, list[str]]:
    needle = _norm(term)
    if not needle:
        raise ValueError("search term must not be empty")
    matched: dict[str, list[str]] = {}
    for key in SEARCH_FIELDS[field]:
        hits = [value for value in _strings(row.get(key, [])) if needle in _norm(value)]
        if hits:
            matched[key] = hits
    return matched


def shortlist_payload(
    data: dict[str, Any],
    term: str,
    field: str,
    readiness: Iterable[str] | None,
) -> dict[str, Any]:
    accepted = set(readiness or [])
    rows = []
    for row in candidates(data):
        if accepted and str(row.get("readiness", "")) not in accepted:
            continue
        matched = _matches(row, term, field)
        if matched:
            rows.append({"candidate": candidate_summary(row), "matched": matched})
    return {
        "format": "csw.framework-shortlist/v1",
        "query": {"term": term, "field": field, "readiness": sorted(accepted)},
        "candidates": rows,
        "interpretation_boundary": (
            "Inventory order is preserved and no fit score or ranking is computed. "
            "A string match is only a recall aid."
        ),
    }


def contrast_payload(data: dict[str, Any], ids: list[str]) -> dict[str, Any]:
    if len(ids) < 2:
        raise ValueError("contrast requires at least two candidate ids")
    if len(set(ids)) != len(ids):
        raise ValueError("contrast candidate ids must be unique")
    index = by_id(data)
    missing = [item_id for item_id in ids if item_id not in index]
    if missing:
        raise ValueError("unknown candidate id(s): " + ", ".join(missing))
    op_sets = {
        item_id: set(map(str, index[item_id].get("cognitive_operations", [])))
        for item_id in ids
    }
    common = set.intersection(*(op_sets[item_id] for item_id in ids))
    rows = []
    for item_id in ids:
        other: set[str] = set()
        for other_id in ids:
            if other_id != item_id:
                other.update(op_sets[other_id])
        rows.append({
            "candidate": candidate_summary(index[item_id]),
            "exact_common_operations": sorted(common),
            "exact_unique_operations": sorted(op_sets[item_id] - other),
        })
    return {
        "format": "csw.framework-contrast/v1",
        "candidate_ids": ids,
        "candidates": rows,
        "interpretation_boundary": (
            "Operation labels are compared by exact string identity only. "
            "No semantic-equivalence claim is inferred from overlap or non-overlap."
        ),
    }


def worksheet_payload(
    data: dict[str, Any],
    need: str,
    ids: list[str],
    baseline: str | None,
) -> dict[str, Any]:
    if not need.strip():
        raise ValueError("need must not be empty")
    if not ids:
        raise ValueError("worksheet requires at least one candidate id")
    if len(set(ids)) != len(ids):
        raise ValueError("worksheet candidate ids must be unique")
    index = by_id(data)
    missing = [item_id for item_id in ids if item_id not in index]
    if missing:
        raise ValueError("unknown candidate id(s): " + ", ".join(missing))

    rows = []
    for item_id in ids:
        row = index[item_id]
        rows.append({
            "id": item_id,
            "readiness": row.get("readiness"),
            "adoption_hold": row.get("adoption_hold"),
            "available_operations": list(row.get("cognitive_operations", [])),
            "do_not_assume": list(row.get("do_not_assume", [])),
            "profile_path": row.get("profile_path"),
            "runtime_path": row.get("runtime_path"),
            "source_packet_path": row.get("source_packet_path"),
            "role": "unassigned",
            "intended_cognitive_job": "",
            "near_neighbor_difference": "",
            "target_return_questions": [],
            "de_bound_target_language": "",
            "what_would_change_this_choice": "",
        })

    return {
        "format": "csw.framework-selection-workspace/v1",
        "missing_cognitive_function": need,
        "target_baseline": baseline or "",
        "candidate_order_note": "Candidate order is working order, not a ranking.",
        "candidates": rows,
        "cross_framework_notes": {
            "primary_framework_job": "",
            "second_framework_job": "",
            "what_the_second_framework_should_disturb": "",
            "near_neighbor_confusions_to_avoid": [],
            "target_pushback_to_preserve": [],
        },
        "exit_record": {
            "questions_created": [],
            "distinctions_created": [],
            "relations_or_transitions_created": [],
            "falsifiers_or_observations_created": [],
            "residuals_created": [],
            "framework_specific_scaffolds_to_keep": [],
        },
        "interpretation_boundary": (
            "This worksheet records selection reasoning. It does not choose a framework, "
            "rank candidates, convert readiness into fit, or treat framework agreement "
            "as target evidence."
        ),
    }


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Externalize CSW framework-selection reasoning without automatic routing."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    shortlist = sub.add_parser("shortlist")
    shortlist.add_argument("inventory", type=Path)
    shortlist.add_argument("term")
    shortlist.add_argument("--field", choices=tuple(SEARCH_FIELDS), default="all")
    shortlist.add_argument("--readiness", action="append")

    contrast = sub.add_parser("contrast")
    contrast.add_argument("inventory", type=Path)
    contrast.add_argument("candidate_id", nargs="+")

    worksheet = sub.add_parser("worksheet")
    worksheet.add_argument("inventory", type=Path)
    worksheet.add_argument("--need", required=True)
    worksheet.add_argument("--candidate", action="append", required=True)
    worksheet.add_argument("--baseline")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        data = load_inventory(args.inventory)
        if args.command == "shortlist":
            print_json(shortlist_payload(data, args.term, args.field, args.readiness))
        elif args.command == "contrast":
            print_json(contrast_payload(data, args.candidate_id))
        elif args.command == "worksheet":
            print_json(worksheet_payload(data, args.need, args.candidate, args.baseline))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
