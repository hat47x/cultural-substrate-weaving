#!/usr/bin/env python3
"""Plan research Skill subtrees without generating package files.

This planner maps declared package sources to distribution-relative target paths.
It intentionally stops before host-specific frontmatter, marketplace metadata,
archive generation, or release validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
VALIDATOR_DIR = ROOT / "scripts"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
for path in (VALIDATOR_DIR, PLANNER_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_suite_layout import plan_suite  # noqa: E402
from validate_research_package_targets import validate_package_targets  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402

PLAN_SCHEMA = "csw.research-skill-subtree-plan/v1"


def _posix_join(*parts: str) -> str:
    return PurePosixPath(*parts).as_posix()


def _source_mappings(root: Path, skill: dict, locale: str) -> list[dict]:
    realization = skill["locale_realizations"][locale]
    package_source = realization["package_source"]
    mode = package_source["mode"]

    if mode == "explicit_files":
        source_root = package_source["root"]
        runtime_entry = PurePosixPath(realization["runtime_entry"]).as_posix()
        mappings = []
        for relative in package_source["files"]:
            source = _posix_join(source_root, relative)
            target_relative = (
                "SKILL.md"
                if PurePosixPath(source).as_posix() == runtime_entry
                else PurePosixPath(relative).as_posix()
            )
            mappings.append(
                {
                    "source": source,
                    "target_relative": target_relative,
                    "operation": "copy",
                }
            )
        return mappings

    if mode == "canonical_manifest":
        manifest_path = root / package_source["manifest"]
        config = json.loads(manifest_path.read_text(encoding="utf-8"))
        locale_root = package_source["locale_root"]
        mappings = [
            {
                "source": realization["runtime_entry"],
                "target_relative": "SKILL.md",
                "operation": "render_runtime_entry",
            }
        ]
        for module in config["modules"]:
            mappings.append(
                {
                    "source": _posix_join(locale_root, module["source"]),
                    "target_relative": _posix_join(
                        "references", module["skill_reference"]
                    ),
                    "operation": "copy",
                }
            )
        return mappings

    raise ValueError(f"unsupported package source mode: {mode!r}")


def _subtree(
    root: Path,
    skill: dict,
    locale: str,
    distribution_name: str,
    distribution_mode: str,
    skill_name: str,
) -> dict:
    if distribution_mode == "standalone_per_skill":
        target_root = skill_name
    elif distribution_mode == "locale_bundle":
        target_root = _posix_join("skills", skill_name)
    else:
        raise ValueError(f"unsupported Skill-tree distribution mode: {distribution_mode!r}")

    mappings = []
    for mapping in _source_mappings(root, skill, locale):
        mappings.append(
            {
                **mapping,
                "target": _posix_join(target_root, mapping["target_relative"]),
            }
        )

    return {
        "skill_id": skill["id"],
        "skill_name": skill_name,
        "target_root": target_root,
        "source_mode": skill["locale_realizations"][locale]["package_source"]["mode"],
        "mappings": mappings,
        "scope": (
            "source-to-target path mapping only; host-specific runtime-entry rendering and "
            "package metadata are not materialized"
        ),
    }


def _collisions(subtrees: list[dict]) -> list[dict]:
    owners: dict[str, list[str]] = {}
    for subtree in subtrees:
        for mapping in subtree["mappings"]:
            owners.setdefault(mapping["target"], []).append(subtree["skill_id"])

    return [
        {"target": target, "skill_ids": skill_ids}
        for target, skill_ids in sorted(owners.items())
        if len(skill_ids) > 1
    ]


def _subtree_state(
    layout_state: str,
    subtrees: list[dict],
    missing: list[str],
    collisions: list[dict],
) -> str:
    if collisions:
        return "collision"
    if layout_state == "buildable" and not missing:
        return "planned"
    if subtrees:
        return "partial"
    return "blocked"


def plan_skill_subtrees(manifest: dict, root: Path = ROOT) -> dict:
    """Return source-to-target path mappings for Skill-tree distribution shapes."""

    layout = plan_suite(manifest)
    skill_map = {
        skill["id"]: skill
        for skill in manifest.get("skills", [])
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    }

    output = {
        "schema": PLAN_SCHEMA,
        "suite_id": manifest.get("suite_id"),
        "note": (
            "This is a read-only Skill-subtree path plan. It does not apply host-specific "
            "frontmatter, adapter metadata, package generation, or release validation."
        ),
        "locales": {},
    }

    for locale in manifest.get("locales", {}):
        locale_output = {"distributions": {}}
        layout_distributions = layout["locales"][locale]["distributions"]

        for distribution_name, config in manifest.get("distribution_prototypes", {}).items():
            mode = config.get("mode") if isinstance(config, dict) else None
            layout_distribution = layout_distributions[distribution_name]

            if mode == "standalone_per_skill":
                item_map = {
                    item["skill_id"]: item
                    for item in layout_distribution["items"]
                }
                subtrees = []
                missing = []
                for skill_id in skill_map:
                    item = item_map[skill_id]
                    if item["state"] != "buildable" or item["package_target"] is None:
                        missing.append(skill_id)
                        continue
                    subtrees.append(
                        _subtree(
                            root,
                            skill_map[skill_id],
                            locale,
                            distribution_name,
                            mode,
                            item["package_target"]["skill_name"],
                        )
                    )

                collisions = _collisions(subtrees)
                locale_output["distributions"][distribution_name] = {
                    "mode": mode,
                    "layout_state": layout_distribution["state"],
                    "subtree_state": _subtree_state(
                        layout_distribution["state"], subtrees, missing, collisions
                    ),
                    "missing_skills": missing,
                    "collisions": collisions,
                    "subtrees": subtrees,
                }
                continue

            if mode == "locale_bundle":
                subtrees = []
                missing = list(layout_distribution["missing_skills"])
                for skill_id in layout_distribution["realized_skills"]:
                    subtrees.append(
                        _subtree(
                            root,
                            skill_map[skill_id],
                            locale,
                            distribution_name,
                            mode,
                            layout_distribution["target_skill_names"][skill_id],
                        )
                    )

                collisions = _collisions(subtrees)
                locale_output["distributions"][distribution_name] = {
                    "mode": mode,
                    "layout_state": layout_distribution["state"],
                    "subtree_state": _subtree_state(
                        layout_distribution["state"], subtrees, missing, collisions
                    ),
                    "missing_skills": missing,
                    "collisions": collisions,
                    "subtrees": subtrees,
                }
                continue

            if mode == "composite_agent_realization":
                locale_output["distributions"][distribution_name] = {
                    "mode": mode,
                    "layout_state": layout_distribution["state"],
                    "subtree_state": "not-applicable",
                    "subtrees": [],
                    "reason": (
                        "composite agent realization does not yet declare sibling Skill-subtree "
                        "materialization in the research packaging contract"
                    ),
                }
                continue

            locale_output["distributions"][distribution_name] = {
                "mode": mode,
                "layout_state": layout_distribution["state"],
                "subtree_state": "unsupported",
                "subtrees": [],
            }

        output["locales"][locale] = locale_output

    return output


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research Skill subtree planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_suite(ROOT, manifest)
    errors.extend(validate_package_targets(manifest))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("research Skill subtree planning stopped on invalid manifest", file=sys.stderr)
        return 1

    try:
        plan = plan_skill_subtrees(manifest, ROOT)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"research Skill subtree planning failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
