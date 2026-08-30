from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


class ReleaseWorkflowContractTests(unittest.TestCase):
    def test_publication_uses_validated_manifest_asset_list(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("make release-check", text)
        self.assertIn('manifest["release_assets"]', text)
        self.assertIn('gh release upload "$TAG" "${ASSETS[@]}" --clobber', text)
        self.assertIn('gh release create "$TAG" "${ASSETS[@]}" --generate-notes', text)

        self.assertNotIn("dist/packages/*", text)
        self.assertNotIn("dist/reports/*", text)


if __name__ == "__main__":
    unittest.main()
