from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from plan_promotion_readiness import (  # noqa: E402
    DESCRIPTOR,
    _translation_status_path,
    observe_promotion_readiness,
)


class ResearchPromotionTranslationExecutionSeparationTests(unittest.TestCase):
    def test_synchronized_translation_does_not_imply_complete_checkout_execution(self) -> None:
        report = observe_promotion_readiness(ROOT)
        by_id = {item["id"]: item for item in report["observations"]}
        descriptor = json.loads((ROOT / DESCRIPTOR).read_text(encoding="utf-8"))
        translation_path = _translation_status_path(descriptor)
        self.assertIsNotNone(translation_path)
        assert translation_path is not None
        translation = json.loads((ROOT / translation_path).read_text(encoding="utf-8"))

        translation_obs = by_id["translation_refresh_state"]
        execution_obs = by_id["complete_checkout_execution"]

        self.assertEqual(translation["status"], "synchronized")
        self.assertEqual(translation["expected_stale_files"], [])
        self.assertEqual(translation_obs["state"], "synchronized")
        self.assertEqual(translation_obs["authority"], translation_path.as_posix())
        self.assertEqual(translation_obs["details"]["expected_stale_files"], [])

        self.assertEqual(
            descriptor["complete_checkout_validation"]["status"],
            "blocked-not-run",
        )
        self.assertEqual(execution_obs["state"], "blocked-not-run")

        self.assertIs(translation_obs["production_promotion_authorized"], False)
        self.assertIs(execution_obs["production_promotion_authorized"], False)
        self.assertIs(report["authorization"]["issued"], False)
        self.assertNotEqual(translation_obs["evidence_kind"], execution_obs["evidence_kind"])


if __name__ == "__main__":
    unittest.main()
