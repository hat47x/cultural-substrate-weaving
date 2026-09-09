from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE_MANIFEST = ROOT / "research/skill-prototypes/suite-manifest.json"
TRANSLATION_STATUS = (
    ROOT
    / "research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json"
)
TRANSLATION_STATUS_RELATIVE = TRANSLATION_STATUS.relative_to(ROOT).as_posix()


class ResearchTranslationAuthorityAssetRegistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_MANIFEST.read_text(encoding="utf-8"))
        self.status = json.loads(TRANSLATION_STATUS.read_text(encoding="utf-8"))

    def test_translation_status_and_human_record_are_registered_research_assets(self) -> None:
        assets = set(self.suite["suite_research_assets"])
        human_record = self.status["human_record"]

        self.assertIn(TRANSLATION_STATUS_RELATIVE, assets)
        self.assertIn(human_record, assets)
        self.assertTrue((ROOT / human_record).is_file())

    def test_translation_authority_remains_non_authorizing(self) -> None:
        self.assertEqual(self.status["status"], "synchronized")
        self.assertEqual(self.status["expected_stale_files"], [])
        self.assertIs(self.status["production_promotion_authorized"], False)


if __name__ == "__main__":
    unittest.main()
