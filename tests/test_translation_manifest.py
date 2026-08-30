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


if __name__ == "__main__":
    unittest.main()
