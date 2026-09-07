#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_production_skill_set import validate_production_skill_set

ROOT = Path(__file__).resolve().parents[1]
SKILL_SET_PATH = ROOT / "src" / "skill-set.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_production_skills(root: Path = ROOT) -> list[dict]:
    """Resolve the production Skill-set into validated source manifests.

    This is a read-only resolver. It does not choose candidates, inspect research
    maturity, generate runtime artifacts, or apply host-specific metadata.
    """

    descriptor_path = root / SKILL_SET_PATH.relative_to(ROOT)
    descriptor = _load(descriptor_path)
    errors = validate_production_skill_set(root, descriptor)
    if errors:
        raise ValueError("invalid production Skill-set: " + "; ".join(errors))

    resolved: list[dict] = []
    for entry in descriptor["skills"]:
        manifest_path = root / entry["source_manifest"]
        resolved.append(
            {
                "id": entry["id"],
                "source_manifest": entry["source_manifest"],
                "manifest": _load(manifest_path),
            }
        )
    return resolved
