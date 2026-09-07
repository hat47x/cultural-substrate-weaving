#!/usr/bin/env python3
"""Validate the design-only research-id -> production-name migration contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
)
EXPECTED_SCHEMA = "csw.public-name-migration-contract/v1"
EXPECTED_RESEARCH_IDS = {
    "cultural-substrate-weaving",
    "affinity-synthesis",
    "iterative-inquiry-synthesis",
}
REQUIRED_POLICY = {
    "research_ids_remain_research_only": True,
    "research_history_is_not_renamed": True,
    "production_frontmatter_uses_production_name": True,
    "production_explicit_skill_references_use_production_name": True,
    "production_runtime_filesystem_sibling_paths_forbidden": True,
    "production_research_path_references_forbidden": True,
    "display_names_are_not_installable_identifiers": True,
    "compatibility_alias_directory_is_not_created_by_default": True,
}


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_public_name_migration(root: Path, contract: dict) -> list[str]:
    errors: list[str] = []

    if contract.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"public-name migration schema must be {EXPECTED_SCHEMA}")
    if contract.get("status") != "design-only":
        errors.append("public-name migration contract must remain status=design-only")

    descriptor_relative = contract.get("descriptor")
    if not isinstance(descriptor_relative, str) or not descriptor_relative:
        return errors + ["public-name migration descriptor must be a repository-relative path"]
    descriptor_path = (root / descriptor_relative).resolve()
    if not descriptor_path.is_relative_to(root.resolve()):
        return errors + ["public-name migration descriptor must remain inside repository"]
    if not descriptor_path.is_file():
        return errors + [f"public-name migration descriptor is missing: {descriptor_relative}"]

    try:
        descriptor = _load_json(descriptor_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return errors + [f"cannot read production descriptor for public-name migration: {exc}"]

    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        return errors + ["production descriptor skills must be a list"]
    derived = {
        skill.get("research_id"): skill.get("proposed_installable_name")
        for skill in skills
        if isinstance(skill, dict)
        and isinstance(skill.get("research_id"), str)
        and isinstance(skill.get("proposed_installable_name"), str)
    }

    mapping = contract.get("research_to_production_name")
    if not isinstance(mapping, dict):
        errors.append("research_to_production_name must be an object")
        mapping = {}
    if set(mapping) != EXPECTED_RESEARCH_IDS:
        errors.append(
            "research_to_production_name must contain exactly the three research IDs"
        )
    if mapping != derived:
        errors.append(
            "research_to_production_name must exactly match production descriptor proposed_installable_name values"
        )

    if mapping.get("affinity-synthesis") != "material-led-synthesis":
        errors.append(
            "Layer 1 migration must remain affinity-synthesis -> material-led-synthesis until the public-name gate is deliberately revised"
        )
    if mapping.get("iterative-inquiry-synthesis") != "iterative-inquiry-synthesis":
        errors.append(
            "Layer 2 migration must keep iterative-inquiry-synthesis until its public-name gate is deliberately revised"
        )

    production_names = [value for value in mapping.values() if isinstance(value, str)]
    if len(production_names) != len(set(production_names)):
        errors.append("production names in migration contract must be unique")

    policy = contract.get("policy")
    if not isinstance(policy, dict):
        errors.append("public-name migration policy must be an object")
    else:
        for key, expected in REQUIRED_POLICY.items():
            if policy.get(key) is not expected:
                errors.append(f"public-name migration policy.{key} must remain {expected!r}")

    display_terms = contract.get("display_terms")
    if not isinstance(display_terms, dict):
        errors.append("display_terms must be an object")
    else:
        affinity_display = display_terms.get("affinity-synthesis")
        if not isinstance(affinity_display, dict):
            errors.append("display_terms must preserve affinity-synthesis display names separately")
        else:
            if affinity_display.get("en") != "Affinity Synthesis":
                errors.append("Layer 1 English display term must remain Affinity Synthesis")
            if affinity_display.get("ja") != "親和統合":
                errors.append("Layer 1 Japanese display term must remain 親和統合")

    prefixes = contract.get("forbidden_production_reference_prefixes")
    expected_prefixes = {"research/skill-prototypes/", "../affinity-synthesis/"}
    if not isinstance(prefixes, list) or set(prefixes) != expected_prefixes:
        errors.append(
            "forbidden_production_reference_prefixes must protect research paths and sibling filesystem paths"
        )

    note = contract.get("note")
    if not isinstance(note, str) or "Research IDs and history remain stable" not in note:
        errors.append("public-name migration note must preserve research-history stability")

    return errors


def main() -> int:
    try:
        contract = _load_json(CONTRACT_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"research public-name migration validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_public_name_migration(ROOT, contract)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research public-name migration contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
