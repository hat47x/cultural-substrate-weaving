from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
SCRIPTS_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_adapter_metadata import plan_adapter_metadata  # noqa: E402
from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402

SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"


class ResearchAdapterMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, metadata: dict, fragment: str) -> None:
        errors = validate_adapter_metadata(ROOT, metadata)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_adapter_metadata_descriptor_is_consistent(self) -> None:
        self.assertEqual(validate_adapter_metadata(ROOT, self.metadata), [])

    def test_openai_metadata_covers_all_suite_skills_and_locales(self) -> None:
        openai = self.metadata["distributions"]["openai_skill"]
        suite_skill_ids = {skill["id"] for skill in self.suite["skills"]}
        suite_locales = set(self.suite["locales"])

        self.assertEqual(set(openai["skills"]), suite_skill_ids)
        for skill in openai["skills"].values():
            self.assertEqual(set(skill), suite_locales)

    def test_planned_openai_metadata_cannot_claim_source(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "affinity-synthesis"
        ]["ja-JP"]["interactive"]
        entry["source"] = "adapters/openai-skill/ja-JP/openai.interactive.yaml"

        self.assert_has_error(metadata, "planned openai_skill metadata")

    def test_existing_openai_metadata_source_must_exist(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["ja-JP"]["interactive"]
        entry["source"] = "adapters/openai-skill/ja-JP/DOES-NOT-EXIST.yaml"

        self.assert_has_error(metadata, "metadata source is missing")

    def test_openai_profile_policy_is_checked_against_source(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        entry = metadata["distributions"]["openai_skill"]["skills"][
            "cultural-substrate-weaving"
        ]["ja-JP"]["interactive"]
        entry["source"] = "adapters/openai-skill/ja-JP/openai.metered.yaml"

        self.assert_has_error(metadata, "allow_implicit_invocation: true")

    def test_multi_skill_bundle_baseline_must_remain_review_required(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["distributions"]["claude_plugin"][
            "review_required_for_multi_skill"
        ] = False

        self.assert_has_error(metadata, "must require review")

    def test_locale_catalog_must_declare_required_fields(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["distributions"]["claude_plugin"]["source"] = (
            "research/skill-prototypes/adapter-metadata-plan.json"
        )

        self.assert_has_error(metadata, "locale catalog does not declare metadata")

    def test_current_openai_coverage_separates_runtime_and_metadata_gaps(self) -> None:
        plan = plan_adapter_metadata(self.suite, self.metadata, ROOT)
        ja = plan["locales"]["ja-JP"]["distributions"]["openai_skill"]
        en = plan["locales"]["en-US"]["distributions"]["openai_skill"]

        self.assertEqual(ja["runtime_state"], "buildable")
        self.assertEqual(ja["metadata_coverage"], "incomplete-for-realized")
        ja_items = {item["skill_id"]: item for item in ja["items"]}
        self.assertEqual(ja_items["cultural-substrate-weaving"]["metadata_state"], "existing")
        self.assertEqual(ja_items["affinity-synthesis"]["metadata_state"], "planned")
        self.assertEqual(ja_items["iterative-inquiry-synthesis"]["metadata_state"], "planned")

        self.assertEqual(en["runtime_state"], "partial")
        self.assertEqual(en["metadata_coverage"], "complete-for-realized")
        en_items = {item["skill_id"]: item for item in en["items"]}
        self.assertEqual(en_items["cultural-substrate-weaving"]["metadata_state"], "existing")
        self.assertEqual(en_items["affinity-synthesis"]["metadata_state"], "runtime-blocked")

    def test_current_bundle_metadata_is_baseline_requiring_review(self) -> None:
        plan = plan_adapter_metadata(self.suite, self.metadata, ROOT)
        ja = plan["locales"]["ja-JP"]["distributions"]
        en = plan["locales"]["en-US"]["distributions"]

        self.assertEqual(ja["claude_plugin"]["runtime_state"], "buildable")
        self.assertEqual(ja["claude_plugin"]["metadata_state"], "review-required")
        self.assertEqual(ja["codex_plugin"]["metadata_state"], "review-required")
        self.assertEqual(ja["claude_plugin"]["catalog_entry"]["plugin_name"], "cultural-substrate-weaving-ja")

        self.assertEqual(en["claude_plugin"]["runtime_state"], "blocked")
        self.assertEqual(en["claude_plugin"]["metadata_state"], "review-required")


if __name__ == "__main__":
    unittest.main()
