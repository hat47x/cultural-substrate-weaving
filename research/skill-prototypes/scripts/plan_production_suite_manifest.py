#!/usr/bin/env python3
"""Project the research promotion descriptor into a production-only suite manifest.

The output models the future src/skill-suite.json shape without writing it. It
strips research IDs, promotion gates, review state, and research paths so the
future production builder does not need to understand research metadata.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_production_suite_descriptor import (  # noqa: E402
    validate_production_suite_descriptor,
)

PLAN_SCHEMA = "csw.production-skill-suite/v1"
FORBIDDEN_OUTPUT_KEYS = {
    "research_id",
    "public_name_status",
    "promotion_preconditions",
    "complete_checkout_validation",
    "public_name_recheck",
    "english_independent_review",
    "forbidden_production_inputs",
    "production_promotion_authorized",
}
ALLOWED_PRODUCTION_ADAPTER_MODES = {"per_locale_profile", "locale_catalog"}


def _project_adapter_metadata(skill: dict) -> dict:
    """Drop research maturity state and retain only production lookup semantics."""

    projected = {}
    for distribution, metadata in skill["adapter_metadata"].items():
        if "source_pattern" in metadata:
            projected[distribution] = {
                "mode": "per_locale_profile",
                "source_pattern": metadata["source_pattern"],
            }
            continue
        if "source" in metadata:
            projected[distribution] = {
                "mode": "locale_catalog",
                "source": metadata["source"],
            }
            continue
        raise ValueError(
            f"adapter metadata for {skill['proposed_installable_name']}/{distribution} "
            "has no production source or source_pattern"
        )
    return projected


def project_production_suite_manifest(descriptor: dict) -> dict:
    public_ids = [skill["proposed_installable_name"] for skill in descriptor["skills"]]
    skills = []
    for skill in descriptor["skills"]:
        skills.append(
            {
                "id": skill["proposed_installable_name"],
                "role": skill["role"],
                "source": skill["production_source"],
                "targets": skill["targets"],
                "adapter_metadata": _project_adapter_metadata(skill),
            }
        )

    return {
        "schema": PLAN_SCHEMA,
        "suite_id": descriptor["suite_id"],
        "version_source": descriptor["version_source"],
        "canonical_locale": descriptor["canonical_locale"],
        "locales": descriptor["locales"],
        "skills": skills,
        "bundle_identity": descriptor["bundle_identity"],
        "distributions": {
            "openai_skill": {
                "mode": "standalone_per_skill",
                "contains": public_ids,
            },
            "claude_plugin": {
                "mode": "locale_bundle",
                "contains": public_ids,
            },
            "codex_plugin": {
                "mode": "reuse_claude_skill_tree",
                "contains": public_ids,
                "shared_skill_tree_distribution": "claude_plugin",
            },
        },
    }


def _walk(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)
    elif isinstance(value, str):
        yield value


def validate_projected_production_suite(manifest: dict, descriptor: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema") != PLAN_SCHEMA:
        errors.append(f"projected production suite schema must be {PLAN_SCHEMA}")
    if manifest.get("suite_id") != descriptor.get("suite_id"):
        errors.append("projected production suite_id must match the promotion descriptor")
    if manifest.get("version_source") != "VERSION":
        errors.append("projected production suite version_source must remain VERSION")
    if manifest.get("canonical_locale") != descriptor.get("canonical_locale"):
        errors.append("projected production canonical_locale must match the promotion descriptor")
    if manifest.get("locales") != descriptor.get("locales"):
        errors.append("projected production locales must match the promotion descriptor")

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        errors.append("projected production skills must be a list")
        return errors

    expected_ids = [
        skill["proposed_installable_name"] for skill in descriptor.get("skills", [])
    ]
    actual_ids = [skill.get("id") for skill in skills if isinstance(skill, dict)]
    if actual_ids != expected_ids:
        errors.append("projected production Skill ids must use descriptor public installable names in order")
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("projected production Skill ids must be unique")

    descriptor_by_public_id = {
        skill["proposed_installable_name"]: skill
        for skill in descriptor.get("skills", [])
        if isinstance(skill, dict)
    }
    for skill in skills:
        if not isinstance(skill, dict):
            errors.append("projected production Skill entries must be objects")
            continue
        public_id = skill.get("id")
        source_skill = descriptor_by_public_id.get(public_id)
        if source_skill is None:
            errors.append(f"projected production Skill has no descriptor source: {public_id}")
            continue
        if set(skill) != {"id", "role", "source", "targets", "adapter_metadata"}:
            errors.append(f"projected production Skill {public_id} contains unexpected fields")
        if skill.get("role") != source_skill.get("role"):
            errors.append(f"projected production Skill {public_id} role mismatch")
        if skill.get("source") != source_skill.get("production_source"):
            errors.append(f"projected production Skill {public_id} source mismatch")
        if skill.get("targets") != source_skill.get("targets"):
            errors.append(f"projected production Skill {public_id} targets mismatch")
        try:
            expected_adapter_metadata = _project_adapter_metadata(source_skill)
        except ValueError as exc:
            errors.append(str(exc))
            expected_adapter_metadata = None
        if skill.get("adapter_metadata") != expected_adapter_metadata:
            errors.append(f"projected production Skill {public_id} adapter metadata mismatch")
        projected_adapter = skill.get("adapter_metadata")
        if isinstance(projected_adapter, dict):
            for distribution, metadata in projected_adapter.items():
                if not isinstance(metadata, dict):
                    errors.append(
                        f"projected production Skill {public_id}/{distribution} adapter metadata must be an object"
                    )
                    continue
                if metadata.get("mode") not in ALLOWED_PRODUCTION_ADAPTER_MODES:
                    errors.append(
                        f"projected production Skill {public_id}/{distribution} uses non-production adapter mode"
                    )

    distributions = manifest.get("distributions")
    if not isinstance(distributions, dict) or set(distributions) != {
        "openai_skill",
        "claude_plugin",
        "codex_plugin",
    }:
        errors.append("projected production distributions must contain only the first-wave Skill-tree distributions")
    else:
        for distribution in ("openai_skill", "claude_plugin", "codex_plugin"):
            item = distributions[distribution]
            if item.get("contains") != expected_ids:
                errors.append(f"projected {distribution} composition must contain all public Skill ids")
        if distributions["openai_skill"].get("mode") != "standalone_per_skill":
            errors.append("projected OpenAI distribution mode must be standalone_per_skill")
        if distributions["claude_plugin"].get("mode") != "locale_bundle":
            errors.append("projected Claude distribution mode must be locale_bundle")
        if distributions["codex_plugin"].get("mode") != "reuse_claude_skill_tree":
            errors.append("projected Codex distribution mode must reuse the Claude Skill tree")
        if distributions["codex_plugin"].get("shared_skill_tree_distribution") != "claude_plugin":
            errors.append("projected Codex distribution must point to claude_plugin as its shared Skill tree")

    if manifest.get("bundle_identity") != descriptor.get("bundle_identity"):
        errors.append("projected production bundle_identity must match the promotion descriptor")

    walked = list(_walk(manifest))
    for forbidden in FORBIDDEN_OUTPUT_KEYS:
        if forbidden in walked:
            errors.append(f"projected production suite must not contain research/promotion key: {forbidden}")
    for value in walked:
        if isinstance(value, str) and "research/skill-prototypes" in value:
            errors.append(f"projected production suite must not contain research path: {value}")
        if isinstance(value, str) and value == "planned-promotion-from-research-prototype":
            errors.append("projected production suite must not retain research promotion adapter state")

    if "affinity-synthesis" in actual_ids:
        errors.append("Layer 1 research ID affinity-synthesis must not become a production Skill id")
    if "material-led-synthesis" not in actual_ids:
        errors.append("Layer 1 production Skill id must be material-led-synthesis")

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production suite manifest projection failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_suite_descriptor(descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        projected = project_production_suite_manifest(descriptor)
    except ValueError as exc:
        print(f"production suite manifest projection failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_projected_production_suite(projected, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(projected, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
