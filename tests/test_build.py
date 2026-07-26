from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("ja-JP", "en-US")


class MultilingualBuildTests(unittest.TestCase):
    def test_openai_profiles_exist_for_each_locale(self):
        for locale in LOCALES:
            for profile in ("interactive", "metered"):
                self.assertTrue(
                    (ROOT / f"dist/{locale}/openai-skill/{profile}/cultural-substrate-weaving/SKILL.md").exists()
                )

    def test_locale_source_trees_are_parallel(self):
        ja = {
            str(path.relative_to(ROOT / "src/ja-JP"))
            for path in (ROOT / "src/ja-JP").rglob("*.md")
        }
        en = {
            str(path.relative_to(ROOT / "src/en-US"))
            for path in (ROOT / "src/en-US").rglob("*.md")
        }
        self.assertEqual(ja, en)

    def test_claude_marketplace_contains_both_locales(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {plugin["name"] for plugin in marketplace["plugins"]},
            {"csw-method-ja", "csw-method-en"},
        )

    def test_m365_instruction_limit_for_each_locale(self):
        for locale in LOCALES:
            path = ROOT / f"dist/{locale}/microsoft-copilot/agent-project/appPackage/declarativeAgent.json"
            agent = json.loads(path.read_text(encoding="utf-8"))
            self.assertLessEqual(len(agent["instructions"]), 8000)

    def test_gpt_knowledge_group_count_for_each_locale(self):
        for locale in LOCALES:
            files = list((ROOT / f"dist/{locale}/chatgpt-gpt/knowledge").glob("*.md"))
            self.assertEqual(len(files), 6)

    def test_skill_frontmatter_uses_expected_language_description(self):
        ja = (ROOT / "dist/ja-JP/openai-skill/metered/cultural-substrate-weaving/SKILL.md").read_text(encoding="utf-8")
        en = (ROOT / "dist/en-US/openai-skill/metered/cultural-substrate-weaving/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("汎用AIスキル", ja)
        self.assertIn("general-purpose AI method", en)


if __name__ == "__main__":
    unittest.main()
