#!/usr/bin/env python3
"""Validate package target naming for the research skill-suite prototype.

This validator is intentionally narrower than promotion or package validation.
It checks only whether realized skills declare safe, non-colliding target names
for distribution shapes that materialize Skill subtrees.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
SKILL_TREE_MODES = {"standalone_per_skill", "locale_bundle"}


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _target_distributions(manifest: dict, skill_id: str) -> list[str]:
    names: list[str] = []
    distributions = manifest.get("distribution_prototypes")
    if not isinstance(distributions, dict):
        return names
    for distribution_name, config in distributions.items():
        if not isinstance(distribution_name, str) or not distribution_name:
            continue
        if not isinstance(config, dict):
            continue
        mode = config.get("mode")
        if mode == "standalone_per_skill":
            names.append(distribution_name)
        elif mode == "locale_bundle":
            contains = config.get("contains")
            if isinstance(contains, list) and skill_id in contains:
                names.append(distribution_name)
    return names


def _safe_skill_name(value: object) -> bool:
    if not isinstance(value, str) or not value or value.strip() != value:
        return False
    if value in {".", ".."}:
        return False
    if "/" in value or "\\" in value or "\x00" in value:
        return False
    return True


def validate_package_targets(manifest: dict) -> list[str]:
    if not isinstance(manifest, dict):
        return ["research skill suite must be an object before package target validation"]

    errors: list[str] = []
    distributions = manifest.get("distribution_prototypes")
    if not isinstance(distributions, dict):
        return ["research skill suite distribution_prototypes must be an object before package target validation"]
    for distribution_name, config in distributions.items():
        if not isinstance(distribution_name, str) or not distribution_name:
            errors.append("research skill suite distribution keys must be non-empty strings")
            continue
        if not isinstance(config, dict):
            errors.append(
                f"research skill suite distribution {distribution_name} must be an object"
            )
            continue
        if config.get("mode") == "locale_bundle" and not isinstance(
            config.get("contains"), list
        ):
            errors.append(
                f"locale_bundle distribution {distribution_name} contains must be a list"
            )

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        return ["research skill suite skills must be a list before package target validation"]

    skill_map = {skill.get("id"): skill for skill in skills if isinstance(skill, dict) and isinstance(skill.get("id"), str)}
    locales = manifest.get("locales")
    if not isinstance(locales, dict):
        return errors + ["research skill suite locales must be an object before package target validation"]
    if not all(isinstance(locale, str) and locale for locale in locales):
        errors.append("research skill suite locale keys must be non-empty strings")

    for skill_id, skill in skill_map.items():
        expected = set(_target_distributions(manifest, skill_id))
        realizations = skill.get("locale_realizations")
        if not isinstance(realizations, dict):
            errors.append(f"skill {skill_id}: locale_realizations must be an object")
            continue
        for locale in locales:
            realization = realizations.get(locale)
            if not isinstance(realization, dict):
                continue
            status = realization.get("status")
            targets = realization.get("package_targets")
            if status == "planned":
                if targets is not None:
                    errors.append(f"skill {skill_id}: planned locale {locale} must not declare package_targets")
                continue
            if not isinstance(targets, dict):
                errors.append(f"skill {skill_id}: realized locale {locale} must declare package_targets")
                continue
            target_keys_are_strings = all(
                isinstance(name, str) and name
                for name in targets
            )
            if not target_keys_are_strings:
                errors.append(
                    f"skill {skill_id}: locale {locale} package target keys must be non-empty strings"
                )
            actual = {
                name
                for name in targets
                if isinstance(name, str) and name
            }
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            if missing or extra:
                errors.append(f"skill {skill_id}: locale {locale} package_targets must match Skill-tree distributions; missing={missing}, extra={extra}")
            for distribution_name in sorted(expected & actual):
                target = targets.get(distribution_name)
                if not isinstance(target, dict):
                    errors.append(f"skill {skill_id}: locale {locale} package target {distribution_name} must be an object")
                    continue
                skill_name = target.get("skill_name")
                if not _safe_skill_name(skill_name):
                    errors.append(f"skill {skill_id}: locale {locale} package target {distribution_name} has unsafe skill_name: {skill_name!r}")

    for locale in locales:
        if not isinstance(locale, str) or not locale:
            continue
        for distribution_name, config in distributions.items():
            if (
                not isinstance(distribution_name, str)
                or not distribution_name
                or not isinstance(config, dict)
                or config.get("mode") not in SKILL_TREE_MODES
            ):
                continue
            if config.get("mode") == "standalone_per_skill":
                target_skill_ids = list(skill_map)
            else:
                contains = config.get("contains")
                target_skill_ids = [
                    skill_id
                    for skill_id in contains
                    if skill_id in skill_map
                ] if isinstance(contains, list) else []
            by_name: dict[str, list[str]] = {}
            for skill_id in target_skill_ids:
                realizations = skill_map[skill_id].get("locale_realizations")
                if not isinstance(realizations, dict):
                    continue
                realization = realizations.get(locale)
                if not isinstance(realization, dict) or realization.get("status") == "planned":
                    continue
                package_targets = realization.get("package_targets")
                if not isinstance(package_targets, dict):
                    continue
                target = package_targets.get(distribution_name)
                if not isinstance(target, dict):
                    continue
                skill_name = target.get("skill_name")
                if not _safe_skill_name(skill_name):
                    continue
                by_name.setdefault(skill_name, []).append(skill_id)
            for skill_name, owners in sorted(by_name.items()):
                if len(owners) > 1:
                    errors.append(f"locale {locale} distribution {distribution_name} target skill_name collision {skill_name!r}: {owners}")
    return errors


def main() -> int:
    try:
        manifest = load_manifest()
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_research_skill_suite import validate_suite
        errors = validate_suite(ROOT, manifest)
        errors.extend(validate_package_targets(manifest))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"research package target validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Research package target names are internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
