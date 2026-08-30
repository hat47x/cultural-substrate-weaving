from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_branch_version import check_branch_version, expected_version  # noqa: E402


class BranchVersionContractTests(unittest.TestCase):
    def test_develop_branch_matches_version(self):
        self.assertEqual(expected_version("develop/v0.4.0"), "0.4.0")
        check_branch_version("develop/v0.4.0", "0.4.0\n")

    def test_release_branch_matches_version(self):
        self.assertEqual(expected_version("release/v1.2.3"), "1.2.3")
        check_branch_version("release/v1.2.3", "1.2.3")

    def test_mismatch_fails_closed(self):
        with self.assertRaisesRegex(
            ValueError,
            r"branch release/v0\.4\.0 expects 0\.4\.0, found 0\.3\.0",
        ):
            check_branch_version("release/v0.4.0", "0.3.0")

    def test_non_versioned_branch_is_not_subject_to_contract(self):
        self.assertIsNone(expected_version("fix/branch-version-contract-tests"))
        check_branch_version("fix/branch-version-contract-tests", "9.9.9")

    def test_malformed_versioned_branch_fails_closed(self):
        with self.assertRaisesRegex(ValueError, r"Malformed version branch"):
            check_branch_version("develop/v0.4", "0.4.0")


if __name__ == "__main__":
    unittest.main()
