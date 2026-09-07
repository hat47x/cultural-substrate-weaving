#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"
SKILL_SET_PATH = ROOT / "src" / "skill-set.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_projection(skill_set: dict, inclusion_plan: dict) -> list[str]:
    errors: list[str] = []
    production_entries = skill_set.get("skills")
    plan_skills = inclusion_plan.get("skills")
    if not isinstance(production_entries, list):
        return ["production Skill-set skills must be an array"]
    if not isinstance(plan_skills, dict):
        return ["research inclusion plan skills must be an object"]

    production = {
        entry.get("id"): entry
        for entry in production_entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    included = {
        skill_id: entry
        for skill_id, entry in plan_skills.items()
        if isinstance(entry, dict) and entry.get("production_state") == "included"
    }

    if set(production) != set(included):
        errors.append(
            "production Skill-set must contain exactly the research Skills marked included"
        )

    for skill_id in sorted(set(production) & set(included)):
        source = included[skill_id].get("production_source")
        expected_manifest = source.get("manifest") if isinstance(source, dict) else None
        actual_manifest = production[skill_id].get("source_manifest")
        if actual_manifest != expected_manifest:
            errors.append(
                f"skill {skill_id}: production source_manifest does not match inclusion decision"
            )

    for skill_id, entry in plan_skills.items():
        if (
            isinstance(entry, dict)
            and entry.get("production_state") != "included"
            and skill_id in production
        ):
            errors.append(f"skill {skill_id}: non-included research Skill leaked into production")

    return errors


def main() -> int:
    try:
        skill_set = _load(SKILL_SET_PATH)
        plan = _load(PLAN_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production projection validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_projection(skill_set, plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research inclusion decision projects cleanly to production Skill set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
