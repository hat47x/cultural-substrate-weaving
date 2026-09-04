from __future__ import annotations

import unittest

from scripts.check_release_changelog import check_release_heading


class ReleaseChangelogTests(unittest.TestCase):
    def test_accepts_exact_dated_release_heading(self) -> None:
        check_release_heading(
            "## Unreleased\n\n## 0.4.0 — 2026-08-31\n\n- Released change.\n",
            "0.4.0",
        )

    def test_rejects_missing_release_heading(self) -> None:
        with self.assertRaises(ValueError):
            check_release_heading("## Unreleased\n", "0.4.0")

    def test_rejects_undated_release_heading(self) -> None:
        with self.assertRaises(ValueError):
            check_release_heading("## 0.4.0\n", "0.4.0")

    def test_rejects_invalid_calendar_date(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid calendar date"):
            check_release_heading(
                "## Unreleased\n\n## 0.4.0 — 2026-99-99\n",
                "0.4.0",
            )

    def test_rejects_duplicate_release_heading(self) -> None:
        text = (
            "## Unreleased\n\n"
            "## 0.4.0 — 2026-08-31\n\n"
            "## 0.4.0 — 2026-09-01\n"
        )
        with self.assertRaises(ValueError):
            check_release_heading(text, "0.4.0")

    def test_rejects_frozen_boundary_without_unreleased_heading(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one '## Unreleased'"):
            check_release_heading("## 0.4.0 — 2026-08-31\n", "0.4.0")

    def test_rejects_duplicate_unreleased_heading(self) -> None:
        text = (
            "## Unreleased\n\n"
            "## Unreleased\n\n"
            "## 0.4.0 — 2026-08-31\n"
        )
        with self.assertRaisesRegex(ValueError, "exactly one '## Unreleased'"):
            check_release_heading(text, "0.4.0")

    def test_rejects_release_heading_before_unreleased(self) -> None:
        text = "## 0.4.0 — 2026-08-31\n\n## Unreleased\n"
        with self.assertRaisesRegex(ValueError, "must precede"):
            check_release_heading(text, "0.4.0")

    def test_rejects_stale_unreleased_contents_after_freeze(self) -> None:
        text = (
            "## Unreleased\n\n"
            "- Change that was not moved into the release section.\n\n"
            "## 0.4.0 — 2026-08-31\n\n"
            "- Released change.\n"
        )
        with self.assertRaisesRegex(ValueError, "must be empty"):
            check_release_heading(text, "0.4.0")

    def test_rejects_empty_dated_release_section(self) -> None:
        text = (
            "## Unreleased\n\n"
            "## 0.4.0 — 2026-08-31\n\n"
            "## 0.3.0 — 2026-08-30\n\n"
            "- Earlier change.\n"
        )
        with self.assertRaisesRegex(ValueError, "must contain release contents"):
            check_release_heading(text, "0.4.0")

    def test_unreleased_only_is_valid_development_state_outside_release_gate(self) -> None:
        changelog = "## Unreleased\n\n- Development work continues here.\n"
        self.assertNotIn("## 0.5.0 —", changelog)
        with self.assertRaises(ValueError):
            check_release_heading(changelog, "0.5.0")


if __name__ == "__main__":
    unittest.main()
