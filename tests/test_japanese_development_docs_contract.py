from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class JapaneseDevelopmentDocsContractTest(unittest.TestCase):
    def test_repository_instructions_require_separate_natural_japanese_pass(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Japanese development-document drafting", text)
        self.assertIn("Always perform a separate natural-Japanese rewriting pass", text)
        self.assertIn("自然な日本語であることを最優先", text)

    def test_japanese_development_guide_defines_the_drafting_stage(self) -> None:
        text = (ROOT / "docs/ja/maintainers/development.md").read_text(encoding="utf-8")
        self.assertIn("## 日本語の開発文書を作成・更新する場合", text)
        self.assertIn("自然な日本語であることを最優先する独立した推敲工程", text)
        self.assertIn("内容が固まった後、文書全体を日本語として読み直す", text)

    def test_pull_request_template_requires_japanese_prose_review(self) -> None:
        text = (ROOT / ".github/pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("## Japanese development-document prose", text)
        self.assertIn("separate natural-Japanese rewriting pass", text)

    def test_review_record_covers_current_japanese_development_documents(self) -> None:
        review = (ROOT / "docs/ja/maintainers/natural-japanese-review.md").read_text(
            encoding="utf-8"
        )

        required_paths = [
            ROOT / "docs/ja/architecture.md",
            ROOT / ".living-lab/README.md",
            ROOT / "research/living-lab/observations/README.md",
        ]
        required_paths.extend(sorted((ROOT / "docs/ja/maintainers").glob("*.md")))
        required_paths.extend(sorted((ROOT / "docs/ja/experiments").glob("*.md")))

        for path in required_paths:
            if path.name == "natural-japanese-review.md":
                continue
            relative = path.relative_to(ROOT).as_posix()
            self.assertIn(
                f"`{relative}`",
                review,
                msg=f"Japanese development document is not recorded as reviewed: {relative}",
            )


if __name__ == "__main__":
    unittest.main()
