from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_translation_hashes import reviewed_file_records  # noqa: E402


class TranslationManifestTests(unittest.TestCase):
    def test_english_source_version_matches_version(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads(
            (ROOT / "i18n" / "translation-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["locales"]["en-US"]["source_version"], version)

    def test_translation_manifest_covers_canonical_markdown(self) -> None:
        runtime_manifest = json.loads(
            (ROOT / "src" / "manifest.json").read_text(encoding="utf-8")
        )
        canonical_root = ROOT / "src" / runtime_manifest["canonical_locale"]
        canonical_files = {
            str(path.relative_to(canonical_root))
            for path in canonical_root.rglob("*.md")
        }
        translation_manifest = json.loads(
            (ROOT / "i18n" / "translation-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(translation_manifest["files"]), canonical_files)

    def test_hash_update_records_exact_canonical_file_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_root = root / "ja-JP"
            translated_root = root / "en-US"
            canonical_root.mkdir()
            translated_root.mkdir()
            (canonical_root / "keep.md").write_text("canonical\n", encoding="utf-8")
            (translated_root / "keep.md").write_text("translated\n", encoding="utf-8")
            (translated_root / "removed.md").write_text("stale translation\n", encoding="utf-8")

            records = reviewed_file_records(canonical_root, translated_root)

        self.assertEqual(set(records), {"keep.md"})


if __name__ == "__main__":
    unittest.main()
