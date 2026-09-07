#!/usr/bin/env python3
"""Plan research adapter-metadata coverage without generating host artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUITE_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
METADATA_PATH = ROOT / "research/skill-prototypes/adapter-metadata-plan.json"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
VALIDATOR_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, VALIDATOR_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_suite_layout import plan_suite  # noqa: E402
from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402
from validate_research_package_targets import validate_package_targets  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402

PLAN_SCHEMA = "csw.research-adapter-metadata-coverage/v1"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _profile_metadata_state(profile_output: dict[str, dict]) -> str:
    states = {entry["status"] for entry in profile_output.values()}
    if len(states) == 1:
        return next(iter(states))
    return "mixed"


def _openai_locale_plan(
    locale: str,
    layout_distribution: dict,
    metadata_config: dict,
) -> dict:
    item_map = {item["skill_id"]: item for item in layout_distribution["items"]}
    profiles = list(metadata_config["profiles"])
    items: list[dict] = []
    realized_metadata_states: list[str] = []

    for skill_id, item in item_map.items():
        declared = metadata_config["skills"][skill_id][locale]
        profile_output = {
            profile: {
                "status": declared[profile]["status"],
                "source": declared[profile].get("source"),
            }
            for profile in profiles
        }
        declared_state = _profile_metadata_state(profile_output)

        if item["state"] != "buildable":
            metadata_state = "runtime-blocked"
        else:
            metadata_state = declared_state
            realized_metadata_states.append(metadata_state)

        items.append(
            {
                "skill_id": skill_id,
                "runtime_state": item["state"],
                "metadata_state": metadata_state,
                "profiles": profile_output,
            }
        )

    if not realized_metadata_states:
        coverage = "no-realized-skills"
    elif all(state == "existing" for state in realized_metadata_states):
        coverage = "complete-for-realized"
    elif all(state in {"existing", "prototype"} for state in realized_metadata_states):
        coverage = "prototype-for-realized"
    else:
        coverage = "incomplete-for-realized"

    return {
        "scope": "per_skill_per_profile",
        "runtime_state": layout_distribution["state"],
        "metadata_coverage": coverage,
        "items": items,
        "note": (
            "Metadata coverage is evaluated only for currently buildable Skill realizations; "
            "prototype is kept distinct from existing production metadata, and runtime-blocked "
            "skills remain separate from metadata gaps."
        ),
    }


def _bundle_locale_plan(
    root: Path,
    locale: str,
    layout_distribution: dict,
    suite_distribution: dict,
    metadata_config: dict,
) -> dict:
    locale_entry = metadata_config["locales"][locale]
    locale_state = locale_entry["status"]
    baseline_source = metadata_config.get("source")
    source = baseline_source
    source_kind = "locale-catalog"
    catalog_entry = None

    if locale_state == "prototype":
        source = locale_entry.get("prototype_source")
        source_kind = "research-prototype"
        if isinstance(source, str):
            value = _load_json(root / source)
            catalog_entry = {
                key: value.get(key)
                for key in ("plugin_name", "description", "display", "contains")
            }
    elif isinstance(baseline_source, str) and locale_state != "planned":
        catalog = _load_json(root / baseline_source)
        value = catalog.get(locale)
        if isinstance(value, dict):
            catalog_entry = {
                key: value.get(key)
                for key in ("plugin_name", "description", "display")
            }

    multi_skill = len(suite_distribution.get("contains", [])) > 1
    review_required = bool(metadata_config.get("review_required_for_multi_skill"))
    if locale_state == "planned":
        metadata_state = "planned"
    elif locale_state == "prototype":
        metadata_state = "prototype"
    elif locale_state == "existing-baseline" and multi_skill and review_required:
        metadata_state = "review-required"
    elif locale_state == "reviewed":
        metadata_state = "reviewed"
    else:
        metadata_state = locale_state

    return {
        "scope": "locale_bundle",
        "runtime_state": layout_distribution["state"],
        "metadata_state": metadata_state,
        "source": source,
        "source_kind": source_kind,
        "catalog_entry": catalog_entry,
        "target_skills": suite_distribution.get("contains", []),
        "note": (
            "Bundle metadata prototypes stay distinct from production-reviewed metadata. "
            "An existing single-Skill locale catalog remains only a baseline until the "
            "multi-Skill wording and host behavior are reviewed."
        ),
    }


def plan_adapter_metadata(
    suite: dict,
    metadata_plan: dict,
    root: Path = ROOT,
) -> dict:
    """Return runtime-vs-adapter-metadata coverage for Skill-tree distributions."""

    layout = plan_suite(suite)
    output = {
        "schema": PLAN_SCHEMA,
        "suite_id": suite.get("suite_id"),
        "note": (
            "This plan separates runtime/package availability from host adapter metadata. "
            "It does not assert package validity, wording approval, or release readiness."
        ),
        "locales": {},
    }

    for locale in suite.get("locales", {}):
        distributions: dict[str, dict] = {}
        for distribution_name, metadata_config in metadata_plan["distributions"].items():
            layout_distribution = layout["locales"][locale]["distributions"][
                distribution_name
            ]
            suite_distribution = suite["distribution_prototypes"][distribution_name]
            scope = metadata_config.get("scope")
            if scope == "per_skill_per_profile":
                distributions[distribution_name] = _openai_locale_plan(
                    locale,
                    layout_distribution,
                    metadata_config,
                )
            elif scope == "locale_bundle":
                distributions[distribution_name] = _bundle_locale_plan(
                    root,
                    locale,
                    layout_distribution,
                    suite_distribution,
                    metadata_config,
                )
            else:
                distributions[distribution_name] = {
                    "scope": scope,
                    "runtime_state": layout_distribution["state"],
                    "metadata_state": "unsupported",
                }

        output["locales"][locale] = {"distributions": distributions}

    return output


def main() -> int:
    try:
        suite = _load_json(SUITE_PATH)
        metadata_plan = _load_json(METADATA_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research adapter metadata planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_suite(ROOT, suite)
    errors.extend(validate_package_targets(suite))
    errors.extend(validate_adapter_metadata(ROOT, metadata_plan))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        plan = plan_adapter_metadata(suite, metadata_plan, ROOT)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"research adapter metadata planning failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
