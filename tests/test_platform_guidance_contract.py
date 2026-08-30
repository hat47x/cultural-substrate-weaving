from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PlatformGuidanceContractTests(unittest.TestCase):
    def read(self, locale: str, name: str) -> str:
        return (ROOT / "docs" / locale / "platforms" / name).read_text(encoding="utf-8")

    def test_web_search_is_task_dependent_across_platform_guides(self) -> None:
        ja_files = [
            self.read("ja", "chatgpt-gpt.md"),
            self.read("ja", "claude-code.md"),
            self.read("ja", "codex.md"),
            self.read("ja", "microsoft-copilot.md"),
        ]
        en_files = [
            self.read("en", "chatgpt-gpt.md"),
            self.read("en", "claude-code.md"),
            self.read("en", "codex.md"),
            self.read("en", "microsoft-copilot.md"),
        ]

        for text in ja_files:
            self.assertIn("必須ではありません", text)
            self.assertNotIn("Web検索に依存する場面があります", text)
            self.assertNotIn("無効のままでは判断精度が落ちます", text)

        for text in en_files:
            self.assertIn("not required", text.lower())
            self.assertNotIn("relies on web search", text.lower())
            self.assertNotIn("leaving it off reduces judgment quality", text.lower())

    def test_codex_does_not_deprecate_direct_skill_use_without_need(self) -> None:
        ja = self.read("ja", "codex.md")
        en = self.read("en", "codex.md")
        self.assertIn("プラグインとして導入", ja)
        self.assertIn("スキル形式（直接配置）", ja)
        self.assertNotIn("openai/skillsは非推奨", ja)
        self.assertIn("install as a plugin", en.lower())
        self.assertIn("skill format (direct placement)", en.lower())
        self.assertNotIn("standalone skills to plugins in june", en.lower())

    def test_claude_wsl_is_not_blanket_disabled(self) -> None:
        ja = self.read("ja", "claude-code.md")
        en = self.read("en", "claude-code.md")
        self.assertIn("Claude CodeはWSLをサポート", ja)
        self.assertNotIn("WSLセッションではプラグインを利用できません", ja)
        self.assertIn("Claude Code supports WSL", en)
        self.assertNotIn("Plugins aren't available in WSL", en)

    def test_chatgpt_skill_upload_path_matches_plugin_directory_model(self) -> None:
        ja = self.read("ja", "chatgpt-gpt.md")
        en = self.read("en", "chatgpt-gpt.md")
        for text in (ja, en):
            self.assertIn("Skills", text)
            self.assertIn("Plugin Directory", text)
        self.assertIn("パソコンからアップロード", ja)
        self.assertIn("Upload from your computer", en)


if __name__ == "__main__":
    unittest.main()
