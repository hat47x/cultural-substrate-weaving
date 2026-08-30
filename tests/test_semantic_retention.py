from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "evals/semantic-retention.json"


class SemanticRetentionTests(unittest.TestCase):
    def test_file_scoped_rules_cover_the_same_modules_in_each_locale(self):
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        guarded_files = {
            locale: set(rules.get("required_by_file", {}))
            for locale, rules in spec.items()
        }
        first_locale, *other_locales = guarded_files
        for locale in other_locales:
            self.assertEqual(
                guarded_files[first_locale],
                guarded_files[locale],
                f"file-scoped semantic guards differ: {first_locale} vs {locale}",
            )

    def test_required_phrases_stay_in_their_owning_modules(self):
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        for locale, rules in spec.items():
            source_root = ROOT / "src" / locale
            for relative_path, phrases in rules.get("required_by_file", {}).items():
                path = source_root / relative_path
                self.assertTrue(path.exists(), f"missing semantic owner: {locale}/{relative_path}")
                text = path.read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(
                        phrase,
                        text,
                        f"{locale}/{relative_path} lost required semantic: {phrase}",
                    )


if __name__ == "__main__":
    unittest.main()
