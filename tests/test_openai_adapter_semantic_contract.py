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
            self.assertIn("必要な範囲で", ja)
            self.assertIn("compatibleな親和統合への接続", ja)
            self.assertIn("その委任に従ってください", ja)
            self.assertNotIn("文化的体系とKJ法を使って", ja)

            en = self.default_prompt("en-US", profile)
            self.assertIn("where needed", en)
            self.assertIn("compatible affinity synthesis", en)
            self.assertIn("Follow that delegation", en)
            self.assertNotIn("use cultural frameworks and KJ to explore and integrate", en)

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
