#!/usr/bin/env python3
"""Validate internal consistency of the research skill-suite prototype manifest.

This checker validates repository-shape and realization contracts only. It does
not decide whether a research skill is methodologically validated, independently
reviewed, or ready for public promotion.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
EXPECTED_SCHEMA = "csw.research-skill-suite/v1"


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_path(root: Path, relative: object, field: str, errors: list[str]) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{field} must be a non-empty repository-relative path")
        return None

    resolved_root = root.resolve()
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(resolved_root):
        errors.append(f"{field} escapes repository root: {relative}")
        return None
    return resolved


def _frontmatter_name(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "name":
            return value.strip().strip("\"'")
    return None


def _validate_runtime_name(
    path: Path | None,
    installable_name: object,
    field: str,
    errors: list[str],
) -> None:
    if path is None or not path.is_file() or not isinstance(installable_name, str):
        return
    frontmatter_name = _frontmatter_name(path)
    if frontmatter_name is not None and frontmatter_name != installable_name:
        errors.append(
            f"{field} frontmatter name must match installable_name: "
            f"{frontmatter_name!r} != {installable_name!r}"
        )


def _declared_paths(
    root: Path,
    source_root: Path,
    skill_id: str,
    field: str,
    value: object,
    errors: list[str],
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"skill {skill_id}: {field} must be a list of repository-relative paths")
        return []

    if len(value) != len(set(value)):
        errors.append(f"skill {skill_id}: {field} contains duplicate paths")

    for relative in value:
        resolved = _repo_path(root, relative, f"skill {skill_id} {field}", errors)
        if resolved is None:
            continue
        if not resolved.is_relative_to(source_root):
            errors.append(
                f"skill {skill_id}: declared {field} path is outside source_root: {relative}"
            )
        if not resolved.is_file():
            errors.append(f"skill {skill_id}: declared {field} file is missing: {relative}")
    return value


def _validate_method_definition(
    root: Path,
    source_root: Path,
    skill_id: str,
    field: str,
    value: object,
    errors: list[str],
) -> Path | None:
    if value is None:
        return None
    path = _repo_path(root, value, f"skill {skill_id} {field}", errors)
    if path is None:
        return None
    if not path.is_relative_to(source_root):
        errors.append(f"skill {skill_id}: {field} is outside source_root: {value}")
    if not path.is_file():
        errors.append(f"skill {skill_id}: {field} is missing: {value}")
    return path


def _validate_locale_realizations(
    root: Path,
    source_root: Path,
    skill_id: str,
    installable_name: object,
    skill_runtime_entry: object,
    skill_method_definition: object,
    declared_references: list[str],
    canonical_locale: object,
    suite_locales: set[str],
    value: object,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"skill {skill_id}: locale_realizations must be an object")
        return

    realization_locales = set(value)
    missing = sorted(suite_locales - realization_locales)
    extra = sorted(realization_locales - suite_locales)
    if missing or extra:
        errors.append(
            f"skill {skill_id}: locale_realizations must match suite locales; "
            f"missing={missing}, extra={extra}"
        )

    for locale in sorted(suite_locales & realization_locales):
        realization = value.get(locale)
        if not isinstance(realization, dict):
            errors.append(f"skill {skill_id}: locale realization {locale} must be an object")
            continue

        status = realization.get("status")
        if not isinstance(status, str) or not status.strip():
            errors.append(
                f"skill {skill_id}: locale realization {locale} status must be a non-empty string"
            )
            continue

        runtime_relative = realization.get("runtime_entry")
        method_relative = realization.get("method_definition")

        if locale == canonical_locale and status == "planned":
            errors.append(f"skill {skill_id}: canonical locale {locale} cannot be planned-only")

        if status != "planned" and (
            not isinstance(runtime_relative, str) or not runtime_relative
        ):
            errors.append(f"skill {skill_id}: realized locale {locale} must declare runtime_entry")
        elif runtime_relative is not None:
            runtime_entry = _repo_path(
                root,
                runtime_relative,
                f"skill {skill_id} locale realization {locale} runtime_entry",
                errors,
            )
            if runtime_entry is not None:
                if not runtime_entry.is_relative_to(source_root):
                    errors.append(
                        f"skill {skill_id}: locale realization {locale} runtime_entry "
                        f"is outside source_root: {runtime_relative}"
                    )
                if not runtime_entry.is_file():
                    errors.append(
                        f"skill {skill_id}: locale realization {locale} runtime_entry "
                        f"is missing: {runtime_relative}"
                    )
                _validate_runtime_name(
                    runtime_entry,
                    installable_name,
                    f"skill {skill_id} locale realization {locale} runtime_entry",
                    errors,
                )

        if status != "planned" and skill_method_definition is not None and method_relative is None:
            errors.append(
                f"skill {skill_id}: realized locale {locale} must declare method_definition"
            )
        if method_relative is not None:
            _validate_method_definition(
                root,
                source_root,
                skill_id,
                f"locale realization {locale} method_definition",
                method_relative,
                errors,
            )
            if isinstance(method_relative, str) and method_relative not in declared_references:
                errors.append(
                    f"skill {skill_id}: locale realization {locale} method_definition "
                    f"must also be declared in references: {method_relative}"
                )

        if locale == canonical_locale and status != "planned":
            if runtime_relative != skill_runtime_entry:
                errors.append(
                    f"skill {skill_id}: canonical locale realization runtime_entry must match "
                    f"skill runtime_entry: {runtime_relative!r} != {skill_runtime_entry!r}"
                )
            if method_relative != skill_method_definition:
                errors.append(
                    f"skill {skill_id}: canonical locale realization method_definition must match "
                    f"skill method_definition: {method_relative!r} != {skill_method_definition!r}"
                )


def validate_suite(root: Path, manifest: dict) -> list[str]:
    errors: list[str] = []

    if manifest.get("schema") != EXPECTED_SCHEMA:
        errors.append(
            f"research skill suite schema must be {EXPECTED_SCHEMA}: {manifest.get('schema')!r}"
        )
    if manifest.get("status") != "research-only":
        errors.append("research skill suite must remain marked research-only before promotion")

    locales = manifest.get("locales")
    canonical_locale = manifest.get("canonical_locale")
    if not isinstance(locales, dict):
        errors.append("research skill suite locales must be an object")
        suite_locales: set[str] = set()
    else:
        suite_locales = set(locales)
        if not isinstance(canonical_locale, str) or canonical_locale not in locales:
            errors.append(
                f"research skill suite canonical_locale must name a declared locale: {canonical_locale!r}"
            )

    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        return errors + ["research skill suite skills must be a non-empty list"]

    skill_ids: list[str] = []
    installable_names: list[str] = []

    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"research skill suite skill[{index}] must be an object")
            continue

        skill_id = skill.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"research skill suite skill[{index}] has invalid id: {skill_id!r}")
            skill_id = f"<skill[{index}]>"
        else:
            skill_ids.append(skill_id)

        installable_name = skill.get("installable_name")
        if not isinstance(installable_name, str) or not installable_name:
            errors.append(f"skill {skill_id}: installable_name must be a non-empty string")
        else:
            installable_names.append(installable_name)

        source_relative = skill.get("source_root")
        source_root = _repo_path(root, source_relative, f"skill {skill_id} source_root", errors)
        if source_root is None:
            continue
        if not source_root.is_dir():
            errors.append(f"skill {skill_id}: source_root is missing or not a directory: {source_relative}")

        runtime_relative = skill.get("runtime_entry")
        runtime_entry = _repo_path(root, runtime_relative, f"skill {skill_id} runtime_entry", errors)
        if runtime_entry is not None:
            if not runtime_entry.is_relative_to(source_root):
                errors.append(f"skill {skill_id}: runtime_entry is outside source_root: {runtime_relative}")
            if not runtime_entry.is_file():
                errors.append(f"skill {skill_id}: runtime_entry is missing: {runtime_relative}")
            _validate_runtime_name(
                runtime_entry,
                installable_name,
                f"skill {skill_id} runtime_entry",
                errors,
            )

        references = _declared_paths(
            root, source_root, skill_id, "references", skill.get("references"), errors
        )
        _declared_paths(root, source_root, skill_id, "evidence", skill.get("evidence"), errors)
        _declared_paths(root, source_root, skill_id, "evals", skill.get("evals"), errors)
        _declared_paths(root, source_root, skill_id, "checks", skill.get("checks", []), errors)

        method_relative = skill.get("method_definition")
        _validate_method_definition(
            root, source_root, skill_id, "method_definition", method_relative, errors
        )
        conventional_method = source_root / "references" / "METHOD.md"
        conventional_method_relative = (
            conventional_method.relative_to(root.resolve()).as_posix()
            if conventional_method.exists() and conventional_method.is_relative_to(root.resolve())
            else None
        )

        if method_relative is None:
            if conventional_method_relative is not None:
                errors.append(
                    f"skill {skill_id}: references/METHOD.md exists but method_definition is not registered: "
                    f"{conventional_method_relative}"
                )
        else:
            if isinstance(method_relative, str) and method_relative not in references:
                errors.append(
                    f"skill {skill_id}: method_definition must also be declared in references: "
                    f"{method_relative}"
                )
            if conventional_method_relative is not None and method_relative != conventional_method_relative:
                errors.append(
                    f"skill {skill_id}: method_definition does not match source_root/references/METHOD.md: "
                    f"{method_relative!r} != {conventional_method_relative!r}"
                )

        _validate_locale_realizations(
            root,
            source_root,
            skill_id,
            installable_name,
            runtime_relative,
            method_relative,
            references,
            canonical_locale,
            suite_locales,
            skill.get("locale_realizations"),
            errors,
        )

        delegation = skill.get("delegation")
        if isinstance(delegation, dict) and delegation.get("hard_dependency") is True:
            errors.append(f"skill {skill_id}: public research contract must not assume hard dependency")

    if len(skill_ids) != len(set(skill_ids)):
        errors.append("research skill suite skill ids must be unique")
    if len(installable_names) != len(set(installable_names)):
        errors.append("research skill suite installable_name values must be unique")

    research_assets = manifest.get("suite_research_assets", [])
    if not isinstance(research_assets, list) or not all(isinstance(item, str) for item in research_assets):
        errors.append("research skill suite suite_research_assets must be a string list")
    else:
        if len(research_assets) != len(set(research_assets)):
            errors.append("research skill suite suite_research_assets contains duplicate paths")
        for relative in research_assets:
            path = _repo_path(root, relative, "suite_research_assets", errors)
            if path is not None and not path.is_file():
                errors.append(f"suite_research_assets file is missing: {relative}")

    known_skill_ids = set(skill_ids)
    distributions = manifest.get("distribution_prototypes")
    if not isinstance(distributions, dict):
        errors.append("research skill suite distribution_prototypes must be an object")
    else:
        for distribution_name, config in distributions.items():
            if not isinstance(config, dict):
                errors.append(f"distribution prototype {distribution_name} must be an object")
                continue

            contains = config.get("contains")
            if contains is not None:
                if not isinstance(contains, list) or not all(isinstance(item, str) for item in contains):
                    errors.append(
                        f"distribution prototype {distribution_name} contains must be a string list"
                    )
                else:
                    if len(contains) != len(set(contains)):
                        errors.append(
                            f"distribution prototype {distribution_name} contains duplicate skill ids"
                        )
                    unknown = sorted(set(contains) - known_skill_ids)
                    if unknown:
                        errors.append(
                            f"distribution prototype {distribution_name} references unknown skills: {unknown}"
                        )

            primary = config.get("primary")
            if primary is not None and primary not in known_skill_ids:
                errors.append(
                    f"distribution prototype {distribution_name} primary references unknown skill: {primary!r}"
                )

    promotion_gates = manifest.get("promotion_gates")
    if not isinstance(promotion_gates, list) or not promotion_gates:
        errors.append("research skill suite promotion_gates must be a non-empty list")

    return errors


def main() -> int:
    try:
        manifest = load_manifest()
        errors = validate_suite(ROOT, manifest)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research skill suite validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research skill suite manifest is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
