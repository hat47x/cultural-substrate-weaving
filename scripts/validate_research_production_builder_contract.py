#!/usr/bin/env python3
"""Validate the research-only production builder generalization contract.

The contract describes how a future production builder should compose the three
Skill suite. Passing this validator is not permission to modify production
sources or to promote the research prototypes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
)
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
EXPECTED_SCHEMA = "csw.production-builder-generalization-contract/v1"
EXPECTED_SOURCE_DESCRIPTOR = (
    "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
EXPECTED_PRODUCTION_FILES = {
    "builder": "scripts/build.py",
    "validator": "scripts/validate.py",
    "packager": "scripts/package.py",
    "planned_suite_descriptor": "src/skill-suite.json",
}
EXPECTED_SOURCE_OPERATIONS = {
    "canonical_manifest": "render_runtime_entry_and_copy_manifest_references",
    "locale_tree": "copy_locale_tree_preserving_runtime_relative_paths",
}
EXPECTED_VALIDATION_FLAGS = {
    "skill_composition",
    "sibling_source_generated_parity",
    "runtime_entry_budget_for_all_installed_skills",
    "installed_reference_closure_for_all_skill_subtrees",
    "release_internal_three_skill_composition",
    "existing_package_kind_set_is_preserved",
}
REQUIRED_INVARIANT_FRAGMENTS = (
    "must not read research/skill-prototypes",
    "src/manifest.json remains",
    "under src/skills",
    "do not default to research IDs",
    "interactive and metered",
    "three Skill subtrees",
    "reuses the Claude plugin Skill tree",
    "outside the first builder generalization",
    "does not create a new Codex release ZIP kind",
    "do not authorize production promotion",
)


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _contains_research_path(value: str) -> bool:
    return "research/skill-prototypes" in value


def validate_production_builder_contract(
    root: Path,
    contract: dict,
    descriptor: dict,
) -> list[str]:
    errors: list[str] = []

    if contract.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"builder contract schema must be {EXPECTED_SCHEMA}")
    if contract.get("status") != "design-only":
        errors.append("builder generalization contract must remain status=design-only")
    if contract.get("source_descriptor") != EXPECTED_SOURCE_DESCRIPTOR:
        errors.append("builder contract must reference the canonical production descriptor prototype")
    if contract.get("production_promotion_authorized") is not False:
        errors.append("builder contract must not authorize production promotion")

    production_files = contract.get("production_files")
    if production_files != EXPECTED_PRODUCTION_FILES:
        errors.append("builder contract production_files must keep the planned production boundary")
    elif isinstance(production_files, dict):
        for label, value in production_files.items():
            if not _safe_repo_relative(value):
                errors.append(f"builder contract {label} path is unsafe: {value!r}")
            if label != "planned_suite_descriptor" and not (root / value).is_file():
                errors.append(f"builder contract existing production file is missing: {value}")
            if _contains_research_path(value):
                errors.append(f"builder contract production file must not live in research: {value}")

    if contract.get("target_name_source") != "production_descriptor.skills[].targets":
        errors.append("production target names must be sourced from production_descriptor.skills[].targets")

    if contract.get("source_mode_operations") != EXPECTED_SOURCE_OPERATIONS:
        errors.append("builder contract source_mode_operations must preserve canonical_manifest and locale_tree separation")

    descriptor_first_wave = descriptor.get("first_wave_distributions")
    first_wave = contract.get("first_wave")
    if not isinstance(first_wave, dict) or set(first_wave) != set(descriptor_first_wave or []):
        errors.append("builder contract first_wave must match the production descriptor first-wave distributions")
    else:
        openai = first_wave.get("openai_skill", {})
        if openai.get("mode") != "standalone_per_skill":
            errors.append("OpenAI builder mode must remain standalone_per_skill")
        if openai.get("profiles") != ["interactive", "metered"]:
            errors.append("OpenAI builder profiles must remain interactive and metered")
        if openai.get("target_pattern") != "dist/{locale}/openai-skill/{profile}/{target_name}":
            errors.append("OpenAI target pattern must preserve the current locale/profile package shape")
        if openai.get("frontmatter_name_uses_target_name") is not True:
            errors.append("OpenAI Skill frontmatter name must use the production target name")

        claude = first_wave.get("claude_plugin", {})
        if claude.get("mode") != "locale_bundle":
            errors.append("Claude builder mode must remain locale_bundle")
        if claude.get("plugin_identity_source") != "production_descriptor.bundle_identity":
            errors.append("Claude plugin identity must come from production_descriptor.bundle_identity")
        if claude.get("target_pattern") != "plugins/{plugin_name}/skills/{target_name}":
            errors.append("Claude target pattern must preserve one locale plugin with Skill subtrees")
        if claude.get("marketplace_plugin_identity_is_preserved") is not True:
            errors.append("Claude marketplace plugin identity must remain preserved")

        codex = first_wave.get("codex_plugin", {})
        if codex.get("mode") != "reuse_claude_skill_tree":
            errors.append("Codex builder mode must reuse the Claude Skill tree")
        if codex.get("shared_skill_tree_distribution") != "claude_plugin":
            errors.append("Codex must identify claude_plugin as its shared Skill tree")
        if codex.get("target_pattern") != claude.get("target_pattern"):
            errors.append("Codex and Claude must resolve to the same plugin Skill subtree pattern")
        if codex.get("new_release_zip_kind") is not False:
            errors.append("Codex must not add a new release ZIP kind in the first wave")

    descriptor_deferred = descriptor.get("deferred_composite_distributions")
    deferred = contract.get("deferred_composite")
    if not isinstance(deferred, dict) or set(deferred) != set(descriptor_deferred or []):
        errors.append("builder contract deferred_composite must match descriptor deferred composites")
    else:
        for distribution_name, item in deferred.items():
            if not isinstance(item, dict) or item.get("first_wave_builder_change") is not False:
                errors.append(
                    f"deferred composite {distribution_name} must remain outside the first builder change"
                )

    validation_requirements = contract.get("validation_requirements")
    if not isinstance(validation_requirements, dict):
        errors.append("builder contract validation_requirements must be an object")
    else:
        if set(validation_requirements) != EXPECTED_VALIDATION_FLAGS:
            errors.append("builder contract validation_requirements set has drifted")
        for key in EXPECTED_VALIDATION_FLAGS:
            if validation_requirements.get(key) is not True:
                errors.append(f"builder contract validation requirement must remain enabled: {key}")

    invariants = contract.get("invariants")
    if not isinstance(invariants, list) or not all(isinstance(item, str) for item in invariants):
        errors.append("builder contract invariants must be a string list")
    else:
        joined = "\n".join(invariants)
        for fragment in REQUIRED_INVARIANT_FRAGMENTS:
            if fragment not in joined:
                errors.append(f"builder contract missing invariant fragment: {fragment}")

    release_shape = descriptor.get("release_shape", {})
    if isinstance(first_wave, dict):
        codex = first_wave.get("codex_plugin", {})
        if release_shape.get("codex_reuses_claude_plugin_skill_tree") is not True:
            errors.append("descriptor must preserve Codex/Claude shared Skill-tree release shape")
        if release_shape.get("add_new_codex_release_zip_kind") is not False:
            errors.append("descriptor must keep add_new_codex_release_zip_kind false")
        if codex.get("new_release_zip_kind") is not False:
            errors.append("builder contract and descriptor disagree on Codex release ZIP policy")

    skills = descriptor.get("skills")
    if isinstance(skills, list):
        for skill in skills:
            if not isinstance(skill, dict):
                continue
            targets = skill.get("targets")
            if not isinstance(targets, dict):
                continue
            for distribution in descriptor_first_wave or []:
                target_name = targets.get(distribution)
                if not isinstance(target_name, str) or not target_name:
                    errors.append(
                        f"descriptor skill {skill.get('research_id')} lacks production target for {distribution}"
                    )
    else:
        errors.append("production descriptor skills must be a list")

    note = contract.get("note")
    if not isinstance(note, str) or "Research-only static contract" not in note:
        errors.append("builder contract note must state its research-only static-contract boundary")

    return errors


def main() -> int:
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research production builder contract validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_builder_contract(ROOT, contract, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research production builder generalization contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
