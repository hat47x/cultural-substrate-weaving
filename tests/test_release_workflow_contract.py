from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"
VALIDATE_WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
VALIDATION_NOTE = ROOT / ".github" / "release-validation-note.md"


class ReleaseWorkflowContractTests(unittest.TestCase):
    def test_publication_uses_validated_manifest_asset_list(self) -> None:
        text = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("make release-check", text)
        self.assertIn('manifest["release_assets"]', text)
        self.assertIn('gh release upload "$TAG" "${ASSETS[@]}" --clobber', text)
        self.assertIn(
            'gh release create "$TAG" "${ASSETS[@]}" --verify-tag --generate-notes --notes "$NOTES"',
            text,
        )

        self.assertNotIn("dist/packages/*", text)
        self.assertNotIn("dist/reports/*", text)

    def test_new_release_prepends_validation_stage_disclosure(self) -> None:
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        note = VALIDATION_NOTE.read_text(encoding="utf-8")
        self.assertIn("release-validation-note.md", workflow)
        self.assertIn("--verify-tag", workflow)
        self.assertIn("still under validation", note)
        self.assertIn("有効性が確立したとは扱いません", note)
        self.assertIn("Technical release checks", note)

    def test_publication_requires_main_ancestry(self) -> None:
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn("Verify release commit is on main", workflow)
        self.assertIn("git fetch --no-tags origin main", workflow)
        self.assertIn("git merge-base --is-ancestor HEAD origin/main", workflow)

    def test_publication_requires_dated_changelog_boundary(self) -> None:
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Verify changelog release boundary", workflow)
        self.assertIn("scripts/check_release_changelog.py", workflow)
        self.assertIn('--version "$(cat VERSION)"', workflow)
        self.assertIn("--changelog CHANGELOG.md", workflow)

    def test_publication_verifies_remote_asset_set_and_digests(self) -> None:
        workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Verify published release assets", workflow)
        self.assertIn('gh api "repos/${GITHUB_REPOSITORY}/releases/tags/${TAG}"', workflow)
        self.assertIn("scripts/verify_published_release.py", workflow)
        self.assertIn("--manifest dist/release-manifest.json", workflow)
        self.assertIn('--tag "$TAG"', workflow)

    def test_release_candidate_validation_persists_final_manifest(self) -> None:
        text = VALIDATE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("name: release-candidate-manifest", text)
        self.assertIn("path: dist/release-manifest.json", text)
        self.assertIn("if-no-files-found: ignore", text)


if __name__ == "__main__":
    unittest.main()
