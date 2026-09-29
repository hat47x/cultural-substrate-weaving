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
SIBLING_RESEARCH_IDS = {research_id for research_id, _ in EXPECTED_ASSETS}


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _file(relative: object, *, root: Path = ROOT) -> Path | None:
    if not _safe_repo_relative(relative):
        return None
    repository = root.resolve()
    path = (root / str(relative)).resolve()
    if not path.is_relative_to(repository) or not path.is_file():
        return None
    return path


def _package_file_set(skill: object) -> set[str]:
    if not isinstance(skill, dict):
        return set()
    realizations = skill.get("locale_realizations")
    if not isinstance(realizations, dict):
        return set()
    english = realizations.get("en-US")
    if not isinstance(english, dict):
        return set()
    package_source = english.get("package_source")
    if not isinstance(package_source, dict):
        return set()
    files = package_source.get("files")
    if not isinstance(files, list):
        return set()
    return {item for item in files if isinstance(item, str)}


def _packaged_non_markdown_paths(suite: dict, errors: list[str]) -> set[str]:
    """Return non-Markdown files selected for sibling en-US runtime packages.

    English Markdown prose is governed by the independent-review snapshot. Any
    other packaged file must still be explicitly classified by the technical
    localization contract so language-neutral schemas/scripts/assets cannot
    silently enter the English package outside both gates.
    """

    skills = suite.get("skills")
    if not isinstance(skills, list):
        errors.append("research suite skills must be a list for technical localization coverage")
        return set()

    found_ids: set[str] = set()
    packaged: set[str] = set()
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        research_id = skill.get("id")
        if research_id not in SIBLING_RESEARCH_IDS:
            continue
        found_ids.add(research_id)

        realizations = skill.get("locale_realizations")
        english = realizations.get("en-US") if isinstance(realizations, dict) else None
        if not isinstance(english, dict) or english.get("status") == "planned":
            errors.append(
                f"technical localization package authority is missing realized en-US sibling: {research_id}"
            )
            continue

        package_source = english.get("package_source")
        if not isinstance(package_source, dict) or package_source.get("mode") != "explicit_files":
            errors.append(
                f"technical localization package authority must use explicit_files for sibling: {research_id}"
            )
            continue
        package_root = package_source.get("root")
        files = package_source.get("files")
        if not isinstance(package_root, str) or not _safe_repo_relative(package_root):
            errors.append(
                f"technical localization package root is missing or unsafe for sibling: {research_id}"
            )
            continue
        if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
            errors.append(
                f"technical localization package files must be a string list for sibling: {research_id}"
            )
            continue

        for relative in files:
            if PurePosixPath(relative).suffix.lower() == ".md":
                continue
            source = (PurePosixPath(package_root) / PurePosixPath(relative)).as_posix()
            if not _safe_repo_relative(source):
                errors.append(
                    f"technical localization package asset path is unsafe for {research_id}: {source}"
                )
                continue
            packaged.add(source)

    missing_ids = sorted(SIBLING_RESEARCH_IDS - found_ids)
    if missing_ids:
        errors.append(
            f"research suite is missing sibling Skills required by technical localization: {missing_ids}"
        )
    return packaged


def validate_localization(
    contract: dict,
    suite: dict,
    *,
    root: Path = ROOT,
) -> list[str]:
    if not isinstance(contract, dict):
        return ["technical localization contract must be an object"]
    if not isinstance(suite, dict):
        return ["research skill suite must be an object"]

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
    covered_english_package_paths: set[str] = set()
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
            ja_relative = item.get("ja")
            en_relative = item.get("en")
            ja = _file(ja_relative, root=root)
            en = _file(en_relative, root=root)
            if ja is None:
                errors.append(f"localized technical asset missing Japanese source: {ja_relative}")
            if en is None:
                errors.append(f"localized technical asset missing English draft: {en_relative}")
            if _safe_repo_relative(en_relative):
                covered_english_package_paths.add(str(en_relative))
            if item.get("english_runtime_reference") is not True:
                errors.append(f"translated runtime technical asset must be runtime-referenced: {research_id}/{role}")
            if item.get("english_package_required") is not True:
                errors.append(f"translated runtime technical asset must be package-required: {research_id}/{role}")
        elif status == "language-neutral-shared":
            shared_relative = item.get("shared")
            shared = _file(shared_relative, root=root)
            if shared is None:
                errors.append(f"shared technical asset missing: {shared_relative}")
            if _safe_repo_relative(shared_relative):
                covered_english_package_paths.add(str(shared_relative))
            if item.get("english_package_required") is not True:
                errors.append(f"shared runtime technical asset must be package-required: {research_id}/{role}")
        else:
            errors.append(f"unsupported technical localization status: {status!r}")

    if actual_pairs != EXPECTED_ASSETS:
        errors.append("technical localization asset set has drifted")

    packaged_non_markdown = _packaged_non_markdown_paths(suite, errors)
    missing_technical_classification = sorted(
        packaged_non_markdown - covered_english_package_paths
    )
    if missing_technical_classification:
        errors.append(
            "English package non-Markdown asset is not classified by technical localization contract: "
            f"{missing_technical_classification}"
        )

    skills = suite.get("skills")
    if isinstance(skills, list):
        skill_by_id = {
            skill.get("id"): skill
            for skill in skills
            if isinstance(skill, dict)
        }
    else:
        skill_by_id = {}

    affinity = skill_by_id.get("affinity-synthesis", {})
    affinity_files = _package_file_set(affinity)
    for required in (
        "SKILL.en.md",
        "references/METHOD.en.md",
        "references/REPRESENTATION.en.md",
        "references/affinity-map.schema.json",
    ):
        if required not in affinity_files:
            errors.append(f"affinity English package source missing localized runtime asset: {required}")

    iterative = skill_by_id.get("iterative-inquiry-synthesis", {})
    iterative_files = _package_file_set(iterative)
    for required in (
        "SKILL.en.md",
        "references/METHOD.en.md",
        "references/ROUND-TEMPLATE.en.md",
    ):
        if required not in iterative_files:
            errors.append(f"iterative English package source missing localized runtime asset: {required}")

    affinity_runtime = _file(
        "research/skill-prototypes/affinity-synthesis/SKILL.en.md",
        root=root,
    )
    if affinity_runtime is not None:
        text = affinity_runtime.read_text(encoding="utf-8")
        if "references/REPRESENTATION.en.md" not in text:
            errors.append("affinity English runtime must reference REPRESENTATION.en.md")
        if "`references/REPRESENTATION.md`" in text:
            errors.append("affinity English runtime must not directly reference Japanese REPRESENTATION.md")

    iterative_runtime = _file(
        "research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md",
        root=root,
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
        if not isinstance(contract, dict):
            raise ValueError("technical localization contract must contain a JSON object")
        if not isinstance(suite, dict):
            raise ValueError("research skill suite must contain a JSON object")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"technical asset localization validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_localization(contract, suite, root=ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research sibling technical asset localization validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
