from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "affinity-synthesis"
    / "scripts"
    / "affinity_board.py"
)


class AffinityBoardTest(unittest.TestCase):
    def run_board(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BOARD), *args],
            cwd=ROOT,
            check=check,
            text=True,
            capture_output=True,
        )

    def test_explicit_card_group_and_provenance_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board(
                "init",
                str(target),
                "--question",
                "What structure is emerging?",
                "--scope",
                "working notes",
            )
            self.assertEqual(
                self.run_board(
                    "add-source",
                    str(target),
                    "--ref",
                    "notes://001",
                    "--provenance",
                    "target-side notes",
                    "--status",
                    "target_supported",
                ).stdout.strip(),
                "S001",
            )
            self.assertEqual(
                self.run_board(
                    "add-card",
                    str(target),
                    "A concrete observation that should remain inspectable",
                    "--source",
                    "S001",
                    "--status",
                    "target_supported",
                ).stdout.strip(),
                "C001",
            )
            self.assertEqual(
                self.run_board(
                    "add-card",
                    str(target),
                    "A second observation with a different emphasis",
                    "--source",
                    "S001",
                ).stdout.strip(),
                "C002",
            )
            self.assertEqual(
                self.run_board(
                    "add-group",
                    str(target),
                    "--label",
                    "The two observations jointly expose a practical tension",
                    "--member",
                    "C001",
                    "--member",
                    "C002",
                ).stdout.strip(),
                "G001",
            )

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["sources"][0]["input_status"], "target_supported")
            self.assertEqual(data["cards"][0]["id"], "C001")
            self.assertEqual(data["cards"][0]["source_refs"], ["S001"])
            self.assertEqual(data["groups"][0]["members"], ["C001", "C002"])
            self.assertEqual(data["relations"], [])

            status = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(status["ungrouped_cards"], [])
            self.assertEqual(status["validation"]["errors"], [])

    def test_move_card_changes_primary_membership_without_changing_card_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board("add-group", str(target), "--label", "First", "--member", "C001")
            self.run_board("add-group", str(target), "--label", "Second")
            self.run_board("move-card", str(target), "C001", "--to", "G002")

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["cards"][0]["id"], "C001")
            self.assertEqual(data["groups"][0]["members"], [])
            self.assertEqual(data["groups"][1]["members"], ["C001"])

    def test_questionable_connection_stays_question_until_explicit_relation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board("add-card", str(target), "Card B")
            self.run_board(
                "add-question",
                str(target),
                "Do these two cards share a delayed connection?",
                "--between",
                "C001",
                "C002",
                "--state",
                "unresolved",
            )

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["questions"][0]["id"], "Q001")
            self.assertEqual(
                data["questions"][0]["candidate_relation_between"],
                ["C001", "C002"],
            )
            self.assertEqual(data["relations"], [])

            self.run_board(
                "add-relation",
                str(target),
                "--from",
                "C001",
                "--to",
                "C002",
                "--direction",
                "unspecified",
                "--predicate",
                "the source-return check supports a concrete connection",
                "--basis",
                "C001",
                "--basis",
                "C002",
            )
            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["relations"][0]["id"], "R001")

    def test_invalid_reference_is_rejected_without_overwriting_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "add-card",
                str(target),
                "Card with missing source",
                "--source",
                "S999",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source_ref does not resolve", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
