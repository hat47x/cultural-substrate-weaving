from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from plan_promotion_readiness import (  # noqa: E402
    ADAPTER_PROMOTION_PLANNER,
    ADAPTER_PROMOTION_TEST,
    DESCRIPTOR,
    OBSERVATION_IDS,
    PAIRED_RUN,
    RELEASE_TEST,
    RELEASE_VALIDATOR,
    SOURCE_PROJECTION_PREVIEW,
    SOURCE_PROJECTION_TEST,
    _declared_field,
    _translation_status_path,
    observe_promotion_readiness,
)


class ResearchPromotionReadinessObserverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = observe_promotion_readiness(ROOT)
        cls.by_id = {item["id"]: item for item in cls.report["observations"]}
        cls.descriptor = json.loads((ROOT / DESCRIPTOR).read_text(encoding="utf-8"))

    def test_report_has_stable_observation_set_without_ready_boolean(self) -> None:
        self.assertEqual(
            tuple(item["id"] for item in self.report["observations"]),
            OBSERVATION_IDS,
        )
        self.assertEqual(
            self.report["schema"],
            "csw.research-promotion-readiness-observation/v4",
        )
        self.assertEqual(len(OBSERVATION_IDS), 18)
        self.assertNotIn("ready", self.report)
        self.assertNotIn("promotion_ready", self.report)
        self.assertIs(self.report["authorization"]["issued"], False)

    def test_meta_gates_are_not_promoted_to_readiness_evidence_axes(self) -> None:
        for meta_gate_id in (
            "current_p4_authority_registry",
            "declared_check_wiring",
            "production_plan_consistency",
            "promotion_precondition_integrity",
            "complete_checkout_evidence_binding",
        ):
            self.assertNotIn(meta_gate_id, OBSERVATION_IDS)
            self.assertNotIn(meta_gate_id, self.by_id)

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

    def test_execution_observation_does_not_mix_binding_contract_with_execution_evidence(self) -> None:
        item = self.by_id["complete_checkout_execution"]
        binding = self.descriptor["complete_checkout_validation"].get("binding_contract")
        self.assertIsInstance(binding, str)
        self.assertNotIn(binding, item["evidence"])
        self.assertEqual(item["evidence_kind"], "execution-gate")
        self.assertIn(
            "Static repository inspection is not command-execution evidence.",
            item["notes"],
        )

    def test_translation_refresh_mirrors_descriptor_selected_authority(self) -> None:
        translation_path = _translation_status_path(self.descriptor)
        self.assertIsNotNone(translation_path)
        assert translation_path is not None
        status = json.loads((ROOT / translation_path).read_text(encoding="utf-8"))
        item = self.by_id["translation_refresh_state"]

        self.assertEqual(item["state"], status["status"])
        self.assertEqual(item["authority"], translation_path.as_posix())
        self.assertEqual(
            item["details"]["authority_pointer"],
            translation_path.as_posix(),
        )
        self.assertIn(translation_path.as_posix(), item["evidence"])
        self.assertEqual(
            item["details"]["expected_stale_files"],
            status["expected_stale_files"],
        )
        self.assertEqual(item["evidence_kind"], "translation-source-tracking-gate")
        self.assertNotEqual(item["evidence_kind"], "independent-review-gate")

    def test_translation_authority_path_follows_descriptor_pointer(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        alternate = Path("research/skill-prototypes/alternate-translation-state.json")
        descriptor["translation_refresh"]["state"] = alternate.as_posix()
        self.assertEqual(_translation_status_path(descriptor), alternate)

    def test_translation_authority_path_rejects_unsafe_pointer(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["translation_refresh"]["state"] = "../outside.json"
        self.assertIsNone(_translation_status_path(descriptor))

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

    def test_method_definition_parity_never_claims_pass(self) -> None:
        item = self.by_id["method_definition_parity"]
        self.assertIn(
            item["state"],
            {
                "declared-checks-present-execution-unrecorded",
                "declared-checks-incomplete",
                "not-observed-in-this-branch",
            },
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_handoff_remains_fixture_evidence(self) -> None:
        item = self.by_id["cross_layer_handoff"]
        self.assertIn(item["state"], {"fixture-only", "not-observed-in-this-branch"})
        self.assertEqual(item["evidence_kind"], "regression-fixture")

    def test_tension_observation_does_not_claim_execution_pass(self) -> None:
        item = self.by_id["csw_tension_ownership_evaluation"]
        self.assertIn(
            item["state"],
            {
                "fixture-and-regression-present-execution-unrecorded",
                "not-observed-in-this-branch",
            },
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_source_projection_is_separate_observation(self) -> None:
        item = self.by_id["production_source_projection"]
        if (ROOT / SOURCE_PROJECTION_PREVIEW).is_file() and (
            ROOT / SOURCE_PROJECTION_TEST
        ).is_file():
            self.assertEqual(
                item["state"],
                "preview-and-regression-present-execution-unrecorded",
            )
            self.assertIn(SOURCE_PROJECTION_PREVIEW.as_posix(), item["evidence"])
            self.assertIn(SOURCE_PROJECTION_TEST.as_posix(), item["evidence"])
        self.assertEqual(
            item["evidence_kind"],
            "read-only-production-source-content-projection",
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_adapter_metadata_promotion_is_separate_observation(self) -> None:
        item = self.by_id["production_adapter_metadata_promotion"]
        if (ROOT / ADAPTER_PROMOTION_PLANNER).is_file() and (
            ROOT / ADAPTER_PROMOTION_TEST
        ).is_file():
            self.assertEqual(
                item["state"],
                "planner-and-regression-present-execution-unrecorded",
            )
            self.assertIn(ADAPTER_PROMOTION_PLANNER.as_posix(), item["evidence"])
            self.assertIn(ADAPTER_PROMOTION_TEST.as_posix(), item["evidence"])
        self.assertEqual(
            item["evidence_kind"],
            "read-only-production-adapter-metadata-promotion-plan",
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

    def test_cross_surface_oracle_presence_never_claims_execution_pass(self) -> None:
        item = self.by_id["cross_surface_host_parity"]
        self.assertIn(
            item["state"],
            {
                "oracle-present-execution-unrecorded",
                "not-observed-in-this-branch",
            },
        )
        self.assertNotIn("pass", item["state"].lower())

    def test_release_composition_keeps_design_and_execution_distinct(self) -> None:
        item = self.by_id["release_internal_composition"]
        if (ROOT / RELEASE_VALIDATOR).is_file() and (ROOT / RELEASE_TEST).is_file():
            self.assertIn(
                item["state"],
                {
                    "design-and-validator-present-execution-unrecorded",
                    "validator-source-present-without-design",
                },
            )
        self.assertNotIn("pass", item["state"].lower())

    def test_real_host_behavior_is_not_inferred(self) -> None:
        item = self.by_id["real_host_behavior"]
        self.assertEqual(item["state"], "unobserved")
        self.assertEqual(item["evidence"], [])
        self.assertEqual(item["evidence_kind"], "real-host-execution")


if __name__ == "__main__":
    unittest.main()
