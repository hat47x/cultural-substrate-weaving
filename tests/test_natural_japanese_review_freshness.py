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

    def test_public_japanese_guides_are_in_scope(self) -> None:
        scoped = set(review_scope(ROOT))
        self.assertIn("README.md", scoped)
        self.assertIn("docs/README.md", scoped)
        self.assertIn("docs/ja/getting-started.md", scoped)
        self.assertIn("docs/ja/usage-context.md", scoped)
        self.assertIn("docs/ja/platforms/chatgpt-gpt.md", scoped)
        self.assertIn("docs/ja/platforms/claude-code.md", scoped)
        self.assertIn("docs/ja/platforms/codex.md", scoped)
        self.assertIn("docs/ja/platforms/microsoft-copilot.md", scoped)
        self.assertIn("docs/ja/platforms/project-instructions.md", scoped)

    def test_release_validation_note_japanese_prose_is_in_scope(self) -> None:
        self.assertIn(".github/release-validation-note.md", review_scope(ROOT))

    def test_current_human_use_research_index_is_in_scope(self) -> None:
        self.assertIn("research/human-use-gap-kj/README.md", review_scope(ROOT))

    def test_m365_japanese_runtime_prose_is_in_scope(self) -> None:
        scoped = set(review_scope(ROOT))
        self.assertIn("adapters/microsoft-copilot/ja-JP/instructions.md", scoped)
        self.assertIn("adapters/microsoft-copilot/ja-JP/package-readme.txt", scoped)

    def test_runtime_canonical_source_is_not_in_prose_review_scope(self) -> None:
        self.assertNotIn("src/ja-JP/ROUTER.md", review_scope(ROOT))

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
