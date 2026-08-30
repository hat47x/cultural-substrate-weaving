from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseLifecycleContractTests(unittest.TestCase):
    def test_release_manifest_is_owned_only_by_packaging(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build.py").read_text(encoding="utf-8")
        package = (ROOT / "scripts" / "package.py").read_text(encoding="utf-8")

        self.assertIn("build:\n\tpython scripts/build.py", makefile)
        self.assertNotIn("rm -f dist/release-manifest.json", makefile)
        self.assertNotIn("release-manifest.json", build)
        self.assertNotIn("write_release_manifest", build)

        self.assertIn('DIST / "release-manifest.json"', package)
        self.assertIn('"schema_version": "1"', package)
        self.assertIn('"release_assets": release_assets', package)
        self.assertIn("release-check: check package release-validate", makefile)

    def test_maintainer_guide_describes_manifest_as_post_package_contract(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("post-package release contract", text)
        self.assertIn("make release-check", text)
        self.assertIn("release_assets", text)
        self.assertNotIn("older build-script manifest-writing step", text)

    def test_maintainer_guide_preserves_validation_disclosure_boundary(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("Publication disclosure", text)
        self.assertIn(".github/release-validation-note.md", text)
        self.assertIn("gh release create --verify-tag", text)
        self.assertIn("technically green release candidate is not evidence", text)
        self.assertIn("does not rewrite the release notes", text)

    def test_maintainer_guide_requires_changelog_freeze_only_for_publication(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("release candidate may keep its pending changes under `## Unreleased`", text)
        self.assertIn("## X.Y.Z — YYYY-MM-DD", text)
        self.assertIn("Release workflow checks the dated version heading", text)
        self.assertIn("finalize `CHANGELOG.md`", text)

    def test_release_history_distinguishes_validated_from_published(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release-history.md").read_text(encoding="utf-8")
        self.assertIn("validated and merged to `main`, but never published", text)
        self.assertIn("No `v0.3.0` tag was created", text)
        self.assertIn("No GitHub Release `v0.3.0` was published", text)
        self.assertIn("superseded by the v0.4.0 release line", text)
        self.assertIn("validated version boundary", text)
        self.assertIn("published release", text)
        self.assertIn("Do not infer state 3 from state 2", text)


if __name__ == "__main__":
    unittest.main()
