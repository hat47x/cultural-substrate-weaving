from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_natural_japanese_review import (  # noqa: E402
    load_manifest,
    review_scope,
    validate_manifest_data,
)


class NaturalJapaneseReviewFreshnessTests(unittest.TestCase):
    def test_current_manifest_matches_all_scoped_documents(self) -> None:
        self.assertEqual(validate_manifest_data(ROOT, load_manifest()), [])

    def test_review_record_itself_is_in_scope(self) -> None:
        self.assertIn(
            "docs/ja/maintainers/natural-japanese-review.md",
            review_scope(ROOT),
        )

    def test_stale_hash_fails_closed(self) -> None:
        manifest = copy.deepcopy(load_manifest())
        path = "docs/ja/architecture.md"
        manifest["documents"][path]["git_blob_sha"] = "0" * 40

        errors = validate_manifest_data(ROOT, manifest)

        self.assertTrue(
            any(f"natural-Japanese review is stale for {path}" in error for error in errors),
            errors,
        )

    def test_missing_record_fails_closed(self) -> None:
        manifest = copy.deepcopy(load_manifest())
        path = "docs/ja/architecture.md"
        manifest["documents"].pop(path)

        errors = validate_manifest_data(ROOT, manifest)

        self.assertIn(f"missing natural-Japanese review record: {path}", errors)

    def test_removed_or_out_of_scope_record_fails_closed(self) -> None:
        manifest = copy.deepcopy(load_manifest())
        path = "docs/ja/maintainers/removed.md"
        manifest["documents"][path] = {
            "git_blob_sha": "0" * 40,
            "reviewed_at": "2026-09-01",
        }

        errors = validate_manifest_data(ROOT, manifest)

        self.assertIn(
            f"review manifest contains out-of-scope or removed document: {path}",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
