from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_skill_suite import validate_suite  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchSkillSuiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, manifest: dict, fragment: str) -> None:
        errors = validate_suite(ROOT, manifest)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_research_suite_manifest_is_internally_consistent(self) -> None:
        self.assertEqual(validate_suite(ROOT, self.manifest), [])

    def test_existing_method_file_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = next(
            skill for skill in manifest["skills"] if skill["id"] == "iterative-inquiry-synthesis"
        )
        iterative["method_definition"] = None
        iterative["references"] = [
            path for path in iterative["references"] if not path.endswith("/METHOD.md")
        ]

        self.assert_has_error(manifest, "METHOD.md exists but method_definition is not registered")

    def test_method_definition_must_also_be_a_declared_reference(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = next(
            skill for skill in manifest["skills"] if skill["id"] == "iterative-inquiry-synthesis"
        )
        iterative["references"] = [
            path for path in iterative["references"] if not path.endswith("/METHOD.md")
        ]

        self.assert_has_error(manifest, "method_definition must also be declared in references")

    def test_installable_names_must_be_unique(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["skills"][1]["installable_name"] = manifest["skills"][0]["installable_name"]

        self.assert_has_error(manifest, "installable_name values must be unique")

    def test_distribution_cannot_reference_unknown_skill(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["claude_plugin"]["contains"].append(
            "missing-skill"
        )

        self.assert_has_error(manifest, "references unknown skills")

    def test_skill_paths_must_stay_inside_their_source_root(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = next(
            skill for skill in manifest["skills"] if skill["id"] == "iterative-inquiry-synthesis"
        )
        iterative["runtime_entry"] = "CHANGELOG.md"

        self.assert_has_error(manifest, "runtime_entry is outside source_root")


if __name__ == "__main__":
    unittest.main()
