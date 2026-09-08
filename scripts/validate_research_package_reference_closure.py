#!/usr/bin/env python3
"""Validate research Skill package reference closure.

The research suite can declare an explicit package file set that is internally
valid yet still omit a progressive-reference file named by SKILL.md. This
checker closes that gap without deciding promotion or release readiness.

`package_local_references()` and `validate_in_memory_package_reference_closure()`
are intentionally shared with the production-source projection preview so
source-stage and post-transform runtime closure use the same reference grammar.

In addition, every Markdown file selected for an explicit package is checked for
clickable relative Markdown links. Those links must resolve to another declared
package file. Nested inline-code tokens are not followed recursively because
method names and research identifiers are too ambiguous to treat as file paths.
"""

from __future__ import annotations

import json
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"

INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PACKAGE_REFERENCE_PREFIXES = {
    "references",
    "evals",
    "evidence",
    "examples",
    "scripts",
}
FILE_LIKE_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py"}


def _candidate_refs(text: str) -> set[str]:
    candidates: set[str] = set()
    for value in INLINE_CODE_RE.findall(text):
        token = value.strip()
        if token:
            candidates.add(token)
    for value in MARKDOWN_LINK_RE.findall(text):
        token = value.strip().split("#", 1)[0]
        if token:
            candidates.add(token)
    return candidates


def _package_local_reference(token: str) -> str | None:
    if "://" in token or token.startswith(("#", "/")):
        return None
    pure = PurePosixPath(token)
    if not pure.parts:
        return None
    if pure.parts[0] not in PACKAGE_REFERENCE_PREFIXES:
        return None
    return pure.as_posix()


def package_local_references(text: str) -> set[str]:
    """Return package-root-relative references recognized by the research grammar.

    This helper deliberately preserves the existing parser semantics: inline-code
    paths and Markdown-link targets are candidates, while only known package-local
    prefixes are treated as package dependencies. Callers decide which documents
    are normative enough to scan; the runtime closure contract scans the runtime
    entry while package-document closure separately follows explicit Markdown
    links in every declared Markdown file.
    """

    references: set[str] = set()
    for token in _candidate_refs(text):
        relative = _package_local_reference(token)
        if relative is not None:
            references.add(relative)
    return references


def _markdown_link_targets(text: str) -> set[str]:
    return {value.strip() for value in MARKDOWN_LINK_RE.findall(text) if value.strip()}


def _resolved_markdown_target(source_relative: str, token: str) -> tuple[str | None, bool]:
    """Resolve an explicit Markdown link relative to its containing document."""

    raw = token.strip()
    if not raw or raw.startswith(("#", "/")) or "://" in raw or raw.startswith("mailto:"):
        return None, False
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw:
        return None, False

    pure = PurePosixPath(raw)
    if pure.suffix.lower() not in FILE_LIKE_SUFFIXES:
        return None, False

    base = PurePosixPath(source_relative).parent
    normalized = posixpath.normpath((base / pure).as_posix())
    if normalized == ".." or normalized.startswith("../") or normalized.startswith("/"):
        return normalized, True
    return PurePosixPath(normalized).as_posix(), False


def validate_in_memory_package_reference_closure(
    files: dict[str, str],
    runtime_entry: str,
    *,
    label: str = "in-memory package",
) -> list[str]:
    """Validate runtime refs and Markdown links against an in-memory package tree.

    `files` keys are package-root-relative target paths after any filename/content
    projection. This lets production-source previews re-check closure after
    `.en.md -> .md` normalization and public-name transforms without writing a
    production tree to disk.
    """

    errors: list[str] = []
    normalized: dict[str, str] = {}
    for relative, text in files.items():
        if not isinstance(relative, str) or not isinstance(text, str):
            errors.append(f"{label} file map must contain string paths and text contents")
            continue
        path = PurePosixPath(relative).as_posix()
        if path == ".." or path.startswith("../") or path.startswith("/"):
            errors.append(f"{label} file path escapes package root: {relative}")
            continue
        if path in normalized:
            errors.append(f"{label} file map contains duplicate normalized path: {path}")
            continue
        normalized[path] = text

    runtime = PurePosixPath(runtime_entry).as_posix()
    runtime_text = normalized.get(runtime)
    if runtime_text is None:
        errors.append(f"{label} runtime entry is missing: {runtime}")
    else:
        for relative in sorted(package_local_references(runtime_text)):
            if relative not in normalized:
                errors.append(f"{label} runtime reference is missing: {relative}")

    for source_relative, text in sorted(normalized.items()):
        if PurePosixPath(source_relative).suffix.lower() != ".md":
            continue
        for token in sorted(_markdown_link_targets(text)):
            target_relative, escaped = _resolved_markdown_target(source_relative, token)
            if target_relative is None:
                continue
            if escaped:
                errors.append(
                    f"{label} packaged Markdown link escapes package root: "
                    f"{source_relative} -> {token}"
                )
                continue
            if target_relative not in normalized:
                errors.append(
                    f"{label} packaged Markdown link is missing: "
                    f"{source_relative} -> {target_relative}"
                )

    return errors


def validate_package_reference_closure(root: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    for skill in manifest.get("skills", []):
        if not isinstance(skill, dict):
            continue
        skill_id = skill.get("id")
        realizations = skill.get("locale_realizations")
        if not isinstance(skill_id, str) or not isinstance(realizations, dict):
            continue

        for locale, realization in realizations.items():
            if not isinstance(realization, dict) or realization.get("status") == "planned":
                continue
            package_source = realization.get("package_source")
            if not isinstance(package_source, dict) or package_source.get("mode") != "explicit_files":
                continue

            package_root_relative = package_source.get("root")
            runtime_relative = realization.get("runtime_entry")
            files = package_source.get("files")
            if not isinstance(package_root_relative, str) or not isinstance(runtime_relative, str):
                continue
            if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
                continue

            package_root = (root / package_root_relative).resolve()
            runtime_path = (root / runtime_relative).resolve()
            if not runtime_path.is_file() or not runtime_path.is_relative_to(package_root):
                continue

            declared = {PurePosixPath(item).as_posix() for item in files}

            runtime_text = runtime_path.read_text(encoding="utf-8")
            for relative in sorted(package_local_references(runtime_text)):
                candidate = (package_root / Path(relative)).resolve()
                if not candidate.is_relative_to(package_root):
                    errors.append(
                        f"skill {skill_id}: locale {locale} runtime reference escapes package root: "
                        f"{relative}"
                    )
                    continue
                if not candidate.is_file():
                    errors.append(
                        f"skill {skill_id}: locale {locale} runtime reference is missing: {relative}"
                    )
                    continue
                if relative not in declared:
                    errors.append(
                        f"skill {skill_id}: locale {locale} runtime reference is not included in "
                        f"package_source.files: {relative}"
                    )

            # A document selected for the package must not contain a clickable
            # local Markdown link that becomes broken after materialization.
            for source_relative in sorted(declared):
                if PurePosixPath(source_relative).suffix.lower() != ".md":
                    continue
                source_path = (package_root / Path(source_relative)).resolve()
                if not source_path.is_file() or not source_path.is_relative_to(package_root):
                    continue
                text = source_path.read_text(encoding="utf-8")
                for token in sorted(_markdown_link_targets(text)):
                    target_relative, escaped = _resolved_markdown_target(source_relative, token)
                    if target_relative is None:
                        continue
                    if escaped:
                        errors.append(
                            f"skill {skill_id}: locale {locale} packaged Markdown link escapes "
                            f"package root: {source_relative} -> {token}"
                        )
                        continue
                    target_path = (package_root / Path(target_relative)).resolve()
                    if not target_path.is_relative_to(package_root):
                        errors.append(
                            f"skill {skill_id}: locale {locale} packaged Markdown link escapes "
                            f"package root: {source_relative} -> {token}"
                        )
                        continue
                    if not target_path.is_file():
                        errors.append(
                            f"skill {skill_id}: locale {locale} packaged Markdown link is missing: "
                            f"{source_relative} -> {target_relative}"
                        )
                        continue
                    if target_relative not in declared:
                        errors.append(
                            f"skill {skill_id}: locale {locale} packaged Markdown link target is not "
                            f"included in package_source.files: {source_relative} -> {target_relative}"
                        )

    return errors


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research package reference-closure validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_package_reference_closure(ROOT, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Research package runtime references and packaged Markdown links are closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
