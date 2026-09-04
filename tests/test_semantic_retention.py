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

    def test_readmes_do_not_treat_debinding_as_target_evidence(self):
        ja = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")

        self.assertIn("対象側の材料によって独立に支えられた部分だけ", ja)
        self.assertIn("体系の権威から切り離せたことを示すだけ", ja)
        self.assertNotIn("残った構造は、体系ではなく対象に属する", ja)
        self.assertNotIn("生存所見", ja)

        self.assertIn("independently supported by target-side material", en)
        self.assertIn("de-bound from the framework's authority", en)
        self.assertNotIn("What remains belongs to the target", en)
        self.assertNotIn("surviving findings", en)

    def test_usage_context_keeps_research_and_generation_exits_distinct(self):
        ja = (ROOT / "docs" / "ja" / "usage-context.md").read_text(encoding="utf-8")
        en = (ROOT / "docs" / "en" / "usage-context.md").read_text(encoding="utf-8")

        self.assertIn("調査・診断では", ja)
        self.assertIn("生成・構成では", ja)
        self.assertIn("来歴を保った構成資源", ja)
        self.assertNotIn("対象側で仮説を検証する材料がない問題", ja)

        self.assertIn("For research and diagnosis", en)
        self.assertIn("For generation and composition", en)
        self.assertIn("retained with provenance as compositional resources", en)
        self.assertNotIn("tasks without material capable of validating structural hypotheses", en)


if __name__ == "__main__":
    unittest.main()
