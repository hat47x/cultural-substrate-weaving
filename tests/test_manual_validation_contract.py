from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ManualValidationContractTests(unittest.TestCase):
    def test_removed_actions_are_not_runtime_validation_dependencies(self) -> None:
        workflows = ROOT / ".github" / "workflows"
        self.assertFalse((workflows / "validate.yml").exists())
        self.assertFalse((workflows / "release.yml").exists())

    def test_make_check_owns_ordinary_local_validation(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn(
            "check: repository-contracts generated-artifacts-check validate japanese-docs-check test tokens living-lab-check living-lab-summary",
            makefile,
        )
        self.assertIn("repository-contracts:", makefile)
        self.assertIn("scripts/check_branch_version.py", makefile)
        self.assertIn("generated-artifacts-check: build", makefile)
        self.assertIn("scripts/check_generated_artifacts.py", makefile)
        self.assertIn("python -m unittest discover -s tests", makefile)

    def test_living_lab_check_validates_examples_and_public_record_set(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("living-lab-check:", makefile)
        self.assertIn("python scripts/validate_living_lab.py\n", makefile)
        self.assertIn(
            "python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json",
            makefile,
        )

    def test_release_validation_is_explicit_and_layered(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn(".NOTPARALLEL: check release-check", makefile)
        self.assertIn("release-check: check package release-validate", makefile)
        self.assertIn("release-tag-contract: main-contract release-validate", makefile)
        self.assertIn("git merge-base --is-ancestor HEAD origin/main", makefile)
        self.assertIn("scripts/check_release_tag.py", makefile)
        self.assertIn("release-remote-tag-contract: release-validate", makefile)
        self.assertIn("scripts/check_remote_release_tag.py", makefile)

    def test_release_docs_explain_revalidation_before_tag_specific_checks(self) -> None:
        ja_release = (ROOT / "docs" / "ja" / "maintainers" / "release.md").read_text(
            encoding="utf-8"
        )
        en_release = (ROOT / "docs" / "en" / "maintainers" / "release.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("タグ固有の検査に入る前に`release-validate`を再実行", ja_release)
        self.assertIn("リモートタグ固有の検査に入る前にも`release-validate`を再実行", ja_release)
        self.assertIn("reruns `release-validate` before the tag-specific check", en_release)
        self.assertIn("reruns `release-validate` before checking the remote tag", en_release)

    def test_release_docs_list_all_required_reports(self) -> None:
        ja_release = (ROOT / "docs" / "ja" / "maintainers" / "release.md").read_text(
            encoding="utf-8"
        )
        en_release = (ROOT / "docs" / "en" / "maintainers" / "release.md").read_text(
            encoding="utf-8"
        )
        for relative in (
            "reports/validation-report.json",
            "reports/token-budget.json",
            "reports/living-lab-observation-summary.json",
        ):
            expected = f"`dist/{relative}`"
            self.assertIn(expected, ja_release)
            self.assertIn(expected, en_release)

    def test_main_shape_diagnostic_remains_local(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        development = (ROOT / "docs" / "en" / "maintainers" / "development.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("main-contract:", makefile)
        self.assertIn("scripts/check_main_push_contract.py", makefile)
        self.assertIn("GitHub Actions are currently disabled", development)
        self.assertIn("branch protection", development)

    def test_publication_contract_uses_manifest_provenance_and_remote_tag_check(self) -> None:
        release = (ROOT / "docs" / "en" / "maintainers" / "release.md").read_text(
            encoding="utf-8"
        )
        package = (ROOT / "scripts" / "package.py").read_text(encoding="utf-8")
        validator = (ROOT / "scripts" / "validate_release.py").read_text(encoding="utf-8")

        self.assertIn('"schema_version": "2"', package)
        self.assertIn('"source_commit": source_commit', package)
        self.assertIn("git_worktree_changes", package)
        self.assertIn("expected_source_commit", validator)
        self.assertIn("worktree_changes", validator)
        self.assertIn("make release-remote-tag-contract", release)
        self.assertIn("remote tag", release)
        self.assertIn("source_commit", release)


if __name__ == "__main__":
    unittest.main()
