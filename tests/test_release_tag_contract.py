from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_release_tag import (  # noqa: E402
    read_manifest_source_commit,
    read_manifest_version,
    validate_release_publication,
    validate_release_tag,
    validate_tag_against_version,
)


FROZEN_CHANGELOG = (
    "## Unreleased\n\n"
    "## 0.5.0 — 2026-09-04\n\n"
    "- Released change.\n"
)


class ReleaseTagContractTests(unittest.TestCase):
    def test_tag_matches_version(self) -> None:
        self.assertEqual(validate_tag_against_version("v0.5.0", "0.5.0"), [])

    def test_wrong_tag_is_rejected(self) -> None:
        errors = validate_tag_against_version("v0.5.1", "0.5.0")
        self.assertTrue(any("release tag mismatch" in error for error in errors))

    def test_malformed_tag_is_rejected(self) -> None:
        errors = validate_tag_against_version("0.5.0", "0.5.0")
        self.assertTrue(any("release tag must be vX.Y.Z" in error for error in errors))

    def test_manifest_version_mismatch_is_rejected(self) -> None:
        errors = validate_release_tag("v0.5.0", "0.5.0", "0.4.0")
        self.assertTrue(any("release manifest version mismatch" in error for error in errors))

    def test_correct_tag_version_and_manifest_pass(self) -> None:
        self.assertEqual(validate_release_tag("v0.5.0", "0.5.0", "0.5.0"), [])

    def test_publication_requires_dated_changelog_boundary(self) -> None:
        head = "a" * 40
        errors = validate_release_publication(
            "v0.5.0",
            "0.5.0",
            "0.5.0",
            head,
            head,
            "",
            "## Unreleased\n\n- Work continues here.\n",
        )
        self.assertTrue(any("CHANGELOG release boundary missing" in error for error in errors))

    def test_publication_rejects_empty_dated_release_section(self) -> None:
        head = "a" * 40
        errors = validate_release_publication(
            "v0.5.0",
            "0.5.0",
            "0.5.0",
            head,
            head,
            "",
            "## Unreleased\n\n## 0.5.0 — 2026-09-04\n",
        )
        self.assertTrue(any("must contain release contents" in error for error in errors))

    def test_publication_rejects_stale_manifest_source_commit(self) -> None:
        errors = validate_release_publication(
            "v0.5.0",
            "0.5.0",
            "0.5.0",
            "a" * 40,
            "b" * 40,
            "",
            FROZEN_CHANGELOG,
        )
        self.assertTrue(any("source_commit mismatch at tag gate" in error for error in errors))

    def test_publication_rejects_dirty_worktree(self) -> None:
        head = "a" * 40
        errors = validate_release_publication(
            "v0.5.0",
            "0.5.0",
            "0.5.0",
            head,
            head,
            " M CHANGELOG.md",
            FROZEN_CHANGELOG,
        )
        self.assertTrue(any("clean Git worktree" in error for error in errors))

    def test_publication_accepts_clean_frozen_exact_release_commit(self) -> None:
        head = "a" * 40
        errors = validate_release_publication(
            "v0.5.0",
            "0.5.0",
            "0.5.0",
            head,
            head,
            "",
            FROZEN_CHANGELOG,
        )
        self.assertEqual(errors, [])

    def test_reads_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            path.write_text(json.dumps({"version": "0.5.0"}) + "\n", encoding="utf-8")
            self.assertEqual(read_manifest_version(path), "0.5.0")

    def test_missing_manifest_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            path.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_manifest_version(path)

    def test_reads_manifest_source_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            source_commit = "a" * 40
            path.write_text(
                json.dumps({"source_commit": source_commit}) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(read_manifest_source_commit(path), source_commit)

    def test_missing_manifest_source_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "release-manifest.json"
            path.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_manifest_source_commit(path)


if __name__ == "__main__":
    unittest.main()
