from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseLifecycleContractTests(unittest.TestCase):
    def test_makefile_keeps_release_manifest_post_package(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn(
            "build:\n\tpython scripts/build.py\n\trm -f dist/release-manifest.json",
            text,
        )
        self.assertIn("package:\n\tpython scripts/package.py", text)
        self.assertIn("release-check: check package release-validate", text)

    def test_maintainer_guide_describes_manifest_as_post_package_contract(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("post-package release contract", text)
        self.assertIn("make release-check", text)
        self.assertIn("release_assets", text)


if __name__ == "__main__":
    unittest.main()
