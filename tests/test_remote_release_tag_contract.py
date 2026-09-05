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
    resolve_remote_tag_commit,
    validate_remote_release_tag,
    validate_remote_tag_commit,
)


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
        (work / "file.txt").write_text("one\n", encoding="utf-8")
        self.git(work, "add", "file.txt")
        self.git(work, "commit", "-m", "first")
        return remote, work

    def test_lightweight_remote_tag_resolves_to_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = self.make_repositories(Path(tmp))
            expected = self.git(work, "rev-parse", "HEAD")
            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            self.assertEqual(actual, expected)
            self.assertEqual(validate_remote_tag_commit(expected, actual), [])
            self.assertEqual(
                validate_remote_release_tag("v1.0.0", "1.0.0", expected, actual),
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
