#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_living_lab import ROOT, ValidationError, load_record, validate_record_set

PUBLIC_OBSERVATIONS = ROOT / "research" / "living-lab" / "observations"
DEFAULT_OUTPUT = ROOT / "dist" / "reports" / "living-lab-observation-summary.json"


def _counter(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Create a review inventory without scoring or collapsing observations into judgments."""
    validate_record_set(records)

    rounds = sorted(
        (record for record in records if "round_id" in record and "event_id" not in record),
        key=lambda item: (item["observed_at"], item["round_id"]),
    )
    events = sorted(
        (record for record in records if "event_id" in record),
        key=lambda item: (item["recorded_at"], item["event_id"]),
    )

    events_by_round: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        events_by_round[event["round_id"]].append(event)

    round_inventory: list[dict[str, Any]] = []
    for round_record in rounds:
        round_events = events_by_round.get(round_record["round_id"], [])
        round_inventory.append(
            {
                "round_id": round_record["round_id"],
                "case_id": round_record["case_id"],
                "observed_at": round_record["observed_at"],
                "mode": round_record["mode"],
                "activation_scope": round_record["activation_scope"],
                "task_domain": round_record["task"].get("domain"),
                "task_summary": round_record["task"]["summary"],
                "task_constraints": round_record["task"].get("constraints", []),
                "framework_contacts": round_record["framework_contacts"],
                "artifacts": round_record["artifacts"],
                "residuals": round_record["residuals"],
                "reopening_conditions": round_record["reopening_conditions"],
                "interpretations": round_record.get("interpretations", []),
                "events": [
                    {
                        "event_id": event["event_id"],
                        "event_type": event["event_type"],
                        "observation_mode": event["observation_mode"],
                        "recorded_at": event["recorded_at"],
                        "observation": event["observation"],
                        "interpretations": event.get("interpretations", []),
                        "reopening_condition": event.get("reopening_condition"),
                    }
                    for event in round_events
                ],
            }
        )

    task_domains = [
        record["task"]["domain"]
        for record in rounds
        if isinstance(record["task"].get("domain"), str) and record["task"]["domain"].strip()
    ]

    interpretation_sources = [
        interpretation["source_type"]
        for record in rounds
        for interpretation in record.get("interpretations", [])
    ] + [
        interpretation["source_type"]
        for event in events
        for interpretation in event.get("interpretations", [])
    ]

    return {
        "schema_version": "0.2",
        "interpretation_note": (
            "This is an inventory for review. Counts and distributions are operational context only, "
            "not KPIs, scores, win/loss labels, judgments of usefulness or harm, or proof of causal effect. "
            "Activation state does not establish whether that state was appropriate. Interpretations remain "
            "attributed to their recorded source and are not measurements."
        ),
        "record_ids": {
            "rounds": [record["round_id"] for record in rounds],
            "events": [record["event_id"] for record in events],
        },
        "inventory": {
            "task_domains": _counter(task_domains),
            "modes": _counter([record["mode"] for record in rounds]),
            "activation_scopes": _counter([record["activation_scope"] for record in rounds]),
            "event_types": _counter([record["event_type"] for record in events]),
            "observation_modes": _counter([record["observation_mode"] for record in events]),
            "interpretation_source_types": _counter(interpretation_sources),
        },
        "rounds": round_inventory,
    }


def load_records(paths: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        _, data = load_record(path)
        records.append(data)
    return records


def default_paths() -> list[Path]:
    return sorted(PUBLIC_OBSERVATIONS.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Living Lab records as a non-scoring review inventory."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Round/event JSON files")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path (default: dist/reports/living-lab-observation-summary.json)",
    )
    args = parser.parse_args()

    paths = args.paths or default_paths()
    if not paths:
        print("Living Lab summary failed: no records found")
        return 1

    try:
        summary = summarize(load_records(paths))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Living Lab summary failed: {exc}")
        return 1

    print(f"Wrote Living Lab review inventory: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
