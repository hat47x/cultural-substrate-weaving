from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_promotion_preconditions import (  # noqa: E402
    EVIDENCE_BINDING_PRECONDITION,
    validate_promotion_preconditions,
)

DESCRIPTOR_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
)


class ResearchPromotionPreconditionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, descriptor: dict, fragment: str) -> None:
        errors = validate_promotion_preconditions(descriptor)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_promotion_preconditions_are_valid(self) -> None:
        self.assertEqual(validate_promotion_preconditions(self.descriptor), [])

    def test_evidence_binding_precondition_cannot_be_removed(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].remove(EVIDENCE_BINDING_PRECONDITION)
        self.assert_has_error(descriptor, "missing required conditions")

    def test_old_exact_head_binding_is_not_the_required_contract(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].remove(EVIDENCE_BINDING_PRECONDITION)
        descriptor["promotion_preconditions"].append(
            "complete-checkout PASS evidence execution commit matches the current checkout HEAD"
        )
        self.assert_has_error(descriptor, "missing required conditions")

    def test_independent_english_review_precondition_cannot_be_removed(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].remove(
            "English sibling Skill realizations receive independent review"
        )
        self.assert_has_error(descriptor, "missing required conditions")

    def test_research_gate_precondition_cannot_be_removed(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].remove(
            "complete-checkout research-skill-check passes"
        )
        self.assert_has_error(descriptor, "missing required conditions")

    def test_duplicate_precondition_is_rejected(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].append(EVIDENCE_BINDING_PRECONDITION)
        self.assert_has_error(descriptor, "must not contain duplicates")

    def test_preconditions_must_be_string_list(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["promotion_preconditions"].append(None)
        self.assert_has_error(descriptor, "only non-empty strings")


if __name__ == "__main__":
    unittest.main()
