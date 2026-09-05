from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleasePrTemplateRemoteTagContractTests(unittest.TestCase):
    def test_public_release_checklist_keeps_remote_tag_gate_independent(self) -> None:
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")

        self.assertIn("revalidates the release set", text)
        self.assertIn("expected two-parent merge-commit shape", text)
        self.assertIn("current remote `main` history", text)
        self.assertIn("frozen CHANGELOG boundary", text)
        self.assertIn("pushed remote tag resolves to that same commit", text)
        self.assertIn("rather than proof of pull-request provenance", text)


if __name__ == "__main__":
    unittest.main()
