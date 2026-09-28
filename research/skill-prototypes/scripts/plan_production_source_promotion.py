#!/usr/bin/env python3
"""Plan research-prototype to production-canonical sibling Skill source promotion.

This planner is read-only. It maps the package-closed research locale realization
into the future production locale_tree without creating src/skills or rewriting
files. Research-only metadata outside package_source.files is exposed as
excluded rather than silently promoted.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
SUITE_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
DESCRIPTOR_PATH = ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
MIGRATION_PATH = ROOT / "research/skill-prototypes/P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
INVENTORY_PATH = ROOT / "research/skill-prototypes/P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_production_suite_descriptor import validate_production_suite_descriptor  # noqa: E402
from validate_research_public_name_migration import validate_public_name_migration  # noqa: E402
from validate_research_public_name_projection_inventory import validate_projection_inventory  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402

PLAN_SCHEMA = "csw.production-source-promotion-plan/v1"


def _safe_repo_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def _target_relative(source_relative: str, locale: str) -> str:
    path = PurePosixPath(source_relative)
    name = path.name
    if locale == "en-US" and name.endswith(".en.md"):
        name = name[: -len(".en.md")] + ".md"
    return (path.parent / name).as_posix() if path.parent.parts else name


def _projection_actions(inventory: dict) -> dict[str, str]:
    actions: dict[str, str] = {}
    for item in inventory.get("content_projection", []):
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        action = item.get("action")
        if isinstance(path, str) and isinstance(action, str):
            actions[path] = action
    return actions


def _expected_content_transforms(
    source_repo: str,
    source_relative: str,
    locale: str,
    inventory_actions: dict[str, str],
) -> list[str]:
    """Derive the exact ordered transform sequence from declared authorities."""

    transforms: list[str] = []
    inventory_action = inventory_actions.get(source_repo)
    if inventory_action:
        transforms.append(inventory_action)

    target_relative = _target_relative(source_relative, locale)
    if locale == "en-US" and target_relative != source_relative:
        transforms.append("normalize-locale-suffixed-filename")
        if source_relative.endswith("SKILL.en.md"):
            transforms.append("rewrite-package-local-locale-suffix-references")
    return transforms


def _skill_metadata_paths(skill: dict) -> set[str]:
    paths: set[str] = set()
    for field in ("references", "evidence", "evals", "checks"):
        values = skill.get(field, [])
        if isinstance(values, list):
            paths.update(value for value in values if isinstance(value, str))
    return paths


def _expected_excluded_research_metadata(skill: dict) -> list[str]:
    """Derive research metadata intentionally left outside production package sources."""

    promoted_sources: set[str] = set()
    realizations = skill.get("locale_realizations")
    if isinstance(realizations, dict):
        for realization in realizations.values():
            package_source = (
                realization.get("package_source")
                if isinstance(realization, dict)
                else None
            )
            if not isinstance(package_source, dict):
                continue
            root = package_source.get("root")
            files = package_source.get("files")
            if not isinstance(root, str) or not isinstance(files, list):
                continue
            root_path = PurePosixPath(root)
            promoted_sources.update(
                (root_path / relative).as_posix()
                for relative in files
                if isinstance(relative, str)
            )
    return sorted(_skill_metadata_paths(skill) - promoted_sources)


def _descriptor_by_id(descriptor: dict) -> dict[str, dict]:
    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        return {}
    return {
        item["research_id"]: item
        for item in skills
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }


def _locale_tree_source_prefixes(suite: dict, descriptor: dict) -> tuple[str, ...]:
    """Return research source roots whose production authority is locale_tree."""

    descriptor_by_id = _descriptor_by_id(descriptor)
    prefixes: set[str] = set()
    for skill in suite.get("skills", []):
        if not isinstance(skill, dict):
            continue
        research_id = skill.get("id")
        source_root = skill.get("source_root")
        descriptor_skill = descriptor_by_id.get(research_id)
        if not isinstance(source_root, str) or not source_root:
            continue
        if not isinstance(descriptor_skill, dict):
            continue
        production_source = descriptor_skill.get("production_source")
        if not isinstance(production_source, dict):
            continue
        if production_source.get("mode") == "locale_tree":
            prefixes.add(source_root.rstrip("/") + "/")
    return tuple(sorted(prefixes))


def _planned_source_prefixes(plan: dict) -> tuple[str, ...]:
    """Compatibility fallback for callers that do not provide the research suite."""

    prefixes: set[str] = set()
    for skill in plan.get("skills", []):
        if not isinstance(skill, dict) or skill.get("state") != "planned-locale-tree-promotion":
            continue
        locales = skill.get("locales")
        if not isinstance(locales, dict):
            continue
        for locale_plan in locales.values():
            if not isinstance(locale_plan, dict):
                continue
            mappings = locale_plan.get("mappings")
            if not isinstance(mappings, list):
                continue
            for mapping in mappings:
                if not isinstance(mapping, dict):
                    continue
                source = mapping.get("source")
                relative = mapping.get("source_relative")
                if not isinstance(source, str) or not isinstance(relative, str) or not relative:
                    continue
                suffix = "/" + relative
                if source.endswith(suffix):
                    prefixes.add(source[: -len(relative)].rstrip("/") + "/")
    return tuple(sorted(prefixes))


def validate_source_promotion_authorities(
    root: Path,
    suite: dict,
    descriptor: dict,
    migration: dict,
    inventory: dict,
) -> list[str]:
    """Validate every source-promotion authority used by the CLI entrypoint."""

    errors = validate_suite(root, suite)
    errors.extend(validate_production_suite_descriptor(descriptor))
    errors.extend(validate_public_name_migration(root, migration))
    errors.extend(validate_projection_inventory(root, inventory))
    return errors


def plan_production_source_promotion(
    suite: dict,
    descriptor: dict,
    migration: dict,
    inventory: dict,
) -> dict:
    descriptor_research_ids = [
        item.get("research_id")
        for item in descriptor.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    ]
    if len(descriptor_research_ids) != len(set(descriptor_research_ids)):
        raise ValueError("production descriptor contains duplicate research Skills")

    suite_research_ids = [
        item.get("id")
        for item in suite.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    if len(suite_research_ids) != len(set(suite_research_ids)):
        raise ValueError("research suite contains duplicate Skills")

    descriptor_by_id = _descriptor_by_id(descriptor)
    suite_by_id = {
        item["id"]: item
        for item in suite.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    descriptor_ids = set(descriptor_by_id)
    suite_ids = set(suite_by_id)
    if suite_ids != descriptor_ids:
        raise ValueError(
            "research suite Skill set must match production descriptor: "
            f"missing={sorted(descriptor_ids - suite_ids)}, "
            f"extra={sorted(suite_ids - descriptor_ids)}"
        )

    declared_locales = descriptor.get("locales")
    if (
        not isinstance(declared_locales, list)
        or not declared_locales
        or not all(isinstance(locale, str) and locale for locale in declared_locales)
        or len(declared_locales) != len(set(declared_locales))
    ):
        raise ValueError(
            "production descriptor locales must be a non-empty unique string list"
        )
    descriptor_locales = set(declared_locales)

    for research_id, skill in suite_by_id.items():
        realizations = skill.get("locale_realizations")
        if not isinstance(realizations, dict):
            raise ValueError(f"research suite locale realizations missing for {research_id}")
        realization_locales = set(realizations)
        if realization_locales != descriptor_locales:
            raise ValueError(
                "research suite locale realizations must match production descriptor: "
                f"{research_id}: missing={sorted(descriptor_locales - realization_locales)}, "
                f"extra={sorted(realization_locales - descriptor_locales)}"
            )

    name_map = migration.get("research_to_production_name")
    if not isinstance(name_map, dict):
        raise ValueError("public-name migration must declare research_to_production_name")
    migration_ids = {
        research_id
        for research_id in name_map
        if isinstance(research_id, str)
    }
    if migration_ids != descriptor_ids:
        raise ValueError(
            "public-name migration Skill set must match production descriptor: "
            f"missing={sorted(descriptor_ids - migration_ids)}, "
            f"extra={sorted(migration_ids - descriptor_ids)}"
        )
    for research_id, descriptor_skill in descriptor_by_id.items():
        expected_name = descriptor_skill.get("proposed_installable_name")
        if name_map.get(research_id) != expected_name:
            raise ValueError(
                "public-name migration must match descriptor installable name: "
                f"{research_id}: {name_map.get(research_id)!r} != {expected_name!r}"
            )

    inventory_actions = _projection_actions(inventory)

    output = {
        "schema": PLAN_SCHEMA,
        "status": "design-only",
        "selection_basis": "research locale package_source.files",
        "note": (
            "Read-only canonical-source promotion plan. Only files already selected by a locale "
            "package_source are candidates for sibling production locale_tree promotion; other "
            "research metadata remains excluded unless the runtime reference contract is changed."
        ),
        "skills": [],
    }

    for skill in suite["skills"]:
        research_id = skill["id"]
        descriptor_skill = descriptor_by_id[research_id]
        production_name = name_map[research_id]
        production_source = descriptor_skill["production_source"]
        source_mode = production_source.get("mode")

        if source_mode == "canonical_manifest":
            output["skills"].append(
                {
                    "research_id": research_id,
                    "production_name": production_name,
                    "state": "existing-canonical-manifest",
                    "source": production_source,
                    "locales": {},
                }
            )
            continue

        if source_mode != "locale_tree":
            raise ValueError(
                "production source is not locale_tree or canonical_manifest "
                f"for {research_id}: {source_mode!r}"
            )

        locale_output: dict[str, dict] = {}
        promoted_repo_sources: set[str] = set()
        for locale, realization in skill["locale_realizations"].items():
            package_source = realization["package_source"]
            if package_source.get("mode") != "explicit_files":
                raise ValueError(
                    f"research locale_tree source {research_id}/{locale} must use explicit_files"
                )
            package_root = package_source.get("root")
            package_files = package_source.get("files")
            if not isinstance(package_root, str) or not _safe_repo_path(package_root):
                raise ValueError(
                    f"research package root is unsafe for {research_id}/{locale}: "
                    f"{package_root!r}"
                )
            if (
                not isinstance(package_files, list)
                or not package_files
                or any(
                    not isinstance(relative, str) or not _safe_repo_path(relative)
                    for relative in package_files
                )
            ):
                raise ValueError(
                    f"research package files are unsafe for {research_id}/{locale}"
                )
            research_root = PurePosixPath(package_root)
            production_root = production_source["root_pattern"].format(locale=locale)
            if (
                not _safe_repo_path(production_root)
                or not production_root.startswith("src/skills/")
            ):
                raise ValueError(
                    f"production source root is unsafe for {research_id}/{locale}: "
                    f"{production_root!r}"
                )
            mappings = []

            for relative in package_source["files"]:
                source_repo = (research_root / relative).as_posix()
                promoted_repo_sources.add(source_repo)
                target_relative = _target_relative(relative, locale)
                target_repo = (PurePosixPath(production_root) / target_relative).as_posix()
                transforms = _expected_content_transforms(
                    source_repo,
                    relative,
                    locale,
                    inventory_actions,
                )

                mappings.append(
                    {
                        "source": source_repo,
                        "source_relative": relative,
                        "target": target_repo,
                        "target_relative": target_relative,
                        "content_transforms": transforms,
                    }
                )

            target_relatives = [item["target_relative"] for item in mappings]
            locale_output[locale] = {
                "research_package_mode": "explicit_files",
                "production_source_mode": "locale_tree",
                "production_root": production_root,
                "copy_scope": "declared-research-package-files-into-future-package-closed-tree",
                "runtime_entry": f"{production_root}/SKILL.md",
                "mappings": mappings,
                "target_collision": len(target_relatives) != len(set(target_relatives)),
            }

        excluded = sorted(_skill_metadata_paths(skill) - promoted_repo_sources)
        output["skills"].append(
            {
                "research_id": research_id,
                "production_name": production_name,
                "state": "planned-locale-tree-promotion",
                "source": production_source,
                "locales": locale_output,
                "excluded_research_metadata": excluded,
            }
        )

    return output


def validate_production_source_promotion_plan(
    plan: dict,
    descriptor: dict,
    inventory: dict | None = None,
    *,
    suite: dict | None = None,
    migration: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_production_suite_descriptor(descriptor))
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"production source promotion plan schema must be {PLAN_SCHEMA}")
    if plan.get("status") != "design-only":
        errors.append("production source promotion plan must remain design-only")
    if plan.get("selection_basis") != "research locale package_source.files":
        errors.append("production source promotion selection must remain package_source.files based")
    if suite is None:
        errors.append(
            "production source promotion validation requires research suite authority"
        )
    else:
        errors.extend(validate_suite(ROOT, suite))
    if inventory is None:
        errors.append(
            "production source promotion validation requires projection-inventory authority"
        )
    else:
        errors.extend(validate_projection_inventory(ROOT, inventory))
    if migration is None:
        errors.append(
            "production source promotion validation requires public-name migration authority"
        )
    else:
        errors.extend(validate_public_name_migration(ROOT, migration))

    descriptor_skills = descriptor.get("skills")
    if not isinstance(descriptor_skills, list):
        descriptor_skills = []
    descriptor_research_ids = [
        item.get("research_id")
        for item in descriptor_skills
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    ]
    if len(descriptor_research_ids) != len(set(descriptor_research_ids)):
        errors.append("production descriptor contains duplicate research Skills")

    suite_skills = suite.get("skills") if suite is not None else []
    if not isinstance(suite_skills, list):
        suite_skills = []
    if suite is not None:
        suite_research_ids = [
            item.get("id")
            for item in suite_skills
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        if len(suite_research_ids) != len(set(suite_research_ids)):
            errors.append("research suite contains duplicate Skills")

    declared_locales = descriptor.get("locales")
    descriptor_locales_valid = (
        isinstance(declared_locales, list)
        and bool(declared_locales)
        and all(isinstance(locale, str) and locale for locale in declared_locales)
        and len(declared_locales) == len(set(declared_locales))
    )
    if not descriptor_locales_valid:
        errors.append(
            "production descriptor locales must be a non-empty unique string list"
        )

    descriptor_by_id = _descriptor_by_id(descriptor)
    inventory_actions = _projection_actions(inventory) if inventory is not None else {}
    plan_skills = plan.get("skills")
    if not isinstance(plan_skills, list):
        errors.append("production source promotion plan Skills must be a list")
        plan_skills = []
    suite_by_id = (
        {
            item["id"]: item
            for item in suite_skills
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        if suite is not None
        else {}
    )
    descriptor_ids = set(descriptor_by_id)
    plan_research_ids = [
        item.get("research_id")
        for item in plan_skills
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    ]
    plan_ids = set(plan_research_ids)
    seen_plan_ids: set[str] = set()
    duplicate_plan_ids: set[str] = set()
    for research_id in plan_research_ids:
        if research_id in seen_plan_ids:
            duplicate_plan_ids.add(research_id)
        seen_plan_ids.add(research_id)
    if duplicate_plan_ids:
        errors.append(
            "production source plan repeats descriptor Skills: "
            f"{sorted(duplicate_plan_ids)}"
        )
    missing_plan_ids = sorted(descriptor_ids - plan_ids)
    extra_plan_ids = sorted(plan_ids - descriptor_ids)
    if missing_plan_ids:
        errors.append(f"production source plan is missing descriptor Skills: {missing_plan_ids}")
    if extra_plan_ids:
        errors.append(f"production source plan has unknown Skills: {extra_plan_ids}")

    mappings_by_source: dict[str, list[dict]] = {}
    for skill in plan.get("skills", []):
        if not isinstance(skill, dict):
            errors.append("production source promotion Skill entries must be objects")
            continue
        research_id = skill.get("research_id")
        descriptor_skill = descriptor_by_id.get(research_id)
        if not isinstance(descriptor_skill, dict):
            continue

        production_source = descriptor_skill.get("production_source")
        if not isinstance(production_source, dict):
            errors.append(f"production source authority missing for {research_id}")
            continue
        source_mode = production_source.get("mode")

        if skill.get("source") != production_source:
            errors.append(
                f"production source plan source snapshot mismatch for {research_id}"
            )

        expected_name = descriptor_skill.get("proposed_installable_name")
        if skill.get("production_name") != expected_name:
            errors.append(f"production source plan name mismatch for {research_id}")

        if source_mode == "canonical_manifest":
            if skill.get("state") != "existing-canonical-manifest":
                errors.append(
                    f"canonical_manifest source state must remain existing-canonical-manifest: {research_id}"
                )
            if skill.get("locales") != {}:
                errors.append(f"canonical_manifest source must not declare locale_tree mappings: {research_id}")
            continue

        if source_mode != "locale_tree":
            errors.append(f"unsupported production source mode for {research_id}: {source_mode!r}")
            continue
        if skill.get("state") != "planned-locale-tree-promotion":
            errors.append(f"locale_tree source state must remain planned-locale-tree-promotion: {research_id}")

        locales = skill.get("locales")
        if not isinstance(locales, dict):
            errors.append(f"production source plan locales missing for {research_id}")
            continue

        expected_locales = None
        if suite is not None:
            suite_skill = suite_by_id.get(research_id)
            realizations = (
                suite_skill.get("locale_realizations")
                if isinstance(suite_skill, dict)
                else None
            )
            if isinstance(realizations, dict):
                expected_locales = set(realizations)
        if expected_locales is None:
            expected_locales = {
                locale
                for locale in descriptor.get("locales", [])
                if isinstance(locale, str)
            }
        actual_locales = set(locales)
        if actual_locales != expected_locales:
            errors.append(
                "production source plan locale set mismatch: "
                f"{research_id}: missing={sorted(expected_locales - actual_locales)}, "
                f"extra={sorted(actual_locales - expected_locales)}"
            )

        if suite is not None:
            suite_skill = suite_by_id.get(research_id)
            if isinstance(suite_skill, dict):
                expected_excluded = _expected_excluded_research_metadata(suite_skill)
                if skill.get("excluded_research_metadata") != expected_excluded:
                    errors.append(
                        "production source plan excluded research metadata mismatch: "
                        f"{research_id}"
                    )

        for locale, locale_plan in locales.items():
            if not isinstance(locale, str):
                errors.append(
                    f"production source plan locale keys must be strings: {research_id}: {locale!r}"
                )
                continue
            if not isinstance(locale_plan, dict):
                errors.append(
                    f"production source plan locale entries must be objects: {research_id}/{locale}"
                )
                continue
            if locale_plan.get("research_package_mode") != "explicit_files":
                errors.append(
                    f"research package mode must remain explicit_files: {research_id}/{locale}"
                )
            if (
                locale_plan.get("copy_scope")
                != "declared-research-package-files-into-future-package-closed-tree"
            ):
                errors.append(
                    f"production source copy scope mismatch: {research_id}/{locale}"
                )
            if locale_plan.get("production_source_mode") != "locale_tree":
                errors.append(f"production source mode must remain locale_tree: {research_id}/{locale}")
            production_root = locale_plan.get("production_root")
            root_pattern = production_source.get("root_pattern")
            expected_production_root = None
            if isinstance(root_pattern, str) and isinstance(locale, str):
                try:
                    expected_production_root = root_pattern.format(locale=locale)
                except (KeyError, ValueError):
                    errors.append(
                        f"production source root pattern is invalid: {research_id}/{locale}"
                    )
            if (
                expected_production_root is not None
                and production_root != expected_production_root
            ):
                errors.append(
                    "production source root does not match descriptor authority: "
                    f"{research_id}/{locale}: {production_root!r} != "
                    f"{expected_production_root!r}"
                )
            if (
                not isinstance(production_root, str)
                or not _safe_repo_path(production_root)
                or not production_root.startswith("src/skills/")
            ):
                errors.append(
                    f"production source root must be a safe path under src/skills: "
                    f"{research_id}/{locale}"
                )
            if isinstance(production_root, str) and research_id in production_root and research_id != expected_name:
                errors.append(f"research id leaked into production source root: {research_id}/{locale}")
            if locale_plan.get("runtime_entry") != f"{production_root}/SKILL.md":
                errors.append(f"production runtime entry must normalize to SKILL.md: {research_id}/{locale}")
            mappings = locale_plan.get("mappings")
            if not isinstance(mappings, list) or not mappings:
                errors.append(f"production source mappings missing: {research_id}/{locale}")
                continue

            if suite is not None:
                suite_skill = suite_by_id.get(research_id)
                realization = (
                    suite_skill.get("locale_realizations", {}).get(locale)
                    if isinstance(suite_skill, dict)
                    else None
                )
                package_source = (
                    realization.get("package_source")
                    if isinstance(realization, dict)
                    else None
                )
                if (
                    not isinstance(package_source, dict)
                    or package_source.get("mode") != "explicit_files"
                    or not isinstance(package_source.get("root"), str)
                    or not isinstance(package_source.get("files"), list)
                ):
                    errors.append(
                        "suite package-source authority missing for locale_tree promotion: "
                        f"{research_id}/{locale}"
                    )
                else:
                    package_root = PurePosixPath(package_source["root"])
                    expected_pairs = {
                        ((package_root / relative).as_posix(), relative)
                        for relative in package_source["files"]
                        if isinstance(relative, str)
                    }
                    actual_pairs = [
                        (mapping.get("source"), mapping.get("source_relative"))
                        for mapping in mappings
                        if isinstance(mapping, dict)
                        and isinstance(mapping.get("source"), str)
                        and isinstance(mapping.get("source_relative"), str)
                    ]
                    actual_pair_set = set(actual_pairs)
                    if len(actual_pairs) != len(actual_pair_set):
                        errors.append(
                            "production source plan repeats package-selected source mapping: "
                            f"{research_id}/{locale}"
                        )
                    missing_pairs = sorted(expected_pairs - actual_pair_set)
                    extra_pairs = sorted(actual_pair_set - expected_pairs)
                    if missing_pairs:
                        errors.append(
                            "production source plan is missing package-selected source mappings: "
                            f"{research_id}/{locale}: {missing_pairs}"
                        )
                    if extra_pairs:
                        errors.append(
                            "production source plan contains undeclared source mappings: "
                            f"{research_id}/{locale}: {extra_pairs}"
                        )

            targets = [item.get("target_relative") for item in mappings if isinstance(item, dict)]
            normalized_targets = [
                target for target in targets if isinstance(target, str)
            ]
            computed_target_collision = (
                len(normalized_targets) != len(set(normalized_targets))
            )
            if locale_plan.get("target_collision") != computed_target_collision:
                errors.append(
                    "production source target collision metadata mismatch: "
                    f"{research_id}/{locale}"
                )
            if computed_target_collision:
                errors.append(
                    f"production source target collision detected: {research_id}/{locale}"
                )
            if "SKILL.md" not in targets:
                errors.append(f"production source mappings must contain SKILL.md: {research_id}/{locale}")
            if locale == "en-US":
                stale = [target for target in targets if isinstance(target, str) and ".en.md" in target]
                if stale:
                    errors.append(f"English production canonical filenames must drop .en suffix: {stale}")
            for mapping in mappings:
                if not isinstance(mapping, dict):
                    errors.append(f"production source mapping must be an object: {research_id}/{locale}")
                    continue
                source = mapping.get("source")
                source_relative = mapping.get("source_relative")
                target_relative = mapping.get("target_relative")
                target = mapping.get("target")
                if not isinstance(source, str) or not _safe_repo_path(source):
                    errors.append(
                        f"production source mapping source path is unsafe: "
                        f"{research_id}/{locale}: {source!r}"
                    )
                if (
                    not isinstance(source_relative, str)
                    or not _safe_repo_path(source_relative)
                ):
                    errors.append(
                        f"production source mapping source_relative is unsafe: "
                        f"{research_id}/{locale}: {source_relative!r}"
                    )
                if (
                    not isinstance(target_relative, str)
                    or not _safe_repo_path(target_relative)
                ):
                    errors.append(
                        f"production source mapping target_relative is unsafe: "
                        f"{research_id}/{locale}: {target_relative!r}"
                    )
                if (
                    not isinstance(target, str)
                    or not _safe_repo_path(target)
                    or not target.startswith("src/skills/")
                ):
                    errors.append(
                        f"production source mapping target path is unsafe: "
                        f"{research_id}/{locale}: {target!r}"
                    )
                if isinstance(source_relative, str):
                    expected_target_relative = _target_relative(source_relative, locale)
                    if target_relative != expected_target_relative:
                        errors.append(
                            "production source mapping target_relative does not match source normalization: "
                            f"{research_id}/{locale}: {source_relative!r} -> {target_relative!r}; "
                            f"expected {expected_target_relative!r}"
                        )
                    if isinstance(production_root, str):
                        expected_target = (
                            PurePosixPath(production_root) / expected_target_relative
                        ).as_posix()
                        if target != expected_target:
                            errors.append(
                                "production source mapping target does not match production root: "
                                f"{research_id}/{locale}: {target!r}; expected {expected_target!r}"
                            )
                if isinstance(source, str):
                    mappings_by_source.setdefault(source, []).append(mapping)
                if (
                    inventory is not None
                    and isinstance(source, str)
                    and isinstance(source_relative, str)
                ):
                    expected_transforms = _expected_content_transforms(
                        source,
                        source_relative,
                        locale,
                        inventory_actions,
                    )
                    actual_transforms = mapping.get("content_transforms")
                    if actual_transforms != expected_transforms:
                        errors.append(
                            "production source mapping content transforms do not match declared authorities: "
                            f"{research_id}/{locale}: {source_relative!r}: "
                            f"{actual_transforms!r} != {expected_transforms!r}"
                        )

    if inventory is not None:
        source_prefixes = (
            _locale_tree_source_prefixes(suite, descriptor)
            if suite is not None
            else _planned_source_prefixes(plan)
        )
        expected_actions = {
            path: action
            for path, action in _projection_actions(inventory).items()
            if any(path.startswith(prefix) for prefix in source_prefixes)
        }
        for source, action in sorted(expected_actions.items()):
            mappings = mappings_by_source.get(source)
            if not mappings:
                errors.append(
                    f"promotion-sensitive source declared by projection inventory is missing from source plan: {source}"
                )
                continue
            for mapping in mappings:
                transforms = mapping.get("content_transforms")
                if not isinstance(transforms, list) or action not in transforms:
                    errors.append(
                        "production source mapping is missing projection-inventory transform: "
                        f"{source} -> {action}"
                    )

    return errors


def main() -> int:
    try:
        suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
        inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production source promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_source_promotion_authorities(
        ROOT,
        suite,
        descriptor,
        migration,
        inventory,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        plan = plan_production_source_promotion(suite, descriptor, migration, inventory)
    except (KeyError, TypeError, ValueError) as exc:
        print(f"production source promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_source_promotion_plan(
        plan,
        descriptor,
        inventory,
        suite=suite,
        migration=migration,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
