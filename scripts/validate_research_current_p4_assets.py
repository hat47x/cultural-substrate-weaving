#!/usr/bin/env python3
"""Validate registration of the current P4 authority assets.

The suite manifest keeps historical research assets, while the design-only
production descriptor points to the current promotion authorities. This
checker makes sure those current pointers are also registered in
suite_research_assets without hard-coding a particular dated packet, evidence,
or target-snapshot filename.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"
DESCRIPTOR_PATH = (
    ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def current_p4_authority_paths(descriptor: dict) -> list[str]:
    complete = descriptor.get("complete_checkout_validation")
    public_name = descriptor.get("public_name_recheck")
    english = descriptor.get("english_independent_review")
    if (
        not isinstance(complete, dict)
        or not isinstance(public_name, dict)
        or not isinstance(english, dict)
    ):
        return []

    values = [
        complete.get("evidence"),
        complete.get("binding_contract"),
        public_name.get("evidence"),
        english.get("packet"),
        english.get("targets"),
        english.get("technical_asset_localization"),
        english.get("completed_review"),
    ]
    return [value for value in values if isinstance(value, str)]


def validate_current_p4_assets(root: Path, manifest: dict, descriptor: dict) -> list[str]:
    errors: list[str] = []

    complete = descriptor.get("complete_checkout_validation")
    public_name = descriptor.get("public_name_recheck")
    english = descriptor.get("english_independent_review")
    if not isinstance(complete, dict):
        errors.append("production descriptor must declare complete_checkout_validation")
        return errors
    if not isinstance(public_name, dict):
        errors.append("production descriptor must declare public_name_recheck")
        return errors
    if not isinstance(english, dict):
        errors.append("production descriptor must declare english_independent_review")
        return errors

    required_fields = {
        "complete_checkout_validation.evidence": complete.get("evidence"),
        "complete_checkout_validation.binding_contract": complete.get("binding_contract"),
        "public_name_recheck.evidence": public_name.get("evidence"),
        "english_independent_review.packet": english.get("packet"),
        "english_independent_review.targets": english.get("targets"),
        "english_independent_review.technical_asset_localization": english.get(
            "technical_asset_localization"
        ),
    }
    completed_review = english.get("completed_review")
    if completed_review is not None:
        required_fields["english_independent_review.completed_review"] = completed_review

    assets = manifest.get("suite_research_assets")
    if not isinstance(assets, list) or not all(isinstance(item, str) for item in assets):
        return ["suite_research_assets must be a string list"]
    registered = set(assets)

    seen: set[str] = set()
    for field, value in required_fields.items():
        if not _safe_repo_relative(value):
            errors.append(f"current P4 authority path is missing or unsafe: {field}")
            continue
        relative = str(value)
        if relative in seen:
            errors.append(f"current P4 authority path is reused by multiple fields: {relative}")
        seen.add(relative)
        if not (root / relative).is_file():
            errors.append(f"current P4 authority file is missing: {relative}")
        if relative not in registered:
            errors.append(
                f"current P4 authority is not registered in suite_research_assets: {relative}"
            )

    return errors


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"current P4 authority-asset validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_current_p4_assets(ROOT, manifest, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Current P4 authority assets are registered in the research suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
