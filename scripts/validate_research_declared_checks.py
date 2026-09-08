#!/usr/bin/env python3
"""Validate research check wiring into the research gate.

Two ownership rules coexist:

1. Skill-owned checks are declared in the research suite manifest and must be
   invoked directly by the `research-skill-check` Makefile target. A Skill-owned
   check must not bypass the manifest.
2. Root suite-level validators follow the repository naming convention
   `scripts/validate_research_*.py`. Every such validator must be invoked
   directly by the same Makefile target, and a Makefile command using that
   convention must resolve to an existing validator file.

This keeps the manifest authoritative for Skill-local checks while making the
suite-level validator filename convention operational instead of relying on
manual Makefile review.
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


def validate_declared_checks(
    manifest: dict,
    makefile_text: str,
    *,
    suite_validator_paths: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    recipe = _target_recipe(makefile_text)
    if recipe is None:
        return [f"Makefile target {TARGET!r} is missing"]

    executed = _direct_python_scripts(recipe)
    executed_set = set(executed)
    execution_counts = Counter(executed)

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
    for validator in sorted(suite_validators):
        if validator not in executed_set:
            errors.append(
                f"suite-level research validator is not wired into {TARGET}: {validator}"
            )
        elif execution_counts[validator] != 1:
            errors.append(
                f"suite-level research validator must be wired exactly once into {TARGET}: "
                f"{validator} (found {execution_counts[validator]})"
            )

    for script in sorted(executed_set):
        if not script.startswith(SUITE_VALIDATOR_PREFIX) or not script.endswith(".py"):
            continue
        if script not in suite_validators:
            errors.append(
                f"research gate references an unknown suite-level validator: {script}"
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
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Research Skill-owned checks and suite-level validators are declared/wired "
        "into research-skill-check"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
