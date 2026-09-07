#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL_SET_PATH = ROOT / "src" / "skill-set.json"
SCHEMA = "csw.production-skill-set/v1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_source_manifest(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    if "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    if not path.parts or path.parts[0] != "src":
        return None
    return value


def validate_production_skill_set(root: Path, skill_set: dict) -> list[str]:
    errors: list[str] = []
    if skill_set.get("schema") != SCHEMA:
        errors.append("production Skill-set schema mismatch")

    raw_skills = skill_set.get("skills")
    if not isinstance(raw_skills, list) or not raw_skills:
        return errors + ["production Skill-set skills must be a non-empty array"]

    seen: set[str] = set()
    for index, raw in enumerate(raw_skills):
        label = f"production Skill-set skills[{index}]"
        if not isinstance(raw, dict):
            errors.append(f"{label} must be an object")
            continue

        skill_id = raw.get("id")
        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if skill_id in seen:
            errors.append(f"duplicate production Skill id: {skill_id}")
            continue
        seen.add(skill_id)

        if set(raw) != {"id", "source_manifest"}:
            errors.append(
                f"skill {skill_id}: production descriptor may contain only id and source_manifest"
            )

        source_manifest = _safe_source_manifest(raw.get("source_manifest"))
        if source_manifest is None:
            errors.append(
                f"skill {skill_id}: source_manifest must be a safe repository path under src/"
            )
            continue

        manifest_path = root / source_manifest
        try:
            manifest = _load(manifest_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"skill {skill_id}: cannot read source manifest: {exc}")
            continue

        if manifest.get("name") != skill_id:
            errors.append(f"skill {skill_id}: source manifest name mismatch")

        locales = manifest.get("locales")
        if not isinstance(locales, dict) or not locales:
            errors.append(f"skill {skill_id}: source manifest must declare locales")
            continue

        canonical_locale = manifest.get("canonical_locale")
        if not isinstance(canonical_locale, str) or canonical_locale not in locales:
            errors.append(
                f"skill {skill_id}: source manifest canonical_locale must name a declared locale"
            )

    return errors


def main() -> int:
    try:
        skill_set = _load(SKILL_SET_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"production Skill-set validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_production_skill_set(ROOT, skill_set)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Production Skill-set descriptor is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
