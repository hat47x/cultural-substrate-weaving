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

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def test_current_research_suite_manifest_is_internally_consistent(self) -> None:
        self.assertEqual(validate_suite(ROOT, self.manifest), [])

    def test_existing_method_file_cannot_be_left_unregistered(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["method_definition"] = None
        iterative["references"] = [
            path for path in iterative["references"] if not path.endswith("/METHOD.md")
        ]
        iterative["locale_realizations"]["ja-JP"]["method_definition"] = None

        self.assert_has_error(manifest, "METHOD.md exists but method_definition is not registered")

    def test_method_definition_must_also_be_a_declared_reference(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["references"] = [
            path for path in iterative["references"] if not path.endswith("/METHOD.md")
        ]

        self.assert_has_error(manifest, "method_definition must also be declared in references")

    def test_installable_names_must_be_unique(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["skills"][1]["installable_name"] = manifest["skills"][0]["installable_name"]
        self.assert_has_error(manifest, "installable_name values must be unique")

    def test_runtime_frontmatter_name_must_match_installable_name(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["installable_name"] = "wrong-name"
        self.assert_has_error(manifest, "frontmatter name must match installable_name")

    def test_distribution_cannot_reference_unknown_skill(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["distribution_prototypes"]["claude_plugin"]["contains"].append("missing-skill")
        self.assert_has_error(manifest, "references unknown skills")

    def test_skill_paths_must_stay_inside_their_source_root(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["runtime_entry"] = "CHANGELOG.md"
        self.assert_has_error(manifest, "runtime_entry is outside source_root")

    def test_checks_are_validated_as_skill_owned_paths(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["checks"].append("CHANGELOG.md")
        self.assert_has_error(manifest, "declared checks path is outside source_root")

    def test_skill_must_declare_every_suite_locale_realization(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"].pop("en-US")
        self.assert_has_error(
            manifest,
            "locale_realizations must match suite locales; missing=['en-US']",
        )

    def test_skill_cannot_declare_unknown_locale_realization(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["fr-FR"] = {"status": "planned"}
        self.assert_has_error(
            manifest,
            "locale_realizations must match suite locales; missing=[], extra=['fr-FR']",
        )

    def test_canonical_locale_cannot_be_planned_only(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"] = {"status": "planned"}
        self.assert_has_error(manifest, "canonical locale ja-JP cannot be planned-only")

    def test_realized_locale_requires_runtime_entry(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        csw = self.skill(manifest, "cultural-substrate-weaving")
        csw["locale_realizations"]["en-US"] = {"status": "existing"}
        self.assert_has_error(manifest, "realized locale en-US must declare runtime_entry")

    def test_realized_locale_requires_method_definition_when_skill_has_one(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["en-US"].pop("method_definition")
        self.assert_has_error(manifest, "realized locale en-US must declare method_definition")

    def test_locale_method_definition_must_be_declared_as_reference(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        en_method = affinity["locale_realizations"]["en-US"]["method_definition"]
        affinity["references"].remove(en_method)
        self.assert_has_error(manifest, "locale realization en-US method_definition must also be declared in references")

    def test_canonical_locale_runtime_entry_matches_skill_entry(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"]["runtime_entry"] = (
            "research/skill-prototypes/affinity-synthesis/references/TEMPLATE.md"
        )
        self.assert_has_error(
            manifest,
            "canonical locale realization runtime_entry must match skill runtime_entry",
        )

    def test_canonical_locale_method_definition_matches_skill_entry(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"]["method_definition"] = (
            "research/skill-prototypes/affinity-synthesis/references/METHOD.en.md"
        )
        self.assert_has_error(
            manifest,
            "canonical locale realization method_definition must match skill method_definition",
        )

    def test_locale_runtime_entry_must_stay_inside_source_root(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        csw = self.skill(manifest, "cultural-substrate-weaving")
        csw["locale_realizations"]["en-US"]["runtime_entry"] = "CHANGELOG.md"
        self.assert_has_error(
            manifest,
            "locale realization en-US runtime_entry is outside source_root",
        )

    def test_hard_dependency_is_not_allowed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["delegation"]["hard_dependency"] = True
        self.assert_has_error(manifest, "must not assume hard dependency")

    def test_suite_research_assets_must_exist(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["suite_research_assets"].append("research/skill-prototypes/DOES-NOT-EXIST.md")
        self.assert_has_error(manifest, "suite_research_assets file is missing")


if __name__ == "__main__":
    unittest.main()
