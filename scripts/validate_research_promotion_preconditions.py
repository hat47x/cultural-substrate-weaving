#!/usr/bin/env python3
"""Validate promotion preconditions in the design-only production descriptor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)

EVIDENCE_BINDING_PRECONDITION = (
    "complete-checkout PASS evidence stays bound to the validated commit with at most one "
    "evidence-only recording child"
)

REQUIRED_PRECONDITIONS = frozenset(
    {
        "translation-manifest source hashes are refreshed after the latest canonical Japanese changes",
        "complete-checkout research-skill-check passes",
        EVIDENCE_BINDING_PRECONDITION,
        "public installable names are rechecked immediately before canonical promotion",
        "English sibling Skill realizations receive independent review",
        "research prototype metadata is promoted into production adapter paths rather than read directly by production build",
        "production builder and validator are generalized with generated-artifact diff review",
        "release validation checks internal three-Skill composition before public promotion",
    }
)


def validate_promotion_preconditions(descriptor: dict) -> list[str]:
    errors: list[str] = []
    values = descriptor.get("promotion_preconditions")
    if not isinstance(values, list) or not values:
        return ["promotion_preconditions must be a non-empty list"]
    if not all(isinstance(value, str) and value.strip() for value in values):
        errors.append("promotion_preconditions must contain only non-empty strings")
        return errors
    if len(values) != len(set(values)):
        errors.append("promotion_preconditions must not contain duplicates")

    missing = sorted(REQUIRED_PRECONDITIONS - set(values))
    if missing:
        errors.append(f"promotion_preconditions is missing required conditions: {missing}")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"promotion-precondition validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_promotion_preconditions(descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research production promotion preconditions validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
