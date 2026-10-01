from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "research" / "skill-prototypes" / "affinity-synthesis" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_map import validate  # noqa: E402


class ResearchAffinityMapValidationTests(unittest.TestCase):
    def fixture(self) -> dict:
        return {
            "format": "affinity-map",
            "version": "0.1",
            "sources": [{"id": "S01", "ref": "source A"}],
            "cards": [
                {"id": "C001", "text": "main card", "source_refs": ["S01"]},
                {"id": "C002", "text": "group member", "source_refs": ["S01"]},
            ],
            "groups": [
                {"id": "G01", "label": "primary group", "members": ["C002"]},
            ],
            "resonances": [
                {
                    "id": "X01",
                    "from": "C001",
                    "to": "G01",
                    "note": "C001 resonates with G01 without becoming its member",
                }
            ],
            "questions": [
                {
                    "id": "Q01",
                    "text": "What would clarify the resonance?",
                    "arises_from": ["X01"],
                }
            ],
        }

    def test_question_may_use_secondary_resonance_as_local_provenance(self) -> None:
        errors, warnings = validate(self.fixture())
        self.assertEqual(errors, [])
        self.assertFalse(
            any("question Q01 arises_from ref does not resolve locally" in warning for warning in warnings)
        )

    def test_catalytic_target_response_refs_must_resolve_to_source_or_card(self) -> None:
        data = self.fixture()
        data["cards"][0]["input_status"] = "framework_generated"
        data["cards"][0]["catalytic_trace"] = {
            "frameworks": ["iching"],
            "operations": ["counter-view"],
            "target_responses": ["pushback"],
            "target_response_refs": ["S01", "C002"],
        }
        errors, _warnings = validate(data)
        self.assertEqual(errors, [])

        data["cards"][0]["catalytic_trace"]["target_response_refs"] = ["G01"]
        errors, _warnings = validate(data)
        self.assertTrue(
            any(
                "catalytic target_response_ref must resolve to source/card: G01"
                in error
                for error in errors
            ),
            errors,
        )

    def test_catalytic_target_response_ref_cannot_reference_framework_card_itself(self) -> None:
        data = self.fixture()
        data["cards"][0]["input_status"] = "framework_generated"
        data["cards"][0]["catalytic_trace"] = {
            "frameworks": ["iching"],
            "operations": ["counter-view"],
            "target_responses": ["pushback"],
            "target_response_refs": ["C001"],
        }
        errors, _warnings = validate(data)
        self.assertTrue(
            any(
                "catalytic target_response_ref cannot reference itself"
                in error
                for error in errors
            ),
            errors,
        )

    def test_cross_field_trace_preserves_target_and_framework_lineage(self) -> None:
        data = self.fixture()
        data["cards"][0]["input_status"] = "target_supported"
        data["cards"].append(
            {
                "id": "C003",
                "text": "framework candidate",
                "input_status": "framework_generated",
                "catalytic_trace": {
                    "frameworks": ["iching"],
                    "operations": ["counter-view"],
                },
            }
        )
        data["cards"].append(
            {
                "id": "C004",
                "text": "cross-field candidate",
                "input_status": "cross_field_emergent",
                "cross_field_trace": {
                    "target_refs": ["C001"],
                    "framework_refs": ["C003"],
                    "newly_recomposed": ["narrower conditional distinction"],
                },
            }
        )
        errors, _warnings = validate(data)
        self.assertEqual(errors, [])

    def test_cross_field_framework_ref_must_be_traced_framework_card(self) -> None:
        data = self.fixture()
        data["cards"][0]["input_status"] = "target_supported"
        data["cards"].append(
            {
                "id": "C003",
                "text": "cross-field candidate",
                "input_status": "cross_field_emergent",
                "cross_field_trace": {
                    "target_refs": ["C002"],
                    "framework_refs": ["C001"],
                },
            }
        )
        errors, _warnings = validate(data)
        self.assertTrue(
            any(
                "cross_field framework_ref must reference framework_generated card"
                in error
                for error in errors
            ),
            errors,
        )

    def test_cross_field_target_ref_must_not_use_framework_candidate_as_target_side(self) -> None:
        data = self.fixture()
        data["cards"].append(
            {
                "id": "C003",
                "text": "framework candidate",
                "input_status": "framework_generated",
                "catalytic_trace": {
                    "frameworks": ["five-phases"],
                    "operations": ["transition-path"],
                },
            }
        )
        data["cards"].append(
            {
                "id": "C004",
                "text": "cross-field candidate",
                "input_status": "cross_field_emergent",
                "cross_field_trace": {
                    "target_refs": ["C003"],
                    "framework_refs": ["C003"],
                },
            }
        )
        errors, _warnings = validate(data)
        self.assertTrue(
            any(
                "cross_field target_ref must not use framework/cross-field card"
                in error
                for error in errors
            ),
            errors,
        )

    def test_unresolved_question_provenance_still_warns(self) -> None:
        data = self.fixture()
        data["questions"][0]["arises_from"] = ["X404"]
        errors, warnings = validate(data)
        self.assertEqual(errors, [])
        self.assertTrue(
            any("question Q01 arises_from ref does not resolve locally: X404" in warning for warning in warnings)
        )


if __name__ == "__main__":
    unittest.main()
