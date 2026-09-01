from __future__ import annotations

import unittest

from scripts.check_main_push_contract import MainPushContractError, check_main_push_parents, parent_shas


class MainPushContractTests(unittest.TestCase):
    def test_accepts_two_parent_merge_commit(self) -> None:
        check_main_push_parents("a" * 40 + " " + "b" * 40)

    def test_accepts_merge_commit_with_more_than_two_parents(self) -> None:
        check_main_push_parents("a b c")

    def test_rejects_single_parent_direct_push(self) -> None:
        with self.assertRaises(MainPushContractError):
            check_main_push_parents("a" * 40)

    def test_rejects_missing_parent_information(self) -> None:
        with self.assertRaises(MainPushContractError):
            check_main_push_parents("")

    def test_parent_parser_ignores_extra_whitespace(self) -> None:
        self.assertEqual(parent_shas("  a   b\n"), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
