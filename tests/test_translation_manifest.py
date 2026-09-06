from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
