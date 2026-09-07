#!/usr/bin/env python3
"""Check that the prose production plan still reflects machine-readable P4 contracts.

The machine-readable production descriptor and builder contract remain the
source of truth. This validator only prevents the maintainer plan from drifting
back to superseded production-source semantics.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
CONTRACT_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
PLAN_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SOURCE-AND-BUILDER-PROMOTION-PLAN-2026-09-07.md"

REQUIRED_PLAN_MARKERS = (
    "`canonical_manifest` mode",
    "`locale_tree` mode",
    "package-closed source boundary",
    "builder側で除外する」設計にはしない",
    "src/skills/material-led-synthesis/",
    "adapters/openai-skill/<locale>/material-led-synthesis/",
)
FORBIDDEN_STALE_PLAN_MARKERS = (
    "Sibling entryはproduction `src/skills/...` を指す `explicit_files` modeでよい。",
    "src/skills/affinity-synthesis/",
    "adapters/openai-skill/<locale>/affinity-synthesis/",
)


def validate_production_plan_consistency(
    descriptor: dict,
    contract: dict,
    plan_text: str,
) -> list[str]:
    errors: list[str] = []

    operations = contract.get("source_mode_operations")
    if not isinstance(operations, dict) or operations.get("locale_tree") != (
        "copy_locale_tree_preserving_runtime_relative_paths"
    ):
        errors.append("builder contract must define locale_tree copy semantics before plan comparison")

    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        errors.append("production descriptor skills must be a list")
    else:
        for skill in skills:
            if not isinstance(skill, dict):
                continue
            research_id = skill.get("research_id")
            source = skill.get("production_source")
            if research_id == "cultural-substrate-weaving":
                if not isinstance(source, dict) or source.get("mode") != "canonical_manifest":
                    errors.append("CSW descriptor source mode must remain canonical_manifest")
            else:
                if not isinstance(source, dict) or source.get("mode") != "locale_tree":
                    errors.append(
                        f"descriptor sibling source mode must remain locale_tree: {research_id}"
                    )

    for marker in REQUIRED_PLAN_MARKERS:
        if marker not in plan_text:
            errors.append(f"production promotion plan missing current-contract marker: {marker}")

    for marker in FORBIDDEN_STALE_PLAN_MARKERS:
        if marker in plan_text:
            errors.append(f"production promotion plan contains stale-contract marker: {marker}")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        plan_text = PLAN_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production plan consistency validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_plan_consistency(descriptor, contract, plan_text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research production promotion plan matches machine-readable source-mode contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
