from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_english_review_gate import (  # noqa: E402
    validate_english_review_gate,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)
PACKET_RELATIVE = Path(
    "research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-PACKET-2026-09-07.md"
)


class ResearchEnglishReviewGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, descriptor: dict, fragment: str) -> None:
        errors = validate_english_review_gate(ROOT, descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_gate_is_valid_and_pending(self) -> None:
        self.assertEqual(validate_english_review_gate(ROOT, self.descriptor), [])
        gate = self.descriptor["english_independent_review"]
        self.assertEqual(gate["status"], "pending")
        self.assertIsNone(gate["completed_review"])
        self.assertFalse(gate["production_promotion_authorized"])

    def test_pending_gate_cannot_claim_completed_review(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["completed_review"] = (
            "research/skill-prototypes/reviews/english-review.md"
        )
        self.assert_has_error(
            descriptor,
            "pending English independent review must not declare completed_review",
        )

    def test_review_gate_never_authorizes_production_promotion(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["english_independent_review"]["production_promotion_authorized"] = True
        self.assert_has_error(
            descriptor,
            "must not authorize production promotion by itself",
        )

    def test_completed_gate_requires_separate_review_record(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        gate = descriptor["english_independent_review"]
        gate["status"] = "completed"
        gate["completed_review"] = str(PACKET_RELATIVE)
        self.assert_has_error(
            descriptor,
            "completed review record must be separate from the review packet",
        )

    def test_completed_gate_accepts_structured_independent_review_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = root / PACKET_RELATIVE
            packet_path.parent.mkdir(parents=True, exist_ok=True)
            packet_path.write_text(
                "review not yet completed\n"
                "Layer 1 必須不変条件\n"
                "Layer 2 必須不変条件\n"
                "Cross-layer査読\n"
                "production promotion全体の承認ではない\n",
                encoding="utf-8",
            )

            review_relative = Path(
                "research/skill-prototypes/reviews/english-independent-review.md"
            )
            review_path = root / review_relative
            review_path.parent.mkdir(parents=True, exist_ok=True)
            review_path.write_text(
                "reviewer: external-reviewer\n"
                "review date: 2026-09-07\n"
                "Layer 1:\n"
                "Layer 2:\n"
                "Cross-layer ownership:\n"
                "KJ lineage / naming:\n"
                "Promotion recommendation:\n"
                "Reviewed commit / blob refs:\n",
                encoding="utf-8",
            )

            descriptor = copy.deepcopy(self.descriptor)
            gate = descriptor["english_independent_review"]
            gate["status"] = "completed"
            gate["completed_review"] = str(review_relative)

            self.assertEqual(validate_english_review_gate(root, descriptor), [])


if __name__ == "__main__":
    unittest.main()
