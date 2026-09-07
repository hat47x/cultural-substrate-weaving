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


def _skill_metadata_paths(skill: dict) -> set[str]:
    paths: set[str] = set()
    for field in ("references", "evidence", "evals", "checks"):
        values = skill.get(field, [])
        if isinstance(values, list):
            paths.update(value for value in values if isinstance(value, str))
    return paths


def plan_production_source_promotion(
    suite: dict,
    descriptor: dict,
    migration: dict,
    inventory: dict,
) -> dict:
    descriptor_by_id = {
        item["research_id"]: item
        for item in descriptor["skills"]
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }
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

        if research_id == "cultural-substrate-weaving":
            output["skills"].append(
                {
                    "research_id": research_id,
                    "production_name": production_name,
                    "state": "existing-canonical-manifest",
                    "source": descriptor_skill["production_source"],
                    "locales": {},
                }
            )
            continue

        production_source = descriptor_skill["production_source"]
        if production_source.get("mode") != "locale_tree":
            raise ValueError(f"sibling {research_id} production source is not locale_tree")

        locale_output: dict[str, dict] = {}
        promoted_repo_sources: set[str] = set()
        for locale, realization in skill["locale_realizations"].items():
            package_source = realization["package_source"]
            if package_source.get("mode") != "explicit_files":
                raise ValueError(
                    f"research sibling {research_id}/{locale} package source must be explicit_files"
                )
            research_root = PurePosixPath(package_source["root"])
            production_root = production_source["root_pattern"].format(locale=locale)
            mappings = []

            for relative in package_source["files"]:
                source_repo = (research_root / relative).as_posix()
                promoted_repo_sources.add(source_repo)
                target_relative = _target_relative(relative, locale)
                target_repo = (PurePosixPath(production_root) / target_relative).as_posix()
                transforms: list[str] = []

                inventory_action = inventory_actions.get(source_repo)
                if inventory_action:
                    transforms.append(inventory_action)
                if locale == "en-US" and target_relative != relative:
                    transforms.append("normalize-locale-suffixed-filename")
                    if relative.endswith("SKILL.en.md"):
                        transforms.append("rewrite-package-local-locale-suffix-references")

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


def validate_production_source_promotion_plan(plan: dict, descriptor: dict) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"production source promotion plan schema must be {PLAN_SCHEMA}")
    if plan.get("status") != "design-only":
        errors.append("production source promotion plan must remain design-only")
    if plan.get("selection_basis") != "research locale package_source.files":
        errors.append("production source promotion selection must remain package_source.files based")

    descriptor_by_id = {
        item["research_id"]: item
        for item in descriptor.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }
    for skill in plan.get("skills", []):
        if not isinstance(skill, dict):
            errors.append("production source promotion Skill entries must be objects")
            continue
        research_id = skill.get("research_id")
        if research_id == "cultural-substrate-weaving":
            if skill.get("state") != "existing-canonical-manifest":
                errors.append("CSW source promotion state must remain existing-canonical-manifest")
            continue

        descriptor_skill = descriptor_by_id.get(research_id, {})
        expected_name = descriptor_skill.get("proposed_installable_name")
        if skill.get("production_name") != expected_name:
            errors.append(f"production source plan name mismatch for {research_id}")
        if research_id == "affinity-synthesis" and skill.get("production_name") != "material-led-synthesis":
            errors.append("Layer 1 production source name must be material-led-synthesis")

        locales = skill.get("locales")
        if not isinstance(locales, dict):
            errors.append(f"production source plan locales missing for {research_id}")
            continue
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
            targets = [item.get("target_relative") for item in mappings if isinstance(item, dict)]
            if "SKILL.md" not in targets:
                errors.append(f"production source mappings must contain SKILL.md: {research_id}/{locale}")
            if locale == "en-US":
                stale = [target for target in targets if isinstance(target, str) and ".en.md" in target]
                if stale:
                    errors.append(f"English production canonical filenames must drop .en suffix: {stale}")

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

    errors = validate_production_source_promotion_plan(plan, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
