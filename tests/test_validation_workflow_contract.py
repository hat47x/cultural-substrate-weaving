from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


class ValidationWorkflowContractTests(unittest.TestCase):
    def test_all_pull_requests_run_release_check(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('[[ "${GITHUB_EVENT_NAME}" == "pull_request" ]]', text)
        self.assertIn("make release-check", text)
        self.assertIn("make check", text)
        self.assertNotIn('"${BASE_REF}" == "main"', text)

    def test_develop_pushes_can_keep_lightweight_check(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('[[ "${GITHUB_REF_NAME}" == release/* ]]', text)
        self.assertIn('[[ "${GITHUB_REF_NAME}" == "main" ]]', text)


if __name__ == "__main__":
    unittest.main()
