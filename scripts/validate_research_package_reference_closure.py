#!/usr/bin/env python3
"""Validate local runtime-entry references against research package contents.

The research suite can declare an explicit package file set that is internally
valid yet still omit a progressive-reference file named by SKILL.md. This
checker closes that gap without deciding promotion or release readiness.
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
            text = runtime_path.read_text(encoding="utf-8")
            for token in sorted(_candidate_refs(text)):
                relative = _package_local_reference(token)
                if relative is None:
                    continue

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

    print("Research package runtime references are closed over declared package files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
