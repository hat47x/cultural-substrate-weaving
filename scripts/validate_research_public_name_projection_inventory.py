#!/usr/bin/env python3
"""Validate promotion-sensitive public-name projection inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"
)
EXPECTED_SCHEMA = "csw.public-name-projection-inventory/v1"
EXPECTED_RESEARCH_ID = "affinity-synthesis"
EXPECTED_PRODUCTION_NAME = "material-led-synthesis"


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _repo_path(root: Path, relative: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(relative, str) or not relative:
        errors.append(f"{label} must be a non-empty repository-relative path")
        return None
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        errors.append(f"{label} escapes repository root: {relative}")
        return None
    return path


def validate_projection_inventory(root: Path, inventory: dict) -> list[str]:
    errors: list[str] = []
    if inventory.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"projection inventory schema must be {EXPECTED_SCHEMA}")
    if inventory.get("status") != "design-only":
        errors.append("projection inventory must remain status=design-only")
    if inventory.get("research_id") != EXPECTED_RESEARCH_ID:
        errors.append("projection inventory research_id must remain affinity-synthesis")
    if inventory.get("production_name") != EXPECTED_PRODUCTION_NAME:
        errors.append("projection inventory production_name must remain material-led-synthesis")

    content_items = inventory.get("content_projection")
    if not isinstance(content_items, list) or not content_items:
        errors.append("content_projection must be a non-empty list")
        content_items = []
    seen_paths: set[str] = set()
    for index, item in enumerate(content_items):
        if not isinstance(item, dict):
            errors.append(f"content_projection[{index}] must be an object")
            continue
        relative = item.get("path")
        if isinstance(relative, str):
            if relative in seen_paths:
                errors.append(f"content_projection repeats path: {relative}")
            seen_paths.add(relative)
        path = _repo_path(root, relative, f"content_projection[{index}].path", errors)
        if path is None:
            continue
        if not path.is_file():
            errors.append(f"projection-sensitive file is missing: {relative}")
            continue
        markers = item.get("required_markers")
        if not isinstance(markers, list) or not markers or not all(
            isinstance(marker, str) and marker for marker in markers
        ):
            errors.append(f"content_projection markers must be non-empty strings: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(
                    f"projection inventory marker changed and requires audit: {relative} -> {marker!r}"
                )

    structured_items = inventory.get("structured_projection")
    if not isinstance(structured_items, list) or not structured_items:
        errors.append("structured_projection must be a non-empty list")
        structured_items = []
    for index, item in enumerate(structured_items):
        if not isinstance(item, dict):
            errors.append(f"structured_projection[{index}] must be an object")
            continue
        relative = item.get("path")
        path = _repo_path(root, relative, f"structured_projection[{index}].path", errors)
        if path is None:
            continue
        if not path.is_file():
            errors.append(f"structured projection source is missing: {relative}")
            continue
        try:
            value = _load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"cannot read structured projection source {relative}: {exc}")
            continue
        field = item.get("field")
        if field != "contains":
            errors.append(f"unsupported structured projection field for {relative}: {field!r}")
            continue
        contains = value.get("contains")
        if not isinstance(contains, list) or EXPECTED_RESEARCH_ID not in contains:
            errors.append(
                f"structured projection source no longer contains research id and requires audit: {relative}"
            )

    path_items = inventory.get("path_projection")
    if not isinstance(path_items, list) or len(path_items) < 2:
        errors.append("path_projection must describe source and adapter promotion paths")
    else:
        for index, item in enumerate(path_items):
            if not isinstance(item, dict):
                errors.append(f"path_projection[{index}] must be an object")
                continue
            research_prefix = item.get("research_prefix")
            production_pattern = item.get("production_pattern")
            if not isinstance(research_prefix, str) or "affinity-synthesis" not in research_prefix:
                errors.append(f"path_projection[{index}] must preserve affinity-synthesis research prefix")
            if not isinstance(production_pattern, str) or "material-led-synthesis" not in production_pattern:
                errors.append(f"path_projection[{index}] must target material-led-synthesis production path")
            if isinstance(production_pattern, str) and production_pattern.startswith("research/"):
                errors.append(f"path_projection[{index}] production path must not point into research")

    keep = inventory.get("research_history_keep")
    if not isinstance(keep, list) or not keep:
        errors.append("research_history_keep must be a non-empty list")
    else:
        for index, relative in enumerate(keep):
            path = _repo_path(root, relative, f"research_history_keep[{index}]", errors)
            if path is not None and not path.exists():
                errors.append(f"research history path is missing: {relative}")

    note = inventory.get("note")
    if not isinstance(note, str) or "not an instruction to perform global string replacement" not in note:
        errors.append("projection inventory note must forbid global string replacement")

    return errors


def main() -> int:
    try:
        inventory = _load_json(INVENTORY_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"research public-name projection inventory validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_projection_inventory(ROOT, inventory)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research public-name projection inventory validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
