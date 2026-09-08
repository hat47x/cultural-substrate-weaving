from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARITY_SCRIPTS = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "iterative-inquiry-synthesis"
    / "scripts"
)
sys.path.insert(0, str(PARITY_SCRIPTS))

from check_method_parity import EN_METHOD, JA_METHOD, validate, validate_texts  # noqa: E402


class IterativeMethodParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ja = JA_METHOD.read_text(encoding="utf-8")
        self.en = EN_METHOD.read_text(encoding="utf-8")

    def test_current_method_definitions_have_required_invariant_surface(self) -> None:
        self.assertEqual(validate(), [])

    def test_missing_english_i15_is_detected(self) -> None:
        mutated = self.en.replace(
            "### I15. Missing synthesis realization stays explicit",
            "### Missing synthesis realization stays explicit",
            1,
        )
        errors = validate_texts(self.ja, mutated)
        self.assertTrue(
            any("missing=[15]" in error for error in errors),
            f"expected missing I15 error; got {errors!r}",
        )

    def test_duplicate_english_i16_is_detected(self) -> None:
        marker = "### I16. Carry-forward state is not reopen or continuation authority"
        mutated = self.en.replace(marker, f"{marker}\n\n{marker}", 1)
        errors = validate_texts(self.ja, mutated)
        self.assertTrue(
            any("duplicate invariant ids: [16]" in error for error in errors),
            f"expected duplicate I16 error; got {errors!r}",
        )

    def test_missing_round_count_non_authority_marker_is_detected(self) -> None:
        marker = (
            "Round count itself is not converted into greater truth, confidence, "
            "or independent support"
        )
        mutated = self.en.replace(marker, "Round count is tracked separately", 1)
        errors = validate_texts(self.ja, mutated)
        self.assertTrue(
            any("Round count itself is not converted" in error for error in errors),
            f"expected round-count marker error; got {errors!r}",
        )


if __name__ == "__main__":
    unittest.main()
