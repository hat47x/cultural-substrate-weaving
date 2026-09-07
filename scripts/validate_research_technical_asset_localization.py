#!/usr/bin/env python3
"""Validate English runtime technical-asset localization for sibling Skills."""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json"
)
SUITE_MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
EXPECTED_SCHEMA = "csw.technical-asset-localization/v1"
EXPECTED_ASSETS = {
    ("affinity-synthesis", "representation_grammar"),
    ("affinity-synthesis", "machine_readable_schema"),
    ("iterative-inquiry-synthesis", "round_template"),
}


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _file(relative: object) -> Path | None:
    if not _safe_repo_relative(relative):
        return None
    path = ROOT / str(relative)
    return path if path.is_file() else None


def validate_localization(contract: dict, suite: dict) -> list[str]:
    errors: list[str] = []

    if contract.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"technical localization schema must be {EXPECTED_SCHEMA}")
    if contract.get("status") != "research-only":
        errors.append("technical localization status must remain research-only")
    if contract.get("locale") != "en-US":
        errors.append("technical localization contract must target en-US")
    if contract.get("production_promotion_authorized") is not False:
        errors.append("technical localization contract must not authorize production promotion")

    assets = contract.get("assets")
    if not isinstance(assets, list):
        return errors + ["technical localization assets must be a list"]

    actual_pairs: set[tuple[str, str]] = set()
    for item in assets:
        if not isinstance(item, dict):
            errors.append("technical localization asset entry must be an object")
            continue
        research_id = item.get("research_id")
        role = item.get("role")
        if isinstance(research_id, str) and isinstance(role, str):
            actual_pairs.add((research_id, role))

        status = item.get("localization_status")
        if status == "translated-draft":
            ja = _file(item.get("ja"))
            en = _file(item.get("en"))
            if ja is None:
                errors.append(f"localized technical asset missing Japanese source: {item.get('ja')}")
            if en is None:
                errors.append(f"localized technical asset missing English draft: {item.get('en')}")
            if item.get("english_runtime_reference") is not True:
                errors.append(f"translated runtime technical asset must be runtime-referenced: {research_id}/{role}")
            if item.get("english_package_required") is not True:
                errors.append(f"translated runtime technical asset must be package-required: {research_id}/{role}")
        elif status == "language-neutral-shared":
            shared = _file(item.get("shared"))
            if shared is None:
                errors.append(f"shared technical asset missing: {item.get('shared')}")
            if item.get("english_package_required") is not True:
                errors.append(f"shared runtime technical asset must be package-required: {research_id}/{role}")
        else:
            errors.append(f"unsupported technical localization status: {status!r}")

    if actual_pairs != EXPECTED_ASSETS:
        errors.append("technical localization asset set has drifted")

    skill_by_id = {
        skill.get("id"): skill
        for skill in suite.get("skills", [])
        if isinstance(skill, dict)
    }

    affinity = skill_by_id.get("affinity-synthesis", {})
    affinity_en = affinity.get("locale_realizations", {}).get("en-US", {})
    affinity_files = set(affinity_en.get("package_source", {}).get("files", []))
    for required in (
        "SKILL.en.md",
        "references/METHOD.en.md",
        "references/REPRESENTATION.en.md",
        "references/affinity-map.schema.json",
    ):
        if required not in affinity_files:
            errors.append(f"affinity English package source missing localized runtime asset: {required}")

    iterative = skill_by_id.get("iterative-inquiry-synthesis", {})
    iterative_en = iterative.get("locale_realizations", {}).get("en-US", {})
    iterative_files = set(iterative_en.get("package_source", {}).get("files", []))
    for required in (
        "SKILL.en.md",
        "references/METHOD.en.md",
        "references/ROUND-TEMPLATE.en.md",
    ):
        if required not in iterative_files:
            errors.append(f"iterative English package source missing localized runtime asset: {required}")

    affinity_runtime = _file(
        "research/skill-prototypes/affinity-synthesis/SKILL.en.md"
    )
    if affinity_runtime is not None:
        text = affinity_runtime.read_text(encoding="utf-8")
        if "references/REPRESENTATION.en.md" not in text:
            errors.append("affinity English runtime must reference REPRESENTATION.en.md")
        if "`references/REPRESENTATION.md`" in text:
            errors.append("affinity English runtime must not directly reference Japanese REPRESENTATION.md")

    iterative_runtime = _file(
        "research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md"
    )
    if iterative_runtime is not None:
        text = iterative_runtime.read_text(encoding="utf-8")
        if "references/ROUND-TEMPLATE.en.md" not in text:
            errors.append("iterative English runtime must reference ROUND-TEMPLATE.en.md")
        if "`references/ROUND-TEMPLATE.md`" in text:
            errors.append("iterative English runtime must not directly reference Japanese ROUND-TEMPLATE.md")

    invariants = contract.get("invariants")
    if not isinstance(invariants, list):
        errors.append("technical localization invariants must be a list")
    else:
        joined = "\n".join(str(item) for item in invariants)
        for marker in (
            "English runtime must not directly depend on Japanese explanatory technical prose",
            "language-neutral schema assets may be shared across locales",
            "does not authorize production promotion",
        ):
            if marker.lower() not in joined.lower():
                errors.append(f"technical localization invariant missing: {marker}")

    classified = contract.get("classified_non_runtime_or_not_required_in_english_package")
    if not isinstance(classified, list) or not classified:
        errors.append("technical localization contract must explicitly classify non-runtime ancillary material")

    return errors


def main() -> int:
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        suite = json.loads(SUITE_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"technical asset localization validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_localization(contract, suite)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research sibling technical asset localization validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
