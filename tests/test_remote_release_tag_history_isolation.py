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
    validate_remote_release_boundary,
)

FROZEN_CHANGELOG = """# Changelog

## Unreleased

## 1.0.0 — 2026-09-05

- Example release content.
"""


class RemoteReleaseTagHistoryIsolationTests(unittest.TestCase):
    def git(self, cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()

    def test_two_parent_source_commit_outside_remote_main_is_rejected_for_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            remote = root / "remote.git"
            work = root / "work"
            self.git(root, "init", "--bare", str(remote))
            self.git(root, "init", "-b", "main", str(work))
            self.git(work, "config", "user.email", "test@example.invalid")
            self.git(work, "config", "user.name", "test")

            (work / "base.txt").write_text("base\n", encoding="utf-8")
            self.git(work, "add", "base.txt")
            self.git(work, "commit", "-m", "base")
            self.git(work, "push", str(remote), "refs/heads/main")

            self.git(work, "checkout", "-b", "candidate")
            self.git(work, "branch", "candidate-topic")
            (work / "candidate.txt").write_text("candidate\n", encoding="utf-8")
            self.git(work, "add", "candidate.txt")
            self.git(work, "commit", "-m", "candidate main change")

            self.git(work, "checkout", "candidate-topic")
            (work / "topic.txt").write_text("topic\n", encoding="utf-8")
            self.git(work, "add", "topic.txt")
            self.git(work, "commit", "-m", "candidate topic change")

            self.git(work, "checkout", "candidate")
            self.git(work, "merge", "--no-ff", "candidate-topic", "-m", "candidate merge")
            expected = self.git(work, "rev-parse", "HEAD")
            self.assertEqual(len(self.git(work, "show", "-s", "--format=%P", expected).split()), 2)

            self.git(work, "tag", "v1.0.0")
            self.git(work, "push", str(remote), "refs/tags/v1.0.0")

            actual = resolve_remote_tag_commit("v1.0.0", str(remote), work)
            remote_main = resolve_remote_main_commit(str(remote), work)
            self.assertEqual(actual, expected)
            self.assertNotEqual(remote_main, expected)

            errors = validate_remote_release_boundary(
                "v1.0.0",
                "1.0.0",
                expected,
                actual,
                remote_main,
                FROZEN_CHANGELOG,
                work,
            )

            self.assertEqual(len(errors), 1)
            self.assertIn("not present in remote main history", errors[0])
            self.assertNotIn("merge-commit shape", errors[0])
            self.assertNotIn("exactly two parents", errors[0])


if __name__ == "__main__":
    unittest.main()
