#!/usr/bin/env python3
"""Plan distribution-specific research Skill package trees without writing them."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_package_targets import validate_package_targets  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402
from plan_suite_layout import plan_suite  # noqa: E402

PLAN_SCHEMA = "csw.research-skill-package-tree-plan/v1"


def _explicit_files(realization: dict) -> list[dict]:
    source = realization["package_source"]
    root = Path(source["root"])
    runtime = Path(realization["runtime_entry"])
    mappings: list[dict] = []
    for relative_text in source["files"]:
        relative = Path(relative_text)
        repo_source = (root / relative).as_posix()
        target = "SKILL.md" if Path(repo_source) == runtime else relative.as_posix()
        mappings.append({"source": repo_source, "target": target})
    return mappings


def _canonical_manifest_files(realization: dict) -> list[dict]:
    source = realization["package_source"]
    manifest_path = ROOT / source["manifest"]
    config = json.loads(manifest_path.read_text(encoding="utf-8"))
    locale_root = Path(source["locale_root"])
    mappings = [
        {
            "source": (locale_root / config["router"]).as_posix(),
            "target": "SKILL.md",
        }
    ]
    for module in config["modules"]:
        mappings.append(
            {
                "source": (locale_root / module["source"]).as_posix(),
                "target": f"references/{module['skill_reference']}",
            }
        )
    return mappings


def _source_files(realization: dict) -> list[dict]:
    mode = realization["package_source"]["mode"]
    if mode == "explicit_files":
        return _explicit_files(realization)
    if mode == "canonical_manifest":
        return _canonical_manifest_files(realization)
    raise ValueError(f"unsupported package_source mode: {mode!r}")


def _skill_ids_for_distribution(manifest: dict, distribution_name: str, config: dict) -> list[str]:
    mode = config.get("mode")
    if mode == "standalone_per_skill":
        return [skill["id"] for skill in manifest["skills"]]
    if mode == "locale_bundle":
        return list(config.get("contains", []))
    return []


def _target_root(mode: str, skill_name: str) -> str:
    if mode == "standalone_per_skill":
        return skill_name
    if mode == "locale_bundle":
        return f"skills/{skill_name}"
    raise ValueError(f"distribution has no Skill-tree target root: {mode!r}")


def plan_package_trees(manifest: dict) -> tuple[dict, list[str]]:
    layout = plan_suite(manifest)
    skill_map = {skill["id"]: skill for skill in manifest["skills"]}
    errors: list[str] = []
    plan = {
        "schema": PLAN_SCHEMA,
        "suite_id": manifest.get("suite_id"),
        "note": (
            "Target paths are a read-only research projection from package_source + "
            "package_targets. They are not generated or release-validated artifacts."
        ),
        "locales": {},
    }

    for locale in manifest["locales"]:
        locale_out: dict[str, dict] = {"distributions": {}}
        for distribution_name, config in manifest["distribution_prototypes"].items():
            mode = config.get("mode")
            layout_distribution = layout["locales"][locale]["distributions"][distribution_name]
            if mode == "composite_agent_realization":
                locale_out["distributions"][distribution_name] = {
                    "mode": mode,
                    "state": layout_distribution["state"],
                    "skill_trees": [],
                    "scope": "composite realization; no sibling Skill subtree is planned here",
                }
                continue
            if mode not in {"standalone_per_skill", "locale_bundle"}:
                locale_out["distributions"][distribution_name] = {
                    "mode": mode,
                    "state": "unsupported",
                    "skill_trees": [],
                }
                continue

            skill_trees: list[dict] = []
            occupied: dict[str, list[str]] = {}
            for skill_id in _skill_ids_for_distribution(manifest, distribution_name, config):
                skill = skill_map.get(skill_id)
                if skill is None:
                    continue
                realization = skill.get("locale_realizations", {}).get(locale, {})
                if realization.get("status") == "planned":
                    continue
                target = realization.get("package_targets", {}).get(distribution_name)
                if not isinstance(target, dict) or not target.get("skill_name"):
                    continue
                root = _target_root(mode, target["skill_name"])
                files = []
                for mapping in _source_files(realization):
                    target_path = f"{root}/{mapping['target']}"
                    files.append({**mapping, "target_path": target_path})
                    occupied.setdefault(target_path, []).append(skill_id)
                skill_trees.append(
                    {
                        "skill_id": skill_id,
                        "skill_name": target["skill_name"],
                        "target_root": root,
                        "files": files,
                    }
                )
            collisions = {
                path: owners for path, owners in occupied.items() if len(owners) > 1
            }
            for path, owners in sorted(collisions.items()):
                errors.append(
                    f"locale {locale} distribution {distribution_name} target path collision "
                    f"{path!r}: {owners}"
                )
            locale_out["distributions"][distribution_name] = {
                "mode": mode,
                "state": layout_distribution["state"],
                "skill_trees": skill_trees,
                "collisions": collisions,
            }
        plan["locales"][locale] = locale_out
    return plan, errors


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        errors = validate_suite(ROOT, manifest)
        errors.extend(validate_package_targets(manifest))
        plan, tree_errors = plan_package_trees(manifest)
        errors.extend(tree_errors)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"research package tree planning failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
