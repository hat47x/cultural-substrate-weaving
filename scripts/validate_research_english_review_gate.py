#!/usr/bin/env python3
"""Validate the research-stage English sibling Skill independent-review gate."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
EXPECTED_PACKET = (
    "research/skill-prototypes/"
    "P4-ENGLISH-INDEPENDENT-REVIEW-PACKET-2026-09-08.md"
)
EXPECTED_TARGETS = (
    "research/skill-prototypes/"
    "P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-08-v3.json"
)
EXPECTED_PREVIOUS_TARGETS = (
    "research/skill-prototypes/"
    "P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-07-v2.json"
)
EXPECTED_LOCALIZATION = (
    "research/skill-prototypes/"
    "P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json"
)
TARGET_SCHEMA = "csw.english-independent-review-targets/v1"
ALLOWED_STATUS = {"pending", "completed"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_PAIRS = {
    ("affinity-synthesis", "runtime"),
    ("affinity-synthesis", "method_definition"),
    ("affinity-synthesis", "representation_grammar"),
    ("iterative-inquiry-synthesis", "runtime"),
    ("iterative-inquiry-synthesis", "method_definition"),
    ("iterative-inquiry-synthesis", "round_template"),
}
SIBLING_RESEARCH_IDS = {research_id for research_id, _ in EXPECTED_PAIRS}


def _safe_repo_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _existing_file(root: Path, value: object) -> Path | None:
    if not _safe_repo_relative(value):
        return None
    path = root / str(value)
    return path if path.is_file() else None


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _packaged_english_markdown_paths(root: Path, errors: list[str]) -> set[str]:
    """Return English Markdown files selected by sibling package authority.

    The independent-review snapshot does not own package composition. It must
    cover the English Markdown that the research suite already selected for the
    two sibling runtime packages. Language-neutral non-Markdown assets remain
    governed by their technical-asset contracts rather than being pulled into
    language review merely because they are packaged.
    """

    suite_path = root / SUITE_PATH.relative_to(ROOT)
    try:
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read research suite for English review coverage: {exc}")
        return set()

    if not isinstance(suite, dict):
        errors.append("research suite for English review coverage must be a JSON object")
        return set()

    skills = suite.get("skills")
    if not isinstance(skills, list):
        errors.append("research suite skills must be a list for English review coverage")
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
                f"English review package authority is missing realized en-US sibling: {research_id}"
            )
            continue

        package_source = english.get("package_source")
        if not isinstance(package_source, dict) or package_source.get("mode") != "explicit_files":
            errors.append(
                f"English review package authority must use explicit_files for sibling: {research_id}"
            )
            continue
        package_root = package_source.get("root")
        files = package_source.get("files")
        if not isinstance(package_root, str) or not _safe_repo_relative(package_root):
            errors.append(
                f"English review package root is missing or unsafe for sibling: {research_id}"
            )
            continue
        if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
            errors.append(
                f"English review package files must be a string list for sibling: {research_id}"
            )
            continue

        for relative in files:
            if PurePosixPath(relative).suffix.lower() != ".md":
                continue
            source = (PurePosixPath(package_root) / PurePosixPath(relative)).as_posix()
            if not _safe_repo_relative(source):
                errors.append(
                    f"English review package Markdown path is unsafe for {research_id}: {source}"
                )
                continue
            packaged.add(source)

    missing_ids = sorted(SIBLING_RESEARCH_IDS - found_ids)
    if missing_ids:
        errors.append(
            f"research suite is missing sibling Skills required by English review: {missing_ids}"
        )
    return packaged


def _validate_targets(root: Path, targets_path: Path, errors: list[str]) -> None:
    try:
        snapshot = json.loads(targets_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read English independent review target snapshot: {exc}")
        return

    if not isinstance(snapshot, dict):
        errors.append("English independent review target snapshot must be a JSON object")
        return
    if snapshot.get("schema") != TARGET_SCHEMA:
        errors.append(f"English review target snapshot schema must be {TARGET_SCHEMA}")
    if snapshot.get("status") != "review-target-snapshot":
        errors.append("English review target snapshot status must remain review-target-snapshot")
    source_commit = snapshot.get("review_source_commit")
    if not isinstance(source_commit, str) or not HEX40.fullmatch(source_commit):
        errors.append("English review target snapshot review_source_commit must be a 40-char SHA")

    supersedes = snapshot.get("supersedes")
    if supersedes != EXPECTED_PREVIOUS_TARGETS:
        errors.append("English review target v3 must preserve the v2 snapshot reference")

    targets = snapshot.get("targets")
    if not isinstance(targets, list):
        errors.append("English review target snapshot targets must be a list")
        return

    actual_pairs: set[tuple[str, str]] = set()
    targeted_english_paths: set[str] = set()
    for item in targets:
        if not isinstance(item, dict):
            errors.append("English review target entry must be an object")
            continue
        research_id = item.get("research_id")
        artifact = item.get("artifact")
        if isinstance(research_id, str) and isinstance(artifact, str):
            pair = (research_id, artifact)
            if pair in actual_pairs:
                errors.append(f"duplicate English review target pair: {pair}")
            actual_pairs.add(pair)

        for locale in ("ja", "en"):
            side = item.get(locale)
            if not isinstance(side, dict):
                errors.append(f"English review target {research_id}/{artifact} missing {locale} side")
                continue
            relative = side.get("path")
            if locale == "en" and isinstance(relative, str):
                targeted_english_paths.add(relative)
            expected_sha = side.get("blob_sha")
            path = _existing_file(root, relative)
            if path is None:
                errors.append(
                    f"English review target file is missing or unsafe: {relative!r}"
                )
                continue
            if not isinstance(expected_sha, str) or not HEX40.fullmatch(expected_sha):
                errors.append(
                    f"English review target blob_sha must be a 40-char SHA: {relative}"
                )
                continue
            actual_sha = _git_blob_sha(path)
            if actual_sha != expected_sha:
                errors.append(
                    f"English review target blob changed since snapshot: {relative}; "
                    f"expected={expected_sha}, actual={actual_sha}"
                )

    if actual_pairs != EXPECTED_PAIRS:
        errors.append(
            "English review target snapshot must contain exactly runtime, method_definition, and directly referenced explanatory technical-asset pairs for both sibling Skills"
        )

    packaged_english_paths = _packaged_english_markdown_paths(root, errors)
    missing_packaged_targets = sorted(packaged_english_paths - targeted_english_paths)
    if missing_packaged_targets:
        errors.append(
            "English review target snapshot is missing packaged English Markdown review targets: "
            f"{missing_packaged_targets}"
        )


def validate_english_review_gate(root: Path, descriptor: dict) -> list[str]:
    errors: list[str] = []
    gate = descriptor.get("english_independent_review")
    if not isinstance(gate, dict):
        return ["production descriptor must declare english_independent_review"]

    status = gate.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("english_independent_review.status must be pending or completed")

    packet = gate.get("packet")
    if packet != EXPECTED_PACKET:
        errors.append(
            "english_independent_review.packet must reference the canonical review packet"
        )
    packet_path = _existing_file(root, packet)
    if packet_path is None:
        errors.append("English independent review packet is missing or unsafe")
    else:
        text = packet_path.read_text(encoding="utf-8")
        for marker in (
            "review not yet completed",
            "固定査読snapshot",
            EXPECTED_TARGETS,
            "representation grammarとround template",
            "Layer 1 必須不変条件",
            "Layer 2 必須不変条件",
            "Cross-layer査読",
            "technical asset parity:",
            "reviewer relation / independence:",
            "Reviewed target snapshot:",
            "production promotion全体の承認ではない",
        ):
            if marker not in text:
                errors.append(f"English review packet missing required marker: {marker}")

    targets = gate.get("targets")
    if targets != EXPECTED_TARGETS:
        errors.append(
            "english_independent_review.targets must reference the canonical v3 review target snapshot"
        )
    targets_path = _existing_file(root, targets)
    if targets_path is None:
        errors.append("English independent review target snapshot is missing or unsafe")
    else:
        _validate_targets(root, targets_path, errors)

    localization = gate.get("technical_asset_localization")
    if localization != EXPECTED_LOCALIZATION:
        errors.append(
            "english_independent_review.technical_asset_localization must reference the canonical localization contract"
        )
    if _existing_file(root, localization) is None:
        errors.append("English technical-asset localization contract is missing or unsafe")

    completed_review = gate.get("completed_review")
    if status == "pending":
        if completed_review is not None:
            errors.append(
                "pending English independent review must not declare completed_review"
            )
    elif status == "completed":
        review_path = _existing_file(root, completed_review)
        if review_path is None:
            errors.append(
                "completed English independent review must reference an existing safe review record"
            )
        elif review_path in {packet_path, targets_path}:
            errors.append(
                "completed review record must be separate from the review packet and target snapshot"
            )
        else:
            review_text = review_path.read_text(encoding="utf-8")
            for marker in (
                "reviewer:",
                "reviewer relation / independence:",
                "review date:",
                "review scope:",
                "Layer 1:",
                "Layer 2:",
                "technical asset parity:",
                "Cross-layer ownership:",
                "KJ lineage / naming:",
                "Promotion recommendation:",
                "Reviewed target snapshot:",
                "Reviewed commit / blob refs:",
            ):
                if marker not in review_text:
                    errors.append(
                        f"completed English review record missing required marker: {marker}"
                    )
            if EXPECTED_TARGETS not in review_text:
                errors.append(
                    "completed English review record must identify the canonical v3 target snapshot"
                )

    if gate.get("production_promotion_authorized") is not False:
        errors.append(
            "English independent review gate must not authorize production promotion by itself"
        )

    return errors


def main() -> int:
    try:
        descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"English independent review gate validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_english_review_gate(ROOT, descriptor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research English independent review gate validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
