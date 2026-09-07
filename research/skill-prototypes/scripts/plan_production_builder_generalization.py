#!/usr/bin/env python3
"""Project the design-only production descriptor into concrete builder targets.

This planner is read-only. It does not create src/skills, adapter metadata,
generated packages, or release artifacts. Its purpose is to make the future
scripts/build.py change reviewable before production promotion is authorized.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json"
)
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_production_builder_contract import (  # noqa: E402
    validate_production_builder_contract,
)
from validate_research_production_suite_descriptor import (  # noqa: E402
    validate_production_suite_descriptor,
)

PLAN_SCHEMA = "csw.production-builder-generalization-plan/v1"


def _format_source(skill: dict, locale: str) -> dict:
    source = skill["production_source"]
    mode = source["mode"]
    if mode == "canonical_manifest":
        return {
            "mode": mode,
            "manifest": source["manifest"],
            "operation": "render_runtime_entry_and_copy_manifest_references",
        }
    if mode == "locale_tree":
        root = source["root_pattern"].format(locale=locale)
        return {
            "mode": mode,
            "root": root,
            "runtime_entry": f"{root}/{source['runtime_entry']}",
            "operation": "copy_locale_tree_preserving_runtime_relative_paths",
            "copy_scope": "entire_locale_tree",
            "package_closed": True,
            "exclusion_filter": "none",
        }
    raise ValueError(f"unsupported production source mode: {mode!r}")


def _adapter_source(skill: dict, distribution: str, locale: str, profile: str | None = None) -> str | None:
    metadata = skill.get("adapter_metadata", {}).get(distribution, {})
    if not isinstance(metadata, dict):
        return None
    pattern = metadata.get("source_pattern")
    if isinstance(pattern, str):
        values = {"locale": locale, "profile": profile or ""}
        return pattern.format(**values)
    source = metadata.get("source")
    return source if isinstance(source, str) else None


def _skill_items(descriptor: dict, locale: str, distribution: str) -> list[dict]:
    items = []
    for skill in descriptor["skills"]:
        target_name = skill["targets"][distribution]
        items.append(
            {
                "research_id": skill["research_id"],
                "public_installable_name": skill["proposed_installable_name"],
                "target_name": target_name,
                "source": _format_source(skill, locale),
            }
        )
    return items


def _collisions(items: list[dict], target_key: str) -> list[dict]:
    owners: dict[str, list[str]] = {}
    for item in items:
        target = item[target_key]
        owners.setdefault(target, []).append(item["research_id"])
    return [
        {"target": target, "research_ids": research_ids}
        for target, research_ids in sorted(owners.items())
        if len(research_ids) > 1
    ]


def plan_production_builder(descriptor: dict, contract: dict) -> dict:
    output = {
        "schema": PLAN_SCHEMA,
        "status": "design-only",
        "suite_id": descriptor["suite_id"],
        "note": (
            "Concrete target projection only. Paths may name future production sources that do not "
            "exist yet. This plan does not authorize production promotion or builder writes."
        ),
        "gate_snapshot": {
            "complete_checkout_validation": descriptor.get("complete_checkout_validation", {}).get("status"),
            "public_name_recheck_date": descriptor.get("public_name_recheck", {}).get("date"),
            "english_independent_review": descriptor.get("english_independent_review", {}).get("status"),
            "production_promotion_authorized": False,
        },
        "locales": {},
        "deferred_composite": contract["deferred_composite"],
    }

    for locale in descriptor["locales"]:
        locale_plan = {"distributions": {}}

        openai_profiles = contract["first_wave"]["openai_skill"]["profiles"]
        profile_plans = {}
        for profile in openai_profiles:
            items = _skill_items(descriptor, locale, "openai_skill")
            planned_items = []
            for item, skill in zip(items, descriptor["skills"]):
                target = f"dist/{locale}/openai-skill/{profile}/{item['target_name']}"
                planned_items.append(
                    {
                        **item,
                        "target_root": target,
                        "runtime_entry": f"{target}/SKILL.md",
                        "adapter_metadata": _adapter_source(
                            skill, "openai_skill", locale, profile
                        ),
                    }
                )
            profile_plans[profile] = {
                "target_root": f"dist/{locale}/openai-skill/{profile}",
                "skills": planned_items,
                "collisions": _collisions(planned_items, "target_root"),
            }
        locale_plan["distributions"]["openai_skill"] = {
            "mode": "standalone_per_skill",
            "profiles": profile_plans,
        }

        bundle = descriptor["bundle_identity"][locale]
        plugin_root = f"plugins/{bundle['plugin_name']}"
        claude_items = _skill_items(descriptor, locale, "claude_plugin")
        claude_planned = []
        for item in claude_items:
            target = f"{plugin_root}/skills/{item['target_name']}"
            claude_planned.append(
                {
                    **item,
                    "target_root": target,
                    "runtime_entry": f"{target}/SKILL.md",
                }
            )
        locale_plan["distributions"]["claude_plugin"] = {
            "mode": "locale_bundle",
            "plugin_name": bundle["plugin_name"],
            "display": bundle["display"],
            "plugin_root": plugin_root,
            "skills": claude_planned,
            "collisions": _collisions(claude_planned, "target_root"),
        }

        codex_items = _skill_items(descriptor, locale, "codex_plugin")
        codex_planned = []
        for item in codex_items:
            target = f"{plugin_root}/skills/{item['target_name']}"
            codex_planned.append(
                {
                    **item,
                    "target_root": target,
                    "runtime_entry": f"{target}/SKILL.md",
                    "materialization": "reuse_claude_plugin_skill_tree",
                }
            )
        locale_plan["distributions"]["codex_plugin"] = {
            "mode": "reuse_claude_skill_tree",
            "plugin_name": bundle["plugin_name"],
            "plugin_root": plugin_root,
            "skills": codex_planned,
            "collisions": _collisions(codex_planned, "target_root"),
            "new_release_zip_kind": False,
        }

        locale_plan["shared_tree_checks"] = {
            "claude_codex_target_roots_equal": [
                item["target_root"] for item in claude_planned
            ]
            == [item["target_root"] for item in codex_planned],
            "research_ids_do_not_control_target_paths": all(
                item["target_name"] == skill["targets"]["claude_plugin"]
                for item, skill in zip(claude_planned, descriptor["skills"])
            ),
        }
        output["locales"][locale] = locale_plan

    return output


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production builder generalization planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_suite_descriptor(descriptor)
    errors.extend(validate_production_builder_contract(ROOT, contract, descriptor))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("production builder generalization planning stopped on invalid research contract", file=sys.stderr)
        return 1

    try:
        plan = plan_production_builder(descriptor, contract)
    except (KeyError, ValueError) as exc:
        print(f"production builder generalization planning failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
