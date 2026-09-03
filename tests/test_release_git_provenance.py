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

from common import git_head, git_worktree_changes  # noqa: E402


class ReleaseGitProvenanceTests(unittest.TestCase):
    def git(self, cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()

    def make_repository(self, root: Path) -> Path:
        repo = root / "repo"
        self.git(root, "init", "-b", "main", str(repo))
        self.git(repo, "config", "user.email", "test@example.invalid")
        self.git(repo, "config", "user.name", "test")
        (repo / "file.txt").write_text("one\n", encoding="utf-8")
        self.git(repo, "add", "file.txt")
        self.git(repo, "commit", "-m", "first")
        return repo

    def test_clean_repository_reports_head_and_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            self.assertEqual(git_head(repo), self.git(repo, "rev-parse", "HEAD"))
            self.assertEqual(git_worktree_changes(repo), "")

    def test_tracked_change_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            (repo / "file.txt").write_text("two\n", encoding="utf-8")
            changes = git_worktree_changes(repo)
            self.assertIn("file.txt", changes)

    def test_untracked_change_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            (repo / "new.txt").write_text("new\n", encoding="utf-8")
            changes = git_worktree_changes(repo)
            self.assertIn("?? new.txt", changes)


if __name__ == "__main__":
    unittest.main()
