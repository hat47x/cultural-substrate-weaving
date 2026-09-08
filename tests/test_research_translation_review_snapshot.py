from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_translation_review_snapshot import _git_blob_sha, validate_review_snapshot

STATUS_PATH = ROOT / "research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"


class TranslationReviewSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))

    def test_current_reviewed_sources_match_snapshot(self) -> None:
        self.assertEqual(validate_review_snapshot(ROOT, self.status), [])

    def test_snapshot_must_cover_exact_scope(self) -> None:
        status = copy.deepcopy(self.status)
        status["reviewed_source_blobs"].pop("ROUTER.md")
        errors = validate_review_snapshot(ROOT, status)
        self.assertTrue(any("cover exactly scope_files" in error for error in errors))

    def test_changed_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src/ja-JP/ROUTER.md"
            source.parent.mkdir(parents=True)
            source.write_text("reviewed\n", encoding="utf-8")
            status = {
                "scope_files": ["ROUTER.md"],
                "reviewed_source_blobs": {"ROUTER.md": _git_blob_sha(source)},
                "invariants": [
                    "reviewed_source_blobs pins the exact Japanese source bytes that received bilingual semantic review"
                ],
            }
            self.assertEqual(validate_review_snapshot(root, status), [])
            source.write_text("changed after review\n", encoding="utf-8")
            errors = validate_review_snapshot(root, status)
            self.assertTrue(any("changed after bilingual semantic review" in error for error in errors))

    def test_snapshot_sha_must_be_lowercase_git_blob_sha(self) -> None:
        status = copy.deepcopy(self.status)
        status["reviewed_source_blobs"]["ROUTER.md"] = "A" * 40
        errors = validate_review_snapshot(ROOT, status)
        self.assertTrue(any("invalid reviewed source blob SHA" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
