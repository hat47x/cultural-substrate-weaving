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

from validate_research_skill_suite import validate_suite  # noqa: E402

MANIFEST_PATH = ROOT / "research/skill-prototypes/suite-manifest.json"

CRITICAL_P4_CONTRACT_ASSETS = (
    "research/skill-prototypes/P4-PRODUCTION-SOURCE-CONTRACT-CONSOLIDATION-2026-09-08.md",
    "research/skill-prototypes/P4-PROMOTION-READINESS-OBSERVER-2026-09-08.md",
)


class ResearchP4ContractAssetRegistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_current_p4_contract_assets_are_registered(self) -> None:
        assets = set(self.manifest["suite_research_assets"])
        for relative in CRITICAL_P4_CONTRACT_ASSETS:
            self.assertIn(relative, assets)
        self.assertEqual(validate_suite(ROOT, self.manifest), [])

    def test_p4_contract_assets_cannot_silently_drop_from_suite_manifest(self) -> None:
        for relative in CRITICAL_P4_CONTRACT_ASSETS:
            with self.subTest(relative=relative):
                manifest = copy.deepcopy(self.manifest)
                manifest["suite_research_assets"].remove(relative)
                errors = validate_suite(ROOT, manifest)
                self.assertTrue(
                    any("missing promotion-critical assets" in error for error in errors),
                    errors,
                )


if __name__ == "__main__":
    unittest.main()
