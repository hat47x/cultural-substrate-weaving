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
from validate_research_skill_suite import validate_suite  # noqa: E402

PLAN_SCHEMA = "csw.production-source-promotion-plan/v1"


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


def _descriptor_by_id(descriptor: dict) -> dict[str, dict]:
    return {
        item["research_id"]: item
        for item in descriptor.get("skills", [])
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


def plan_production_source_promotion(
    suite: dict,
    descriptor: dict,
    migration: dict,
    inventory: dict,
) -> dict:
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

    descriptor_locales = {
        locale
        for locale in descriptor.get("locales", [])
        if isinstance(locale, str)
    }
    if not descriptor_locales:
        raise ValueError("production descriptor must declare locales")

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

    name_map = migration["research_to_production_name"]
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
            research_root = PurePosixPath(package_source["root"])
            production_root = production_source["root_pattern"].format(locale=locale)
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
) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"production source promotion plan schema must be {PLAN_SCHEMA}")
    if plan.get("status") != "design-only":
        errors.append("production source promotion plan must remain design-only")
    if plan.get("selection_basis") != "research locale package_source.files":
        errors.append("production source promotion selection must remain package_source.files based")

    descriptor_by_id = _descriptor_by_id(descriptor)
    inventory_actions = _projection_actions(inventory) if inventory is not None else {}
    suite_by_id = (
        {
            item["id"]: item
            for item in suite.get("skills", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        if suite is not None
        else {}
    )
    descriptor_ids = set(descriptor_by_id)
    plan_ids = {
        item.get("research_id")
        for item in plan.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }
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

        for locale, locale_plan in locales.items():
            if locale_plan.get("production_source_mode") != "locale_tree":
                errors.append(f"production source mode must remain locale_tree: {research_id}/{locale}")
            production_root = locale_plan.get("production_root")
            if not isinstance(production_root, str) or not production_root.startswith("src/skills/"):
                errors.append(f"production source root must stay under src/skills: {research_id}/{locale}")
            if isinstance(production_root, str) and research_id in production_root and research_id != expected_name:
                errors.append(f"research id leaked into production source root: {research_id}/{locale}")
            if locale_plan.get("runtime_entry") != f"{production_root}/SKILL.md":
                errors.append(f"production runtime entry must normalize to SKILL.md: {research_id}/{locale}")
            if locale_plan.get("target_collision") is not False:
                errors.append(f"production source target collision detected: {research_id}/{locale}")

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

    errors = validate_suite(ROOT, suite)
    errors.extend(validate_production_suite_descriptor(descriptor))
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
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
