from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_declared_checks import validate_declared_checks  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
MAKEFILE_PATH = ROOT / "Makefile"


class ResearchDeclaredCheckWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.makefile = MAKEFILE_PATH.read_text(encoding="utf-8")

    def assert_has_error(self, manifest: dict, makefile: str, fragment: str) -> None:
        errors = validate_declared_checks(manifest, makefile)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_declared_checks_are_wired(self) -> None:
        self.assertEqual(validate_declared_checks(self.manifest, self.makefile), [])

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

    def test_missing_research_gate_target_is_rejected(self) -> None:
        self.assert_has_error(
            self.manifest,
            "build:\n\tpython scripts/build.py\n",
            "Makefile target 'research-skill-check' is missing",
        )


if __name__ == "__main__":
    unittest.main()
