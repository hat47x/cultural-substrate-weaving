from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ("interactive", "metered")


class OpenAIAdapterSemanticContractTests(unittest.TestCase):
    def read_profile(self, locale: str, profile: str) -> str:
        return (
            ROOT / "adapters" / "openai-skill" / locale / f"openai.{profile}.yaml"
        ).read_text(encoding="utf-8")

    def default_prompt(self, locale: str, profile: str) -> str:
        for line in self.read_profile(locale, profile).splitlines():
            if line.startswith("  default_prompt: "):
                value = line.removeprefix("  default_prompt: ").strip()
                self.assertGreaterEqual(len(value), 2)
                self.assertEqual(value[0], '"')
                self.assertEqual(value[-1], '"')
                return value[1:-1]
        self.fail(f"default_prompt is missing: {locale}/{profile}")

    def test_default_prompt_preserves_delegated_method_depth(self) -> None:
        for profile in PROFILES:
            ja = self.default_prompt("ja-JP", profile)
            self.assertRegex(ja, r"必要(?:な範囲|に応じ|であれば|な場合)")
            self.assertIn("compatible", ja)
            self.assertIn("親和統合", ja)
            self.assertIn("委任", ja)
            self.assertNotIn("文化的体系とKJ法を使って", ja)

            en = self.default_prompt("en-US", profile)
            en_lower = en.lower()
            self.assertRegex(
                en_lower,
                r"\b(?:where|as|when|if) (?:needed|necessary)\b",
            )
            self.assertIn("compatible", en_lower)
            self.assertIn("affinity-synthesis", en_lower)
            self.assertIn("delegat", en_lower)
            self.assertNotIn(
                "use cultural frameworks and kj to explore and integrate",
                en_lower,
            )

    def test_invocation_profile_does_not_rewrite_default_prompt_semantics(self) -> None:
        for locale in ("ja-JP", "en-US"):
            self.assertEqual(
                self.default_prompt(locale, "interactive"),
                self.default_prompt(locale, "metered"),
            )

    def test_invocation_policy_remains_profile_specific(self) -> None:
        for locale in ("ja-JP", "en-US"):
            self.assertIn(
                "allow_implicit_invocation: true",
                self.read_profile(locale, "interactive"),
            )
            self.assertIn(
                "allow_implicit_invocation: false",
                self.read_profile(locale, "metered"),
            )


if __name__ == "__main__":
    unittest.main()
