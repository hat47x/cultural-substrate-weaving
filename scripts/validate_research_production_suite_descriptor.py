#!/usr/bin/env python3
"""Validate the design-only production suite promotion descriptor.

This checker validates promotion boundaries without requiring planned production
source paths to exist. It must not be used as evidence that production promotion
or public naming has been approved.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
EXPECTED_SCHEMA = "csw.production-suite-promotion-prototype/v1"
EXPECTED_SKILLS = {
    "cultural-substrate-weaving",
    "affinity-synthesis",
    "iterative-inquiry-synthesis",
}
FIRST_WAVE = {"openai_skill", "claude_plugin", "codex_plugin"}
DEFERRED_COMPOSITE = {"chatgpt_gpt", "microsoft_copilot"}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _is_research_path(value: str) -> bool:
    return PurePosixPath(value).parts[:2] == ("research", "skill-prototypes")


def _validate_name(value: object, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not (1 <= len(value) <= 64):
        errors.append(f"{label} must be a 1-64 character string")
        return None
    if not SKILL_NAME_RE.fullmatch(value):
        errors.append(
            f"{label} must use lowercase letters, numbers, and single hyphens only: {value!r}"
        )
        return None
    return value


def validate_production_suite_descriptor(descriptor: dict) -> list[str]:
    errors: list[str] = []
    if descriptor.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"descriptor schema must be {EXPECTED_SCHEMA}")
    if descriptor.get("status") != "design-only":
        errors.append("production promotion descriptor must remain status=design-only")
    if descriptor.get("version_source") != "VERSION":
        errors.append("production promotion descriptor version_source must remain VERSION")
    if descriptor.get("canonical_locale") != "ja-JP":
        errors.append("production promotion descriptor canonical_locale must remain ja-JP")
    if descriptor.get("locales") != ["ja-JP", "en-US"]:
        errors.append("production promotion descriptor locales must remain [ja-JP, en-US]")

    first_wave = descriptor.get("first_wave_distributions")
    if not isinstance(first_wave, list) or set(first_wave) != FIRST_WAVE or len(first_wave) != 3:
        errors.append(
            "first_wave_distributions must contain exactly openai_skill, claude_plugin, codex_plugin"
        )
    deferred = descriptor.get("deferred_composite_distributions")
    if (
        not isinstance(deferred, list)
        or set(deferred) != DEFERRED_COMPOSITE
        or len(deferred) != 2
    ):
        errors.append(
            "deferred_composite_distributions must contain exactly chatgpt_gpt and microsoft_copilot"
        )
    if isinstance(first_wave, list) and isinstance(deferred, list):
        overlap = set(first_wave) & set(deferred)
        if overlap:
            errors.append(f"first-wave and deferred distributions must not overlap: {sorted(overlap)}")

    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        return errors + ["production promotion descriptor skills must be a list"]
    ids = [skill.get("research_id") for skill in skills if isinstance(skill, dict)]
    if len(ids) != len(skills) or set(ids) != EXPECTED_SKILLS or len(ids) != len(set(ids)):
        errors.append("descriptor research_id set must contain exactly the three research suite Skills")

    public_names: list[str] = []
    openai_targets: list[str] = []
    claude_targets: list[str] = []
    codex_targets: list[str] = []

    for skill in skills:
        if not isinstance(skill, dict):
            continue
        research_id = skill.get("research_id")
        public_name = _validate_name(
            skill.get("proposed_installable_name"),
            f"skill {research_id} proposed_installable_name",
            errors,
        )
        if public_name is not None:
            public_names.append(public_name)

        source = skill.get("production_source")
        if not isinstance(source, dict):
            errors.append(f"skill {research_id} production_source must be an object")
        else:
            mode = source.get("mode")
            if research_id == "cultural-substrate-weaving":
                if mode != "canonical_manifest" or source.get("manifest") != "src/manifest.json":
                    errors.append(
                        "cultural-substrate-weaving production_source must keep canonical_manifest src/manifest.json"
                    )
            else:
                root_pattern = source.get("root_pattern")
                if mode != "locale_tree":
                    errors.append(f"skill {research_id} sibling production_source must use locale_tree")
                if not isinstance(root_pattern, str) or not root_pattern.startswith("src/skills/"):
                    errors.append(
                        f"skill {research_id} sibling production root must stay under src/skills/"
                    )
                elif _is_research_path(root_pattern):
                    errors.append(f"skill {research_id} production root must not point into research")
                if isinstance(root_pattern, str) and "{locale}" not in root_pattern:
                    errors.append(f"skill {research_id} production root_pattern must include {{locale}}")
                if source.get("runtime_entry") != "SKILL.md":
                    errors.append(f"skill {research_id} production runtime_entry must be SKILL.md")

        targets = skill.get("targets")
        if not isinstance(targets, dict) or set(targets) != FIRST_WAVE:
            errors.append(f"skill {research_id} targets must declare exactly the first-wave distributions")
        else:
            openai = _validate_name(
                targets.get("openai_skill"),
                f"skill {research_id} OpenAI target",
                errors,
            )
            claude = _validate_name(
                targets.get("claude_plugin"),
                f"skill {research_id} Claude target",
                errors,
            )
            codex = _validate_name(
                targets.get("codex_plugin"),
                f"skill {research_id} Codex target",
                errors,
            )
            if openai:
                openai_targets.append(openai)
            if claude:
                claude_targets.append(claude)
            if codex:
                codex_targets.append(codex)

        adapter_metadata = skill.get("adapter_metadata")
        if not isinstance(adapter_metadata, dict) or set(adapter_metadata) != FIRST_WAVE:
            errors.append(
                f"skill {research_id} adapter_metadata must declare exactly the first-wave distributions"
            )
        elif research_id != "cultural-substrate-weaving":
            openai_meta = adapter_metadata.get("openai_skill")
            if isinstance(openai_meta, dict):
                source_pattern = openai_meta.get("source_pattern")
                if not isinstance(source_pattern, str) or not source_pattern.startswith(
                    "adapters/openai-skill/"
                ):
                    errors.append(
                        f"skill {research_id} promoted OpenAI metadata must live under adapters/openai-skill/"
                    )
                elif _is_research_path(source_pattern):
                    errors.append(
                        f"skill {research_id} production adapter metadata must not point into research"
                    )

    if len(public_names) != len(set(public_names)):
        errors.append("proposed_installable_name values must be unique")
    for label, values in (
        ("OpenAI", openai_targets),
        ("Claude", claude_targets),
        ("Codex", codex_targets),
    ):
        if len(values) != len(set(values)):
            errors.append(f"{label} production Skill target names must be unique")

    by_id = {
        skill.get("research_id"): skill
        for skill in skills
        if isinstance(skill, dict) and isinstance(skill.get("research_id"), str)
    }
    affinity = by_id.get("affinity-synthesis", {})
    if affinity.get("proposed_installable_name") != "material-led-synthesis":
        errors.append(
            "Layer 1 production candidate must remain material-led-synthesis until the public-name gate is deliberately revised"
        )
    iterative = by_id.get("iterative-inquiry-synthesis", {})
    if iterative.get("proposed_installable_name") != "iterative-inquiry-synthesis":
        errors.append(
            "Layer 2 production candidate must remain iterative-inquiry-synthesis until the public-name gate is deliberately revised"
        )

    forbidden = descriptor.get("forbidden_production_inputs")
    if not isinstance(forbidden, list) or not forbidden:
        errors.append("forbidden_production_inputs must be a non-empty list")
    else:
        for value in forbidden:
            if not _safe_repo_relative(value):
                errors.append(f"invalid forbidden production input path: {value!r}")
            elif not _is_research_path(value):
                errors.append(
                    f"forbidden production input must identify a research/skill-prototypes path: {value}"
                )

    release_shape = descriptor.get("release_shape")
    required_release_flags = {
        "keep_existing_distribution_package_kinds": True,
        "openai_package_contains_three_standalone_skills": True,
        "claude_package_contains_three_skill_subtrees": True,
        "codex_reuses_claude_plugin_skill_tree": True,
        "add_new_codex_release_zip_kind": False,
        "marketplace_generation_in_first_builder_change": False,
    }
    if not isinstance(release_shape, dict):
        errors.append("release_shape must be an object")
    else:
        for key, expected in required_release_flags.items():
            if release_shape.get(key) is not expected:
                errors.append(f"release_shape.{key} must remain {expected!r}")

    note = descriptor.get("note")
    if not isinstance(note, str) or "not a production manifest" not in note:
        errors.append("descriptor note must explicitly state that it is not a production manifest")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research production suite descriptor validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_suite_descriptor(descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research production suite promotion descriptor validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
