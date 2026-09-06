#!/usr/bin/env python3
"""Validate internal consistency of the research skill-suite prototype manifest.

This checker does not decide whether a research skill is ready for promotion.
It only keeps declared research metadata synchronized with the repository tree.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
EXPECTED_SCHEMA = "csw.research-skill-suite/v1"
PACKAGE_SOURCE_MODES = {"explicit_files", "canonical_manifest"}


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


def _package_relative_file(
    package_root: Path,
    relative: object,
    field: str,
    errors: list[str],
) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{field} must be a non-empty path relative to package root")
        return None
    path = Path(relative)
    if path.is_absolute():
        errors.append(f"{field} must be relative to package root: {relative}")
        return None

    resolved_root = package_root.resolve()
    resolved = (package_root / path).resolve()
    if not resolved.is_relative_to(resolved_root):
        errors.append(f"{field} escapes package root: {relative}")
        return None
    return resolved


def _validate_package_source(
    root: Path,
    source_root: Path,
    skill_id: str,
    locale: str,
    runtime_relative: str,
    value: object,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(
            f"skill {skill_id}: realized locale {locale} must declare package_source"
        )
        return

    mode = value.get("mode")
    if mode not in PACKAGE_SOURCE_MODES:
        errors.append(
            f"skill {skill_id}: locale realization {locale} package_source mode "
            f"must be one of {sorted(PACKAGE_SOURCE_MODES)}: {mode!r}"
        )
        return

    runtime_path = _repo_path(
        root,
        runtime_relative,
        f"skill {skill_id} locale realization {locale} runtime_entry",
        errors,
    )

    if mode == "explicit_files":
        package_root_relative = value.get("root")
        package_root = _repo_path(
            root,
            package_root_relative,
            f"skill {skill_id} locale realization {locale} package_source root",
            errors,
        )
        if package_root is None:
            return
        if not package_root.is_relative_to(source_root):
            errors.append(
                f"skill {skill_id}: locale realization {locale} package_source root "
                f"is outside source_root: {package_root_relative}"
            )
        if not package_root.is_dir():
            errors.append(
                f"skill {skill_id}: locale realization {locale} package_source root "
                f"is missing or not a directory: {package_root_relative}"
            )

        files = value.get("files")
        if (
            not isinstance(files, list)
            or not files
            or not all(isinstance(item, str) for item in files)
        ):
            errors.append(
                f"skill {skill_id}: locale realization {locale} explicit_files "
                "must declare a non-empty string list"
            )
            return
        if len(files) != len(set(files)):
            errors.append(
                f"skill {skill_id}: locale realization {locale} explicit_files "
                "contains duplicate paths"
            )

        resolved_files: list[Path] = []
        for relative in files:
            resolved = _package_relative_file(
                package_root,
                relative,
                f"skill {skill_id} locale realization {locale} package file",
                errors,
            )
            if resolved is None:
                continue
            resolved_files.append(resolved)
            if not resolved.is_file():
                errors.append(
                    f"skill {skill_id}: locale realization {locale} package file "
                    f"is missing: {relative}"
                )

        if runtime_path is not None and runtime_path not in resolved_files:
            errors.append(
                f"skill {skill_id}: locale realization {locale} package_source "
                "must include runtime_entry"
            )
        return

    manifest_relative = value.get("manifest")
    locale_root_relative = value.get("locale_root")
    source_manifest = _repo_path(
        root,
        manifest_relative,
        f"skill {skill_id} locale realization {locale} package manifest",
        errors,
    )
    locale_root = _repo_path(
        root,
        locale_root_relative,
        f"skill {skill_id} locale realization {locale} locale_root",
        errors,
    )
    if source_manifest is None or locale_root is None:
        return
    if not source_manifest.is_relative_to(source_root):
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            f"is outside source_root: {manifest_relative}"
        )
    if not locale_root.is_relative_to(source_root):
        errors.append(
            f"skill {skill_id}: locale realization {locale} locale_root "
            f"is outside source_root: {locale_root_relative}"
        )
    if not source_manifest.is_file():
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            f"is missing: {manifest_relative}"
        )
        return
    if not locale_root.is_dir():
        errors.append(
            f"skill {skill_id}: locale realization {locale} locale_root "
            f"is missing or not a directory: {locale_root_relative}"
        )
        return

    try:
        config = json.loads(source_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            f"cannot be read as JSON: {exc}"
        )
        return

    declared_locales = config.get("locales")
    if not isinstance(declared_locales, dict) or locale not in declared_locales:
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            "does not declare this locale"
        )

    router = config.get("router")
    if not isinstance(router, str) or not router:
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            "must declare a router"
        )
    elif runtime_path is not None and (locale_root / router).resolve() != runtime_path:
        errors.append(
            f"skill {skill_id}: locale realization {locale} canonical_manifest "
            "router does not match runtime_entry"
        )

    modules = config.get("modules")
    if not isinstance(modules, list) or not modules:
        errors.append(
            f"skill {skill_id}: locale realization {locale} package manifest "
            "must declare modules"
        )
        return
    for index, module in enumerate(modules):
        if not isinstance(module, dict):
            errors.append(
                f"skill {skill_id}: locale realization {locale} package manifest "
                f"module[{index}] must be an object"
            )
            continue
        module_source = module.get("source")
        module_path = _package_relative_file(
            locale_root,
            module_source,
            f"skill {skill_id} locale realization {locale} manifest module[{index}] source",
            errors,
        )
        if module_path is not None and not module_path.is_file():
            errors.append(
                f"skill {skill_id}: locale realization {locale} manifest module "
                f"is missing: {module_source}"
            )


def _validate_locale_realizations(
    root: Path,
    source_root: Path,
    skill_id: str,
    skill_runtime_entry: object,
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
        package_source = realization.get("package_source")
        if locale == canonical_locale and status == "planned":
            errors.append(
                f"skill {skill_id}: canonical locale {locale} cannot be planned-only"
            )

        if status == "planned":
            if package_source is not None:
                errors.append(
                    f"skill {skill_id}: planned locale {locale} must not declare package_source"
                )
            continue

        if not isinstance(runtime_relative, str) or not runtime_relative:
            errors.append(
                f"skill {skill_id}: realized locale {locale} must declare runtime_entry"
            )
            continue

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

        _validate_package_source(
            root,
            source_root,
            skill_id,
            locale,
            runtime_relative,
            package_source,
            errors,
        )

        if locale == canonical_locale and runtime_relative != skill_runtime_entry:
            errors.append(
                f"skill {skill_id}: canonical locale realization runtime_entry must match "
                f"skill runtime_entry: {runtime_relative!r} != {skill_runtime_entry!r}"
            )


def validate_suite(root: Path, manifest: dict) -> list[str]:
    errors: list[str] = []

    if manifest.get("schema") != EXPECTED_SCHEMA:
        errors.append(
            f"research skill suite schema must be {EXPECTED_SCHEMA}: {manifest.get('schema')!r}"
        )

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
            errors.append(
                f"skill {skill_id}: source_root is missing or not a directory: {source_relative}"
            )

        runtime_relative = skill.get("runtime_entry")
        runtime_entry = _repo_path(
            root, runtime_relative, f"skill {skill_id} runtime_entry", errors
        )
        if runtime_entry is not None:
            if not runtime_entry.is_relative_to(source_root):
                errors.append(
                    f"skill {skill_id}: runtime_entry is outside source_root: {runtime_relative}"
                )
            if not runtime_entry.is_file():
                errors.append(
                    f"skill {skill_id}: runtime_entry is missing: {runtime_relative}"
                )

        _validate_locale_realizations(
            root,
            source_root,
            skill_id,
            runtime_relative,
            canonical_locale,
            suite_locales,
            skill.get("locale_realizations"),
            errors,
        )

        references = _declared_paths(
            root,
            source_root,
            skill_id,
            "references",
            skill.get("references"),
            errors,
        )
        _declared_paths(
            root, source_root, skill_id, "evidence", skill.get("evidence"), errors
        )
        _declared_paths(
            root, source_root, skill_id, "evals", skill.get("evals"), errors
        )

        method_relative = skill.get("method_definition")
        conventional_method = source_root / "references" / "METHOD.md"
        conventional_method_relative = (
            conventional_method.relative_to(root.resolve()).as_posix()
            if conventional_method.exists()
            and conventional_method.is_relative_to(root.resolve())
            else None
        )

        if method_relative is None:
            if conventional_method_relative is not None:
                errors.append(
                    f"skill {skill_id}: references/METHOD.md exists but method_definition "
                    f"is not registered: {conventional_method_relative}"
                )
        else:
            method_path = _repo_path(
                root,
                method_relative,
                f"skill {skill_id} method_definition",
                errors,
            )
            if method_path is not None:
                if not method_path.is_relative_to(source_root):
                    errors.append(
                        f"skill {skill_id}: method_definition is outside source_root: "
                        f"{method_relative}"
                    )
                if not method_path.is_file():
                    errors.append(
                        f"skill {skill_id}: method_definition is missing: {method_relative}"
                    )
            if isinstance(method_relative, str) and method_relative not in references:
                errors.append(
                    f"skill {skill_id}: method_definition must also be declared in references: "
                    f"{method_relative}"
                )
            if (
                conventional_method_relative is not None
                and method_relative != conventional_method_relative
            ):
                errors.append(
                    f"skill {skill_id}: method_definition does not match "
                    f"source_root/references/METHOD.md: {method_relative!r} != "
                    f"{conventional_method_relative!r}"
                )

    if len(skill_ids) != len(set(skill_ids)):
        errors.append("research skill suite skill ids must be unique")
    if len(installable_names) != len(set(installable_names)):
        errors.append("research skill suite installable_name values must be unique")

    known_skill_ids = set(skill_ids)
    distributions = manifest.get("distribution_prototypes")
    if not isinstance(distributions, dict):
        errors.append("research skill suite distribution_prototypes must be an object")
    else:
        for distribution_name, config in distributions.items():
            if not isinstance(config, dict):
                errors.append(
                    f"distribution prototype {distribution_name} must be an object"
                )
                continue

            contains = config.get("contains")
            if contains is not None:
                if not isinstance(contains, list) or not all(
                    isinstance(skill_id, str) for skill_id in contains
                ):
                    errors.append(
                        f"distribution prototype {distribution_name} contains "
                        "must be a string list"
                    )
                else:
                    if len(contains) != len(set(contains)):
                        errors.append(
                            f"distribution prototype {distribution_name} contains "
                            "duplicate skill ids"
                        )
                    unknown = sorted(set(contains) - known_skill_ids)
                    if unknown:
                        errors.append(
                            f"distribution prototype {distribution_name} references "
                            f"unknown skills: {unknown}"
                        )

            primary = config.get("primary")
            if primary is not None and primary not in known_skill_ids:
                errors.append(
                    f"distribution prototype {distribution_name} primary references "
                    f"unknown skill: {primary!r}"
                )

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
