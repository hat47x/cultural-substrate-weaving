from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


class ReleaseMainAncestryTests(unittest.TestCase):
    def git(self, cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=check,
            text=True,
            capture_output=True,
        )

    def test_release_commit_must_be_ancestor_of_main(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.git(repo, "init", "-b", "main")
            self.git(repo, "config", "user.email", "test@example.invalid")
            self.git(repo, "config", "user.name", "test")

            (repo / "file.txt").write_text("main\n", encoding="utf-8")
            self.git(repo, "add", "file.txt")
            self.git(repo, "commit", "-m", "main")
            main_commit = self.git(repo, "rev-parse", "HEAD").stdout.strip()

            self.git(repo, "switch", "-c", "release")
            (repo / "file.txt").write_text("release only\n", encoding="utf-8")
            self.git(repo, "commit", "-am", "release-only")
            release_only = self.git(repo, "rev-parse", "HEAD").stdout.strip()

            accepted = self.git(
                repo,
                "merge-base",
                "--is-ancestor",
                main_commit,
                "main",
                check=False,
            )
            rejected = self.git(
                repo,
                "merge-base",
                "--is-ancestor",
                release_only,
                "main",
                check=False,
            )

            self.assertEqual(accepted.returncode, 0)
            self.assertNotEqual(rejected.returncode, 0)


if __name__ == "__main__":
    unittest.main()
