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
    OBSERVATION_IDS,
    PAIRED_RUN,
    TRANSLATION_STATUS,
    _declared_field,
    observe_promotion_readiness,
)


class ResearchPromotionReadinessObserverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = observe_promotion_readiness(ROOT)
        cls.by_id = {item["id"]: item for item in cls.report["observations"]}
        cls.descriptor = json.loads((ROOT / DESCRIPTOR).read_text(encoding="utf-8"))

    def test_report_has_stable_observation_set_without_ready_boolean(self) -> None:
        self.assertEqual(tuple(item["id"] for item in self.report["observations"]), OBSERVATION_IDS)
        self.assertEqual(self.report["schema"], "csw.research-promotion-readiness-observation/v3")
        self.assertNotIn("ready", self.report)
        self.assertNotIn("promotion_ready", self.report)
        self.assertIs(self.report["authorization"]["issued"], False)

    def test_each_observation_cannot_authorize_production(self) -> None:
        for item in self.report["observations"]:
            self.assertIs(item["production_promotion_authorized"], False)

    def test_execution_and_english_review_mirror_descriptor_authorities(self) -> None:
        self.assertEqual(
            self.by_id["complete_checkout_execution"]["state"],
            self.descriptor["complete_checkout_validation"]["status"],
        )
        self.assertEqual(
            self.by_id["english_independent_review"]["state"],
            self.descriptor["english_independent_review"]["status"],
        )

    def test_translation_refresh_mirrors_own_authority(self) -> None:
        status = json.loads((ROOT / TRANSLATION_STATUS).read_text(encoding="utf-8"))
        item = self.by_id["translation_refresh_state"]
        self.assertEqual(item["state"], status["status"])
        self.assertEqual(item["details"]["expected_stale_files"], status["expected_stale_files"])
        self.assertEqual(item["evidence_kind"], "translation-source-tracking-gate")
        self.assertNotEqual(item["evidence_kind"], "independent-review-gate")

    def test_method_evaluation_uses_declared_metadata_field(self) -> None:
        paired = (ROOT / PAIRED_RUN).read_text(encoding="utf-8")
        declared = _declared_field(paired, "Evaluation type")
        item = self.by_id["method_split_evaluation"]
        self.assertEqual(item["details"]["declared_evaluation_type"], declared)
        if declared is not None and declared.lower().startswith("same-model"):
            self.assertEqual(item["state"], "same-model-evidence-present")
            self.assertEqual(
                item["evidence_kind"],
                "self-described-same-model-comparative-evaluation",
            )

    def test_method_definition_parity_is_declared_but_unexecuted(self) -> None:
        item = self.by_id["method_definition_parity"]
        self.assertIn(
            item["state"],
            {
                "declared-checks-present-unexecuted",
                "declared-checks-incomplete",
                "not-observed-in-this-branch",
            },
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_handoff_remains_fixture_evidence(self) -> None:
        item = self.by_id["cross_layer_handoff"]
        self.assertIn(item["state"], {"fixture-only", "not-observed-in-this-branch"})
        self.assertEqual(item["evidence_kind"], "regression-fixture")

    def test_tension_observation_does_not_claim_execution(self) -> None:
        item = self.by_id["csw_tension_ownership_evaluation"]
        self.assertIn(
            item["state"],
            {"fixture-and-regression-present-unexecuted", "not-observed-in-this-branch"},
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_production_mechanics_are_not_inferred_from_function_names(self) -> None:
        allowed = {
            "design-and-production-file-present-unclassified",
            "design-only",
            "production-file-present-unclassified",
            "not-observed-in-this-branch",
        }
        for observation_id in (
            "production_builder_generalization",
            "production_validator_generalization",
        ):
            item = self.by_id[observation_id]
            self.assertIn(item["state"], allowed)
            self.assertNotIn("pass", item["state"].lower())
            self.assertNotIn("implemented", item["state"].lower())

    def test_cross_surface_oracle_presence_never_claims_execution(self) -> None:
        item = self.by_id["cross_surface_host_parity"]
        self.assertIn(
            item["state"],
            {"oracle-present-unexecuted", "not-observed-in-this-branch"},
        )

    def test_real_host_behavior_is_not_inferred(self) -> None:
        item = self.by_id["real_host_behavior"]
        self.assertEqual(item["state"], "unobserved")
        self.assertEqual(item["evidence"], [])
        self.assertEqual(item["evidence_kind"], "real-host-execution")


if __name__ == "__main__":
    unittest.main()
