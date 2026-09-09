#!/usr/bin/env python3
"""Validate future three-Skill release composition without changing release code."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "skill-prototypes"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
PLAN_PATH = BASE / "P4-RELEASE-INTERNAL-COMPOSITION-PLAN-2026-09-07.md"
PACKAGE_PATH = ROOT / "scripts" / "package.py"

EXPECTED_PACKAGE_PATTERNS = (
    "cultural-substrate-weaving-openai-interactive-{suffix}-v{v}.zip",
    "cultural-substrate-weaving-openai-metered-{suffix}-v{v}.zip",
    "cultural-substrate-weaving-claude-plugin-{suffix}-v{v}.zip",
)


def _declared_target_names(
    descriptor: dict,
    distribution: str,
    errors: list[str],
) -> tuple[str, ...]:
    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        errors.append("production descriptor skills must be a list")
        return ()

    names: list[str] = []
    for item in skills:
        if not isinstance(item, dict):
            errors.append("production descriptor Skill entries must be objects")
            continue
        research_id = item.get("research_id")
        targets = item.get("targets")
        if not isinstance(targets, dict):
            errors.append(f"production descriptor targets missing for {research_id}")
            continue
        target = targets.get(distribution)
        if not isinstance(target, str) or not target:
            errors.append(
                f"production descriptor target missing for {research_id}/{distribution}"
            )
            continue
        names.append(target)

    if len(names) != len(set(names)):
        errors.append(f"production descriptor has duplicate {distribution} Skill targets")
    return tuple(names)


def _renamed_research_ids(descriptor: dict) -> tuple[str, ...]:
    renamed: list[str] = []
    for item in descriptor.get("skills", []):
        if not isinstance(item, dict):
            continue
        research_id = item.get("research_id")
        production_name = item.get("proposed_installable_name")
        if (
            isinstance(research_id, str)
            and isinstance(production_name, str)
            and research_id
            and production_name
            and research_id != production_name
        ):
            renamed.append(research_id)
    return tuple(renamed)


def validate_release_composition_plan(
    descriptor: dict,
    plan_text: str,
    package_text: str,
) -> list[str]:
    errors: list[str] = []
    release_shape = descriptor.get("release_shape")
    required_flags = {
        "keep_existing_distribution_package_kinds": True,
        "openai_package_contains_three_standalone_skills": True,
        "claude_package_contains_three_skill_subtrees": True,
        "codex_reuses_claude_plugin_skill_tree": True,
        "add_new_codex_release_zip_kind": False,
        "marketplace_generation_in_first_builder_change": False,
    }
    if not isinstance(release_shape, dict):
        errors.append("production descriptor release_shape must be an object")
    else:
        for key, expected in required_flags.items():
            if release_shape.get(key) is not expected:
                errors.append(f"release_shape.{key} must remain {expected!r}")

    openai_skills = _declared_target_names(descriptor, "openai_skill", errors)
    claude_skills = _declared_target_names(descriptor, "claude_plugin", errors)
    codex_skills = _declared_target_names(descriptor, "codex_plugin", errors)

    if len(openai_skills) != 3:
        errors.append("three-Skill release must declare exactly three OpenAI Skill targets")
    if len(claude_skills) != 3:
        errors.append("three-Skill release must declare exactly three Claude Skill targets")
    if codex_skills != claude_skills:
        errors.append("Codex release Skill targets must match Claude subtree targets")

    for skill_name in openai_skills:
        marker = f"{skill_name}/"
        if marker not in plan_text:
            errors.append(f"release composition plan missing OpenAI Skill directory: {skill_name}")
    for skill_name in claude_skills:
        marker = f"    {skill_name}/"
        if marker not in plan_text:
            errors.append(f"release composition plan missing Claude Skill subtree: {skill_name}")

    required_plan_markers = (
        "openai-interactive",
        "openai-metered",
        "disable-model-invocation: true",
        "skills = ./skills/",
        "新しいrelease ZIP kindは作らない",
        "cultural-substrate-weaving-openai-interactive-<locale>-v<version>.zip",
        "cultural-substrate-weaving-openai-metered-<locale>-v<version>.zip",
        "cultural-substrate-weaving-claude-plugin-<locale>-v<version>.zip",
    )
    for marker in required_plan_markers:
        if marker not in plan_text:
            errors.append(f"release composition plan missing required marker: {marker}")

    forbidden_plan_markers = [
        "cultural-substrate-weaving-codex-plugin-<locale>-v<version>.zip",
    ]
    for research_id in _renamed_research_ids(descriptor):
        forbidden_plan_markers.extend(
            (
                f"{research_id}/\n  SKILL.md",
                f"skills/\n    {research_id}/",
            )
        )
    for marker in forbidden_plan_markers:
        if marker in plan_text:
            errors.append(f"release composition plan contains stale/forbidden marker: {marker}")

    for pattern in EXPECTED_PACKAGE_PATTERNS:
        if pattern not in package_text:
            errors.append(f"current package.py no longer preserves expected package filename family: {pattern}")

    if "cultural-substrate-weaving-codex" in package_text:
        errors.append("current package.py must not introduce a separate Codex release ZIP kind")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        plan_text = PLAN_PATH.read_text(encoding="utf-8")
        package_text = PACKAGE_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research release composition validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_release_composition_plan(descriptor, plan_text, package_text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research release internal composition plan validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
