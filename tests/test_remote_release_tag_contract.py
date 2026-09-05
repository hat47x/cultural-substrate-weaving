from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_remote_release_tag import (  # noqa: E402
    resolve_remote_main_commit,
    resolve_remote_tag_commit,
    validate_remote_main_history,
    validate_remote_release_boundary,
    validate_remote_release_tag,
    validate_remote_tag_commit,
)

FROZEN_CHANGELOG = """# Changelog

## Unreleased

## 1.0.0 — 2026-09-05

- Example release content.
"""
UNFROZEN_CHANGELOG = """# Changelog

## Unreleased

- Example release content.
"""


class RemoteReleaseTagContractTests(unittest.TestCase):
    def git(self, cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()

    def make_repositories(self, root: Path) -> tuple[Path, Path]:
        remote = root / "remote.git"
        work = root / "work"
        self.git(root, "init", "--bare", str(remote))
        self.git(root, "init", "-b", "main", str(work))
        self.git(work, "config", "user.email", "test@example.invalid")
        self.git(work, "config", "user.name", "test")

        (work / "file.txt").write_text("base\n", encoding="utf-8")
        self.git(work, "add", "file.txt")
        self.git(work, "commit", "-m", "base")
        self.git(work, "branch", "topic")

        (work / "file.txt").write_text("main\n", encoding="utf-8")
        self.git(work, "commit", "-am", "main change")

        self.git(work, "checkout", "topic")
        (work / "topic.txt").write_text("topic\n", encoding="utf-8")
        self.git(work, "add", "topic.txt")
        self.git(work, "commit", "-m", "topic change")

        self.git(work, "checkout", "main")
        self.git(work, "merge", "--no-ff", "topic", "-m", "release merge")
        self.git(work, "push", str(remote), "refs/heads/main")
        return remote, work

    def test_lightweight_remote_tag_resolves_to_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            remote_main = resolve_remote_main_commit(str(remote), work)
            self.assertEqual(actual, expected)
            self.assertEqual(remote_main, expected)
            self.assertEqual(validate_remote_tag_commit(expected, actual), [])
            self.assertEqual(validate_remote_main_history(expected, remote_main, work), [])
            self.assertEqual(
                validate_remote_release_boundary(
                    "v1.0.0",
                    "1.0.0",
                    expected,
                    actual,
                    remote_main,
                    FROZEN_CHANGELOG,
                    work,
                ),
                [],
            )

    def test_annotated_remote_tag_is_peeled_to_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "-a", "v1.0.0", "-m", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            self.assertEqual(actual, expected)

    def test_same_commit_wrong_version_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.1")
            self.git(work, "push", str(remote), "refs/tags/v1.0.1")

            actual = resolve_remote_tag_commit("v1.0.1", str(remote), work)
            errors = validate_remote_release_tag("v1.0.1", "1.0.0", expected, actual)
            self.assertTrue(any("release tag mismatch" in error for error in errors))

    def test_single_parent_source_commit_on_remote_main_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            (work / "direct.txt").write_text("direct\n", encoding="utf-8")
            self.git(work, "add", "direct.txt")
            self.git(work, "commit", "-m", "direct main commit")
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "push", str(remote), "refs/heads/main")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            remote_main = resolve_remote_main_commit(str(remote), work)
            errors = validate_remote_release_boundary(
                "v1.0.0",
                "1.0.0",
                expected,
                actual,
                remote_main,
                FROZEN_CHANGELOG,
                work,
            )
            self.assertTrue(any("exactly two parents" in error for error in errors))

    def test_source_commit_not_in_remote_main_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            (work / "file.txt").write_text("two\n", encoding="utf-8")
            self.git(work, "commit", "-am", "second")
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            remote_main = resolve_remote_main_commit(str(remote), work)
            errors = validate_remote_release_boundary(
                "v1.0.0",
                "1.0.0",
                expected,
                actual,
                remote_main,
                FROZEN_CHANGELOG,
                work,
            )
            self.assertTrue(
                any("not present in remote main history" in error for error in errors)
            )

    def test_unfrozen_changelog_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            remote_main = resolve_remote_main_commit(str(remote), work)
            errors = validate_remote_release_boundary(
                "v1.0.0",
                "1.0.0",
                expected,
                actual,
                remote_main,
                UNFROZEN_CHANGELOG,
                work,
            )
            self.assertTrue(
                any("CHANGELOG release boundary missing" in error for error in errors)
            )

    def test_moved_remote_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            (work / "file.txt").write_text("two\n", encoding="utf-8")
            self.git(work, "commit", "-am", "second")
            self.git(work, "tag", "-f", "v1.0.0")
            self.git(work, "push", "--force", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            errors = validate_remote_tag_commit(expected, actual)
            self.assertTrue(any("remote release tag commit mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
