#!/usr/bin/env python3
"""Validate package-local references across declared research package Markdown.

An explicit package file set can be internally valid yet still contain a
progressive-reference path to a file that was omitted from the package. Check
all declared Markdown files, not only the runtime entry, so a packaged Method
Definition cannot introduce an unchecked second-hop reference.

The research corpus uses two path styles:

- package-root paths such as ``references/METHOD.md`` from ``SKILL.md``;
- same-directory paths such as ``REPRESENTATION.md`` from a file already under
  ``references/``.

Package-root paths are strict references. Explicit ``./`` / ``../`` paths and
Markdown links are also strict. A bare filename inside inline code is treated
as a reference only when it resolves to an existing sibling file; this avoids
mistaking conceptual mentions such as ``SKILL.md`` in an evidence dossier for
package dependencies.
"""

from __future__ import annotations

import json
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
PATHLIKE_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}


def _candidate_refs(text: str) -> list[tuple[str, bool]]:
    candidates: list[tuple[str, bool]] = []
    for value in INLINE_CODE_RE.findall(text):
        token = value.strip()
        if token:
            candidates.append((token, False))
    for value in MARKDOWN_LINK_RE.findall(text):
        token = value.strip().split("#", 1)[0]
        if token:
            candidates.append((token, True))
    return candidates


def _reference_candidate(
    token: str,
    *,
    package_root: Path,
    source: Path,
    from_markdown_link: bool,
) -> tuple[str, Path, bool] | None:
    """Return (package-relative path, resolved path, strict-existence flag)."""

    token = token.strip().split("#", 1)[0]
    if not token or "://" in token or token.startswith(("#", "/")):
        return None
    if any(char.isspace() for char in token):
        return None

    pure = PurePosixPath(token)
    if not pure.parts:
        return None

    if pure.parts[0] in PACKAGE_REFERENCE_PREFIXES:
        candidate = (package_root / Path(pure.as_posix())).resolve()
        strict = True
    elif token.startswith(("./", "../")) or from_markdown_link:
        candidate = (source.parent / Path(pure.as_posix())).resolve()
        strict = True
    elif len(pure.parts) == 1 and pure.suffix.lower() in PATHLIKE_SUFFIXES:
        candidate = (source.parent / pure.name).resolve()
        # Inline code often names a file conceptually. Treat a bare filename as
        # a dependency only when an actual sibling file exists.
        if not candidate.is_file():
            return None
        strict = False
    else:
        return None

    try:
        relative = candidate.relative_to(package_root).as_posix()
    except ValueError:
        relative = pure.as_posix()
    return relative, candidate, strict


def _validate_markdown_references(
    *,
    errors: list[str],
    skill_id: str,
    locale: str,
    package_root: Path,
    declared: set[str],
    source_relative: str,
) -> None:
    source = (package_root / Path(source_relative)).resolve()
    if not source.is_relative_to(package_root) or not source.is_file():
        return
    if source.suffix.lower() != ".md":
        return

    text = source.read_text(encoding="utf-8")
    seen: set[tuple[str, str]] = set()
    for token, from_markdown_link in _candidate_refs(text):
        resolved = _reference_candidate(
            token,
            package_root=package_root,
            source=source,
            from_markdown_link=from_markdown_link,
        )
        if resolved is None:
            continue
        relative, candidate, strict = resolved
        identity = (source_relative, relative)
        if identity in seen:
            continue
        seen.add(identity)

        if not candidate.is_relative_to(package_root):
            errors.append(
                f"skill {skill_id}: locale {locale} package file {source_relative} "
                f"reference escapes package root: {token}"
            )
            continue
        if strict and not candidate.is_file():
            errors.append(
                f"skill {skill_id}: locale {locale} package file {source_relative} "
                f"reference is missing: {relative}"
            )
            continue
        if candidate.is_file() and relative not in declared:
            errors.append(
                f"skill {skill_id}: locale {locale} package file {source_relative} "
                f"reference is not included in package_source.files: {relative}"
            )


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
            for source_relative in sorted(declared):
                _validate_markdown_references(
                    errors=errors,
                    skill_id=skill_id,
                    locale=str(locale),
                    package_root=package_root,
                    declared=declared,
                    source_relative=source_relative,
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

    print("Research package Markdown references are closed over declared package files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
