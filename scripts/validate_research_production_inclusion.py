#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"
EXPECTED_SUITE_MANIFEST = "research/skill-prototypes/suite-manifest.json"

from validate_research_skill_suite import validate_suite  # noqa: E402


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _safe_repo_file(
    root: Path,
    relative: object,
    label: str,
    errors: list[str],
) -> Path | None:
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or "\x00" in relative
    ):
        errors.append(f"{label} must be a non-empty repository-relative POSIX path")
        return None
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        errors.append(f"{label} must remain inside repository")
        return None
    repository = root.resolve()
    path = root.joinpath(*pure.parts).resolve()
    if not path.is_relative_to(repository):
        errors.append(f"{label} must remain inside repository")
        return None
    if not path.is_file():
        errors.append(f"{label} is missing: {relative}")
        return None
    return path


def validate_production_inclusion(root: Path, plan: dict) -> list[str]:
    if not isinstance(plan, dict):
        return ["production inclusion plan must be an object"]

    errors: list[str] = []
    if plan.get("schema") != "csw.research-production-inclusion-plan/v1":
        errors.append("production inclusion plan schema mismatch")

    suite_path = plan.get("suite_manifest")
    if suite_path != EXPECTED_SUITE_MANIFEST:
        return errors + [
            "production inclusion suite_manifest must remain canonical: "
            f"{suite_path!r} != {EXPECTED_SUITE_MANIFEST!r}"
        ]
    suite_file = _safe_repo_file(
        root,
        suite_path,
        "production inclusion suite_manifest",
        errors,
    )
    if suite_file is None:
        return errors
    try:
        suite = _load(suite_file)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return errors + [f"cannot read suite manifest: {exc}"]

    suite_errors = validate_suite(root, suite)
    if suite_errors:
        return errors + suite_errors

    suite_skills = {
        skill["id"]: skill
        for skill in suite.get("skills", [])
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    }
    plan_skills = plan.get("skills")
    if not isinstance(plan_skills, dict):
        return errors + ["production inclusion plan skills must be an object"]
    if not all(isinstance(skill_id, str) and skill_id for skill_id in plan_skills):
        errors.append("production inclusion plan skill ids must be non-empty strings")
    valid_plan_skill_ids = {
        skill_id
        for skill_id in plan_skills
        if isinstance(skill_id, str) and skill_id
    }
    if valid_plan_skill_ids != set(suite_skills):
        errors.append("production inclusion plan skill set must match research suite skill set")

    locales = set(suite.get("locales", {}))
    included_count = 0
    for skill_id, entry in plan_skills.items():
        if not isinstance(skill_id, str) or not skill_id:
            continue
        if skill_id not in suite_skills:
            continue
        if not isinstance(entry, dict):
            errors.append(f"skill {skill_id}: production inclusion entry must be an object")
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
                manifest_file = _safe_repo_file(
                    root,
                    manifest_path,
                    f"skill {skill_id}: production manifest",
                    errors,
                )
                if manifest_file is not None:
                    try:
                        manifest = _load(manifest_file)
                    except (OSError, json.JSONDecodeError, ValueError) as exc:
                        errors.append(
                            f"skill {skill_id}: cannot read production manifest: {exc}"
                        )
                        manifest = {}
                    if manifest.get("name") != skill_id:
                        errors.append(f"skill {skill_id}: production manifest name mismatch")
                    manifest_locales = manifest.get("locales")
                    if not isinstance(manifest_locales, dict):
                        errors.append(
                            f"skill {skill_id}: production manifest locales must be an object"
                        )
                    elif not all(
                        isinstance(locale, str) and locale
                        for locale in manifest_locales
                    ):
                        errors.append(
                            f"skill {skill_id}: production manifest locale keys must be non-empty strings"
                        )
                    elif set(manifest_locales) != locales:
                        errors.append(f"skill {skill_id}: production manifest locale set mismatch")
                    router = manifest.get("router")
                    if not isinstance(router, str) or not router or "\\" in router or "\x00" in router:
                        errors.append(
                            f"skill {skill_id}: production router must be a non-empty POSIX path"
                        )
                    else:
                        router_pure = PurePosixPath(router)
                        if router_pure.is_absolute() or ".." in router_pure.parts:
                            errors.append(
                                f"skill {skill_id}: production router must remain inside locale root"
                            )
                        else:
                            repository = root.resolve()
                            for locale in locales:
                                locale_root = (root / "src" / locale).resolve()
                                runtime = (
                                    locale_root / Path(*router_pure.parts)
                                ).resolve()
                                if (
                                    not locale_root.is_relative_to(repository)
                                    or not runtime.is_relative_to(locale_root)
                                    or not runtime.is_file()
                                ):
                                    errors.append(
                                        f"skill {skill_id}: production runtime entry is missing for {locale}"
                                    )
        elif source is not None:
            errors.append(f"skill {skill_id}: candidate Skill must not claim production_source")

        locale_states = entry.get("locales")
        if not isinstance(locale_states, dict):
            errors.append(f"skill {skill_id}: locale states must be an object")
            continue
        if not all(isinstance(locale, str) and locale for locale in locale_states):
            errors.append(f"skill {skill_id}: locale state keys must be non-empty strings")
        valid_locale_keys = {
            locale
            for locale in locale_states
            if isinstance(locale, str) and locale
        }
        if valid_locale_keys != locales:
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
    except (OSError, json.JSONDecodeError, ValueError) as exc:
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
