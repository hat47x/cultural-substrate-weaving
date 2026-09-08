#!/usr/bin/env python3
"""Validate research check/planner wiring into the research gate.

Three ownership rules coexist:

1. Skill-owned checks are declared in the research suite manifest and must be
   invoked directly by the `research-skill-check` Makefile target. A Skill-owned
   check must not bypass the manifest.
2. Root suite-level validators follow the repository naming convention
   `scripts/validate_research_*.py`. Every such validator must be invoked
   directly by the same Makefile target, and a Makefile command using that
   convention must resolve to an existing validator file.
3. Read-only research planners follow
   `research/skill-prototypes/scripts/plan_*.py`. Every such planner must also
   be invoked directly by the research gate exactly once, and an unknown
   planner path using that convention must not be wired into the gate.

This keeps the manifest authoritative for Skill-local checks while making the
suite-level validator and planner filename conventions operational instead of
relying on manual Makefile review.
"""

from __future__ import annotations

import json
import posixpath
import shlex
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
MAKEFILE_PATH = ROOT / "Makefile"
TARGET = "research-skill-check"
SUITE_VALIDATOR_GLOB = "validate_research_*.py"
SUITE_VALIDATOR_PREFIX = "scripts/validate_research_"
PLANNER_DIR = "research/skill-prototypes/scripts"
PLANNER_GLOB = "plan_*.py"
PLANNER_PREFIX = f"{PLANNER_DIR}/plan_"


def _normalize_path(value: str) -> str:
    return posixpath.normpath(value.replace("\\", "/"))


def _target_recipe(makefile_text: str, target: str = TARGET) -> list[str] | None:
    lines = makefile_text.splitlines()
    target_prefix = f"{target}:"
    start: int | None = None

    for index, line in enumerate(lines):
        if line.startswith(target_prefix):
            start = index + 1
            break

    if start is None:
        return None

    recipe: list[str] = []
    for line in lines[start:]:
        if line.startswith("\t"):
            recipe.append(line[1:])
            continue
        if not line.strip():
            continue
        break
    return recipe


def _direct_python_scripts(recipe: list[str]) -> list[str]:
    scripts: list[str] = []
    for raw_command in recipe:
        command = raw_command.lstrip("@-+").strip()
        if not command:
            continue
        try:
            tokens = shlex.split(command, comments=False, posix=True)
        except ValueError:
            continue
        if len(tokens) < 2:
            continue
        executable = Path(tokens[0]).name
        if executable not in {"python", "python3"}:
            continue
        if tokens[1] == "-m" or tokens[1].startswith("-"):
            continue
        scripts.append(_normalize_path(tokens[1]))
    return scripts


def _suite_validator_paths(root: Path = ROOT) -> set[str]:
    scripts_dir = root / "scripts"
    return {
        _normalize_path(f"scripts/{path.name}")
        for path in scripts_dir.glob(SUITE_VALIDATOR_GLOB)
        if path.is_file()
    }


def _planner_paths(root: Path = ROOT) -> set[str]:
    scripts_dir = root / PLANNER_DIR
    return {
        _normalize_path(f"{PLANNER_DIR}/{path.name}")
        for path in scripts_dir.glob(PLANNER_GLOB)
        if path.is_file()
    }


def _validate_convention_wiring(
    *,
    label: str,
    expected: set[str],
    prefix: str,
    executed: list[str],
    errors: list[str],
) -> None:
    executed_set = set(executed)
    execution_counts = Counter(executed)

    for path in sorted(expected):
        if path not in executed_set:
            errors.append(f"{label} is not wired into {TARGET}: {path}")
        elif execution_counts[path] != 1:
            errors.append(
                f"{label} must be wired exactly once into {TARGET}: "
                f"{path} (found {execution_counts[path]})"
            )

    for path in sorted(executed_set):
        if not path.startswith(prefix) or not path.endswith(".py"):
            continue
        if path not in expected:
            errors.append(f"research gate references an unknown {label}: {path}")


def validate_declared_checks(
    manifest: dict,
    makefile_text: str,
    *,
    suite_validator_paths: set[str] | None = None,
    planner_paths: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    recipe = _target_recipe(makefile_text)
    if recipe is None:
        return [f"Makefile target {TARGET!r} is missing"]

    executed = _direct_python_scripts(recipe)
    executed_set = set(executed)

    declared: set[str] = set()
    skill_roots: list[str] = []
    for skill in manifest.get("skills", []):
        if not isinstance(skill, dict):
            continue
        skill_id = skill.get("id", "<unknown>")
        source_root = skill.get("source_root")
        if isinstance(source_root, str) and source_root:
            skill_roots.append(_normalize_path(source_root))

        checks = skill.get("checks", [])
        if not isinstance(checks, list):
            continue
        for check in checks:
            if not isinstance(check, str) or not check:
                continue
            normalized = _normalize_path(check)
            declared.add(normalized)
            if normalized not in executed_set:
                errors.append(
                    f"skill {skill_id}: declared check is not wired into {TARGET}: {normalized}"
                )

    for script in sorted(executed_set):
        owner_root = next(
            (
                root
                for root in skill_roots
                if script == root or script.startswith(root.rstrip("/") + "/")
            ),
            None,
        )
        if owner_root is None:
            continue
        if "/scripts/" not in script:
            continue
        if script not in declared:
            errors.append(
                f"Skill-owned check is wired into {TARGET} but not declared in suite manifest: {script}"
            )

    suite_validators = {
        _normalize_path(path)
        for path in (
            suite_validator_paths
            if suite_validator_paths is not None
            else _suite_validator_paths()
        )
    }
    _validate_convention_wiring(
        label="suite-level research validator",
        expected=suite_validators,
        prefix=SUITE_VALIDATOR_PREFIX,
        executed=executed,
        errors=errors,
    )

    planners = {
        _normalize_path(path)
        for path in planner_paths if planner_paths is not None
    } if planner_paths is not None else _planner_paths()
    _validate_convention_wiring(
        label="research planner",
        expected=planners,
        prefix=PLANNER_PREFIX,
        executed=executed,
        errors=errors,
    )

    return errors


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        makefile_text = MAKEFILE_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research declared-check wiring validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_declared_checks(
        manifest,
        makefile_text,
        suite_validator_paths=_suite_validator_paths(ROOT),
        planner_paths=_planner_paths(ROOT),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Research Skill-owned checks, suite-level validators, and planners are "
        "declared/wired into research-skill-check"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
