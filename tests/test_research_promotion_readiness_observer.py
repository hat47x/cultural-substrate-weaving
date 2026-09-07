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
    TRANSLATION_STATUS,
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
        self.assertEqual(self.report["schema"], "csw.research-promotion-readiness-observation/v2")
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

    def test_same_model_evaluation_is_not_relabelled_as_independent(self) -> None:
        item = self.by_id["method_split_evaluation"]
        self.assertIn(
            item["state"],
            {"same-model-evidence-present", "evaluation-evidence-present", "not-observed-in-this-branch"},
        )
        if item["state"] == "same-model-evidence-present":
            self.assertEqual(item["evidence_kind"], "same-model-comparative-evaluation")

    def test_handoff_remains_fixture_evidence(self) -> None:
        item = self.by_id["cross_layer_handoff"]
        self.assertIn(item["state"], {"fixture-only", "not-observed-in-this-branch"})
        self.assertEqual(item["evidence_kind"], "regression-fixture")

    def test_tension_ownership_is_a_distinct_unexecuted_evidence_kind(self) -> None:
        item = self.by_id["csw_tension_ownership_evaluation"]
        self.assertIn(
            item["state"],
            {"fixture-and-ownership-regression-present-unexecuted", "not-observed-in-this-branch"},
        )
        self.assertEqual(item["evidence_kind"], "csw-specific-regression-fixture-and-ownership-test")
        if item["state"].startswith("fixture-and"):
            self.assertTrue(any(path.endswith("CSW-TENSION-EMERGENCE-CASES.md") for path in item["evidence"]))
            self.assertTrue(any(path.endswith("test_research_tension_emergence.py") for path in item["evidence"]))

    def test_repository_feature_probes_never_claim_execution_pass(self) -> None:
        mechanical_states = {
            "design-and-mechanical-implementation-present-unexecuted",
            "design-only",
            "mechanical-generalization-present-unexecuted",
            "not-observed-in-this-branch",
        }
        allowed = {
            "host_package_materialization": {
                "contract-present-unexecuted",
                "implementation-present-unexecuted",
                "not-observed-in-this-branch",
            },
            "cross_surface_host_parity": {
                "oracle-present-unexecuted",
                "not-observed-in-this-branch",
            },
            "production_builder_generalization": mechanical_states,
            "production_validator_generalization": mechanical_states,
            "production_inclusion_descriptor": {
                "descriptor-present-unexecuted",
                "not-observed-in-this-branch",
            },
        }
        for observation_id, states in allowed.items():
            self.assertIn(self.by_id[observation_id]["state"], states)

    def test_real_host_behavior_is_not_inferred(self) -> None:
        item = self.by_id["real_host_behavior"]
        self.assertEqual(item["state"], "unobserved")
        self.assertEqual(item["evidence"], [])
        self.assertEqual(item["evidence_kind"], "real-host-execution")


if __name__ == "__main__":
    unittest.main()
