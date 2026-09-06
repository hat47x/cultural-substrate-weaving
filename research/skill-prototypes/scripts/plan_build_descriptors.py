#!/usr/bin/env python3
"""Normalize research skill realizations into build descriptors.

Descriptors are a research bridge between the suite manifest and a future
multi-skill production builder. They describe source inputs only and do not
claim package validity, host routing support, or public promotion readiness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
VALIDATOR_DIR = ROOT / "scripts"
if str(VALIDATOR_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_DIR))

from validate_research_skill_suite import validate_suite  # noqa: E402

DESCRIPTOR_SCHEMA = "csw.research-skill-build-descriptors/v1"


def _realized(realization: dict) -> bool:
    status = realization.get("status")
    runtime = realization.get("runtime_entry")
    return (
        isinstance(status, str)
        and status != "planned"
        and isinstance(runtime, str)
        and bool(runtime)
    )


def skill_descriptor(skill: dict, locale: str) -> dict:
    realization = skill.get("locale_realizations", {}).get(locale, {})
    assembly = skill.get("assembly", {})
    realized = _realized(realization)

    descriptor = {
        "skill_id": skill.get("id"),
        "installable_name": skill.get("installable_name"),
        "role": skill.get("role"),
        "locale": locale,
        "state": "buildable-input" if realized else "blocked-input",
        "realization_status": realization.get("status"),
        "method_version": skill.get("method_version"),
        "realization_version": skill.get("realization_version"),
        "source_root": skill.get("source_root"),
        "assembly_mode": assembly.get("mode"),
        "runtime_source": realization.get("runtime_entry") if realized else None,
        "method_source": realization.get("method_definition") if realized else None,
        "package_reference_sources": (
            list(realization.get("package_references", [])) if realized else []
        ),
        "source_manifest": assembly.get("source_manifest"),
        "research_only": True,
        "release_readiness_asserted": False,
    }
    return descriptor


def plan_build_descriptors(manifest: dict) -> dict:
    skills = [skill for skill in manifest.get("skills", []) if isinstance(skill, dict)]
    return {
        "schema": DESCRIPTOR_SCHEMA,
        "suite_id": manifest.get("suite_id"),
        "note": (
            "Descriptors normalize research source inputs only; buildable-input "
            "does not mean package or promotion readiness."
        ),
        "locales": {
            locale: {
                "suite_locale_status": (
                    config.get("status") if isinstance(config, dict) else None
                ),
                "skills": [skill_descriptor(skill, locale) for skill in skills],
            }
            for locale, config in manifest.get("locales", {}).items()
        },
    }


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research build descriptor planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_suite(ROOT, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("research build descriptor planning stopped on invalid manifest", file=sys.stderr)
        return 1

    print(json.dumps(plan_build_descriptors(manifest), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
