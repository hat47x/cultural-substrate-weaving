from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_declared_checks import (  # noqa: E402
    _planner_paths,
    _research_validator_paths,
    _suite_validator_paths,
    validate_declared_checks,
)

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
MAKEFILE_PATH = ROOT / "Makefile"
META_VALIDATOR_COMMAND = "\tpython scripts/validate_research_declared_checks.py\n"


class ResearchDeclaredCheckWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.makefile = MAKEFILE_PATH.read_text(encoding="utf-8")
        self.suite_validators = _suite_validator_paths(ROOT)
        self.research_validators = _research_validator_paths(ROOT)
        self.planners = _planner_paths(ROOT)

    def validate(self, manifest: dict, makefile: str) -> list[str]:
        return validate_declared_checks(
            manifest,
            makefile,
            suite_validator_paths=self.suite_validators,
            research_validator_paths=self.research_validators,
            planner_paths=self.planners,
        )

    def assert_has_error(self, manifest: dict, makefile: str, fragment: str) -> None:
        errors = self.validate(manifest, makefile)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_declared_checks_validators_and_planners_are_wired(self) -> None:
        self.assertEqual(self.validate(self.manifest, self.makefile), [])

    def test_meta_validator_itself_is_wired_into_research_gate(self) -> None:
        self.assertIn(META_VALIDATOR_COMMAND, self.makefile)
        self.assertIn(
            "scripts/validate_research_declared_checks.py",
            self.suite_validators,
        )

    def test_declared_check_cannot_disappear_from_research_gate(self) -> None:
        makefile = self.makefile.replace(
            "\tpython research/skill-prototypes/iterative-inquiry-synthesis/scripts/check_method_parity.py\n",
            "",
        )
        self.assert_has_error(
            self.manifest,
            makefile,
            "declared check is not wired into research-skill-check",
        )

    def test_skill_owned_check_cannot_bypass_manifest(self) -> None:
        injected = (
            "\tpython research/skill-prototypes/affinity-synthesis/scripts/unregistered_check.py\n"
        )
        makefile = self.makefile.replace(
            "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
            injected + "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
        )
        self.assert_has_error(
            self.manifest,
            makefile,
            "Skill-owned check is wired into research-skill-check but not declared in suite manifest",
        )

    def test_manifest_check_addition_requires_gate_wiring(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = next(
            skill for skill in manifest["skills"] if skill["id"] == "iterative-inquiry-synthesis"
        )
        iterative["checks"].append(
            "research/skill-prototypes/iterative-inquiry-synthesis/scripts/future_check.py"
        )
        self.assert_has_error(
            manifest,
            self.makefile,
            "future_check.py",
        )

    def test_suite_level_validator_cannot_disappear_from_research_gate(self) -> None:
        validator = "scripts/validate_research_production_plan_consistency.py"
        self.assertIn(validator, self.suite_validators)
        makefile = self.makefile.replace(f"\tpython {validator}\n", "")
        self.assert_has_error(
            self.manifest,
            makefile,
            f"suite-level research validator is not wired into research-skill-check: {validator}",
        )

    def test_unknown_suite_level_validator_cannot_be_wired(self) -> None:
        injected = "\tpython scripts/validate_research_does_not_exist.py\n"
        makefile = self.makefile.replace(
            "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
            injected + "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
        )
        self.assert_has_error(
            self.manifest,
            makefile,
            "research gate references an unknown suite-level research validator",
        )

    def test_suite_level_validator_cannot_be_wired_twice(self) -> None:
        validator = "scripts/validate_research_skill_suite.py"
        command = f"\tpython {validator}\n"
        self.assertIn(command, self.makefile)
        makefile = self.makefile.replace(command, command + command, 1)
        self.assert_has_error(
            self.manifest,
            makefile,
            "suite-level research validator must be wired exactly once",
        )

    def test_research_cross_lane_validator_cannot_disappear_from_research_gate(self) -> None:
        validator = "research/skill-prototypes/scripts/validate_production_projection.py"
        self.assertIn(validator, self.research_validators)
        makefile = self.makefile.replace(f"\tpython {validator}\n", "")
        self.assert_has_error(
            self.manifest,
            makefile,
            f"research cross-lane validator is not wired into research-skill-check: {validator}",
        )

    def test_unknown_research_cross_lane_validator_cannot_be_wired(self) -> None:
        injected = "\tpython research/skill-prototypes/scripts/validate_does_not_exist.py\n"
        makefile = self.makefile.replace(
            "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
            injected + "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
        )
        self.assert_has_error(
            self.manifest,
            makefile,
            "research gate references an unknown research cross-lane validator",
        )

    def test_research_cross_lane_validator_cannot_be_wired_twice(self) -> None:
        validator = "research/skill-prototypes/scripts/validate_production_projection.py"
        command = f"\tpython {validator}\n"
        self.assertIn(command, self.makefile)
        makefile = self.makefile.replace(command, command + command, 1)
        self.assert_has_error(
            self.manifest,
            makefile,
            "research cross-lane validator must be wired exactly once",
        )

    def test_planner_cannot_disappear_from_research_gate(self) -> None:
        planner = "research/skill-prototypes/scripts/plan_production_source_promotion.py"
        self.assertIn(planner, self.planners)
        makefile = self.makefile.replace(f"\tpython {planner} >/dev/null\n", "")
        self.assert_has_error(
            self.manifest,
            makefile,
            f"research planner is not wired into research-skill-check: {planner}",
        )

    def test_unknown_planner_cannot_be_wired(self) -> None:
        injected = "\tpython research/skill-prototypes/scripts/plan_does_not_exist.py >/dev/null\n"
        makefile = self.makefile.replace(
            "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
            injected + "\tpython -m unittest discover -s tests -p 'test_research_*.py'\n",
        )
        self.assert_has_error(
            self.manifest,
            makefile,
            "research gate references an unknown research planner",
        )

    def test_planner_cannot_be_wired_twice(self) -> None:
        planner = "research/skill-prototypes/scripts/plan_suite_layout.py"
        command = f"\tpython {planner} >/dev/null\n"
        self.assertIn(command, self.makefile)
        makefile = self.makefile.replace(command, command + command, 1)
        self.assert_has_error(
            self.manifest,
            makefile,
            "research planner must be wired exactly once",
        )

    def test_missing_research_gate_target_is_rejected(self) -> None:
        self.assert_has_error(
            self.manifest,
            "build:\n\tpython scripts/build.py\n",
            "Makefile target 'research-skill-check' is missing",
        )


if __name__ == "__main__":
    unittest.main()
