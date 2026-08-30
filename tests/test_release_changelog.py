from __future__ import annotations

import unittest

from scripts.check_release_changelog import check_release_heading


class ReleaseChangelogTests(unittest.TestCase):
    def test_accepts_exact_dated_release_heading(self) -> None:
        check_release_heading("## Unreleased\n\n## 0.4.0 — 2026-08-31\n", "0.4.0")

    def test_rejects_missing_release_heading(self) -> None:
        with self.assertRaises(ValueError):
            check_release_heading("## Unreleased\n", "0.4.0")

    def test_rejects_undated_release_heading(self) -> None:
        with self.assertRaises(ValueError):
            check_release_heading("## 0.4.0\n", "0.4.0")

    def test_rejects_duplicate_release_heading(self) -> None:
        text = "## 0.4.0 — 2026-08-31\n\n## 0.4.0 — 2026-09-01\n"
        with self.assertRaises(ValueError):
            check_release_heading(text, "0.4.0")


if __name__ == "__main__":
    unittest.main()
