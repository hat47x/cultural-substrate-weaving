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

from check_generated_artifacts import generated_artifact_changes  # noqa: E402


class GeneratedArtifactFreshnessTests(unittest.TestCase):
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
        for relative in (
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
            "plugins/example/README.md",
            "source.txt",
        ):
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{relative}\n", encoding="utf-8")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "initial")
        return repo

    def test_clean_generated_artifacts_have_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            self.assertEqual(generated_artifact_changes(repo), [])

    def test_tracked_generated_change_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            path = repo / "plugins/example/README.md"
            path.write_text("changed\n", encoding="utf-8")
            self.assertTrue(any("plugins/example/README.md" in line for line in generated_artifact_changes(repo)))

    def test_deleted_generated_file_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            (repo / ".claude-plugin/marketplace.json").unlink()
            self.assertTrue(any(".claude-plugin/marketplace.json" in line for line in generated_artifact_changes(repo)))

    def test_untracked_generated_file_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            path = repo / ".agents/plugins/new.json"
            path.write_text("{}\n", encoding="utf-8")
            self.assertTrue(any("?? .agents/plugins/new.json" in line for line in generated_artifact_changes(repo)))

    def test_unrelated_worktree_change_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repository(Path(tmp))
            (repo / "source.txt").write_text("changed\n", encoding="utf-8")
            self.assertEqual(generated_artifact_changes(repo), [])


if __name__ == "__main__":
    unittest.main()
