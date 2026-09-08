#!/usr/bin/env python3
"""Preview production-canonical sibling Skill source transforms without writing src/skills.

This is a research-only content projection probe. It consumes the read-only
production-source promotion plan, applies only declared content transforms in
memory, validates promotion-sensitive runtime/Method results, and prints hashes
and target paths. It never writes production source files.

The preview also re-runs package-local runtime and Markdown-link closure after
all path and content transforms. Source-stage closure alone is insufficient
because locale filename normalization and public-name projection can change the
final package tree.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "skill-prototypes"
SUITE_PATH = BASE / "suite-manifest.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
MIGRATION_PATH = BASE / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
INVENTORY_PATH = BASE / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"
PLANNER_DIR = BASE / "scripts"
VALIDATOR_DIR = ROOT / "scripts"
for directory in (PLANNER_DIR, VALIDATOR_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from plan_production_source_promotion import (  # noqa: E402
    plan_production_source_promotion,
    validate_production_source_promotion_plan,
)
from validate_research_package_reference_closure import (  # noqa: E402
    validate_in_memory_package_reference_closure,
)

PREVIEW_SCHEMA = "csw.production-source-content-preview/v1"
FRONTMATTER_NAME_RE = re.compile(r"(?m)^name:\s*([^\n]+)$")


class ProjectionError(ValueError):
    pass


def _replace_required(text: str, old: str, new: str, action: str, source: str) -> str:
    count = text.count(old)
    if count == 0:
        raise ProjectionError(f"{action}: required marker missing in {source}: {old!r}")
    return text.replace(old, new)


def _rename_pair(plan: dict) -> tuple[str, str]:
    pairs: list[tuple[str, str]] = []
    for skill in plan.get("skills", []):
        if not isinstance(skill, dict):
            continue
        research_id = skill.get("research_id")
        production_name = skill.get("production_name")
        if (
            isinstance(research_id, str)
            and isinstance(production_name, str)
            and research_id
            and production_name
            and research_id != production_name
        ):
            pairs.append((research_id, production_name))
    if len(pairs) != 1:
        raise ProjectionError(
            "production source preview requires exactly one declared renamed Skill identity; "
            f"found {pairs!r}"
        )
    return pairs[0]


def _rewrite_frontmatter_name(
    text: str,
    research_id: str,
    production_name: str,
    source: str,
) -> str:
    match = FRONTMATTER_NAME_RE.search(text)
    if match is None:
        raise ProjectionError(f"rewrite-frontmatter-name-only: frontmatter name missing in {source}")
    current = match.group(1).strip().strip("\"'")
    if current != research_id:
        raise ProjectionError(
            "rewrite-frontmatter-name-only: unexpected source name "
            f"in {source}: {current!r} != {research_id!r}"
        )
    start, end = match.span()
    return text[:start] + f"name: {production_name}" + text[end:]


def apply_content_transforms(
    text: str,
    transforms: list[str],
    *,
    source: str,
    research_id: str,
    production_name: str,
) -> str:
    projected = text
    for action in transforms:
        if action == "rewrite-frontmatter-name-only":
            projected = _rewrite_frontmatter_name(
                projected,
                research_id,
                production_name,
                source,
            )
        elif action == "rewrite-explicit-installable-name":
            projected = _replace_required(
                projected,
                f"`{research_id}`",
                f"`{production_name}`",
                action,
                source,
            )
        elif action == "rewrite-explicit-installable-name-and-remove-sibling-filesystem-reference":
            projected = _replace_required(
                projected,
                f"sibling prototype `../{research_id}/`",
                f"companion Skill `{production_name}`",
                action,
                source,
            )
            projected = _replace_required(
                projected,
                f"`{research_id}`",
                f"`{production_name}`",
                action,
                source,
            )
        elif action == "rewrite-realization-identifier-not-method-role":
            projected = _replace_required(
                projected,
                f"`{research_id}`",
                f"`{production_name}`",
                action,
                source,
            )
        elif action == "normalize-locale-suffixed-filename":
            continue
        elif action == "rewrite-package-local-locale-suffix-references":
            if ".en.md" not in projected:
                raise ProjectionError(
                    f"{action}: no package-local .en.md reference remains in {source}"
                )
            projected = projected.replace(".en.md", ".md")
        else:
            raise ProjectionError(f"unsupported production source content transform: {action}")
    return projected


def _frontmatter_name(text: str) -> str | None:
    match = FRONTMATTER_NAME_RE.search(text)
    if match is None:
        return None
    return match.group(1).strip().strip("\"'")


def project_production_source_contents(plan: dict, root: Path = ROOT) -> dict[str, dict]:
    projected: dict[str, dict] = {}
    rename_research_id, rename_production_name = _rename_pair(plan)
    for skill in plan.get("skills", []):
        if not isinstance(skill, dict) or skill.get("research_id") == "cultural-substrate-weaving":
            continue
        production_name = skill.get("production_name")
        for locale, locale_plan in skill.get("locales", {}).items():
            for mapping in locale_plan.get("mappings", []):
                source = mapping["source"]
                target = mapping["target"]
                source_path = root / source
                text = source_path.read_text(encoding="utf-8")
                transforms = mapping.get("content_transforms", [])
                result = apply_content_transforms(
                    text,
                    transforms,
                    source=source,
                    research_id=rename_research_id,
                    production_name=rename_production_name,
                )
                if target in projected:
                    raise ProjectionError(f"duplicate projected production target: {target}")
                projected[target] = {
                    "research_id": skill["research_id"],
                    "production_name": production_name,
                    "locale": locale,
                    "source": source,
                    "target": target,
                    "target_relative": mapping["target_relative"],
                    "content_transforms": transforms,
                    "content": result,
                    "sha256": hashlib.sha256(result.encode("utf-8")).hexdigest(),
                }
    return projected


def validate_projected_contents(projected: dict[str, dict], plan: dict) -> list[str]:
    errors: list[str] = []
    rename_research_id, _ = _rename_pair(plan)
    by_skill_locale: dict[tuple[str, str], list[dict]] = {}
    for item in projected.values():
        key = (item["research_id"], item["locale"])
        by_skill_locale.setdefault(key, []).append(item)

        content = item.get("content", "")
        if f"`{rename_research_id}`" in content:
            errors.append(
                "projected production package content retains research installable identifier: "
                f"{item['target']}"
            )
        if f"../{rename_research_id}/" in content:
            errors.append(
                "projected production package content retains research sibling filesystem path: "
                f"{item['target']}"
            )

    for skill in plan.get("skills", []):
        if not isinstance(skill, dict) or skill.get("research_id") == "cultural-substrate-weaving":
            continue
        research_id = skill["research_id"]
        production_name = skill["production_name"]
        for locale, locale_plan in skill.get("locales", {}).items():
            items = by_skill_locale.get((research_id, locale), [])
            runtime_target = locale_plan.get("runtime_entry")
            runtime = projected.get(runtime_target)
            if runtime is None:
                errors.append(f"projected runtime entry missing: {research_id}/{locale}")
                continue
            frontmatter_name = _frontmatter_name(runtime["content"])
            if frontmatter_name != production_name:
                errors.append(
                    f"projected runtime frontmatter name mismatch: {research_id}/{locale}: "
                    f"{frontmatter_name!r} != {production_name!r}"
                )

            target_relatives = {item["target_relative"] for item in items}
            if len(target_relatives) != len(items):
                errors.append(f"projected target-relative collision: {research_id}/{locale}")

            projected_file_map = {
                item["target_relative"]: item["content"]
                for item in items
                if isinstance(item.get("target_relative"), str)
                and isinstance(item.get("content"), str)
            }
            errors.extend(
                validate_in_memory_package_reference_closure(
                    projected_file_map,
                    "SKILL.md",
                    label=f"projected package {research_id}/{locale}",
                )
            )

            if locale == "en-US":
                if any(".en.md" in relative for relative in target_relatives):
                    errors.append(f"English projected filenames retain .en suffix: {research_id}")
                if ".en.md" in runtime["content"]:
                    errors.append(f"English projected runtime retains package-local .en.md reference: {research_id}")

    return errors


def build_preview() -> dict:
    suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
    descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    plan = plan_production_source_promotion(suite, descriptor, migration, inventory)
    plan_errors = validate_production_source_promotion_plan(plan, descriptor, inventory)
    if plan_errors:
        raise ProjectionError("; ".join(plan_errors))
    projected = project_production_source_contents(plan)
    errors = validate_projected_contents(projected, plan)
    if errors:
        raise ProjectionError("; ".join(errors))
    return {
        "schema": PREVIEW_SCHEMA,
        "status": "design-only-preview",
        "writes_production_source": False,
        "files": [
            {key: value for key, value in item.items() if key != "content"}
            for _, item in sorted(projected.items())
        ],
    }


def main() -> int:
    try:
        preview = build_preview()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ProjectionError, ValueError) as exc:
        print(f"production source content preview failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(preview, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
