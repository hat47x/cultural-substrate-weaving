from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
RESEARCH_SCRIPTS_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
for path in (SCRIPTS_DIR, RESEARCH_SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from validate_production_skill_set import validate_production_skill_set  # noqa: E402
from validate_production_projection import validate_projection  # noqa: E402

SKILL_SET_PATH = ROOT / "src" / "skill-set.json"
INCLUSION_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"


class ProductionSkillSetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_set = json.loads(SKILL_SET_PATH.read_text(encoding="utf-8"))
        self.inclusion = json.loads(INCLUSION_PATH.read_text(encoding="utf-8"))

    def test_current_production_skill_set_is_valid(self) -> None:
        self.assertEqual(validate_production_skill_set(ROOT, self.skill_set), [])

    def test_current_descriptor_owns_only_identity_and_source_manifest(self) -> None:
        self.assertEqual(
            self.skill_set,
            {
                "schema": "csw.production-skill-set/v1",
                "skills": [
                    {
                        "id": "cultural-substrate-weaving",
                        "source_manifest": "src/manifest.json",
                    }
                ],
            },
        )

    def test_descriptor_rejects_duplicate_skill_ids(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"].append(copy.deepcopy(value["skills"][0]))
        errors = validate_production_skill_set(ROOT, value)
        self.assertTrue(any("duplicate production Skill id" in error for error in errors))

    def test_descriptor_rejects_extra_metadata_ownership(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"][0]["description"] = "must stay in source/adapter metadata"
        errors = validate_production_skill_set(ROOT, value)
        self.assertTrue(any("may contain only id and source_manifest" in error for error in errors))

    def test_source_manifest_must_stay_under_src(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"][0]["source_manifest"] = (
            "research/skill-prototypes/suite-manifest.json"
        )
        errors = validate_production_skill_set(ROOT, value)
        self.assertTrue(any("safe repository path under src/" in error for error in errors))

    def test_manifest_identity_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            (root / "src" / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "another-skill",
                        "canonical_locale": "ja-JP",
                        "locales": {"ja-JP": {}},
                    }
                ),
                encoding="utf-8",
            )
            errors = validate_production_skill_set(root, self.skill_set)
            self.assertTrue(any("source manifest name mismatch" in error for error in errors))

    def test_research_inclusion_projects_exactly_to_production(self) -> None:
        self.assertEqual(validate_projection(self.skill_set, self.inclusion), [])

    def test_candidate_cannot_leak_into_production_projection(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"].append(
            {
                "id": "affinity-synthesis",
                "source_manifest": "src/affinity-synthesis/manifest.json",
            }
        )
        errors = validate_projection(value, self.inclusion)
        self.assertTrue(any("exactly" in error for error in errors))
        self.assertTrue(any("leaked into production" in error for error in errors))

    def test_included_skill_cannot_disappear_from_production_projection(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"] = []
        errors = validate_projection(value, self.inclusion)
        self.assertTrue(any("exactly" in error for error in errors))

    def test_projection_source_manifest_must_match_inclusion_decision(self) -> None:
        value = copy.deepcopy(self.skill_set)
        value["skills"][0]["source_manifest"] = "src/other-manifest.json"
        errors = validate_projection(value, self.inclusion)
        self.assertTrue(any("does not match inclusion decision" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
