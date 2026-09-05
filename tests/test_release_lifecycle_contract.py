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
        self.assertIn('"schema_version": "2"', package)
        self.assertIn('"source_commit": source_commit', package)
        self.assertIn("clean Git worktree", package)
        self.assertIn('"release_assets": release_assets', package)
        self.assertIn("release-check: check package release-validate", makefile)
        self.assertIn("release-tag-contract:", makefile)
        self.assertIn('python scripts/check_release_tag.py --tag "$(TAG)"', makefile)
        self.assertIn("release-remote-tag-contract:", makefile)
        self.assertIn('python scripts/check_remote_release_tag.py --tag "$(TAG)"', makefile)

    def test_release_validator_uses_current_publication_and_provenance_contracts(self) -> None:
        text = (ROOT / "scripts" / "validate_release.py").read_text(encoding="utf-8")
        self.assertIn("release publication boundary", text)
        self.assertIn("clean Git worktree", text)
        self.assertIn("source_commit", text)
        self.assertNotIn("files published by the release workflow", text)

    def test_release_internals_describe_manifest_as_post_package_contract(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("post-package release contract", text)
        self.assertIn("make release-check", text)
        self.assertIn("make release-tag-contract", text)
        self.assertIn("bound to the public `main` commit", text)
        self.assertIn("refreshes `origin/main` from the remote", text)
        self.assertIn("present in that current remote history", text)
        self.assertIn("reruns the full `release-validate` contract", text)
        self.assertIn("clean Git worktree", text)
        self.assertIn("release_assets", text)
        self.assertIn("GitHub Actions are currently disabled", text)
        self.assertNotIn("The GitHub Release workflow", text)

    def test_release_internals_preserve_validation_disclosure_boundary(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("Publication disclosure", text)
        self.assertIn(".github/release-validation-note.md", text)
        self.assertIn("verified again from the published Release object", text)
        self.assertIn("gh release create --verify-tag", text)
        self.assertIn("not evidence that the method is empirically effective", text)
        self.assertIn("edit the notes deliberately", text)

    def test_release_validation_note_distinguishes_observation_modes(self) -> None:
        text = (ROOT / ".github" / "release-validation-note.md").read_text(encoding="utf-8")
        self.assertIn("prospective observations", text)
        self.assertIn("retrospective records", text)
        self.assertIn("prospectiveな観測", text)
        self.assertIn("retrospectiveな記録", text)
        self.assertIn("effectiveness of cultural-substrate-weaving is not treated as established", text)
        self.assertIn("cultural-substrate-weavingの有効性が確立したとは扱いません", text)

    def test_publication_requires_explicit_changelog_main_history_and_tag_gates(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("## X.Y.Z — YYYY-MM-DD", text)
        self.assertIn("leave it empty until publication is complete", text)
        self.assertIn("dated release section itself must contain release contents", text)
        self.assertIn("scripts/check_release_changelog.py", text)
        self.assertIn("make main-contract", text)
        self.assertIn("exactly two parents", text)
        self.assertIn("does not prove pull-request provenance", text)
        self.assertIn("git merge-base --is-ancestor HEAD origin/main", text)
        self.assertIn("fails closed on those publication prerequisites itself", text)
        self.assertIn("refreshes `origin/main` from the remote", text)
        self.assertIn("rechecks that HEAD is in that current remote history", text)
        self.assertIn('TAG="v$(cat VERSION)"', text)
        self.assertIn("make release-tag-contract", text)
        self.assertIn("make release-remote-tag-contract", text)
        self.assertIn("source_commit", text)
        self.assertIn("exact `main` commit", text)
        self.assertNotIn("Release workflow checks the dated version heading", text)

    def test_release_pr_template_keeps_changelog_publication_boundary_explicit(self) -> None:
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("exactly one empty `## Unreleased` section", text)
        self.assertIn("non-empty dated `## X.Y.Z — YYYY-MM-DD` section", text)
        self.assertIn("scripts/check_release_changelog.py", text)
        self.assertIn("before the final candidate `make release-check`", text)

    def test_release_pr_template_allows_develop_or_optional_release_branch_to_main(self) -> None:
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("a public release targets `main` from `develop/vX.Y.Z`", text)
        self.assertIn("when intentionally used, `release/vX.Y.Z`", text)

    def test_release_pr_template_keeps_post_publication_verification_explicit(self) -> None:
        text = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("reruns the full `release-validate` contract", text)
        self.assertIn("revalidates the release set", text)
        self.assertIn("scripts/verify_published_release.py", text)
        self.assertIn("non-draft, non-prerelease Release", text)
        self.assertIn(".github/release-validation-note.md", text)
        self.assertIn("exact manifest-declared asset names, sizes, and digests", text)

    def test_localized_release_procedures_keep_the_same_publication_gates(self) -> None:
        ja = (ROOT / "docs" / "ja" / "maintainers" / "release.md").read_text(encoding="utf-8")
        en = (ROOT / "docs" / "en" / "maintainers" / "release.md").read_text(encoding="utf-8")

        for text in (ja, en):
            self.assertIn("scripts/check_release_changelog.py", text)
            self.assertIn("git merge-base --is-ancestor HEAD origin/main", text)
            self.assertIn("make main-contract", text)
            self.assertIn("make release-check", text)
            self.assertIn("make release-tag-contract", text)
            self.assertIn("make release-remote-tag-contract", text)
            self.assertIn("scripts/verify_published_release.py", text)
            self.assertIn(".github/release-validation-note.md", text)
            self.assertIn('TAG="v$(cat VERSION)"', text)
            self.assertIn("source_commit", text)
            self.assertIn("release_assets", text)

        self.assertIn("未コミットの変更がない状態", ja)
        self.assertIn("ちょうど2つの親", ja)
        self.assertIn("GitHubのPRから生成されたことまでは証明できません", ja)
        self.assertIn("origin/main`をリモートから更新", ja)
        self.assertIn("タグ固有の検査に入る前に`release-validate`を再実行", ja)
        self.assertIn("リモートタグ名と最終manifestの版が一致", ja)
        self.assertIn("日付付きの節そのものも空にはせず", ja)
        self.assertIn("Releaseがdraftやprereleaseではなく", ja)
        self.assertIn("リモートタグが最終的に指すコミット", ja)
        self.assertIn("GitHub Actionsは現在リポジトリで無効化されています", ja)
        self.assertIn("clean Git worktree", en)
        self.assertIn("exactly two parents", en)
        self.assertIn("do not prove that GitHub created the commit from a pull request", en)
        self.assertIn("refreshes `origin/main` from the remote", en)
        self.assertIn("reruns `release-validate` before the tag-specific check", en)
        self.assertIn("remote tag name matches the final manifest version", en)
        self.assertIn("dated release section itself must contain release content", en)
        self.assertIn("non-draft, non-prerelease Release", en)
        self.assertIn("GitHub Actions are currently disabled", en)

    def test_remote_release_verification_remains_a_manual_publication_gate(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release.md").read_text(encoding="utf-8")
        self.assertIn("scripts/verify_published_release.py", text)
        self.assertIn("supplied remote tag name to match the final manifest version", text)
        self.assertIn("supplied tag to match the final manifest version", text)
        self.assertIn("neither a draft nor a prerelease", text)
        self.assertIn("required `.github/release-validation-note.md` disclosure", text)
        self.assertIn("remote tag", text)
        self.assertIn("source_commit", text)
        self.assertIn("published asset-name set", text)
        self.assertIn("sha256:", text)
        self.assertIn("publish exactly the files listed by `release_assets`", text)

    def test_docs_index_separates_procedures_from_shared_internals(self) -> None:
        text = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        self.assertIn("ja/maintainers/release.md", text)
        self.assertIn("en/maintainers/release.md", text)
        self.assertIn("Release internals", text)

    def test_release_history_distinguishes_validated_from_published(self) -> None:
        text = (ROOT / "docs" / "maintainers" / "release-history.md").read_text(encoding="utf-8")
        self.assertIn("validated and merged to `main`, but never published", text)
        self.assertIn("No `v0.3.0` tag was created", text)
        self.assertIn("No GitHub Release `v0.3.0` was published", text)
        self.assertIn("superseded by the v0.4.0 release line", text)
        self.assertIn("validated version boundary", text)
        self.assertIn("published release", text)
        self.assertIn("Do not infer state 3 from state 2", text)

        interpretation = text.split("## Interpretation", 1)[1]
        self.assertIn("post-publication verification", interpretation)
        self.assertIn("not on one particular automation mechanism", interpretation)
        self.assertNotIn("publication workflow has completed", interpretation)


if __name__ == "__main__":
    unittest.main()
