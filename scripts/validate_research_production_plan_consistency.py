#!/usr/bin/env python3
"""Check that prose P4 plans still reflect machine-readable production contracts.

The machine-readable production descriptor and builder contract remain the
source of truth. This validator prevents maintainer prose from drifting back to
superseded production-source, public-name, or package-closure semantics.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "skill-prototypes"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
CONTRACT_PATH = BASE / "P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
PROMOTION_PLAN_PATH = BASE / "P4-PRODUCTION-SOURCE-AND-BUILDER-PROMOTION-PLAN-2026-09-07.md"
CONSOLIDATION_PATH = BASE / "P4-PRODUCTION-SOURCE-CONTRACT-CONSOLIDATION-2026-09-08.md"
STATIC_PLAN_PATH = BASE / "P4-PRODUCTION-BUILDER-STATIC-PLAN-2026-09-07.md"

COMMON_REQUIRED_MARKERS = (
    "material-led-synthesis",
    "locale_tree",
)
COMMON_FORBIDDEN_MARKERS = (
    "src/skills/affinity-synthesis/",
    "adapters/openai-skill/<locale>/affinity-synthesis/",
)
DOCUMENT_RULES = {
    "promotion plan": {
        "path": PROMOTION_PLAN_PATH,
        "required": (
            "`canonical_manifest` mode",
            "`locale_tree` mode",
            "package-closed source boundary",
            "builder側で除外する」設計にはしない",
            "src/skills/material-led-synthesis/",
            "adapters/openai-skill/<locale>/material-led-synthesis/",
        ),
        "forbidden": (
            "Sibling entryはproduction `src/skills/...` を指す `explicit_files` modeでよい。",
            *COMMON_FORBIDDEN_MARKERS,
        ),
    },
    "source contract consolidation": {
        "path": CONSOLIDATION_PATH,
        "required": (
            "production source modeは二種類",
            "`canonical_manifest`",
            "`locale_tree`",
            "public candidate: material-led-synthesis",
            "src/skills/material-led-synthesis/{locale}",
        ),
        "forbidden": COMMON_FORBIDDEN_MARKERS,
    },
    "builder static plan": {
        "path": STATIC_PLAN_PATH,
        "required": (
            "### `canonical_manifest`",
            "### `locale_tree`",
            "src/skills/<public-name>/<locale>/",
            "material-led-synthesis",
            "research sourceの `affinity-synthesis` をそのままproductionへcopyしない",
        ),
        "forbidden": COMMON_FORBIDDEN_MARKERS,
    },
}


def validate_production_plan_consistency(
    descriptor: dict,
    contract: dict,
    documents: dict[str, str],
) -> list[str]:
    errors: list[str] = []

    operations = contract.get("source_mode_operations")
    if not isinstance(operations, dict) or operations.get("locale_tree") != (
        "copy_locale_tree_preserving_runtime_relative_paths"
    ):
        errors.append("builder contract must define locale_tree copy semantics before plan comparison")

    validation_requirements = contract.get("validation_requirements")
    if (
        not isinstance(validation_requirements, dict)
        or validation_requirements.get("locale_tree_source_package_purity") is not True
    ):
        errors.append("builder contract must keep locale_tree source package-purity validation enabled")

    invariants = contract.get("invariants")
    joined_invariants = "\n".join(invariants) if isinstance(invariants, list) else ""
    for marker in (
        "each locale-tree source root is package-closed",
        "without a research-only exclusion filter",
    ):
        if marker not in joined_invariants:
            errors.append(f"builder contract missing locale_tree package-closure invariant: {marker}")

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

    for label, rules in DOCUMENT_RULES.items():
        text = documents.get(label)
        if not isinstance(text, str):
            errors.append(f"production consistency document is missing: {label}")
            continue
        for marker in (*COMMON_REQUIRED_MARKERS, *rules["required"]):
            if marker not in text:
                errors.append(f"{label} missing current-contract marker: {marker}")
        for marker in rules["forbidden"]:
            if marker in text:
                errors.append(f"{label} contains stale-contract marker: {marker}")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        documents = {
            label: rules["path"].read_text(encoding="utf-8")
            for label, rules in DOCUMENT_RULES.items()
        }
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production plan consistency validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_plan_consistency(descriptor, contract, documents)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research P4 prose plans match machine-readable production source contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
