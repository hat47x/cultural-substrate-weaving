#!/usr/bin/env python3
"""Validate research adapter-metadata declarations against the repository tree.

This checker keeps metadata provenance and planned/prototype/existing states honest.
It does not decide whether wording is production-ready or whether a package may release.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "research/skill-prototypes/adapter-metadata-plan.json"
EXPECTED_SCHEMA = "csw.research-adapter-metadata-plan/v1"
EXPECTED_BUNDLE_PROTOTYPE_SCHEMA = "csw.research-locale-bundle-metadata/v1"
ALLOWED_SOURCE_STATUS = {"planned", "prototype", "existing"}
ALLOWED_BUNDLE_STATUS = {"planned", "existing-baseline", "prototype", "reviewed"}
SKILL_TREE_MODES = {"standalone_per_skill", "locale_bundle"}


def _repo_path(root: Path, relative: object, field: str, errors: list[str]) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{field} must be a non-empty repository-relative path")
        return None
    path = (root / relative).resolve()
    resolved_root = root.resolve()
    if not path.is_relative_to(resolved_root):
        errors.append(f"{field} escapes repository root: {relative}")
        return None
    return path


def _load_json(path: Path, field: str, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{field} cannot be read as JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{field} must contain a JSON object")
        return None
    return value


def _set_mismatch(expected: set[str], actual: set[str]) -> str:
    return f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"


def _validate_openai(
    root: Path,
    config: dict,
    skill_ids: set[str],
    locales: set[str],
    errors: list[str],
) -> None:
    if config.get("scope") != "per_skill_per_profile":
        errors.append("openai_skill adapter metadata scope must be per_skill_per_profile")

    profiles = config.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        errors.append("openai_skill adapter metadata profiles must be a non-empty object")
        return
    profile_names = set(profiles)
    for profile, profile_config in profiles.items():
        if not isinstance(profile_config, dict):
            errors.append(f"openai_skill profile {profile} must be an object")
            continue
        expected_implicit = profile_config.get("expected_allow_implicit_invocation")
        if not isinstance(expected_implicit, bool):
            errors.append(
                f"openai_skill profile {profile} expected_allow_implicit_invocation must be boolean"
            )

    skills = config.get("skills")
    if not isinstance(skills, dict):
        errors.append("openai_skill adapter metadata skills must be an object")
        return
    if set(skills) != skill_ids:
        errors.append(
            "openai_skill adapter metadata skill ids must match suite skills; "
            + _set_mismatch(skill_ids, set(skills))
        )

    required_markers = (
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        "policy:",
    )

    for skill_id in sorted(skill_ids & set(skills)):
        locale_map = skills.get(skill_id)
        if not isinstance(locale_map, dict):
            errors.append(f"openai_skill metadata for {skill_id} must be an object")
            continue
        if set(locale_map) != locales:
            errors.append(
                f"openai_skill metadata locales for {skill_id} must match suite locales; "
                + _set_mismatch(locales, set(locale_map))
            )

        for locale in sorted(locales & set(locale_map)):
            profile_map = locale_map.get(locale)
            if not isinstance(profile_map, dict):
                errors.append(f"openai_skill metadata for {skill_id}/{locale} must be an object")
                continue
            if set(profile_map) != profile_names:
                errors.append(
                    f"openai_skill metadata profiles for {skill_id}/{locale} must match profiles; "
                    + _set_mismatch(profile_names, set(profile_map))
                )

            for profile in sorted(profile_names & set(profile_map)):
                entry = profile_map.get(profile)
                if not isinstance(entry, dict):
                    errors.append(
                        f"openai_skill metadata entry {skill_id}/{locale}/{profile} must be an object"
                    )
                    continue
                status = entry.get("status")
                if status not in ALLOWED_SOURCE_STATUS:
                    errors.append(
                        f"openai_skill metadata entry {skill_id}/{locale}/{profile} has invalid status: "
                        f"{status!r}"
                    )
                    continue

                source_relative = entry.get("source")
                if status == "planned":
                    if source_relative is not None:
                        errors.append(
                            f"planned openai_skill metadata {skill_id}/{locale}/{profile} "
                            "must not declare source"
                        )
                    continue

                source = _repo_path(
                    root,
                    source_relative,
                    f"openai_skill metadata source {skill_id}/{locale}/{profile}",
                    errors,
                )
                if source is None:
                    continue
                if not source.is_file():
                    errors.append(
                        f"openai_skill metadata source is missing for {skill_id}/{locale}/{profile}: "
                        f"{source_relative}"
                    )
                    continue
                text = source.read_text(encoding="utf-8")
                for marker in required_markers:
                    if marker not in text:
                        errors.append(
                            f"openai_skill metadata source {skill_id}/{locale}/{profile} "
                            f"is missing marker {marker!r}"
                        )
                profile_config = profiles.get(profile)
                if isinstance(profile_config, dict):
                    expected_implicit = profile_config.get(
                        "expected_allow_implicit_invocation"
                    )
                    if isinstance(expected_implicit, bool):
                        expected_line = (
                            "allow_implicit_invocation: true"
                            if expected_implicit
                            else "allow_implicit_invocation: false"
                        )
                        if expected_line not in text:
                            errors.append(
                                f"openai_skill metadata source {skill_id}/{locale}/{profile} "
                                f"must contain {expected_line!r}"
                            )


def _validate_bundle_prototype(
    root: Path,
    distribution_name: str,
    locale: str,
    entry: dict,
    suite_distribution: dict,
    baseline_catalog: dict | None,
    errors: list[str],
) -> None:
    source_relative = entry.get("prototype_source")
    source = _repo_path(
        root,
        source_relative,
        f"{distribution_name} prototype metadata source {locale}",
        errors,
    )
    if source is None:
        return
    if not source.is_file():
        errors.append(
            f"{distribution_name} prototype metadata source is missing for {locale}: "
            f"{source_relative}"
        )
        return
    prototype = _load_json(
        source,
        f"{distribution_name} prototype metadata source {locale}",
        errors,
    )
    if prototype is None:
        return

    if prototype.get("schema") != EXPECTED_BUNDLE_PROTOTYPE_SCHEMA:
        errors.append(
            f"{distribution_name} prototype metadata {locale} schema must be "
            f"{EXPECTED_BUNDLE_PROTOTYPE_SCHEMA}"
        )
    if prototype.get("locale") != locale:
        errors.append(
            f"{distribution_name} prototype metadata locale mismatch: "
            f"expected {locale!r}, got {prototype.get('locale')!r}"
        )
    if prototype.get("status") != "prototype":
        errors.append(
            f"{distribution_name} prototype metadata {locale} must declare status=prototype"
        )
    if prototype.get("invocation_policy") != "explicit":
        errors.append(
            f"{distribution_name} prototype metadata {locale} must remain explicit invocation"
        )

    for field in ("plugin_name", "description", "display"):
        value = prototype.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{distribution_name} prototype metadata {locale} must declare {field}"
            )

    expected_contains = suite_distribution.get("contains", [])
    actual_contains = prototype.get("contains")
    if not isinstance(expected_contains, list) or not all(
        isinstance(value, str) for value in expected_contains
    ):
        errors.append(f"{distribution_name} suite contains must be a string list")
    elif not isinstance(actual_contains, list) or not all(
        isinstance(value, str) for value in actual_contains
    ):
        errors.append(
            f"{distribution_name} prototype metadata {locale} contains must be a string list"
        )
    elif len(actual_contains) != len(set(actual_contains)):
        errors.append(
            f"{distribution_name} prototype metadata {locale} contains must not repeat skills"
        )
    elif set(actual_contains) != set(expected_contains):
        errors.append(
            f"{distribution_name} prototype metadata {locale} skill composition must match suite; "
            + _set_mismatch(set(expected_contains), set(actual_contains))
        )

    if isinstance(baseline_catalog, dict):
        baseline_entry = baseline_catalog.get(locale)
        if isinstance(baseline_entry, dict):
            baseline_name = baseline_entry.get("plugin_name")
            if isinstance(baseline_name, str) and prototype.get("plugin_name") != baseline_name:
                errors.append(
                    f"{distribution_name} prototype metadata {locale} must preserve existing "
                    f"plugin_name {baseline_name!r}"
                )


def _validate_locale_bundle(
    root: Path,
    distribution_name: str,
    suite_distribution: dict,
    config: dict,
    locales: set[str],
    errors: list[str],
) -> None:
    if config.get("scope") != "locale_bundle":
        errors.append(f"{distribution_name} adapter metadata scope must be locale_bundle")
    if config.get("source_mode") != "locale_catalog":
        errors.append(f"{distribution_name} adapter metadata source_mode must be locale_catalog")

    source_relative = config.get("source")
    source = _repo_path(
        root,
        source_relative,
        f"{distribution_name} adapter metadata source",
        errors,
    )
    catalog = None
    if source is not None:
        if not source.is_file():
            errors.append(
                f"{distribution_name} adapter metadata source is missing: {source_relative}"
            )
        else:
            catalog = _load_json(
                source,
                f"{distribution_name} adapter metadata source",
                errors,
            )

    locale_states = config.get("locales")
    if not isinstance(locale_states, dict):
        errors.append(f"{distribution_name} adapter metadata locales must be an object")
        return
    if set(locale_states) != locales:
        errors.append(
            f"{distribution_name} adapter metadata locales must match suite locales; "
            + _set_mismatch(locales, set(locale_states))
        )

    multi_skill = len(suite_distribution.get("contains", [])) > 1
    review_required = config.get("review_required_for_multi_skill")
    if not isinstance(review_required, bool):
        errors.append(
            f"{distribution_name} review_required_for_multi_skill must be boolean"
        )
        review_required = False

    for locale in sorted(locales & set(locale_states)):
        entry = locale_states.get(locale)
        if not isinstance(entry, dict):
            errors.append(f"{distribution_name} metadata locale {locale} must be an object")
            continue
        status = entry.get("status")
        if status not in ALLOWED_BUNDLE_STATUS:
            errors.append(
                f"{distribution_name} metadata locale {locale} has invalid status: {status!r}"
            )
            continue

        if multi_skill and status in {"existing-baseline", "prototype"} and not review_required:
            errors.append(
                f"{distribution_name} multi-Skill bundle using {status} metadata must require review"
            )

        prototype_source = entry.get("prototype_source")
        if status == "planned":
            if prototype_source is not None:
                errors.append(
                    f"planned {distribution_name} metadata {locale} must not declare prototype_source"
                )
            continue

        if status == "prototype":
            _validate_bundle_prototype(
                root,
                distribution_name,
                locale,
                entry,
                suite_distribution,
                catalog,
                errors,
            )
            continue

        if prototype_source is not None:
            errors.append(
                f"{distribution_name} metadata {locale} with status {status} must not declare "
                "prototype_source"
            )

        if catalog is None:
            continue
        catalog_entry = catalog.get(locale)
        if not isinstance(catalog_entry, dict):
            errors.append(
                f"{distribution_name} locale catalog does not declare metadata for {locale}"
            )
            continue
        for field in ("plugin_name", "skill_name", "description", "display"):
            value = catalog_entry.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{distribution_name} locale catalog {locale} must declare {field}"
                )


def validate_adapter_metadata(root: Path, plan: dict) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != EXPECTED_SCHEMA:
        errors.append(
            f"research adapter metadata schema must be {EXPECTED_SCHEMA}: {plan.get('schema')!r}"
        )

    suite_relative = plan.get("suite_manifest")
    suite_path = _repo_path(root, suite_relative, "adapter metadata suite_manifest", errors)
    if suite_path is None or not suite_path.is_file():
        if suite_path is not None:
            errors.append(f"adapter metadata suite_manifest is missing: {suite_relative}")
        return errors
    suite = _load_json(suite_path, "adapter metadata suite_manifest", errors)
    if suite is None:
        return errors

    skills = suite.get("skills")
    locales_obj = suite.get("locales")
    distributions = suite.get("distribution_prototypes")
    if not isinstance(skills, list) or not isinstance(locales_obj, dict) or not isinstance(
        distributions, dict
    ):
        return errors + ["suite manifest shape is invalid for adapter metadata validation"]

    skill_ids = {
        skill.get("id")
        for skill in skills
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    }
    locales = set(locales_obj)
    skill_tree_distributions = {
        name
        for name, config in distributions.items()
        if isinstance(config, dict) and config.get("mode") in SKILL_TREE_MODES
    }

    metadata_distributions = plan.get("distributions")
    if not isinstance(metadata_distributions, dict):
        return errors + ["research adapter metadata distributions must be an object"]
    if set(metadata_distributions) != skill_tree_distributions:
        errors.append(
            "adapter metadata distributions must match Skill-tree distributions; "
            + _set_mismatch(skill_tree_distributions, set(metadata_distributions))
        )

    openai = metadata_distributions.get("openai_skill")
    if isinstance(openai, dict):
        _validate_openai(root, openai, skill_ids, locales, errors)

    for distribution_name in ("claude_plugin", "codex_plugin"):
        config = metadata_distributions.get(distribution_name)
        suite_distribution = distributions.get(distribution_name)
        if isinstance(config, dict) and isinstance(suite_distribution, dict):
            _validate_locale_bundle(
                root,
                distribution_name,
                suite_distribution,
                config,
                locales,
                errors,
            )

    return errors


def main() -> int:
    try:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research adapter metadata validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_adapter_metadata(ROOT, plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research adapter metadata plan is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
