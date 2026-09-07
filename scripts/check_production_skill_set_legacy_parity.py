#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from common import ROOT, manifest as legacy_manifest
from production_skill_set import resolve_production_skills


def validate_legacy_parity(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        resolved = resolve_production_skills(root)
    except (OSError, ValueError) as exc:
        return [f"cannot resolve production Skill-set: {exc}"]

    if len(resolved) != 1:
        return [
            "legacy production build bridge requires exactly one Skill; "
            "replace this gate intentionally when multi-Skill build wiring is introduced"
        ]

    skill = resolved[0]
    if skill.get("id") != "cultural-substrate-weaving":
        errors.append("legacy production build bridge must resolve cultural-substrate-weaving")
    if skill.get("source_manifest") != "src/manifest.json":
        errors.append("legacy production build bridge must resolve src/manifest.json")

    try:
        legacy = legacy_manifest()
    except (OSError, ValueError) as exc:
        return errors + [f"cannot read legacy production manifest: {exc}"]

    if skill.get("manifest") != legacy:
        errors.append(
            "production Skill-set resolver differs from the manifest used by the current legacy build"
        )
    return errors


def main() -> int:
    errors = validate_legacy_parity(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Production Skill-set resolver matches the current single-Skill build input")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
