from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from edit_map import (  # noqa: E402
    add_card,
    add_group,
    add_question,
    add_resonance,
    add_source,
    move_card,
    promote_question,
    write_map,
)
from validate_map import validate  # noqa: E402


class ResearchAffinityMapEditorTests(unittest.TestCase):
    def fixture(self) -> dict:
        return {
            "format": "affinity-map",
            "version": "0.1",
            "sources": [
                {"id": "S01", "ref": "source A"},
                {"id": "S02", "ref": "source B"},
            ],
            "cards": [
                {"id": "C001", "text": "first card", "source_refs": ["S01"]},
                {"id": "C002", "text": "second card", "source_refs": ["S02"]},
                {"id": "C003", "text": "third card", "source_refs": ["S02"]},
            ],
            "groups": [
                {"id": "G01", "label": "first group", "members": ["C001", "C002"]},
                {"id": "G02", "label": "second group", "members": ["C003"]},
            ],
            "resonances": [],
            "relations": [],
            "questions": [],
        }

    def assert_valid(self, data: dict) -> None:
        errors, _warnings = validate(data)
        self.assertEqual(errors, [])

    def test_add_source_and_card_are_explicit_and_traceable(self) -> None:
        data, warnings = add_source(
            self.fixture(),
            source_id="S03",
            ref="source C",
            provenance="direct interview note",
            discovery_route="follow-up",
        )
        self.assertEqual(warnings, [])

        data, warnings = add_card(
            data,
            card_id="C004",
            text="new material remains separate until grouping is justified",
            source_refs=["S03"],
            preservation_note="retain uncertainty",
        )
        self.assertEqual(warnings, [])
        self.assertEqual(data["cards"][-1]["source_refs"], ["S03"])
        self.assertNotIn("C004", {
            member
            for group in data["groups"]
            for member in group["members"]
        })
        self.assert_valid(data)

    def test_add_group_rejects_unresolved_member(self) -> None:
        with self.assertRaisesRegex(ValueError, "member does not resolve"):
            add_group(
                self.fixture(),
                group_id="G03",
                label="new group",
                members=["C404"],
            )

    def test_move_card_replaces_primary_membership_without_creating_resonance(self) -> None:
        data = self.fixture()
        data["groups"][1]["members"].append("C001")

        moved, warnings = move_card(data, card_id="C001", to_group="G02")
        self.assertEqual(warnings, [])
        self.assertNotIn("C001", moved["groups"][0]["members"])
        self.assertEqual(moved["groups"][1]["members"].count("C001"), 1)
        self.assertEqual(moved["resonances"], [])
        self.assert_valid(moved)

    def test_resonance_is_distinct_from_membership(self) -> None:
        data, warnings = add_resonance(
            self.fixture(),
            resonance_id="X01",
            source="C003",
            target_group="G01",
            note="C003 constrains G01 without becoming its member",
        )
        self.assertEqual(warnings, [])
        self.assertEqual(data["resonances"][0]["from"], "C003")
        self.assertNotIn("C003", data["groups"][0]["members"])
        self.assert_valid(data)

        with self.assertRaisesRegex(
            ValueError,
            "secondary resonance must not duplicate direct group membership",
        ):
            add_resonance(
                self.fixture(),
                resonance_id="X02",
                source="C001",
                target_group="G01",
                note="must be rejected",
            )

    def test_question_candidate_can_be_promoted_only_explicitly(self) -> None:
        data, warnings = add_question(
            self.fixture(),
            question_id="Q01",
            text="Does G01 constrain G02 under the observed condition?",
            arises_from=["G01", "G02"],
            candidate_relation_between=["G01", "G02"],
            would_clarify_refs=["C001", "C003"],
            state="unresolved",
        )
        self.assertEqual(warnings, [])
        self.assertEqual(data["relations"], [])

        promoted, warnings = promote_question(
            data,
            question_id="Q01",
            relation_id="R01",
            predicate="G01 constrains G02 under the observed condition",
            direction="directed",
            basis=["C001", "C003"],
            state="supported",
        )
        self.assertEqual(warnings, [])
        self.assertEqual(promoted["relations"][0]["from"], "G01")
        self.assertEqual(promoted["relations"][0]["to"], "G02")
        question = promoted["questions"][0]
        self.assertEqual(question["state"], "promoted-after-return-check")
        self.assertEqual(question["handling"], "promoted to R01")
        self.assert_valid(promoted)

    def test_question_without_candidate_relation_cannot_be_promoted(self) -> None:
        data, _warnings = add_question(
            self.fixture(),
            question_id="Q01",
            text="What should be checked next?",
            arises_from=["G01"],
        )
        with self.assertRaisesRegex(
            ValueError,
            "must declare two candidate_relation_between endpoints",
        ):
            promote_question(
                data,
                question_id="Q01",
                relation_id="R01",
                predicate="invented relation",
                direction="directed",
            )

    def test_new_id_must_not_reuse_existing_namespace_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "id already exists"):
            add_card(
                self.fixture(),
                card_id="G01",
                text="global id reuse is too ambiguous for the editor",
            )

    def test_write_map_preserves_unicode_and_valid_json(self) -> None:
        data, _warnings = add_card(
            self.fixture(),
            card_id="C004",
            text="温度差を消さずに残す",
            source_refs=["S01"],
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "map.json"
            write_map(data, output)
            loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["cards"][-1]["text"], "温度差を消さずに残す")
        self.assert_valid(loaded)


if __name__ == "__main__":
    unittest.main()
