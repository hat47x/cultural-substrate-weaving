from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "activation-cases.json"


class ActivationFixtureSemanticContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    def case(self, locale: str, case_id: str) -> dict:
        matches = [item for item in self.cases[locale] if item.get("id") == case_id]
        self.assertEqual(1, len(matches), f"missing or duplicated activation case: {locale}/{case_id}")
        return matches[0]

    def test_split_ownership_cases_have_locale_parity(self) -> None:
        semantic_ids = {
            "explicit-limited": "limited",
            "affinity-only-no-csw": "no_activation",
            "explicit-exploratory": "exploratory",
        }
        for suffix, expected in semantic_ids.items():
            ja = self.case("ja-JP", f"ja-{suffix}")
            en = self.case("en-US", f"en-{suffix}")
            self.assertEqual(expected, ja.get("expected"))
            self.assertEqual(expected, en.get("expected"))

    def test_limited_use_delegates_one_round_affinity_synthesis(self) -> None:
        for locale, case_id in (
            ("ja-JP", "ja-explicit-limited"),
            ("en-US", "en-explicit-limited"),
        ):
            item = self.case(locale, case_id)
            text = f"{item.get('request', '')}\n{item.get('reason', '')}"
            self.assertIn("affinity-synthesis", text)
            self.assertIn("compatible realization", text)

    def test_affinity_only_case_does_not_activate_csw(self) -> None:
        ja = self.case("ja-JP", "ja-affinity-only-no-csw")
        en = self.case("en-US", "en-affinity-only-no-csw")

        self.assertEqual("no_activation", ja.get("expected"))
        self.assertIn("affinity-synthesis", ja.get("request", ""))
        self.assertIn("CSWと文化体系は使わない", ja.get("request", ""))

        self.assertEqual("no_activation", en.get("expected"))
        self.assertIn("affinity-synthesis", en.get("request", ""))
        self.assertIn("Do not use CSW or a cultural framework", en.get("request", ""))

    def test_exploratory_use_keeps_affinity_synthesis_outside_csw(self) -> None:
        for locale, case_id in (
            ("ja-JP", "ja-explicit-exploratory"),
            ("en-US", "en-explicit-exploratory"),
        ):
            item = self.case(locale, case_id)
            request = item.get("request", "")
            self.assertIn("affinity-synthesis", request)
            self.assertIn("compatible realization", request)


if __name__ == "__main__":
    unittest.main()
