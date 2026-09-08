from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from mark_research_translation_refresh_synchronized import (  # noqa: E402
    transition_to_synchronized,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class ResearchTranslationRefreshTransitionTests(unittest.TestCase):
    def make_fixture(self, root: Path, *, synchronized_manifest: bool = True) -> tuple[dict, dict]:
        ja = root / "src/ja-JP/x.md"
        en = root / "src/en-US/x.md"
        ja.parent.mkdir(parents=True, exist_ok=True)
        en.parent.mkdir(parents=True, exist_ok=True)
        ja.write_text("日本語 current\n", encoding="utf-8")
        en.write_text("English tension marker\n", encoding="utf-8")

        ja_bytes = ja.read_bytes()
        current = sha256(ja_bytes)
        old = "0" * 64
        tracked = current if synchronized_manifest else old
        status = {
            "status": "pending-review-hash-refresh",
            "scope_files": ["x.md"],
            "expected_stale_files": ["x.md"],
            "english_markers": {"x.md": ["tension marker"]},
            "reviewed_source_blobs": {"x.md": git_blob_sha(ja_bytes)},
            "invariants": [
                "reviewed_source_blobs pins the exact Japanese source bytes accepted by bilingual semantic review and is not rewritten by hash synchronization"
            ],
        }
        manifest = {
            "files": {
                "x.md": {
                    "ja_sha256": tracked,
                    "en_source_ja_sha256": tracked,
                }
            }
        }
        return status, manifest

    def test_transition_succeeds_only_after_manifest_is_synchronized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status, manifest = self.make_fixture(root, synchronized_manifest=True)
            updated, errors = transition_to_synchronized(root, status, manifest)
            self.assertEqual(errors, [])
            self.assertEqual(updated["status"], "synchronized")
            self.assertEqual(updated["expected_stale_files"], [])
            self.assertEqual(updated["scope_files"], ["x.md"])
            self.assertEqual(updated["english_markers"], {"x.md": ["tension marker"]})
            self.assertEqual(updated["reviewed_source_blobs"], status["reviewed_source_blobs"])

    def test_transition_refuses_stale_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status, manifest = self.make_fixture(root, synchronized_manifest=False)
            updated, errors = transition_to_synchronized(root, status, manifest)
            self.assertIs(updated, status)
            self.assertTrue(any("not synchronized" in error for error in errors))

    def test_transition_refuses_missing_english_semantic_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status, manifest = self.make_fixture(root, synchronized_manifest=True)
            status["english_markers"]["x.md"] = ["marker that is absent"]
            updated, errors = transition_to_synchronized(root, status, manifest)
            self.assertIs(updated, status)
            self.assertTrue(any("missing declared tension marker" in error for error in errors))

    def test_transition_refuses_source_changed_after_semantic_review_even_if_hashes_are_refreshed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status, manifest = self.make_fixture(root, synchronized_manifest=True)
            ja = root / "src/ja-JP/x.md"
            ja.write_text("日本語 changed after review\n", encoding="utf-8")
            refreshed = sha256(ja.read_bytes())
            manifest["files"]["x.md"]["ja_sha256"] = refreshed
            manifest["files"]["x.md"]["en_source_ja_sha256"] = refreshed

            updated, errors = transition_to_synchronized(root, status, manifest)
            self.assertIs(updated, status)
            self.assertTrue(any("changed after bilingual semantic review" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
