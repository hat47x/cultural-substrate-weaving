from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractIntegrationTests(unittest.TestCase):
    def test_make_check_runs_versioned_branch_contract(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn("repository-contracts:", makefile)
        self.assertIn(
            'python scripts/check_branch_version.py --ref "$$(git branch --show-current)"',
            makefile,
        )
        self.assertIn(
            "check: repository-contracts generated-artifacts-check validate",
            makefile,
        )
        self.assertIn("generated-artifacts-check: build", makefile)

    def test_main_contract_is_explicit_and_not_part_of_normal_feature_checks(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertIn("main-contract:", makefile)
        self.assertIn('if [ "$$branch" != "main" ]', makefile)
        self.assertIn(
            'python scripts/check_main_push_contract.py --parents "$$(git show -s --format=%P HEAD)"',
            makefile,
        )

        check_line = next(
            line for line in makefile.splitlines() if line.startswith("check:")
        )
        self.assertNotIn("main-contract", check_line)

    def test_main_contract_description_does_not_claim_pull_request_provenance(self) -> None:
        script = (ROOT / "scripts" / "check_main_push_contract.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("exactly two parents", script)
        self.assertIn("does not prove that", script)
        self.assertIn("GitHub created the commit from a pull request", script)
        self.assertNotIn("merge commit produced by a PR", script)


if __name__ == "__main__":
    unittest.main()
