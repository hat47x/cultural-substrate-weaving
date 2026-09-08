from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
DESCRIPTOR = ROOT / "research/skill-prototypes/P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"


class ResearchTranslationPrepareContractTests(unittest.TestCase):
    def test_prepare_target_preserves_preflight_mutation_postflight_order(self) -> None:
        lines = MAKEFILE.read_text(encoding="utf-8").splitlines()
        start = lines.index("research-translation-prepare:") + 1
        recipe: list[str] = []
        for line in lines[start:]:
            if line and not line.startswith("\t"):
                break
            if line.startswith("\t"):
                recipe.append(line[1:])

        self.assertEqual(
            recipe,
            [
                "python scripts/validate_research_translation_refresh_state.py",
                "python scripts/validate_research_translation_review_snapshot.py",
                "$(MAKE) update-en-hashes",
                "python scripts/mark_research_translation_refresh_synchronized.py",
                "python scripts/validate_research_translation_refresh_state.py",
                "python scripts/validate_research_translation_review_snapshot.py",
            ],
        )

    def test_prepare_target_is_not_promoted_into_descriptor_command_authority(self) -> None:
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        required = descriptor["complete_checkout_validation"]["required_commands"]
        self.assertEqual(
            required,
            [
                "make update-en-hashes",
                "make research-skill-check",
                "make build",
                "make check",
            ],
        )
        self.assertNotIn("make research-translation-prepare", required)


if __name__ == "__main__":
    unittest.main()
