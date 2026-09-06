#!/usr/bin/env python3
"""Plan research skill-suite distribution buildability without generating packages.

The planner answers only whether the currently declared locale realizations are
sufficient for each research distribution shape. It does not claim method
parity, routing support, package validity, or release readiness.
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

PLAN_SCHEMA = "csw.research-skill-suite-layout-plan/v1"


def _realization(skill: dict | None, locale: str) -> dict:
    if skill is None:
        return {
            "status": "unknown-skill",
            "realized": False,
            "runtime_entry": None,
        }

    realization = skill.get("locale_realizations", {}).get(locale, {})
    status = realization.get("status")
    runtime_entry = realization.get("runtime_entry")
    realized = (
        isinstance(status, str)
        and status != "planned"
        and isinstance(runtime_entry, str)
        and bool(runtime_entry)
    )
    return {
        "status": status,
        "realized": realized,
        "runtime_entry": runtime_entry if isinstance(runtime_entry, str) else None,
    }


def _aggregate_state(realized_count: int, target_count: int) -> str:
    if target_count == 0:
        return "blocked"
    if realized_count == target_count:
        return "buildable"
    if realized_count:
        return "partial"
    return "blocked"


def plan_suite(manifest: dict) -> dict:
    """Return a deterministic buildability plan for the research suite manifest."""

    skills = manifest.get("skills", [])
    skills_by_id = {
        skill.get("id"): skill
        for skill in skills
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    }
    skill_order = [
        skill.get("id")
        for skill in skills
        if isinstance(skill, dict) and isinstance(skill.get("id"), str)
    ]

    plan = {
        "schema": PLAN_SCHEMA,
        "suite_id": manifest.get("suite_id"),
        "note": (
            "Buildability reflects declared research locale realizations only; "
            "it is not promotion or release readiness."
        ),
        "locales": {},
    }

    for locale, locale_config in manifest.get("locales", {}).items():
        availability = {
            skill_id: _realization(skills_by_id.get(skill_id), locale)
            for skill_id in skill_order
        }
        distributions: dict[str, dict] = {}

        for distribution_name, config in manifest.get(
            "distribution_prototypes", {}
        ).items():
            mode = config.get("mode")

            if mode == "standalone_per_skill":
                items = []
                realized_count = 0
                for skill_id in skill_order:
                    realization = availability[skill_id]
                    item_state = "buildable" if realization["realized"] else "blocked"
                    if realization["realized"]:
                        realized_count += 1
                    items.append(
                        {
                            "skill_id": skill_id,
                            "state": item_state,
                            "status": realization["status"],
                            "runtime_entry": realization["runtime_entry"],
                        }
                    )

                distributions[distribution_name] = {
                    "mode": mode,
                    "state": _aggregate_state(realized_count, len(skill_order)),
                    "items": items,
                    "scope": "per-skill realization availability only",
                }
                continue

            if mode == "locale_bundle":
                target_skills = config.get("contains", [])
                missing_skills = []
                realized_skills = []
                for skill_id in target_skills:
                    realization = _realization(skills_by_id.get(skill_id), locale)
                    if realization["realized"]:
                        realized_skills.append(skill_id)
                    else:
                        missing_skills.append(skill_id)

                distributions[distribution_name] = {
                    "mode": mode,
                    "state": "buildable" if not missing_skills else "blocked",
                    "target_skills": target_skills,
                    "realized_skills": realized_skills,
                    "missing_skills": missing_skills,
                    "scope": "declared bundle composition and realization availability only",
                }
                continue

            if mode == "composite_agent_realization":
                primary = config.get("primary")
                realization = _realization(skills_by_id.get(primary), locale)
                distributions[distribution_name] = {
                    "mode": mode,
                    "state": "buildable" if realization["realized"] else "blocked",
                    "primary": primary,
                    "primary_status": realization["status"],
                    "primary_runtime_entry": realization["runtime_entry"],
                    "scope": (
                        "primary realization availability only; internal method-composition "
                        "parity is not asserted"
                    ),
                }
                continue

            distributions[distribution_name] = {
                "mode": mode,
                "state": "unsupported",
                "scope": "planner has no rule for this research distribution mode",
            }

        plan["locales"][locale] = {
            "suite_locale_status": (
                locale_config.get("status") if isinstance(locale_config, dict) else None
            ),
            "skill_realizations": availability,
            "distributions": distributions,
        }

    return plan


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research suite layout planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_suite(ROOT, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("research suite layout planning stopped on invalid manifest", file=sys.stderr)
        return 1

    print(json.dumps(plan_suite(manifest), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
