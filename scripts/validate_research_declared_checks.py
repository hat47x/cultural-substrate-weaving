#!/usr/bin/env python3
"""Validate wiring between research Skill-owned checks and the research gate.

The research suite manifest declares check scripts owned by individual Skills.
This validator makes that declaration operational by requiring every declared
Skill-owned check to be invoked directly by the `research-skill-check` Makefile
target. It also rejects Skill-owned check invocations that bypass the manifest.

Suite-level validators remain outside this contract; only checks under a
registered Skill source root are compared here.
"""

from __future__ import annotations

import json
import posixpath
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
MAKEFILE_PATH = ROOT / "Makefile"
TARGET = "research-skill-check"


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


def validate_declared_checks(manifest: dict, makefile_text: str) -> list[str]:
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

    return errors


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        makefile_text = MAKEFILE_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research declared-check wiring validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_declared_checks(manifest, makefile_text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research Skill-owned checks are declared and wired into research-skill-check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
