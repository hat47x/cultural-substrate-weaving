from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


RESEARCH_READY = {"sourced-candidate", "profile-ready", "adopted"}
PROFILE_READY = "profile-ready"
ADOPTED = "adopted"

PROFILE_REQUIRED_MARKERS = (
    "## Source basis",
    "## Target-return questions",
)
PROFILE_OPERATION_MARKERS = (
    "## Native operation candidates",
    "## Candidate operations",
)
PROFILE_DEBINDING_MARKERS = (
    "## De-binding",
    "## De-binding route",
)


def _list_of_nonempty_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def _path_exists(root: Path, value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and (root / value).is_file()


def validate_candidate(root: Path, row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    item_id = str(row.get("id", "")).strip() or "<missing-id>"
    readiness = str(row.get("readiness", "")).strip()

    if readiness in RESEARCH_READY:
        for field in (
            "names",
            "structural_primitives",
            "cognitive_operations",
            "useful_for",
            "do_not_assume",
        ):
            if not _list_of_nonempty_strings(row.get(field)):
                errors.append(f"{item_id}: {field} must be a non-empty string list")

        sources = row.get("sources")
        if not isinstance(sources, list) or len(sources) < 2:
            errors.append(f"{item_id}: readiness {readiness} requires at least two sources")
        else:
            for index, source in enumerate(sources):
                if not isinstance(source, dict):
                    errors.append(f"{item_id}: sources[{index}] must be an object")
                    continue
                for key in ("kind", "title", "url"):
                    value = source.get(key)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{item_id}: sources[{index}].{key} is required")

    if readiness == PROFILE_READY:
        if not _path_exists(root, row.get("profile_path")):
            errors.append(f"{item_id}: profile-ready requires an existing profile_path")

        cues = row.get("selection_cues")
        if not _list_of_nonempty_strings(cues) or len(cues) < 2:
            errors.append(f"{item_id}: profile-ready requires at least two selection_cues")

        for field in ("worked_example_paths", "negative_example_paths"):
            values = row.get(field)
            if not _list_of_nonempty_strings(values):
                errors.append(f"{item_id}: profile-ready requires {field}")
                continue
            for value in values:
                if not (root / value).is_file():
                    errors.append(f"{item_id}: missing {field} file: {value}")

        profile_path = row.get("profile_path")
        if _path_exists(root, profile_path):
            text = (root / str(profile_path)).read_text(encoding="utf-8")
            if "Status: profile-ready" not in text:
                errors.append(f"{item_id}: profile file must declare Status: profile-ready")
            for marker in PROFILE_REQUIRED_MARKERS:
                if marker not in text:
                    errors.append(f"{item_id}: profile missing marker {marker}")
            if not any(marker in text for marker in PROFILE_OPERATION_MARKERS):
                errors.append(f"{item_id}: profile missing operation section")
            if not any(marker in text for marker in PROFILE_DEBINDING_MARKERS):
                errors.append(f"{item_id}: profile missing de-binding section")

    if readiness == ADOPTED:
        if not _path_exists(root, row.get("runtime_path")):
            errors.append(f"{item_id}: adopted requires an existing runtime_path")
        cues = row.get("selection_cues")
        if not _list_of_nonempty_strings(cues) or len(cues) < 2:
            errors.append(f"{item_id}: adopted requires at least two selection_cues")

    return errors


def validate_inventory(root: Path, data: dict[str, Any]) -> list[str]:
    if data.get("schema") != "csw.framework-candidate-inventory/v1":
        return ["unsupported framework candidate inventory schema"]
    rows = data.get("candidates")
    if not isinstance(rows, list):
        return ["inventory.candidates must be an array"]

    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("candidate must be an object")
            continue
        item_id = str(row.get("id", "")).strip()
        if not item_id:
            errors.append("candidate id is required")
        elif item_id in seen:
            errors.append(f"duplicate candidate id: {item_id}")
        else:
            seen.add(item_id)
        errors.extend(validate_candidate(root, row))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate readiness-specific quality contracts for CSW framework candidates."
    )
    parser.add_argument(
        "inventory",
        type=Path,
        nargs="?",
        default=Path("research/framework-candidates/cognitive-operation-inventory.json"),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="repository root used to resolve profile/runtime/example paths",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.inventory.read_text(encoding="utf-8"))
        errors = validate_inventory(args.root, data)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    print("framework corpus contract: ok")


if __name__ == "__main__":
    main()
