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

from validate_research_production_inclusion import validate_production_inclusion  # noqa: E402

PLAN_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"


class ResearchProductionInclusionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, plan: dict, fragment: str) -> None:
        errors = validate_production_inclusion(ROOT, plan)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_inclusion_plan_is_consistent(self) -> None:
        self.assertEqual(validate_production_inclusion(ROOT, self.plan), [])

    def test_research_candidate_cannot_claim_production_source(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"]["affinity-synthesis"]["production_source"] = {
            "mode": "canonical_manifest",
            "manifest": "src/manifest.json",
        }
        self.assert_has_error(plan, "candidate Skill must not claim production_source")

    def test_realized_candidate_locale_does_not_become_included_automatically(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"]["affinity-synthesis"]["locales"]["ja-JP"] = "included"
        self.assert_has_error(plan, "locale ja-JP state 'included' != expected 'candidate'")

    def test_planned_candidate_locale_must_remain_blocked(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["skills"]["iterative-inquiry-synthesis"]["locales"]["en-US"] = "candidate"
        self.assert_has_error(plan, "locale en-US state 'candidate' != expected 'blocked'")

    def test_included_skill_cannot_have_only_planned_locale_realization(self) -> None:
        plan = copy.deepcopy(self.plan)
        affinity = plan["skills"]["affinity-synthesis"]
        affinity["production_state"] = "included"
        affinity["production_source"] = {
            "mode": "canonical_manifest",
            "manifest": "src/manifest.json",
        }
        affinity["locales"] = {"ja-JP": "included", "en-US": "included"}
        self.assert_has_error(plan, "included locale en-US has only a planned realization")

    def test_plan_must_keep_at_least_one_production_included_skill(self) -> None:
        plan = copy.deepcopy(self.plan)
        csw = plan["skills"]["cultural-substrate-weaving"]
        csw["production_state"] = "candidate"
        csw["production_source"] = None
        csw["locales"] = {"ja-JP": "candidate", "en-US": "candidate"}
        self.assert_has_error(plan, "must include at least one Skill")

    def test_plan_skill_set_cannot_silently_omit_a_research_candidate(self) -> None:
        plan = copy.deepcopy(self.plan)
        del plan["skills"]["iterative-inquiry-synthesis"]
        self.assert_has_error(plan, "skill set must match research suite skill set")


if __name__ == "__main__":
    unittest.main()
