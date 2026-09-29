#!/usr/bin/env python3
"""Validate public-name identity on host-visible research adapter metadata.

Research paths, prototype composition fields, and historical records may retain
research IDs. Host-visible prose that is planned for production promotion must
not leak a renamed research ID when the production installable name differs.

This checker intentionally scans only:
- OpenAI per-Skill YAML content that is promoted byte-identically, and
- Claude/Codex prototype bundle descriptions that are promoted as host wording.

It does not reject research IDs in prototype `contains` fields or repository
paths because those are transformed/dropped by the production promotion plan.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "skill-prototypes"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def renamed_skill_ids(descriptor: dict) -> dict[str, str]:
    mapping: dict[str, str] = {}
    skills = descriptor.get("skills")
    if not isinstance(skills, list):
        return mapping
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        research_id = skill.get("research_id")
        production_name = skill.get("proposed_installable_name")
        if (
            isinstance(research_id, str)
            and isinstance(production_name, str)
            and research_id
            and production_name
            and research_id != production_name
        ):
            mapping[research_id] = production_name
    return mapping


def validate_host_visible_text(
    label: str,
    text: str,
    renamed_ids: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    for research_id, production_name in sorted(renamed_ids.items()):
        if research_id in text:
            errors.append(
                f"{label} leaks renamed research id {research_id!r}; "
                f"host-visible production prose must use public identity {production_name!r} "
                "or neutral/display wording"
            )
    return errors


def _read_text(root: Path, relative: object, label: str, errors: list[str]) -> str | None:
    if not _safe_repo_relative(relative):
        errors.append(f"unsafe or missing adapter metadata source for {label}: {relative!r}")
        return None
    path = root / str(relative)
    if not path.is_file():
        errors.append(f"adapter metadata source is missing for {label}: {relative}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read adapter metadata source for {label}: {relative}: {exc}")
        return None


def validate_adapter_public_identity(
    root: Path,
    descriptor: dict,
    adapter_plan: dict,
) -> list[str]:
    errors: list[str] = []
    renamed_ids = renamed_skill_ids(descriptor)
    if not renamed_ids:
        return errors

    distributions = adapter_plan.get("distributions")
    if not isinstance(distributions, dict):
        return ["adapter metadata plan distributions must be an object"]

    openai = distributions.get("openai_skill")
    if not isinstance(openai, dict):
        errors.append("adapter metadata plan must declare openai_skill")
    else:
        skills = openai.get("skills")
        if not isinstance(skills, dict):
            errors.append("OpenAI adapter metadata plan skills must be an object")
        else:
            for skill_id, locales in skills.items():
                if not isinstance(locales, dict):
                    continue
                for locale, profiles in locales.items():
                    if not isinstance(profiles, dict):
                        continue
                    for profile, item in profiles.items():
                        if not isinstance(item, dict):
                            continue
                        source = item.get("source")
                        label = f"OpenAI {skill_id}/{locale}/{profile}"
                        text = _read_text(root, source, label, errors)
                        if text is not None:
                            errors.extend(
                                validate_host_visible_text(label, text, renamed_ids)
                            )

    claude = distributions.get("claude_plugin")
    if not isinstance(claude, dict):
        errors.append("adapter metadata plan must declare claude_plugin")
    else:
        locales = claude.get("locales")
        if not isinstance(locales, dict):
            errors.append("Claude adapter metadata plan locales must be an object")
        else:
            seen_sources: set[str] = set()
            for locale, item in locales.items():
                if not isinstance(item, dict):
                    continue
                source = item.get("prototype_source")
                if isinstance(source, str) and source in seen_sources:
                    continue
                if isinstance(source, str):
                    seen_sources.add(source)
                label = f"Claude/Codex bundle description {locale}"
                text = _read_text(root, source, label, errors)
                if text is None:
                    continue
                try:
                    payload = json.loads(text)
                except json.JSONDecodeError as exc:
                    errors.append(f"bundle metadata is not valid JSON for {locale}: {exc}")
                    continue
                description = payload.get("description") if isinstance(payload, dict) else None
                if not isinstance(description, str) or not description.strip():
                    errors.append(f"bundle metadata description is missing for {locale}")
                    continue
                errors.extend(
                    validate_host_visible_text(label, description, renamed_ids)
                )

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research adapter public-identity validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_adapter_public_identity(ROOT, descriptor, adapter_plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research host-visible adapter metadata uses production/public identity boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
