from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate import check_projected_reference, check_skill_entry_budget  # noqa: E402


class GenericSkillValidationHelperTests(unittest.TestCase):
    def test_projected_reference_accepts_byte_identical_content(self) -> None:
        source = ROOT / "src" / "ja-JP" / "core" / "activation.md"
        errors: list[str] = []

        check_projected_reference(
            errors,
            source=source,
            generated=source,
            source_label="ja-JP/core/activation.md",
        )

        self.assertEqual(errors, [])

    def test_projected_reference_reports_missing_generated_path(self) -> None:
        source = ROOT / "src" / "ja-JP" / "core" / "activation.md"
        generated = ROOT / "dist" / "DOES-NOT-EXIST" / "references" / "activation.md"
        errors: list[str] = []

        check_projected_reference(
            errors,
            source=source,
            generated=generated,
            source_label="ja-JP/core/activation.md",
        )

        self.assertEqual(
            errors,
            [
                "Missing generated reference: "
                "dist/DOES-NOT-EXIST/references/activation.md"
            ],
        )

    def test_projected_reference_reports_source_mismatch(self) -> None:
        source = ROOT / "src" / "ja-JP" / "core" / "activation.md"
        generated = ROOT / "src" / "ja-JP" / "ROUTER.md"
        errors: list[str] = []

        check_projected_reference(
            errors,
            source=source,
            generated=generated,
            source_label="ja-JP/core/activation.md",
        )

        self.assertEqual(
            errors,
            ["Generated reference differs from ja-JP/core/activation.md"],
        )

    def test_skill_entry_budget_returns_size_without_error_when_within_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_md = Path(temp_dir) / "SKILL.md"
            skill_md.write_bytes(b"12345")
            errors: list[str] = []

            size = check_skill_entry_budget(
                errors,
                skill_md=skill_md,
                max_bytes=5,
                label="example Skill SKILL.md",
            )

            self.assertEqual(size, 5)
            self.assertEqual(errors, [])

    def test_skill_entry_budget_reports_label_and_size_when_over_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_md = Path(temp_dir) / "SKILL.md"
            skill_md.write_bytes(b"123456")
            errors: list[str] = []

            size = check_skill_entry_budget(
                errors,
                skill_md=skill_md,
                max_bytes=5,
                label="example Skill SKILL.md",
            )

            self.assertEqual(size, 6)
            self.assertEqual(
                errors,
                ["example Skill SKILL.md exceeds budget: 6"],
            )


if __name__ == "__main__":
    unittest.main()
