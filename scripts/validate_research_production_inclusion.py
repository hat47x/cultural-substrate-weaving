#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_production_inclusion(root: Path, plan: dict) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != "csw.research-production-inclusion-plan/v1":
        errors.append("production inclusion plan schema mismatch")

    suite_path = plan.get("suite_manifest")
    if not isinstance(suite_path, str):
        return errors + ["production inclusion plan must declare suite_manifest"]
    try:
        suite = _load(root / suite_path)
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"cannot read suite manifest: {exc}"]

    suite_skills = {
        skill["id"]: skill
        for skill in suite.get("skills", [])
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    }
    plan_skills = plan.get("skills")
    if not isinstance(plan_skills, dict):
        return errors + ["production inclusion plan skills must be an object"]
    if set(plan_skills) != set(suite_skills):
        errors.append("production inclusion plan skill set must match research suite skill set")

    locales = set(suite.get("locales", {}))
    included_count = 0
    for skill_id, entry in plan_skills.items():
        if not isinstance(entry, dict) or skill_id not in suite_skills:
            continue
        state = entry.get("production_state")
        if state not in {"included", "candidate"}:
            errors.append(f"skill {skill_id}: invalid production_state {state!r}")
            continue

        source = entry.get("production_source")
        if state == "included":
            included_count += 1
            if not isinstance(source, dict):
                errors.append(f"skill {skill_id}: included Skill requires production_source")
            elif source.get("mode") != "canonical_manifest":
                errors.append(f"skill {skill_id}: unsupported production source mode")
            else:
                manifest_path = source.get("manifest")
                if not isinstance(manifest_path, str) or not (root / manifest_path).is_file():
                    errors.append(f"skill {skill_id}: production manifest is missing")
                else:
                    manifest = _load(root / manifest_path)
                    if manifest.get("name") != skill_id:
                        errors.append(f"skill {skill_id}: production manifest name mismatch")
                    if set(manifest.get("locales", {})) != locales:
                        errors.append(f"skill {skill_id}: production manifest locale set mismatch")
                    router = manifest.get("router")
                    if isinstance(router, str):
                        for locale in locales:
                            if not (root / "src" / locale / router).is_file():
                                errors.append(
                                    f"skill {skill_id}: production runtime entry is missing for {locale}"
                                )
        elif source is not None:
            errors.append(f"skill {skill_id}: candidate Skill must not claim production_source")

        locale_states = entry.get("locales")
        if not isinstance(locale_states, dict) or set(locale_states) != locales:
            errors.append(f"skill {skill_id}: locale state set must match suite locales")
            continue
        realizations = suite_skills[skill_id].get("locale_realizations", {})
        for locale in locales:
            locale_state = locale_states.get(locale)
            realization = realizations.get(locale, {})
            realization_status = realization.get("status") if isinstance(realization, dict) else None
            expected = (
                "included"
                if state == "included"
                else "blocked" if realization_status == "planned" else "candidate"
            )
            if locale_state != expected:
                errors.append(
                    f"skill {skill_id}: locale {locale} state {locale_state!r} != expected {expected!r}"
                )
            if state == "included" and realization_status == "planned":
                errors.append(f"skill {skill_id}: included locale {locale} has only a planned realization")

    if included_count == 0:
        errors.append("production inclusion plan must include at least one Skill")
    return errors


def main() -> int:
    try:
        plan = _load(PLAN_PATH)
        errors = validate_production_inclusion(ROOT, plan)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production inclusion validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Research production inclusion boundary is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
