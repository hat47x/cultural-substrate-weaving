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

    def test_after_upload_checklist_reruns_remote_tag_gate_before_release_verifier(self) -> None:
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        after_upload = next(
            line for line in text.splitlines() if line.startswith("- [ ] After upload,")
        )

        self.assertIn('make release-remote-tag-contract TAG="$TAG"', after_upload)
        self.assertIn("current remote `main` history", after_upload)
        self.assertIn("expected two-parent merge-commit shape", after_upload)
        self.assertIn("frozen CHANGELOG boundary", after_upload)
        self.assertIn("scripts/verify_published_release.py", after_upload)
        self.assertLess(
            after_upload.index("make release-remote-tag-contract"),
            after_upload.index("scripts/verify_published_release.py"),
        )


if __name__ == "__main__":
    unittest.main()
