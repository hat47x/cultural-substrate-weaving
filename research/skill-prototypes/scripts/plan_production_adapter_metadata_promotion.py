#!/usr/bin/env python3
"""Plan research adapter metadata promotion into future production sources.

Read-only research planner. It does not write adapters/openai-skill or mutate
adapters/claude-code/locales.json. OpenAI sibling metadata is copied to the
public-name production path without content rewriting; Claude/Codex bundle
prototypes contribute reviewed wording only while existing locale/plugin
identity remains authoritative.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "skill-prototypes"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
LOCALE_CATALOG_PATH = ROOT / "adapters" / "claude-code" / "locales.json"
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402
from validate_research_production_suite_descriptor import (  # noqa: E402
    validate_production_suite_descriptor,
)

PLAN_SCHEMA = "csw.production-adapter-metadata-promotion-plan/v1"
PROFILES = ("interactive", "metered")
SIBLING_IDS = ("affinity-synthesis", "iterative-inquiry-synthesis")
RESEARCH_SKILL_SET = {
    "cultural-substrate-weaving",
    "affinity-synthesis",
    "iterative-inquiry-synthesis",
}


def _safe_repo_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def plan_production_adapter_metadata_promotion(
    adapter_plan: dict,
    descriptor: dict,
    locale_catalog: dict,
    root: Path = ROOT,
) -> dict:
    descriptor_by_id = {
        item["research_id"]: item
        for item in descriptor["skills"]
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }
    openai_research = adapter_plan["distributions"]["openai_skill"]["skills"]

    openai: list[dict] = []
    for research_id, skill_metadata in openai_research.items():
        descriptor_skill = descriptor_by_id[research_id]
        production_name = descriptor_skill["proposed_installable_name"]
        production_meta = descriptor_skill["adapter_metadata"]["openai_skill"]
        source_pattern = production_meta.get("source_pattern")

        for locale, locale_profiles in skill_metadata.items():
            for profile in PROFILES:
                research_item = locale_profiles[profile]
                source = research_item["source"]
                if research_id == "cultural-substrate-weaving":
                    target = source_pattern.format(locale=locale, profile=profile)
                    openai.append(
                        {
                            "research_id": research_id,
                            "production_name": production_name,
                            "locale": locale,
                            "profile": profile,
                            "state": "existing-production-source",
                            "source": source,
                            "target": target,
                            "content_operation": "keep-existing-production-metadata",
                        }
                    )
                    continue

                target = source_pattern.format(locale=locale, profile=profile)
                text = (root / source).read_text(encoding="utf-8")
                openai.append(
                    {
                        "research_id": research_id,
                        "production_name": production_name,
                        "locale": locale,
                        "profile": profile,
                        "state": "planned-prototype-promotion",
                        "source": source,
                        "target": target,
                        "content_operation": "copy-byte-identical",
                        "sha256": _sha256_text(text),
                    }
                )

    bundle_plan = adapter_plan["distributions"]["claude_plugin"]
    bundle_promotions: list[dict] = []
    public_skill_set = [item["proposed_installable_name"] for item in descriptor["skills"]]
    for locale, locale_info in bundle_plan["locales"].items():
        prototype_source = locale_info["prototype_source"]
        prototype = json.loads((root / prototype_source).read_text(encoding="utf-8"))
        current = locale_catalog[locale]
        bundle_promotions.append(
            {
                "locale": locale,
                "state": "planned-locale-catalog-wording-update",
                "prototype_source": prototype_source,
                "production_catalog": bundle_plan["source"],
                "preserve": {
                    "plugin_name": current["plugin_name"],
                    "skill_name": current["skill_name"],
                    "display": current["display"],
                },
                "update": {"description": prototype["description"]},
                "prototype_research_contains": prototype["contains"],
                "production_suite_contains": public_skill_set,
                "drop_prototype_fields_from_host_catalog": [
                    "schema",
                    "locale",
                    "contains",
                    "invocation_policy",
                    "status",
                ],
                "shared_by": ["claude_plugin", "codex_plugin"],
            }
        )

    return {
        "schema": PLAN_SCHEMA,
        "status": "design-only",
        "writes_production_metadata": False,
        "openai_profile_promotions": openai,
        "locale_bundle_promotions": bundle_promotions,
        "note": (
            "Research-only adapter metadata promotion plan. OpenAI sibling YAML content is "
            "promoted unchanged to public-name production paths. Claude/Codex share the existing "
            "locale catalog identity and promote only split-aware description wording; suite "
            "composition remains owned by the production suite descriptor."
        ),
    }


def validate_production_adapter_metadata_promotion_plan(
    plan: dict,
    descriptor: dict,
    locale_catalog: dict,
) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != PLAN_SCHEMA:
        errors.append(f"adapter metadata promotion plan schema must be {PLAN_SCHEMA}")
    if plan.get("status") != "design-only":
        errors.append("adapter metadata promotion plan must remain design-only")
    if plan.get("writes_production_metadata") is not False:
        errors.append("adapter metadata promotion plan must not write production metadata")

    descriptor_by_id = {
        item["research_id"]: item
        for item in descriptor.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("research_id"), str)
    }
    expected_openai_count = len(descriptor_by_id) * len(descriptor.get("locales", [])) * len(PROFILES)
    openai = plan.get("openai_profile_promotions")
    if not isinstance(openai, list) or len(openai) != expected_openai_count:
        errors.append("OpenAI adapter promotion plan must cover every Skill × locale × profile")
        openai = []
    seen_openai: set[tuple[str, str, str]] = set()
    for item in openai:
        if not isinstance(item, dict):
            errors.append("OpenAI adapter promotion entries must be objects")
            continue
        key = (item.get("research_id"), item.get("locale"), item.get("profile"))
        if key in seen_openai:
            errors.append(f"duplicate OpenAI adapter promotion entry: {key}")
        seen_openai.add(key)
        research_id, locale, profile = key
        descriptor_skill = descriptor_by_id.get(research_id)
        if descriptor_skill is None:
            errors.append(f"unknown research Skill in OpenAI adapter promotion: {research_id}")
            continue
        production_name = descriptor_skill["proposed_installable_name"]
        if item.get("production_name") != production_name:
            errors.append(f"OpenAI adapter promotion production name mismatch: {research_id}")
        target = item.get("target")
        if not isinstance(target, str) or not _safe_repo_path(target) or not target.startswith("adapters/openai-skill/"):
            errors.append(f"unsafe OpenAI production metadata target: {target!r}")
        if isinstance(target, str) and target.startswith("research/"):
            errors.append(f"OpenAI production metadata target must not point into research: {target}")
        if research_id == "affinity-synthesis":
            if "/material-led-synthesis/" not in target:
                errors.append("Layer 1 OpenAI production metadata target must use material-led-synthesis")
            if "/affinity-synthesis/" in target:
                errors.append("Layer 1 research ID leaked into OpenAI production metadata target")
        if research_id in SIBLING_IDS:
            if item.get("state") != "planned-prototype-promotion":
                errors.append(f"sibling OpenAI metadata must remain planned prototype promotion: {key}")
            if item.get("content_operation") != "copy-byte-identical":
                errors.append(f"sibling OpenAI metadata content must promote byte-identically: {key}")
            digest = item.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64:
                errors.append(f"sibling OpenAI metadata must retain source sha256: {key}")
        else:
            if item.get("state") != "existing-production-source":
                errors.append(f"CSW OpenAI metadata must remain existing production source: {key}")

    bundle = plan.get("locale_bundle_promotions")
    if not isinstance(bundle, list) or len(bundle) != len(descriptor.get("locales", [])):
        errors.append("bundle metadata promotion plan must contain one entry per locale")
        bundle = []
    expected_public = [item["proposed_installable_name"] for item in descriptor.get("skills", [])]
    for item in bundle:
        if not isinstance(item, dict):
            errors.append("bundle metadata promotion entries must be objects")
            continue
        locale = item.get("locale")
        current = locale_catalog.get(locale)
        if not isinstance(current, dict):
            errors.append(f"bundle promotion references unknown locale: {locale}")
            continue
        preserve = item.get("preserve")
        if preserve != {
            "plugin_name": current.get("plugin_name"),
            "skill_name": current.get("skill_name"),
            "display": current.get("display"),
        }:
            errors.append(f"bundle promotion must preserve existing locale/plugin identity: {locale}")
        update = item.get("update")
        if not isinstance(update, dict) or set(update) != {"description"} or not isinstance(update.get("description"), str):
            errors.append(f"bundle promotion may update description only: {locale}")
        research_contains = item.get("prototype_research_contains")
        if not isinstance(research_contains, list) or set(research_contains) != RESEARCH_SKILL_SET:
            errors.append(f"bundle prototype research composition mismatch: {locale}")
        if item.get("production_suite_contains") != expected_public:
            errors.append(f"bundle production composition must use public Skill identities: {locale}")
        if item.get("shared_by") != ["claude_plugin", "codex_plugin"]:
            errors.append(f"Claude/Codex bundle wording promotion must be shared once per locale: {locale}")
        dropped = item.get("drop_prototype_fields_from_host_catalog")
        if not isinstance(dropped, list) or "contains" not in dropped or "status" not in dropped:
            errors.append(f"prototype-only bundle fields must not enter production locale catalog: {locale}")

    return errors


def main() -> int:
    try:
        adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        locale_catalog = json.loads(LOCALE_CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production adapter metadata promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_adapter_metadata(ROOT, adapter_plan)
    errors.extend(validate_production_suite_descriptor(descriptor))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        plan = plan_production_adapter_metadata_promotion(
            adapter_plan,
            descriptor,
            locale_catalog,
        )
    except (KeyError, OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"production adapter metadata promotion planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_adapter_metadata_promotion_plan(plan, descriptor, locale_catalog)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
