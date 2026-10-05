from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable


SEARCH_FIELDS = {
    "name": ("names",),
    "operation": ("cognitive_operations",),
    "primitive": ("structural_primitives",),
    "useful": ("useful_for",),
    "cue": ("selection_cues",),
    "all": (
        "names",
        "cognitive_operations",
        "structural_primitives",
        "useful_for",
        "selection_cues",
    ),
}

WORKSPACE_FORMAT = "csw.framework-selection-workspace/v1"
TYPOLOGY_SCHEMA = "csw.efficacy-framework-typology/v1"

EXIT_RECORD_FIELDS = {
    "question": "questions_created",
    "distinction": "distinctions_created",
    "relation-or-transition": "relations_or_transitions_created",
    "falsifier-or-observation": "falsifiers_or_observations_created",
    "residual": "residuals_created",
    "framework-specific-scaffold": "framework_specific_scaffolds_to_keep",
}

NON_FORCE_GUARDRAIL_FIELDS = (
    "contact_if",
    "stop_if",
    "survive_if",
)

CONSIDERATION_FIELDS = {
    "target_connection": "target_connection",
    "structural_difference": "structural_difference",
    "redundancy_or_overlap": "redundancy_or_overlap",
    "target_return_feasibility": "target_return_feasibility",
    "misuse_or_authority_risk": "misuse_or_authority_risk",
    "domain_constraint": "domain_constraint",
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


def load_typology(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("framework typology must be a JSON object")
    if data.get("schema") != TYPOLOGY_SCHEMA:
        raise ValueError("unsupported framework typology schema")

    target_structures = data.get("target_structures")
    if not isinstance(target_structures, dict):
        raise ValueError("typology.target_structures must be an object")
    for structure_id, definition in target_structures.items():
        if not str(structure_id).strip():
            raise ValueError("target structure id must not be empty")
        if not isinstance(definition, str) or not definition.strip():
            raise ValueError(
                f"target structure definition must be non-empty: {structure_id}"
            )

    rows = data.get("frameworks")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("typology.frameworks must be an array of objects")

    seen: set[str] = set()
    known_structures = set(map(str, target_structures))
    for row in rows:
        item_id = str(row.get("id", "")).strip()
        if not item_id:
            raise ValueError("every typology framework requires a non-empty id")
        if item_id in seen:
            raise ValueError(f"duplicate typology framework id: {item_id}")
        seen.add(item_id)

        structure_refs = row.get("ts", [])
        if not isinstance(structure_refs, list) or any(
            not isinstance(value, str) or not value.strip()
            for value in structure_refs
        ):
            raise ValueError(
                f"typology framework ts must be an array of target structure ids: {item_id}"
            )
        unknown = [
            value for value in structure_refs
            if value not in known_structures
        ]
        if unknown:
            raise ValueError(
                f"typology framework references unknown target structure {item_id}: "
                + ", ".join(unknown)
            )
    return data


def target_structure_catalog_payload(
    typology: dict[str, Any],
) -> dict[str, Any]:
    return {
        "format": "csw.target-structure-catalog/v0",
        "typology_date": typology.get("date"),
        "typology_status": typology.get("status"),
        "target_structures": [
            {"id": structure_id, "definition": definition}
            for structure_id, definition in typology["target_structures"].items()
        ],
        "interpretation_boundary": (
            "Target structures are a provisional human-authored research vocabulary. "
            "They are prompts for describing target-side structure, not diagnoses, "
            "framework selections, scores, or routing decisions."
        ),
    }


def target_structure_candidates_payload(
    typology: dict[str, Any],
    inventory: dict[str, Any],
    structure_ids: list[str],
) -> dict[str, Any]:
    requested = [str(value).strip() for value in structure_ids if str(value).strip()]
    if not requested:
        raise ValueError("structure-lookup requires at least one target structure id")
    if len(set(requested)) != len(requested):
        raise ValueError("target structure ids must be unique")

    target_structures = typology["target_structures"]
    missing = [value for value in requested if value not in target_structures]
    if missing:
        raise ValueError("unknown target structure id(s): " + ", ".join(missing))

    inventory_index = by_id(inventory)
    mapping_by_id: dict[str, dict[str, Any]] = {}
    for row in typology["frameworks"]:
        item_id = str(row["id"])
        if item_id not in inventory_index:
            raise ValueError(
                f"typology framework is missing from candidate inventory: {item_id}"
            )
        mapping_by_id[item_id] = row

    structures = []
    for structure_id in requested:
        mapped_candidates = []
        for candidate in candidates(inventory):
            item_id = str(candidate["id"])
            mapping = mapping_by_id.get(item_id)
            if mapping is None or structure_id not in mapping.get("ts", []):
                continue
            mapped_candidates.append({
                "candidate": candidate_summary(candidate),
                "mapping": {
                    "super_family": mapping.get("sf"),
                    "super_family_label": typology.get("super_families", {}).get(
                        mapping.get("sf")
                    ),
                    "structure_kind": mapping.get("structure_kind"),
                },
            })

        structures.append({
            "id": structure_id,
            "definition": target_structures[structure_id],
            "mapped_candidates": mapped_candidates,
        })

    return {
        "format": "csw.target-structure-candidate-view/v0",
        "typology_date": typology.get("date"),
        "typology_status": typology.get("status"),
        "target_structures": structures,
        "candidate_order_note": (
            "Mapped candidates preserve framework inventory order. "
            "The order is not a ranking."
        ),
        "interpretation_boundary": (
            "This view uses exact target-structure ids from a provisional human-authored "
            "research typology. It performs no semantic classification, fit scoring, "
            "ranking, activation, or recommendation. A mapping means only that the "
            "typology records the framework as intended to address that target structure."
        ),
    }


def target_structure_contrast_payload(
    typology: dict[str, Any],
    inventory: dict[str, Any],
    structure_ids: list[str],
) -> dict[str, Any]:
    lookup = target_structure_candidates_payload(
        typology,
        inventory,
        structure_ids,
    )
    requested = [
        str(item["id"])
        for item in lookup["target_structures"]
    ]
    definitions = {
        str(item["id"]): str(item["definition"])
        for item in lookup["target_structures"]
    }

    mapping_by_id = {
        str(row["id"]): row
        for row in typology["frameworks"]
    }
    displayed = [
        row
        for row in candidates(inventory)
        if any(
            structure_id in mapping_by_id.get(str(row["id"]), {}).get("ts", [])
            for structure_id in requested
        )
    ]
    operation_sets = {
        str(row["id"]): set(map(str, row.get("cognitive_operations", [])))
        for row in displayed
    }

    rows = []
    for candidate in displayed:
        candidate_id = str(candidate["id"])
        mapping = mapping_by_id[candidate_id]
        mapped = [
            structure_id
            for structure_id in requested
            if structure_id in mapping.get("ts", [])
        ]
        other_operations: set[str] = set()
        overlap = []
        for other in displayed:
            other_id = str(other["id"])
            if other_id == candidate_id:
                continue
            other_set = operation_sets[other_id]
            other_operations.update(other_set)
            common = sorted(operation_sets[candidate_id] & other_set)
            if common:
                overlap.append({
                    "candidate_id": other_id,
                    "exact_common_operations": common,
                })

        rows.append({
            "candidate": candidate_summary(candidate),
            "mapped_target_structures": [
                {
                    "id": structure_id,
                    "definition": definitions[structure_id],
                }
                for structure_id in mapped
            ],
            "unmapped_requested_target_structures": [
                structure_id
                for structure_id in requested
                if structure_id not in mapped
            ],
            "mapping": {
                "super_family": mapping.get("sf"),
                "super_family_label": typology.get("super_families", {}).get(
                    mapping.get("sf")
                ),
                "structure_kind": mapping.get("structure_kind"),
            },
            "exact_unique_operations_vs_displayed": sorted(
                operation_sets[candidate_id] - other_operations
            ),
            "exact_operation_overlap": overlap,
        })

    return {
        "format": "csw.target-structure-contrast/v0",
        "typology_date": typology.get("date"),
        "typology_status": typology.get("status"),
        "target_structures": [
            {
                "id": structure_id,
                "definition": definitions[structure_id],
            }
            for structure_id in requested
        ],
        "candidates": rows,
        "no_framework_option": {
            "available": True,
            "reasoning_prompt": (
                "Exact typology mappings are recall material only. "
                "Keep the target-side baseline and non-activation available "
                "when framework contact adds no useful cognitive job."
            ),
        },
        "candidate_order_note": (
            "Candidates preserve framework inventory order. "
            "Mapping breadth, readiness, source count, and operation count are not rankings."
        ),
        "interpretation_boundary": (
            "This view mechanically joins exact target-structure mappings with exact-string "
            "operation overlap. It does not infer semantic fit, novelty, complementarity, "
            "activation priority, or recommendation. A candidate mapped to more requested "
            "structures is not therefore better, and an exact-unique operation label is not "
            "therefore a useful or novel operation for the target."
        ),
    }


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
        "selection_cues": list(row.get("selection_cues", [])),
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


def registry_entry_payload(
    data: dict[str, Any],
    candidate_id: str,
) -> dict[str, Any]:
    index = by_id(data)
    if candidate_id not in index:
        raise ValueError(f"unknown candidate id: {candidate_id}")

    row = index[candidate_id]
    sources = []
    for source in row.get("sources", []):
        if not isinstance(source, dict):
            continue
        sources.append({
            "kind": source.get("kind"),
            "title": source.get("title"),
            "url": source.get("url"),
        })

    artifact_keys = (
        "source_packet_path",
        "profile_path",
        "runtime_path",
        "worked_example_paths",
        "negative_example_paths",
    )
    artifacts = {
        key: row.get(key)
        for key in artifact_keys
        if row.get(key)
    }

    readiness = str(row.get("readiness", ""))
    runtime_path = row.get("runtime_path")
    return {
        "format": "csw.framework-registry-entry/v0",
        "candidate": candidate_summary(row),
        "registry": {
            "readiness": readiness,
            "adoption_hold": row.get("adoption_hold"),
            "runtime_enabled": readiness == "adopted" and bool(runtime_path),
            "artifacts": artifacts,
            "sources": sources,
        },
        "activation_material": {
            "selection_cues": list(row.get("selection_cues", [])),
            "useful_for": list(row.get("useful_for", [])),
            "structural_primitives": list(row.get("structural_primitives", [])),
            "cognitive_operations": list(row.get("cognitive_operations", [])),
        },
        "authority_boundary": {
            "do_not_assume": list(row.get("do_not_assume", [])),
            "interpretation": (
                "Registry readiness and artifact availability describe research/runtime "
                "materialization, not framework fit, truth, recommendation strength, "
                "or target-side evidence."
            ),
        },
        "target_return_material": {
            "worked_example_paths": list(row.get("worked_example_paths", [])),
            "negative_example_paths": list(row.get("negative_example_paths", [])),
        },
        "interpretation_boundary": (
            "This view assembles one registry entry for deliberate inspection. "
            "It does not score, rank, activate, or recommend the framework. "
            "Source citations and examples remain inputs to human/model reasoning, "
            "and framework-generated candidates must still return to target material."
        ),
    }


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



def _literal_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(char for char in normalized if char.isalnum())


def recall_payload(
    data: dict[str, Any],
    need: str,
    readiness: Iterable[str] | None = None,
) -> dict[str, Any]:
    need_key = _literal_key(need)
    if not need_key:
        raise ValueError("need must not be empty")

    accepted = set(readiness or ["adopted"])
    rows = []
    for row in candidates(data):
        if accepted and str(row.get("readiness", "")) not in accepted:
            continue

        matched_cues = []
        for cue in _strings(row.get("selection_cues", [])):
            cue_key = _literal_key(cue)
            if cue_key and (cue_key in need_key or need_key in cue_key):
                matched_cues.append(cue)

        if matched_cues:
            rows.append({
                "candidate": candidate_summary(row),
                "matched_selection_cues": matched_cues,
            })

    return {
        "format": "csw.framework-need-recall/v1",
        "need": need,
        "readiness": sorted(accepted),
        "candidates": rows,
        "interpretation_boundary": (
            "Selection cues are explicit literal recall aids. "
            "Candidate order is inventory order, not ranking. "
            "A cue match does not choose a framework, establish semantic fit, "
            "or bypass adoption and lineage boundaries."
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
    workspace_ref: str | None = None,
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
            "planned_operations": [],
            "intended_cognitive_job": "",
            "near_neighbor_difference": "",
            "target_return_questions": [],
            "de_bound_target_language": "",
            "what_would_change_this_choice": "",
            "non_force_guardrails": {
                "contact_if": "",
                "stop_if": "",
                "survive_if": "",
            },
            "contact_record": {
                "contacted": None,
                "reason": "",
                "selection_snapshot": None,
            },
            "consideration_axes": {
                "target_connection": "",
                "structural_difference": "",
                "redundancy_or_overlap": "",
                "target_return_feasibility": "",
                "misuse_or_authority_risk": "",
                "domain_constraint": "",
            },
        })

    return {
        "format": WORKSPACE_FORMAT,
        "workspace_ref": (workspace_ref or "").strip(),
        "missing_cognitive_function": need,
        "target_baseline": baseline or "",
        "target_structure_hypotheses": [],
        "candidate_order_note": "Candidate order is working order, not a ranking.",
        "no_framework_option": {
            "reason": "",
            "baseline_note": "",
            "what_would_change_this": "",
            "remained_viable_after_contact": None,
            "post_contact_note": "",
        },
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


def target_structure_selection_audit_payload(
    workspace: dict[str, Any],
    typology: dict[str, Any],
    inventory: dict[str, Any],
) -> dict[str, Any]:
    ensure_consideration_fields(workspace)
    hypotheses = list(workspace.get("target_structure_hypotheses", []))
    current_typology = {
        "schema": str(typology.get("schema", "")),
        "date": str(typology.get("date", "")),
        "status": str(typology.get("status", "")),
    }

    hypothesis_audits = []
    drifted = False
    for row in hypotheses:
        structure_id = str(row["id"])
        source_typology = dict(row.get("source_typology", {}))
        current_definition = typology["target_structures"].get(structure_id)
        definition_matches = (
            isinstance(current_definition, str)
            and current_definition == row.get("definition")
        )
        provenance_matches = all(
            str(source_typology.get(key, "")) == current_typology[key]
            for key in ("schema", "date", "status")
        )
        snapshot_matches = definition_matches and provenance_matches
        if not snapshot_matches:
            drifted = True
        hypothesis_audits.append({
            "id": structure_id,
            "basis": row.get("basis", ""),
            "snapshot_definition": row.get("definition"),
            "current_definition": current_definition,
            "snapshot_typology": source_typology,
            "current_typology": current_typology,
            "definition_matches_current": definition_matches,
            "typology_provenance_matches_current": provenance_matches,
            "snapshot_matches_current": snapshot_matches,
        })

    workspace_candidates = [
        {
            "candidate_id": str(row["id"]),
            "role": row.get("role"),
            "planned_operations": list(row.get("planned_operations", [])),
        }
        for row in workspace.get("candidates", [])
    ]

    if not hypotheses:
        comparison_state = "no_recorded_target_structure_hypothesis"
        candidate_audits = [
            {
                **row,
                "comparison_state": comparison_state,
                "mapped_target_structures": [],
            }
            for row in workspace_candidates
        ]
        mapped_not_in_workspace: list[str] = []
        outside_mapping: list[str] = []
    elif drifted:
        comparison_state = "not_compared_due_to_typology_snapshot_drift"
        candidate_audits = [
            {
                **row,
                "comparison_state": comparison_state,
                "mapped_target_structures": [],
            }
            for row in workspace_candidates
        ]
        mapped_not_in_workspace = []
        outside_mapping = []
    else:
        comparison_state = "compared_against_matching_typology_snapshot"
        structure_ids = [str(row["id"]) for row in hypotheses]
        contrast = target_structure_contrast_payload(
            typology,
            inventory,
            structure_ids,
        )
        mapped_by_id = {
            str(row["candidate"]["id"]): [
                str(item["id"])
                for item in row["mapped_target_structures"]
            ]
            for row in contrast["candidates"]
        }
        workspace_ids = [
            str(row["candidate_id"])
            for row in workspace_candidates
        ]
        candidate_audits = []
        outside_mapping = []
        for row in workspace_candidates:
            candidate_id = str(row["candidate_id"])
            mapped = mapped_by_id.get(candidate_id, [])
            state = (
                "mapped_to_recorded_hypothesis"
                if mapped
                else "outside_exact_typology_mapping"
            )
            if not mapped:
                outside_mapping.append(candidate_id)
            candidate_audits.append({
                **row,
                "comparison_state": state,
                "mapped_target_structures": mapped,
            })
        mapped_not_in_workspace = [
            candidate_id
            for candidate_id in mapped_by_id
            if candidate_id not in workspace_ids
        ]

    return {
        "format": "csw.target-structure-selection-audit/v0",
        "workspace_ref": workspace.get("workspace_ref", ""),
        "typology_snapshot_state": (
            "drifted"
            if drifted
            else ("matching" if hypotheses else "not-recorded")
        ),
        "hypotheses": hypothesis_audits,
        "candidate_audits": candidate_audits,
        "mapped_candidates_not_in_workspace": mapped_not_in_workspace,
        "workspace_candidates_outside_exact_mapping": outside_mapping,
        "no_framework_option": dict(workspace.get("no_framework_option", {})),
        "comparison_state": comparison_state,
        "interpretation_boundary": (
            "This audit checks explicit provenance and exact typology mappings only. "
            "A workspace candidate outside the exact mapping is not therefore wrong, "
            "and a mapped candidate omitted from the workspace is not therefore missing. "
            "If the stored typology snapshot has drifted, historical candidate mapping is "
            "not reinterpreted against the current typology; the audit stops at drift. "
            "Neither mapping nor drift establishes framework fit, target truth, or error."
        ),
    }


def load_workspace(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != WORKSPACE_FORMAT:
        raise ValueError("unsupported framework selection workspace format")
    rows = data.get("candidates")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("workspace.candidates must be an array of objects")
    seen: set[str] = set()
    for row in rows:
        item_id = str(row.get("id", "")).strip()
        if not item_id:
            raise ValueError("every workspace candidate requires a non-empty id")
        if item_id in seen:
            raise ValueError(f"duplicate workspace candidate id: {item_id}")
        seen.add(item_id)
    for key in ("cross_framework_notes", "exit_record"):
        if not isinstance(data.get(key), dict):
            raise ValueError(f"workspace.{key} must be an object")
    ensure_consideration_fields(data)
    return data


def ensure_consideration_fields(data: dict[str, Any]) -> None:
    for row in data.get("candidates", []):
        axes = row.get("consideration_axes")
        if axes is None:
            axes = {}
            row["consideration_axes"] = axes
        if not isinstance(axes, dict):
            raise ValueError(
                f"candidate consideration_axes must be an object: {row.get('id', '')}"
            )
        for key in CONSIDERATION_FIELDS:
            axes.setdefault(key, "")

        guardrails = row.get("non_force_guardrails")
        if guardrails is None:
            guardrails = {}
            row["non_force_guardrails"] = guardrails
        if not isinstance(guardrails, dict):
            raise ValueError(
                f"candidate non_force_guardrails must be an object: {row.get('id', '')}"
            )
        for key in NON_FORCE_GUARDRAIL_FIELDS:
            guardrails.setdefault(key, "")

        contact_record = row.get("contact_record")
        if contact_record is None:
            contact_record = {
                "contacted": None,
                "reason": "",
                "selection_snapshot": None,
            }
            row["contact_record"] = contact_record
        if not isinstance(contact_record, dict):
            raise ValueError(
                f"candidate contact_record must be an object: {row.get('id', '')}"
            )
        contacted = contact_record.get("contacted")
        if contacted is not None and not isinstance(contacted, bool):
            raise ValueError(
                f"candidate contact_record.contacted must be boolean or null: "
                f"{row.get('id', '')}"
            )
        reason = contact_record.get("reason", "")
        if not isinstance(reason, str):
            raise ValueError(
                f"candidate contact_record.reason must be a string: {row.get('id', '')}"
            )
        snapshot = contact_record.get("selection_snapshot")
        if snapshot is not None and not isinstance(snapshot, dict):
            raise ValueError(
                f"candidate contact_record.selection_snapshot must be an object or null: "
                f"{row.get('id', '')}"
            )
        contact_record.setdefault("contacted", None)
        contact_record.setdefault("reason", "")
        contact_record.setdefault("selection_snapshot", None)

    hypotheses = data.get("target_structure_hypotheses")
    if hypotheses is None:
        hypotheses = []
        data["target_structure_hypotheses"] = hypotheses
    if not isinstance(hypotheses, list) or any(
        not isinstance(row, dict) for row in hypotheses
    ):
        raise ValueError("workspace.target_structure_hypotheses must be an array of objects")

    seen_structure_ids: set[str] = set()
    for row in hypotheses:
        structure_id = str(row.get("id", "")).strip()
        definition = row.get("definition")
        if not structure_id:
            raise ValueError("target structure hypothesis requires a non-empty id")
        if structure_id in seen_structure_ids:
            raise ValueError(f"duplicate target structure hypothesis id: {structure_id}")
        seen_structure_ids.add(structure_id)
        if not isinstance(definition, str) or not definition.strip():
            raise ValueError(
                f"target structure hypothesis requires a definition: {structure_id}"
            )
        basis = row.get("basis", "")
        if not isinstance(basis, str):
            raise ValueError(
                f"target structure hypothesis basis must be a string: {structure_id}"
            )
        row.setdefault("basis", "")

        source_typology = row.get("source_typology")
        if source_typology is None:
            source_typology = {"schema": "", "date": "", "status": ""}
            row["source_typology"] = source_typology
        if not isinstance(source_typology, dict):
            raise ValueError(
                f"target structure hypothesis source_typology must be an object: "
                f"{structure_id}"
            )
        for key in ("schema", "date", "status"):
            value = source_typology.get(key, "")
            if not isinstance(value, str):
                raise ValueError(
                    f"target structure hypothesis source_typology.{key} must be a string: "
                    f"{structure_id}"
                )
            source_typology.setdefault(key, "")

    option = data.get("no_framework_option")
    if option is None:
        option = {}
        data["no_framework_option"] = option
    if not isinstance(option, dict):
        raise ValueError("workspace.no_framework_option must be an object")
    option.setdefault("reason", "")
    option.setdefault("baseline_note", "")
    option.setdefault("what_would_change_this", "")
    option.setdefault("remained_viable_after_contact", None)
    option.setdefault("post_contact_note", "")
    remained_viable = option.get("remained_viable_after_contact")
    if remained_viable is not None and not isinstance(remained_viable, bool):
        raise ValueError(
            "workspace.no_framework_option.remained_viable_after_contact "
            "must be boolean or null"
        )
    if not isinstance(option.get("post_contact_note", ""), str):
        raise ValueError(
            "workspace.no_framework_option.post_contact_note must be a string"
        )


def set_target_structure_hypothesis(
    data: dict[str, Any],
    typology: dict[str, Any],
    structure_id: str,
    *,
    basis: str | None = None,
) -> None:
    ensure_consideration_fields(data)
    structure_id = structure_id.strip()
    if structure_id not in typology["target_structures"]:
        raise ValueError(f"unknown target structure id: {structure_id}")

    hypotheses = data["target_structure_hypotheses"]
    for row in hypotheses:
        if row["id"] != structure_id:
            continue
        row["definition"] = typology["target_structures"][structure_id]
        row["source_typology"] = {
            "schema": str(typology.get("schema", "")),
            "date": str(typology.get("date", "")),
            "status": str(typology.get("status", "")),
        }
        if basis is not None:
            row["basis"] = basis
        return

    hypotheses.append({
        "id": structure_id,
        "definition": typology["target_structures"][structure_id],
        "basis": basis or "",
        "source_typology": {
            "schema": str(typology.get("schema", "")),
            "date": str(typology.get("date", "")),
            "status": str(typology.get("status", "")),
        },
    })


def save_workspace(path: Path, data: dict[str, Any]) -> None:
    if data.get("format") != WORKSPACE_FORMAT:
        raise ValueError("unsupported framework selection workspace format")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def find_workspace_candidate(
    data: dict[str, Any],
    candidate_id: str,
) -> dict[str, Any]:
    for row in data["candidates"]:
        if str(row.get("id", "")) == candidate_id:
            return row
    raise ValueError(f"workspace candidate does not exist: {candidate_id}")


def update_candidate(
    data: dict[str, Any],
    candidate_id: str,
    *,
    role: str | None = None,
    job: str | None = None,
    difference: str | None = None,
    de_bound: str | None = None,
    revisit_if: str | None = None,
    planned_operations: Iterable[str] | None = None,
    return_questions: Iterable[str] | None = None,
) -> None:
    if not any(
        value is not None
        for value in (role, job, difference, de_bound, revisit_if)
    ) and not list(planned_operations or []) and not list(return_questions or []):
        raise ValueError("set-candidate requires at least one update")

    row = find_workspace_candidate(data, candidate_id)

    planned = [
        str(value)
        for value in (planned_operations or [])
        if str(value).strip()
    ]
    if planned:
        available = {str(value) for value in row.get("available_operations", [])}
        unknown = [value for value in planned if value not in available]
        if unknown:
            raise ValueError(
                f"planned operation is not available for candidate {candidate_id}: "
                + ", ".join(unknown)
            )

        existing_planned = row.get("planned_operations", [])
        if not isinstance(existing_planned, list):
            raise ValueError(
                f"candidate planned_operations must be an array: {candidate_id}"
            )
        row["planned_operations"] = list(
            dict.fromkeys([str(value) for value in existing_planned] + planned)
        )

    for key, value in (
        ("role", role),
        ("intended_cognitive_job", job),
        ("near_neighbor_difference", difference),
        ("de_bound_target_language", de_bound),
        ("what_would_change_this_choice", revisit_if),
    ):
        if value is not None:
            row[key] = value

    additions = [str(value) for value in (return_questions or []) if str(value).strip()]
    if additions:
        existing = row.get("target_return_questions", [])
        if not isinstance(existing, list):
            raise ValueError(
                f"candidate target_return_questions must be an array: {candidate_id}"
            )
        row["target_return_questions"] = list(
            dict.fromkeys([str(value) for value in existing] + additions)
        )


def update_consideration(
    data: dict[str, Any],
    candidate_id: str,
    **values: str | None,
) -> None:
    row = find_workspace_candidate(data, candidate_id)
    ensure_consideration_fields(data)
    axes = row["consideration_axes"]
    changed = False
    for arg_name, key in CONSIDERATION_FIELDS.items():
        value = values.get(arg_name)
        if value is not None:
            axes[key] = value
            changed = True
    if not changed:
        raise ValueError("set-consideration requires at least one update")


def update_non_force_guardrail(
    data: dict[str, Any],
    candidate_id: str,
    *,
    contact_if: str | None = None,
    stop_if: str | None = None,
    survive_if: str | None = None,
) -> None:
    ensure_consideration_fields(data)
    row = find_workspace_candidate(data, candidate_id)
    if contact_if is None and stop_if is None and survive_if is None:
        raise ValueError("set-guardrail requires at least one update")

    guardrails = row["non_force_guardrails"]
    for key, value in (
        ("contact_if", contact_if),
        ("stop_if", stop_if),
        ("survive_if", survive_if),
    ):
        if value is not None:
            guardrails[key] = value


def _selection_snapshot_for_candidate(
    data: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, Any]:
    ensure_consideration_fields(data)
    option = data["no_framework_option"]
    return {
        "target_baseline": data.get("target_baseline", ""),
        "target_structure_hypotheses": json.loads(
            json.dumps(data.get("target_structure_hypotheses", []))
        ),
        "candidate_reasoning": {
            "role": row.get("role"),
            "planned_operations": list(row.get("planned_operations", [])),
            "intended_cognitive_job": row.get("intended_cognitive_job", ""),
            "near_neighbor_difference": row.get("near_neighbor_difference", ""),
            "target_return_questions": list(row.get("target_return_questions", [])),
            "de_bound_target_language": row.get("de_bound_target_language", ""),
            "what_would_change_this_choice": row.get(
                "what_would_change_this_choice",
                "",
            ),
            "consideration_axes": dict(row.get("consideration_axes", {})),
            "non_force_guardrails": dict(row.get("non_force_guardrails", {})),
        },
        "no_framework_option": {
            "reason": option.get("reason", ""),
            "baseline_note": option.get("baseline_note", ""),
            "what_would_change_this": option.get("what_would_change_this", ""),
        },
    }


def record_contact_disposition(
    data: dict[str, Any],
    candidate_id: str,
    *,
    contacted: bool,
    reason: str,
) -> None:
    ensure_consideration_fields(data)
    reason = reason.strip()
    if not reason:
        raise ValueError("record-contact requires a non-empty reason")
    row = find_workspace_candidate(data, candidate_id)
    row["contact_record"] = {
        "contacted": contacted,
        "reason": reason,
        "selection_snapshot": _selection_snapshot_for_candidate(data, row),
    }


def update_non_activation(
    data: dict[str, Any],
    *,
    reason: str | None = None,
    baseline_note: str | None = None,
    revisit_if: str | None = None,
    remained_viable_after_contact: bool | None = None,
    post_contact_note: str | None = None,
) -> None:
    ensure_consideration_fields(data)
    if (
        reason is None
        and baseline_note is None
        and revisit_if is None
        and remained_viable_after_contact is None
        and post_contact_note is None
    ):
        raise ValueError("set-non-activation requires at least one update")
    option = data["no_framework_option"]
    if reason is not None:
        option["reason"] = reason
    if baseline_note is not None:
        option["baseline_note"] = baseline_note
    if revisit_if is not None:
        option["what_would_change_this"] = revisit_if
    if remained_viable_after_contact is not None:
        option["remained_viable_after_contact"] = remained_viable_after_contact
    if post_contact_note is not None:
        option["post_contact_note"] = post_contact_note


def review_payload(data: dict[str, Any]) -> dict[str, Any]:
    ensure_consideration_fields(data)
    rows = []
    for row in data.get("candidates", []):
        axes = row["consideration_axes"]
        rows.append({
            "candidate_id": row.get("id"),
            "role": row.get("role"),
            "consideration_axes": dict(axes),
            "non_force_guardrails": dict(row["non_force_guardrails"]),
            "contact_record": dict(row["contact_record"]),
            "unfilled_guardrails": [
                key for key in NON_FORCE_GUARDRAIL_FIELDS
                if not str(row["non_force_guardrails"].get(key, "")).strip()
            ],
            "unfilled_axes": [
                key for key in CONSIDERATION_FIELDS
                if not str(axes.get(key, "")).strip()
            ],
        })

    option = data["no_framework_option"]
    return {
        "format": "csw.framework-selection-review/v1",
        "workspace_ref": data.get("workspace_ref", ""),
        "missing_cognitive_function": data.get("missing_cognitive_function", ""),
        "target_structure_hypotheses": [
            dict(row) for row in data["target_structure_hypotheses"]
        ],
        "candidates": rows,
        "no_framework_option": dict(option),
        "no_framework_unfilled": [
            key for key in ("reason", "baseline_note", "what_would_change_this")
            if not str(option.get(key, "")).strip()
        ],
        "interpretation_boundary": (
            "Unfilled fields are prompts for deliberate consideration, not failures, "
            "coverage scores, or requirements to activate a framework. This review "
            "does not rank candidates or choose between activation and non-activation."
        ),
    }


def update_cross_framework(
    data: dict[str, Any],
    *,
    primary_job: str | None = None,
    second_job: str | None = None,
    disturb: str | None = None,
    confusions: Iterable[str] | None = None,
    pushbacks: Iterable[str] | None = None,
) -> None:
    if not any(value is not None for value in (primary_job, second_job, disturb)) \
        and not list(confusions or []) \
        and not list(pushbacks or []):
        raise ValueError("set-cross-framework requires at least one update")

    notes = data["cross_framework_notes"]
    for key, value in (
        ("primary_framework_job", primary_job),
        ("second_framework_job", second_job),
        ("what_the_second_framework_should_disturb", disturb),
    ):
        if value is not None:
            notes[key] = value

    for key, values in (
        ("near_neighbor_confusions_to_avoid", confusions),
        ("target_pushback_to_preserve", pushbacks),
    ):
        additions = [str(value) for value in (values or []) if str(value).strip()]
        if not additions:
            continue
        existing = notes.get(key, [])
        if not isinstance(existing, list):
            raise ValueError(f"workspace cross-framework {key} must be an array")
        notes[key] = list(dict.fromkeys([str(value) for value in existing] + additions))


def add_exit_record(data: dict[str, Any], kind: str, text_value: str) -> None:
    value = text_value.strip()
    if not value:
        raise ValueError("exit record text must not be empty")
    key = EXIT_RECORD_FIELDS[kind]
    values = data["exit_record"].get(key, [])
    if not isinstance(values, list):
        raise ValueError(f"workspace exit_record.{key} must be an array")
    data["exit_record"][key] = list(dict.fromkeys([str(item) for item in values] + [value]))


def load_affinity_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != "affinity-map":
        raise ValueError("unsupported affinity map format")
    cards = data.get("cards", [])
    if not isinstance(cards, list) or any(not isinstance(card, dict) for card in cards):
        raise ValueError("affinity map cards must be an array of objects")
    return data


def load_living_lab_round(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Living Lab round must be a JSON object")
    if data.get("schema_version") != "0.2":
        raise ValueError("unsupported Living Lab round schema version")
    round_id = str(data.get("round_id", "")).strip()
    if not round_id:
        raise ValueError("Living Lab round requires a round_id")

    contacts = data.get("framework_contacts", [])
    deltas = data.get("catalytic_deltas", [])
    traces = data.get("artifact_traces", [])
    if not isinstance(contacts, list) or any(
        not isinstance(contact, dict) for contact in contacts
    ):
        raise ValueError("Living Lab framework_contacts must be an array of objects")
    if not isinstance(deltas, list) or any(
        not isinstance(delta, dict) for delta in deltas
    ):
        raise ValueError("Living Lab catalytic_deltas must be an array of objects")
    if not isinstance(traces, list) or any(
        not isinstance(trace, dict) for trace in traces
    ):
        raise ValueError("Living Lab artifact_traces must be an array of objects")
    return data


def _append_unique(target: list[str], values: Iterable[Any]) -> None:
    for value in values:
        text_value = str(value)
        if text_value and text_value not in target:
            target.append(text_value)


def audit_map_payload(
    workspace: dict[str, Any],
    affinity_map: dict[str, Any],
) -> dict[str, Any]:
    workspace_ref = str(workspace.get("workspace_ref", "")).strip()
    if not workspace_ref:
        raise ValueError("audit-map requires a workspace_ref")

    linked_cards: list[dict[str, Any]] = []
    linked_card_ids: list[str] = []
    observed_operations: list[str] = []
    framework_labels: list[str] = []
    yield_kinds: list[str] = []
    target_responses: list[str] = []
    return_states: list[str] = []

    for card in affinity_map.get("cards", []):
        trace = card.get("catalytic_trace")
        if not isinstance(trace, dict):
            continue
        selection_refs = [str(value) for value in trace.get("selection_refs", [])]
        if workspace_ref not in selection_refs:
            continue

        card_id = str(card.get("id", "")).strip()
        if card_id:
            linked_card_ids.append(card_id)
        _append_unique(observed_operations, trace.get("operations", []))
        _append_unique(framework_labels, trace.get("frameworks", []))
        _append_unique(yield_kinds, trace.get("yield_kinds", []))
        _append_unique(target_responses, trace.get("target_responses", []))
        for audit in trace.get("target_return_audits", []):
            if isinstance(audit, dict) and str(audit.get("state", "")).strip():
                _append_unique(return_states, [audit["state"]])

        linked_cards.append({
            "id": card_id,
            "text": card.get("text"),
            "frameworks": list(trace.get("frameworks", [])),
            "operations": list(trace.get("operations", [])),
            "yield_kinds": list(trace.get("yield_kinds", [])),
            "target_responses": list(trace.get("target_responses", [])),
            "target_response_refs": list(trace.get("target_response_refs", [])),
            "target_return_states": [
                audit.get("state")
                for audit in trace.get("target_return_audits", [])
                if isinstance(audit, dict) and audit.get("state")
            ],
        })

    planned_operations: list[str] = []
    candidate_ids: list[str] = []
    cards_by_exact_candidate_id: dict[str, list[str]] = {}
    for row in workspace.get("candidates", []):
        candidate_id = str(row.get("id", "")).strip()
        if candidate_id:
            candidate_ids.append(candidate_id)
            cards_by_exact_candidate_id[candidate_id] = []
        _append_unique(planned_operations, row.get("planned_operations", []))

    candidate_id_set = set(candidate_ids)
    for card in linked_cards:
        for framework in card["frameworks"]:
            label = str(framework)
            if label in candidate_id_set and card["id"]:
                cards_by_exact_candidate_id[label].append(card["id"])

    unmatched_framework_labels = [
        label for label in framework_labels if label not in candidate_id_set
    ]

    candidate_operation_audits: list[dict[str, Any]] = []
    candidate_guardrail_contexts: list[dict[str, Any]] = []
    for row in workspace.get("candidates", []):
        candidate_id = str(row.get("id", "")).strip()
        if not candidate_id:
            continue
        planned_for_candidate: list[str] = []
        _append_unique(planned_for_candidate, row.get("planned_operations", []))
        candidate_cards = [
            card
            for card in linked_cards
            if candidate_id in [str(value) for value in card["frameworks"]]
        ]
        observed_for_candidate: list[str] = []
        yield_kinds_for_candidate: list[str] = []
        target_responses_for_candidate: list[str] = []
        return_states_for_candidate: list[str] = []
        for card in candidate_cards:
            _append_unique(observed_for_candidate, card["operations"])
            _append_unique(yield_kinds_for_candidate, card["yield_kinds"])
            _append_unique(
                target_responses_for_candidate,
                card["target_responses"],
            )
            _append_unique(
                return_states_for_candidate,
                card["target_return_states"],
            )
        candidate_guardrail_contexts.append({
            "candidate_id": candidate_id,
            "linked_card_ids": [
                card["id"] for card in candidate_cards if card["id"]
            ],
            "guardrails": dict(row.get("non_force_guardrails", {})),
            "contact_record": dict(row.get("contact_record", {})),
            "target_responses": target_responses_for_candidate,
            "target_return_states": return_states_for_candidate,
            "interpretation_boundary": (
                "Guardrails are pre-contact reasoning notes shown beside observed "
                "target-return context. This audit does not decide whether a guardrail "
                "was satisfied, violated, or sufficient."
            ),
        })

        candidate_operation_audits.append({
            "candidate_id": candidate_id,
            "linked_card_ids": [
                card["id"] for card in candidate_cards if card["id"]
            ],
            "planned_operations": planned_for_candidate,
            "observed_operations": observed_for_candidate,
            "planned_not_observed_exact": [
                value
                for value in planned_for_candidate
                if value not in observed_for_candidate
            ],
            "observed_not_planned_exact": [
                value
                for value in observed_for_candidate
                if value not in planned_for_candidate
            ],
            "yield_kinds": yield_kinds_for_candidate,
            "target_responses": target_responses_for_candidate,
            "target_return_states": return_states_for_candidate,
        })

    downstream_cross_field_cards: list[str] = []
    linked_id_set = set(linked_card_ids)
    for card in affinity_map.get("cards", []):
        if str(card.get("input_status", "")) != "cross_field_emergent":
            continue
        trace = card.get("cross_field_trace")
        if not isinstance(trace, dict):
            continue
        framework_refs = {str(value) for value in trace.get("framework_refs", [])}
        if framework_refs & linked_id_set:
            card_id = str(card.get("id", "")).strip()
            if card_id:
                downstream_cross_field_cards.append(card_id)

    return {
        "format": "csw.framework-selection-map-audit/v1",
        "workspace_ref": workspace_ref,
        "linked_cards": linked_cards,
        "planned_operations": planned_operations,
        "observed_operations": observed_operations,
        "planned_not_observed_exact": [
            value for value in planned_operations if value not in observed_operations
        ],
        "observed_not_planned_exact": [
            value for value in observed_operations if value not in planned_operations
        ],
        "framework_labels": framework_labels,
        "cards_by_exact_candidate_id": cards_by_exact_candidate_id,
        "framework_labels_without_exact_candidate_id_match": unmatched_framework_labels,
        "candidate_operation_audits": candidate_operation_audits,
        "candidate_guardrail_contexts": candidate_guardrail_contexts,
        "yield_kinds": yield_kinds,
        "target_responses": target_responses,
        "target_return_states": return_states,
        "downstream_cross_field_cards": downstream_cross_field_cards,
        "interpretation_boundary": (
            "This is an exact-string provenance audit. Missing observed operations do "
            "not mean the selection failed; unmatched framework labels do not mean the "
            "framework is wrong; candidate-level exact matches, yields, target responses, "
            "and return states show provenance, not framework effectiveness; their absence "
            "or presence requires return to the actual material and selection reasoning."
        ),
    }


def audit_living_lab_payload(
    workspace: dict[str, Any],
    round_record: dict[str, Any],
) -> dict[str, Any]:
    workspace_ref = str(workspace.get("workspace_ref", "")).strip()
    if not workspace_ref:
        raise ValueError("audit-living-lab requires a workspace_ref")

    linked_contacts: list[dict[str, Any]] = []
    linked_deltas: list[dict[str, Any]] = []
    linked_artifacts: list[dict[str, Any]] = []
    contacted_operations: list[str] = []
    delta_operations: list[str] = []
    artifact_operations: list[str] = []
    delta_kinds: list[str] = []
    delta_pre_contact_states: list[str] = []
    delta_target_return_states: list[str] = []
    delta_user_dispositions: list[str] = []
    framework_labels: list[str] = []
    target_return_states: list[str] = []
    user_dispositions: list[str] = []

    for contact in round_record.get("framework_contacts", []):
        if str(contact.get("selection_ref", "")).strip() != workspace_ref:
            continue
        operations = [str(value) for value in contact.get("operations", [])]
        framework = str(contact.get("framework", "")).strip()
        if framework:
            _append_unique(framework_labels, [framework])
        _append_unique(contacted_operations, operations)
        linked_contacts.append({
            "framework": framework,
            "depth": contact.get("depth"),
            "use": contact.get("use"),
            "selection_ref": contact.get("selection_ref"),
            "operations": operations,
        })

    for delta in round_record.get("catalytic_deltas", []):
        selection_refs = [str(value) for value in delta.get("selection_refs", [])]
        if workspace_ref not in selection_refs:
            continue
        frameworks = [str(value) for value in delta.get("framework_refs", [])]
        operations = [str(value) for value in delta.get("operation_refs", [])]
        _append_unique(framework_labels, frameworks)
        _append_unique(delta_operations, operations)

        kind = str(delta.get("kind", "")).strip()
        if kind:
            _append_unique(delta_kinds, [kind])

        pre_contact_relation = delta.get("pre_contact_relation")
        if not isinstance(pre_contact_relation, dict):
            pre_contact_relation = None
        if pre_contact_relation is not None:
            state = str(pre_contact_relation.get("state", "")).strip()
            if state:
                _append_unique(delta_pre_contact_states, [state])

        target_return = delta.get("target_return")
        if not isinstance(target_return, dict):
            target_return = {}
        return_state = str(target_return.get("state", "")).strip()
        if return_state:
            _append_unique(delta_target_return_states, [return_state])

        user_disposition = delta.get("user_disposition")
        if not isinstance(user_disposition, dict):
            user_disposition = None
        if user_disposition is not None:
            state = str(user_disposition.get("state", "")).strip()
            if state:
                _append_unique(delta_user_dispositions, [state])

        linked_deltas.append({
            "delta_ref": delta.get("delta_ref"),
            "kind": delta.get("kind"),
            "statement": delta.get("statement"),
            "framework_refs": frameworks,
            "selection_refs": selection_refs,
            "operation_refs": operations,
            "artifact_refs": [str(value) for value in delta.get("artifact_refs", [])],
            "pre_contact_relation": pre_contact_relation,
            "target_return": target_return,
            "user_disposition": user_disposition,
        })

    for trace in round_record.get("artifact_traces", []):
        selection_refs = [str(value) for value in trace.get("selection_refs", [])]
        if workspace_ref not in selection_refs:
            continue
        frameworks = [str(value) for value in trace.get("framework_refs", [])]
        operations = [str(value) for value in trace.get("operation_refs", [])]
        _append_unique(framework_labels, frameworks)
        _append_unique(artifact_operations, operations)

        target_return = trace.get("target_return")
        if not isinstance(target_return, dict):
            target_return = {}
        return_state = str(target_return.get("state", "")).strip()
        if return_state:
            _append_unique(target_return_states, [return_state])

        user_disposition = trace.get("user_disposition")
        if not isinstance(user_disposition, dict):
            user_disposition = None
        if user_disposition is not None:
            state = str(user_disposition.get("state", "")).strip()
            if state:
                _append_unique(user_dispositions, [state])

        linked_artifacts.append({
            "artifact_ref": trace.get("artifact_ref"),
            "origin": trace.get("origin"),
            "framework_refs": frameworks,
            "selection_refs": selection_refs,
            "operation_refs": operations,
            "target_return": target_return,
            "user_disposition": user_disposition,
        })

    planned_operations: list[str] = []
    candidate_ids: list[str] = []
    for row in workspace.get("candidates", []):
        candidate_id = str(row.get("id", "")).strip()
        if candidate_id:
            candidate_ids.append(candidate_id)
        _append_unique(planned_operations, row.get("planned_operations", []))

    candidate_id_set = set(candidate_ids)
    unmatched_framework_labels = [
        value for value in framework_labels if value not in candidate_id_set
    ]

    candidate_audits: list[dict[str, Any]] = []
    for row in workspace.get("candidates", []):
        candidate_id = str(row.get("id", "")).strip()
        if not candidate_id:
            continue

        planned_for_candidate: list[str] = []
        _append_unique(planned_for_candidate, row.get("planned_operations", []))

        contacts_for_candidate = [
            contact
            for contact in linked_contacts
            if contact["framework"] == candidate_id
        ]
        deltas_for_candidate = [
            delta
            for delta in linked_deltas
            if candidate_id in delta["framework_refs"]
        ]
        artifacts_for_candidate = [
            trace
            for trace in linked_artifacts
            if candidate_id in trace["framework_refs"]
        ]

        contact_operations_for_candidate: list[str] = []
        delta_operations_for_candidate: list[str] = []
        artifact_operations_for_candidate: list[str] = []
        delta_kinds_for_candidate: list[str] = []
        delta_pre_contact_states_for_candidate: list[str] = []
        delta_return_states_for_candidate: list[str] = []
        delta_dispositions_for_candidate: list[str] = []
        return_states_for_candidate: list[str] = []
        dispositions_for_candidate: list[str] = []

        for contact in contacts_for_candidate:
            _append_unique(
                contact_operations_for_candidate,
                contact["operations"],
            )
        for delta in deltas_for_candidate:
            _append_unique(
                delta_operations_for_candidate,
                delta["operation_refs"],
            )
            kind = str(delta.get("kind", "")).strip()
            if kind:
                _append_unique(delta_kinds_for_candidate, [kind])
            pre_contact = delta.get("pre_contact_relation")
            if isinstance(pre_contact, dict):
                pre_contact_state = str(pre_contact.get("state", "")).strip()
                if pre_contact_state:
                    _append_unique(
                        delta_pre_contact_states_for_candidate,
                        [pre_contact_state],
                    )
            state = str(delta["target_return"].get("state", "")).strip()
            if state:
                _append_unique(delta_return_states_for_candidate, [state])
            disposition = delta.get("user_disposition")
            if isinstance(disposition, dict):
                disposition_state = str(disposition.get("state", "")).strip()
                if disposition_state:
                    _append_unique(
                        delta_dispositions_for_candidate,
                        [disposition_state],
                    )
        for trace in artifacts_for_candidate:
            _append_unique(
                artifact_operations_for_candidate,
                trace["operation_refs"],
            )
            state = str(trace["target_return"].get("state", "")).strip()
            if state:
                _append_unique(return_states_for_candidate, [state])
            disposition = trace.get("user_disposition")
            if isinstance(disposition, dict):
                disposition_state = str(disposition.get("state", "")).strip()
                if disposition_state:
                    _append_unique(
                        dispositions_for_candidate,
                        [disposition_state],
                    )

        candidate_audits.append({
            "candidate_id": candidate_id,
            "role": row.get("role"),
            "planned_operations": planned_for_candidate,
            "contact_operations": contact_operations_for_candidate,
            "delta_operations": delta_operations_for_candidate,
            "artifact_operations": artifact_operations_for_candidate,
            "delta_kinds": delta_kinds_for_candidate,
            "planned_not_contacted_exact": [
                value
                for value in planned_for_candidate
                if value not in contact_operations_for_candidate
            ],
            "contacted_not_delta_traced_exact": [
                value
                for value in contact_operations_for_candidate
                if value not in delta_operations_for_candidate
            ],
            "delta_not_contacted_exact": [
                value
                for value in delta_operations_for_candidate
                if value not in contact_operations_for_candidate
            ],
            "delta_not_artifact_traced_exact": [
                value
                for value in delta_operations_for_candidate
                if value not in artifact_operations_for_candidate
            ],
            "artifact_not_delta_traced_exact": [
                value
                for value in artifact_operations_for_candidate
                if value not in delta_operations_for_candidate
            ],
            "contacted_not_artifact_traced_exact": [
                value
                for value in contact_operations_for_candidate
                if value not in artifact_operations_for_candidate
            ],
            "artifact_not_contacted_exact": [
                value
                for value in artifact_operations_for_candidate
                if value not in contact_operations_for_candidate
            ],
            "linked_delta_refs": [
                str(delta.get("delta_ref", ""))
                for delta in deltas_for_candidate
                if str(delta.get("delta_ref", "")).strip()
            ],
            "linked_artifact_refs": [
                str(trace.get("artifact_ref", ""))
                for trace in artifacts_for_candidate
                if str(trace.get("artifact_ref", "")).strip()
            ],
            "delta_pre_contact_states": delta_pre_contact_states_for_candidate,
            "delta_target_return_states": delta_return_states_for_candidate,
            "delta_user_dispositions": delta_dispositions_for_candidate,
            "target_return_states": return_states_for_candidate,
            "user_dispositions": dispositions_for_candidate,
            "guardrails": dict(row.get("non_force_guardrails", {})),
            "contact_record": dict(row.get("contact_record", {})),
        })

    return {
        "format": "csw.framework-selection-living-lab-audit/v1",
        "workspace_ref": workspace_ref,
        "round_id": round_record.get("round_id"),
        "activation_scope": round_record.get("activation_scope"),
        "target_structure_hypotheses": [
            dict(row) for row in workspace.get("target_structure_hypotheses", [])
        ],
        "linked_contacts": linked_contacts,
        "linked_deltas": linked_deltas,
        "linked_artifacts": linked_artifacts,
        "planned_operations": planned_operations,
        "contacted_operations": contacted_operations,
        "delta_operations": delta_operations,
        "artifact_operations": artifact_operations,
        "delta_kinds": delta_kinds,
        "delta_target_return_states": delta_target_return_states,
        "delta_user_dispositions": delta_user_dispositions,
        "planned_not_contacted_exact": [
            value for value in planned_operations if value not in contacted_operations
        ],
        "contacted_not_artifact_traced_exact": [
            value for value in contacted_operations if value not in artifact_operations
        ],
        "artifact_not_contacted_exact": [
            value for value in artifact_operations if value not in contacted_operations
        ],
        "framework_labels": framework_labels,
        "framework_labels_without_exact_candidate_id_match": unmatched_framework_labels,
        "target_return_states": target_return_states,
        "user_dispositions": user_dispositions,
        "candidate_audits": candidate_audits,
        "no_framework_option": dict(workspace.get("no_framework_option", {})),
        "interpretation_boundary": (
            "This is an exact-string provenance inventory joining recorded selection "
            "reasoning to one Living Lab round. Presence or absence of a contact, "
            "operation, catalytic delta, pre-contact relation, artifact, target-return state, or user disposition does not "
            "establish usefulness, causation, correctness, guardrail compliance, or "
            "whether a framework should be activated. Return to the recorded target "
            "material and user evidence for interpretation."
        ),
    }


def cmd_list_target_structures(args: argparse.Namespace) -> None:
    print_json(
        target_structure_catalog_payload(
            load_typology(args.typology),
        )
    )


def cmd_structure_lookup(args: argparse.Namespace) -> None:
    print_json(
        target_structure_candidates_payload(
            load_typology(args.typology),
            load_inventory(args.inventory),
            args.target_structure_id,
        )
    )


def cmd_structure_contrast(args: argparse.Namespace) -> None:
    print_json(
        target_structure_contrast_payload(
            load_typology(args.typology),
            load_inventory(args.inventory),
            args.target_structure_id,
        )
    )


def cmd_set_target_structure(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    set_target_structure_hypothesis(
        data,
        load_typology(args.typology),
        args.target_structure_id,
        basis=args.basis,
    )
    save_workspace(args.workspace, data)
    print(args.target_structure_id)


def cmd_audit_target_structure(args: argparse.Namespace) -> None:
    print_json(
        target_structure_selection_audit_payload(
            load_workspace(args.workspace),
            load_typology(args.typology),
            load_inventory(args.inventory),
        )
    )


def cmd_audit_living_lab(args: argparse.Namespace) -> None:
    print_json(
        audit_living_lab_payload(
            load_workspace(args.workspace),
            load_living_lab_round(args.living_lab_round),
        )
    )


def cmd_audit_map(args: argparse.Namespace) -> None:
    print_json(
        audit_map_payload(
            load_workspace(args.workspace),
            load_affinity_map(args.affinity_map),
        )
    )


def cmd_set_candidate(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    update_candidate(
        data,
        args.candidate_id,
        role=args.role,
        job=args.job,
        difference=args.difference,
        de_bound=args.de_bound,
        revisit_if=args.revisit_if,
        planned_operations=args.operation,
        return_questions=args.return_question,
    )
    save_workspace(args.workspace, data)
    print(args.candidate_id)


def cmd_set_consideration(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    update_consideration(
        data,
        args.candidate_id,
        target_connection=args.target_connection,
        structural_difference=args.structural_difference,
        redundancy_or_overlap=args.redundancy,
        target_return_feasibility=args.target_return,
        misuse_or_authority_risk=args.misuse_risk,
        domain_constraint=args.domain_constraint,
    )
    save_workspace(args.workspace, data)
    print(args.candidate_id)


def cmd_set_guardrail(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    update_non_force_guardrail(
        data,
        args.candidate_id,
        contact_if=args.contact_if,
        stop_if=args.stop_if,
        survive_if=args.survive_if,
    )
    save_workspace(args.workspace, data)
    print(args.candidate_id)


def cmd_record_contact(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    record_contact_disposition(
        data,
        args.candidate_id,
        contacted=args.contacted,
        reason=args.reason,
    )
    save_workspace(args.workspace, data)
    print(args.candidate_id)


def cmd_set_non_activation(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    remained_viable_after_contact = None
    if args.remained_viable_after_contact:
        remained_viable_after_contact = True
    elif args.no_longer_viable_after_contact:
        remained_viable_after_contact = False
    update_non_activation(
        data,
        reason=args.reason,
        baseline_note=args.baseline_note,
        revisit_if=args.revisit_if,
        remained_viable_after_contact=remained_viable_after_contact,
        post_contact_note=args.post_contact_note,
    )
    save_workspace(args.workspace, data)
    print(args.workspace)


def cmd_review(args: argparse.Namespace) -> None:
    print_json(review_payload(load_workspace(args.workspace)))


def cmd_set_cross_framework(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    update_cross_framework(
        data,
        primary_job=args.primary_job,
        second_job=args.second_job,
        disturb=args.disturb,
        confusions=args.confusion,
        pushbacks=args.pushback,
    )
    save_workspace(args.workspace, data)
    print(args.workspace)


def cmd_record_exit(args: argparse.Namespace) -> None:
    data = load_workspace(args.workspace)
    add_exit_record(data, args.kind, args.text)
    save_workspace(args.workspace, data)
    print(args.kind)


def cmd_show(args: argparse.Namespace) -> None:
    print_json(load_workspace(args.workspace))


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Externalize CSW framework-selection reasoning without automatic routing."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser(
        "inspect",
        help=(
            "show one provenance-rich Registry-0 entry without scoring, ranking, "
            "activation, or routing"
        ),
    )
    inspect.add_argument("inventory", type=Path)
    inspect.add_argument("candidate_id")

    list_target_structures = sub.add_parser(
        "list-target-structures",
        help=(
            "show the provisional target-side structure vocabulary without selecting "
            "a framework"
        ),
    )
    list_target_structures.add_argument("typology", type=Path)
    list_target_structures.set_defaults(func=cmd_list_target_structures)

    structure_lookup = sub.add_parser(
        "structure-lookup",
        help=(
            "show exact typology mappings for explicit target-structure ids without "
            "semantic classification, scoring, or ranking"
        ),
    )
    structure_lookup.add_argument("typology", type=Path)
    structure_lookup.add_argument("inventory", type=Path)
    structure_lookup.add_argument("target_structure_id", nargs="+")
    structure_lookup.set_defaults(func=cmd_structure_lookup)

    structure_contrast = sub.add_parser(
        "structure-contrast",
        help=(
            "compare candidates mapped to explicit target-structure ids using exact "
            "mapping and exact operation overlap only, without scoring or ranking"
        ),
    )
    structure_contrast.add_argument("typology", type=Path)
    structure_contrast.add_argument("inventory", type=Path)
    structure_contrast.add_argument("target_structure_id", nargs="+")
    structure_contrast.set_defaults(func=cmd_structure_contrast)

    audit_target_structure = sub.add_parser(
        "audit-target-structure",
        help=(
            "audit saved candidate choices against the exact recorded target-structure "
            "snapshot without reinterpreting drifted typology"
        ),
    )
    audit_target_structure.add_argument("workspace", type=Path)
    audit_target_structure.add_argument("typology", type=Path)
    audit_target_structure.add_argument("inventory", type=Path)
    audit_target_structure.set_defaults(func=cmd_audit_target_structure)

    shortlist = sub.add_parser("shortlist")
    shortlist.add_argument("inventory", type=Path)
    shortlist.add_argument("term")
    shortlist.add_argument("--field", choices=tuple(SEARCH_FIELDS), default="all")
    shortlist.add_argument("--readiness", action="append")

    recall = sub.add_parser("recall")
    recall.add_argument("inventory", type=Path)
    recall.add_argument("--need", required=True)
    recall.add_argument(
        "--readiness",
        action="append",
        help="readiness states to include; defaults to adopted only",
    )

    contrast = sub.add_parser("contrast")
    contrast.add_argument("inventory", type=Path)
    contrast.add_argument("candidate_id", nargs="+")

    worksheet = sub.add_parser("worksheet")
    worksheet.add_argument("inventory", type=Path)
    worksheet.add_argument("--need", required=True)
    worksheet.add_argument("--candidate", action="append", required=True)
    worksheet.add_argument("--baseline")
    worksheet.add_argument(
        "--output",
        type=Path,
        help="write the new workspace atomically instead of printing it",
    )
    worksheet.add_argument(
        "--ref",
        dest="workspace_ref",
        help="stable provenance handle that downstream catalytic traces may reuse",
    )

    audit_map = sub.add_parser("audit-map")
    audit_map.add_argument("workspace", type=Path)
    audit_map.add_argument("affinity_map", type=Path)
    audit_map.set_defaults(func=cmd_audit_map)

    audit_living_lab = sub.add_parser(
        "audit-living-lab",
        help=(
            "join a selection workspace to one Living Lab round by exact selection_ref "
            "without evaluating framework effectiveness"
        ),
    )
    audit_living_lab.add_argument("workspace", type=Path)
    audit_living_lab.add_argument("living_lab_round", type=Path)
    audit_living_lab.set_defaults(func=cmd_audit_living_lab)

    set_target_structure = sub.add_parser(
        "set-target-structure",
        help=(
            "record an explicit provisional target-structure hypothesis in the "
            "selection workspace"
        ),
    )
    set_target_structure.add_argument("workspace", type=Path)
    set_target_structure.add_argument("typology", type=Path)
    set_target_structure.add_argument("target_structure_id")
    set_target_structure.add_argument("--basis")
    set_target_structure.set_defaults(func=cmd_set_target_structure)

    set_candidate = sub.add_parser("set-candidate")
    set_candidate.add_argument("workspace", type=Path)
    set_candidate.add_argument("candidate_id")
    set_candidate.add_argument("--role")
    set_candidate.add_argument("--job")
    set_candidate.add_argument("--difference")
    set_candidate.add_argument("--de-bound")
    set_candidate.add_argument("--revisit-if")
    set_candidate.add_argument(
        "--operation",
        action="append",
        help="explicit inventory operation to try; must exist for the candidate",
    )
    set_candidate.add_argument("--return-question", action="append")
    set_candidate.set_defaults(func=cmd_set_candidate)

    set_consideration = sub.add_parser("set-consideration")
    set_consideration.add_argument("workspace", type=Path)
    set_consideration.add_argument("candidate_id")
    set_consideration.add_argument("--target-connection")
    set_consideration.add_argument("--structural-difference")
    set_consideration.add_argument("--redundancy")
    set_consideration.add_argument("--target-return")
    set_consideration.add_argument("--misuse-risk")
    set_consideration.add_argument("--domain-constraint")
    set_consideration.set_defaults(func=cmd_set_consideration)

    set_guardrail = sub.add_parser(
        "set-guardrail",
        help=(
            "record explicit contact/stop/survival conditions without turning them "
            "into an automatic activation gate"
        ),
    )
    set_guardrail.add_argument("workspace", type=Path)
    set_guardrail.add_argument("candidate_id")
    set_guardrail.add_argument("--contact-if")
    set_guardrail.add_argument("--stop-if")
    set_guardrail.add_argument("--survive-if")
    set_guardrail.set_defaults(func=cmd_set_guardrail)

    record_contact = sub.add_parser(
        "record-contact",
        help=(
            "record whether a deliberately considered candidate was actually contacted, "
            "with a snapshot of the selection reasoning at that moment"
        ),
    )
    record_contact.add_argument("workspace", type=Path)
    record_contact.add_argument("candidate_id")
    contact_state = record_contact.add_mutually_exclusive_group(required=True)
    contact_state.add_argument(
        "--contacted",
        dest="contacted",
        action="store_true",
        help="record that framework contact occurred",
    )
    contact_state.add_argument(
        "--not-contacted",
        dest="contacted",
        action="store_false",
        help="record that the candidate was deliberately left unused",
    )
    record_contact.add_argument("--reason", required=True)
    record_contact.set_defaults(func=cmd_record_contact)

    set_non_activation = sub.add_parser("set-non-activation")
    set_non_activation.add_argument("workspace", type=Path)
    set_non_activation.add_argument("--reason")
    set_non_activation.add_argument("--baseline-note")
    set_non_activation.add_argument("--revisit-if")
    post_contact_viability = set_non_activation.add_mutually_exclusive_group()
    post_contact_viability.add_argument(
        "--remained-viable-after-contact",
        action="store_true",
        help="record that no-framework remained a viable option after framework contact",
    )
    post_contact_viability.add_argument(
        "--no-longer-viable-after-contact",
        action="store_true",
        help="record that no-framework was no longer viable after contact; this is provenance, not a recommendation",
    )
    set_non_activation.add_argument("--post-contact-note")
    set_non_activation.set_defaults(func=cmd_set_non_activation)

    review = sub.add_parser("review")
    review.add_argument("workspace", type=Path)
    review.set_defaults(func=cmd_review)

    set_cross = sub.add_parser("set-cross-framework")
    set_cross.add_argument("workspace", type=Path)
    set_cross.add_argument("--primary-job")
    set_cross.add_argument("--second-job")
    set_cross.add_argument("--disturb")
    set_cross.add_argument("--confusion", action="append")
    set_cross.add_argument("--pushback", action="append")
    set_cross.set_defaults(func=cmd_set_cross_framework)

    record_exit = sub.add_parser("record-exit")
    record_exit.add_argument("workspace", type=Path)
    record_exit.add_argument("--kind", choices=tuple(EXIT_RECORD_FIELDS), required=True)
    record_exit.add_argument("text")
    record_exit.set_defaults(func=cmd_record_exit)

    show = sub.add_parser("show")
    show.add_argument("workspace", type=Path)
    show.set_defaults(func=cmd_show)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command in {
            "list-target-structures",
            "structure-lookup",
            "structure-contrast",
            "set-target-structure",
            "audit-target-structure",
            "audit-map",
            "audit-living-lab",
            "set-candidate",
            "set-consideration",
            "set-guardrail",
            "record-contact",
            "set-non-activation",
            "set-cross-framework",
            "record-exit",
            "review",
            "show",
        }:
            args.func(args)
            return
        data = load_inventory(args.inventory)
        if args.command == "inspect":
            print_json(registry_entry_payload(data, args.candidate_id))
        elif args.command == "shortlist":
            print_json(shortlist_payload(data, args.term, args.field, args.readiness))
        elif args.command == "recall":
            print_json(recall_payload(data, args.need, args.readiness))
        elif args.command == "contrast":
            print_json(contrast_payload(data, args.candidate_id))
        elif args.command == "worksheet":
            payload = worksheet_payload(
                data,
                args.need,
                args.candidate,
                args.baseline,
                args.workspace_ref,
            )
            if args.output is not None:
                if args.output.exists():
                    raise ValueError(f"refusing to overwrite existing workspace: {args.output}")
                save_workspace(args.output, payload)
                print(args.output)
            else:
                print_json(payload)
        elif args.command == "set-candidate":
            cmd_set_candidate(args)
        elif args.command == "set-cross-framework":
            cmd_set_cross_framework(args)
        elif args.command == "record-exit":
            cmd_record_exit(args)
        elif args.command == "show":
            cmd_show(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
