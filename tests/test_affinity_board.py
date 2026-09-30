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
            self.assertEqual(
                status["input_status_counts"]["sources"],
                {"target_supported": 1},
            )
            self.assertEqual(
                status["input_status_counts"]["cards"],
                {"(unspecified)": 1, "target_supported": 1},
            )
            self.assertEqual(status["validation"]["errors"], [])

    def test_group_transformation_audit_is_explicit_and_status_visible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board("add-card", str(target), "Card B")
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "Integrated meaning",
                "--member",
                "C001",
                "--member",
                "C002",
            )

            before = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(
                before["groups_without_transformation_audit"],
                ["G001"],
            )

            self.run_board(
                "audit-group",
                str(target),
                "G001",
                "--inherited",
                "C001 retains the practical constraint",
                "--emergent",
                "the cards together expose a trade-off",
                "--residual",
                "their timing remains different",
                "--preserved-difference",
                "timing remains visibly different",
            )

            data = json.loads(target.read_text(encoding="utf-8"))
            group = data["groups"][0]
            self.assertEqual(
                group["transformation_audit"]["inherited"],
                ["C001 retains the practical constraint"],
            )
            self.assertEqual(
                group["transformation_audit"]["emergent"],
                ["the cards together expose a trade-off"],
            )
            self.assertEqual(
                group["transformation_audit"]["residual"],
                ["their timing remains different"],
            )
            self.assertEqual(
                group["preserved_differences"],
                ["timing remains visibly different"],
            )

            after = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(
                after["groups_without_transformation_audit"],
                [],
            )
            self.assertEqual(after["validation"]["errors"], [])

    def test_preserved_difference_alone_does_not_mark_group_audited(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-group", str(target), "--label", "Group")
            self.run_board(
                "audit-group",
                str(target),
                "G001",
                "--preserved-difference",
                "This difference remains intentionally visible",
            )

            data = json.loads(target.read_text(encoding="utf-8"))
            group = data["groups"][0]
            self.assertEqual(
                group["preserved_differences"],
                ["This difference remains intentionally visible"],
            )
            self.assertNotIn("transformation_audit", group)

            status = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(
                status["groups_without_transformation_audit"],
                ["G001"],
            )

    def test_group_audit_requires_explicit_content_without_overwriting_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-group", str(target), "--label", "Group")
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "audit-group",
                str(target),
                "G001",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "requires at least one transformation audit",
                result.stderr,
            )
            self.assertEqual(target.read_text(encoding="utf-8"), before)

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
                "promote-question",
                str(target),
                "Q001",
                "--direction",
                "unspecified",
                "--predicate",
                "the source-return check supports a concrete connection",
                "--basis",
                "C001",
                "--basis",
                "C002",
                "--state",
                "supported",
            )
            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["relations"][0]["id"], "R001")
            self.assertEqual(data["questions"][0]["state"], "promoted-after-return-check")
            self.assertEqual(data["questions"][0]["handling"], "promoted to R001")

    def test_relation_can_be_weakened_then_reopened_as_question(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board("add-card", str(target), "Card B")
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "First group",
                "--member",
                "C001",
            )
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "Second group",
                "--member",
                "C002",
            )
            self.run_board(
                "add-question",
                str(target),
                "Does G001 constrain G002?",
                "--between",
                "G001",
                "G002",
                "--state",
                "unresolved",
            )
            self.run_board(
                "promote-question",
                str(target),
                "Q001",
                "--direction",
                "directed",
                "--predicate",
                "G001 constrains G002",
                "--basis",
                "C001",
                "--basis",
                "C002",
                "--state",
                "supported",
            )

            self.run_board(
                "revise-relation",
                str(target),
                "R001",
                "--direction",
                "directed",
                "--predicate",
                "G001 may narrow one option visible in G002",
                "--basis",
                "C001",
                "--state",
                "tentative",
                "--note",
                "weakened after return-to-source",
            )
            data = json.loads(target.read_text(encoding="utf-8"))
            relation = data["relations"][0]
            self.assertEqual(relation["from"], "G001")
            self.assertEqual(relation["to"], "G002")
            self.assertEqual(
                relation["predicate"],
                "G001 may narrow one option visible in G002",
            )
            self.assertEqual(relation["basis"], ["C001"])
            self.assertEqual(relation["state"], "tentative")
            self.assertEqual(
                relation["note"],
                "weakened after return-to-source",
            )

            self.assertEqual(
                self.run_board(
                    "demote-relation",
                    str(target),
                    "R001",
                    "Is any defensible relation left between G001 and G002?",
                    "--id",
                    "Q002",
                    "--would-clarify",
                    "C001",
                    "--would-clarify",
                    "C002",
                ).stdout.strip(),
                "Q002",
            )
            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["relations"], [])

            prior_question = next(
                item for item in data["questions"] if item["id"] == "Q001"
            )
            self.assertEqual(
                prior_question["state"],
                "relation-demoted-after-return-check",
            )
            self.assertEqual(
                prior_question["handling"],
                "relation R001 demoted to Q002 after return-check",
            )

            reopened = next(
                item for item in data["questions"] if item["id"] == "Q002"
            )
            self.assertEqual(
                reopened["candidate_relation_between"],
                ["G001", "G002"],
            )
            self.assertEqual(
                reopened["arises_from"],
                ["G001", "G002"],
            )
            self.assertEqual(reopened["state"], "unresolved")
            self.assertEqual(
                reopened["would_clarify_refs"],
                ["C001", "C002"],
            )
            self.assertIn("prior predicate:", reopened["handling"])
            self.assertIn(
                "G001 may narrow one option visible in G002",
                reopened["handling"],
            )

            status = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(status["counts"]["relation"], 0)
            self.assertEqual(status["counts"]["question"], 2)
            self.assertEqual(status["validation"]["errors"], [])

    def test_question_without_candidate_relation_cannot_be_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board(
                "add-question",
                str(target),
                "What should be checked next?",
                "--arises-from",
                "C001",
            )
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "promote-question",
                str(target),
                "Q001",
                "--direction",
                "directed",
                "--predicate",
                "invented relation",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "must declare two candidate_relation_between endpoints",
                result.stderr,
            )
            self.assertEqual(target.read_text(encoding="utf-8"), before)

    def test_narrative_synthesis_keeps_basis_and_transformation_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board("add-card", str(target), "Card A")
            self.run_board("add-card", str(target), "Card B")
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "First integrated meaning",
                "--member",
                "C001",
            )
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "Second integrated meaning",
                "--member",
                "C002",
            )
            self.run_board(
                "add-question",
                str(target),
                "Does G001 constrain G002?",
                "--between",
                "G001",
                "G002",
                "--state",
                "unresolved",
            )
            self.run_board(
                "promote-question",
                str(target),
                "Q001",
                "--direction",
                "directed",
                "--predicate",
                "the return-check supports a constraint from G001 toward G002",
                "--basis",
                "C001",
                "--basis",
                "C002",
                "--state",
                "supported",
            )

            result = self.run_board(
                "add-narrative",
                str(target),
                "G001 constrains G002, while the remaining condition stays unresolved.",
                "--basis",
                "G001",
                "--basis",
                "G002",
                "--basis",
                "R001",
                "--state",
                "draft-after-map-read",
                "--inherited",
                "G001 and G002 remain distinct meanings",
                "--emergent",
                "their supported relation exposes a constraint",
                "--residual",
                "the condition under which the constraint disappears is unresolved",
            )
            self.assertEqual(result.stdout.strip(), "N001")

            data = json.loads(target.read_text(encoding="utf-8"))
            narrative = data["narratives"][0]
            self.assertEqual(narrative["basis"], ["G001", "G002", "R001"])
            self.assertEqual(
                narrative["transformation_audit"]["emergent"],
                ["their supported relation exposes a constraint"],
            )

            status = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(status["counts"]["narrative"], 1)
            self.assertEqual(status["narrative_refs"], ["N001"])
            self.assertEqual(status["validation"]["errors"], [])

    def test_focus_reopens_only_one_hop_semantic_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board(
                "add-source",
                str(target),
                "--ref",
                "notes://focus",
                "--status",
                "target_supported",
            )
            self.run_board(
                "add-card",
                str(target),
                "Card A",
                "--source",
                "S001",
                "--status",
                "target_supported",
            )
            self.run_board("add-card", str(target), "Card B")
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "First meaning",
                "--member",
                "C001",
            )
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "Second meaning",
                "--member",
                "C002",
            )
            self.run_board(
                "add-resonance",
                str(target),
                "--from",
                "C002",
                "--to",
                "G001",
                "--note",
                "C002 constrains G001 without becoming a member",
            )
            self.run_board(
                "add-question",
                str(target),
                "Does G001 constrain G002?",
                "--arises-from",
                "G001",
                "--between",
                "G001",
                "G002",
                "--state",
                "unresolved",
            )
            self.run_board(
                "promote-question",
                str(target),
                "Q001",
                "--direction",
                "directed",
                "--predicate",
                "the return-check supports a constraint",
                "--basis",
                "C001",
                "--basis",
                "C002",
                "--state",
                "supported",
            )
            self.run_board(
                "add-residual",
                str(target),
                "The boundary condition is still unresolved",
                "--ref",
                "G001",
            )
            self.run_board(
                "add-narrative",
                str(target),
                "G001 constrains G002 while a boundary condition remains open.",
                "--basis",
                "G001",
                "--basis",
                "R001",
            )
            self.run_board(
                "update-handoff",
                str(target),
                "--semantic-ref",
                "G001",
                "--residual-ref",
                "U001",
                "--source-ref",
                "S001",
            )
            self.run_board(
                "handoff-add-check",
                str(target),
                "Reinspect G001 only if later material touches the boundary.",
                "--ref",
                "G001",
                "--ref",
                "U001",
                "--status",
                "candidate",
            )

            group_focus = json.loads(
                self.run_board("focus", str(target), "G001").stdout
            )
            self.assertEqual(group_focus["kind"], "group")
            self.assertEqual(group_focus["artifact"]["id"], "G001")
            self.assertEqual(
                [item["id"] for item in group_focus["endpoint_relations"]],
                ["R001"],
            )
            self.assertEqual(
                [item["id"] for item in group_focus["resonances"]],
                ["X001"],
            )
            self.assertEqual(
                [item["id"] for item in group_focus["narratives"]],
                ["N001"],
            )
            self.assertEqual(
                [item["id"] for item in group_focus["residuals"]],
                ["U001"],
            )
            self.assertEqual(
                [item["id"] for item in group_focus["questions"]],
                ["Q001"],
            )
            self.assertTrue(group_focus["handoff"]["semantic_ref"])
            self.assertEqual(
                [
                    item["text"]
                    for item in group_focus["handoff"]["next_check_candidates"]
                ],
                ["Reinspect G001 only if later material touches the boundary."],
            )

            card_focus = json.loads(
                self.run_board("focus", str(target), "C001").stdout
            )
            self.assertEqual(card_focus["member_of_groups"], ["G001"])
            self.assertEqual(card_focus["source_refs"], ["S001"])
            self.assertEqual(
                [item["id"] for item in card_focus["sources"]],
                ["S001"],
            )
            self.assertEqual(
                [item["id"] for item in card_focus["basis_relations"]],
                ["R001"],
            )

            source_focus = json.loads(
                self.run_board("focus", str(target), "S001").stdout
            )
            self.assertEqual(
                [item["id"] for item in source_focus["cards_from_source"]],
                ["C001"],
            )
            self.assertTrue(
                source_focus["handoff"]["source_ref_to_preserve"]
            )

    def test_focus_rejects_ambiguous_imported_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            target.write_text(
                json.dumps(
                    {
                        "format": "affinity-map",
                        "version": "0.1",
                        "sources": [{"id": "C001", "ref": "source with reused id"}],
                        "cards": [{"id": "C001", "text": "card with reused id"}],
                        "groups": [],
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_board(
                "focus",
                str(target),
                "C001",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "semantic ref is ambiguous across namespaces",
                result.stderr,
            )

    def test_narrative_requires_explicit_basis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "add-narrative",
                str(target),
                "A narrative without inspectable map refs must not be added by the board.",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--basis", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), before)

    def test_handoff_capsule_preserves_refs_without_starting_next_round(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            self.run_board(
                "add-source",
                str(target),
                "--ref",
                "notes://001",
            )
            self.run_board(
                "add-card",
                str(target),
                "Card A",
                "--source",
                "S001",
            )
            self.run_board(
                "add-group",
                str(target),
                "--label",
                "Working group",
                "--member",
                "C001",
            )
            self.run_board(
                "add-residual",
                str(target),
                "Difference to preserve",
                "--ref",
                "C001",
            )
            self.run_board(
                "update-handoff",
                str(target),
                "--semantic-ref",
                "G001",
                "--residual-ref",
                "U001",
                "--source-ref",
                "S001",
                "--do-not-assume",
                "U001 implies a supported relation",
            )
            self.run_board(
                "handoff-add-check",
                str(target),
                "Reopen U001 only if new material touches the difference",
                "--ref",
                "U001",
                "--ref",
                "G001",
                "--status",
                "candidate",
            )

            data = json.loads(target.read_text(encoding="utf-8"))
            handoff = data["handoff"]
            self.assertEqual(handoff["semantic_refs"], ["G001"])
            self.assertEqual(handoff["residual_refs"], ["U001"])
            self.assertEqual(handoff["source_refs_to_preserve"], ["S001"])
            self.assertEqual(
                handoff["do_not_assume"],
                ["U001 implies a supported relation"],
            )
            self.assertEqual(
                handoff["next_check_candidates"],
                [
                    {
                        "text": "Reopen U001 only if new material touches the difference",
                        "refs": ["U001", "G001"],
                        "status": "candidate",
                    }
                ],
            )

            status = json.loads(
                self.run_board("status", str(target), "--json").stdout
            )
            self.assertEqual(
                status["handoff"],
                {
                    "present": True,
                    "semantic_refs": 1,
                    "residual_refs": 1,
                    "source_refs_to_preserve": 1,
                    "next_check_candidates": 1,
                    "do_not_assume": 1,
                },
            )
            self.assertEqual(status["validation"]["errors"], [])

    def test_invalid_handoff_ref_is_rejected_without_overwriting_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "update-handoff",
                str(target),
                "--semantic-ref",
                "G999",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "handoff semantic_ref does not resolve locally",
                result.stderr,
            )
            self.assertEqual(target.read_text(encoding="utf-8"), before)

    def test_handoff_update_requires_explicit_field_without_overwriting_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "board.json"
            self.run_board("init", str(target))
            before = target.read_text(encoding="utf-8")
            result = self.run_board(
                "update-handoff",
                str(target),
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "requires at least one handoff field",
                result.stderr,
            )
            self.assertEqual(target.read_text(encoding="utf-8"), before)

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
