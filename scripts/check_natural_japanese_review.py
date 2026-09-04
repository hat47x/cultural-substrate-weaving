#!/usr/bin/env python3
"""Track freshness of the natural-Japanese review for scoped Japanese prose."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/ja/maintainers/natural-japanese-review-manifest.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def review_scope(root: Path = ROOT) -> list[str]:
    paths = {
        "README.md",
        ".github/release-validation-note.md",
        "docs/ja/architecture.md",
        "docs/ja/getting-started.md",
        "docs/ja/usage-context.md",
        ".living-lab/README.md",
        "research/living-lab/observations/README.md",
        "adapters/microsoft-copilot/ja-JP/instructions.md",
        "adapters/microsoft-copilot/ja-JP/package-readme.txt",
    }
    paths.update(
        path.relative_to(root).as_posix()
        for path in (root / "docs/ja/maintainers").glob("*.md")
    )
    paths.update(
        path.relative_to(root).as_posix()
        for path in (root / "docs/ja/experiments").glob("*.md")
    )
    paths.update(
        path.relative_to(root).as_posix()
        for path in (root / "docs/ja/platforms").glob("*.md")
    )
    return sorted(paths)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest_data(root: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("natural-Japanese review manifest must use schema_version 1")

    documents = manifest.get("documents")
    if not isinstance(documents, dict):
        return errors + ["natural-Japanese review manifest documents must be an object"]

    expected = set(review_scope(root))
    recorded = set(documents)

    for path in sorted(expected - recorded):
        errors.append(f"missing natural-Japanese review record: {path}")
    for path in sorted(recorded - expected):
        errors.append(f"review manifest contains out-of-scope or removed document: {path}")

    for relative in sorted(expected & recorded):
        record = documents.get(relative)
        if not isinstance(record, dict):
            errors.append(f"invalid natural-Japanese review record: {relative}")
            continue

        reviewed_at = record.get("reviewed_at")
        try:
            date.fromisoformat(reviewed_at)
        except (TypeError, ValueError):
            errors.append(f"invalid reviewed_at for {relative}: {reviewed_at!r}")

        recorded_sha = record.get("git_blob_sha")
        if not isinstance(recorded_sha, str) or not SHA_RE.fullmatch(recorded_sha):
            errors.append(f"invalid git_blob_sha for {relative}: {recorded_sha!r}")
            continue

        path = root / relative
        if not path.is_file():
            errors.append(f"reviewed Japanese document is missing: {relative}")
            continue

        actual_sha = git_blob_sha(path.read_bytes())
        if actual_sha != recorded_sha:
            errors.append(
                "natural-Japanese review is stale for "
                f"{relative}: recorded {recorded_sha}, current {actual_sha}"
            )

    return errors


def write_review_records(
    root: Path,
    manifest_path: Path,
    relative_paths: list[str],
    review_date: str,
) -> None:
    date.fromisoformat(review_date)
    manifest = load_manifest(manifest_path) if manifest_path.exists() else {
        "schema_version": 1,
        "documents": {},
    }
    if manifest.get("schema_version") != 1 or not isinstance(
        manifest.get("documents"), dict
    ):
        raise ValueError("cannot update an invalid natural-Japanese review manifest")

    scope = set(review_scope(root))
    for relative in relative_paths:
        normalized = Path(relative).as_posix()
        if normalized not in scope:
            raise ValueError(f"not in natural-Japanese review scope: {normalized}")
        path = root / normalized
        manifest["documents"][normalized] = {
            "git_blob_sha": git_blob_sha(path.read_bytes()),
            "reviewed_at": review_date,
        }

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        nargs="+",
        metavar="PATH",
        help="record only documents that have actually completed the full prose review",
    )
    parser.add_argument(
        "--review-date",
        default=date.today().isoformat(),
        help="ISO review date used with --record (default: today)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.record:
            write_review_records(ROOT, MANIFEST_PATH, args.record, args.review_date)
        errors = validate_manifest_data(ROOT, load_manifest())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"natural-Japanese review check failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            "Reread each stale/missing document as continuous Japanese prose, then "
            "record only the reviewed paths with --record.",
            file=sys.stderr,
        )
        return 1

    print(f"ok: natural-Japanese review is current for {len(review_scope())} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
