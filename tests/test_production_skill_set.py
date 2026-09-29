from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
RESEARCH_SCRIPTS_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
for path in (SCRIPTS_DIR, RESEARCH_SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import validate_production_skill_set as production_skill_set  # noqa: E402
from validate_production_skill_set import (  # noqa: E402
    _load,
    main as production_skill_set_main,
    validate_production_skill_set,
)
from validate_production_projection import validate_projection  # noqa: E402

SKILL_SET_PATH = ROOT / "src" / "skill-set.json"
INCLUSION_PATH = ROOT / "research" / "skill-prototypes" / "production-inclusion-plan.json"


class ProductionSkillSetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_set = json.loads(SKILL_SET_PATH.read_text(encoding="utf-8"))
        self.inclusion = json.loads(INCLUSION_PATH.read_text(encoding="utf-8"))

    def test_current_production_skill_set_is_valid(self) -> None:
        self.assertEqual(validate_production_skill_set(ROOT, self.skill_set), [])

    def test_validator_rejects_non_object_root_without_crashing(self) -> None:
        self.assertEqual(
            validate_production_skill_set(ROOT, []),
            ["production Skill-set must be an object"],
        )

    def test_json_loader_rejects_non_object_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "array.json"
            path.write_text("[]\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must contain a JSON object"):
                _load(path)

    def test_cli_catches_non_object_json_root(self) -> None:
        with patch(
            "validate_production_skill_set._load",
            side_effect=ValueError("skill-set must contain a JSON object"),
        ):
            self.assertEqual(production_skill_set_main(), 1)

    def test_source_manifest_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root = base / "repo"
            src = root / "src"
            src.mkdir(parents=True)
            outside = base / "manifest.json"
            outside.write_text(
                json.dumps(
                    {
                        "name": "cultural-substrate-weaving",
                        "canonical_locale": "ja-JP",
                        "locales": {"ja-JP": {}},
                    }
                ),
                encoding="utf-8",
            )
            link = src / "manifest.json"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            errors = validate_production_skill_set(root, self.skill_set)
            self.assertTrue(
                any("must resolve inside repository src/" in error for error in errors),
                errors,
            )

    def test_source_manifest_must_be_json_object(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            (root / "src" / "manifest.json").write_text("[]\n", encoding="utf-8")
            errors = validate_production_skill_set(root, self.skill_set)
            self.assertTrue(
                any("must contain a JSON object" in error for error in errors),
                errors,
            )

    def test_source_manifest_locale_keys_must_be_strings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            (root / "src" / "manifest.json").write_text("{}\n", encoding="utf-8")
            with patch.object(
                production_skill_set,
                "_load",
                return_value={
                    "name": "cultural-substrate-weaving",
                    "canonical_locale": "ja-JP",
                    "locales": {1: {}},
                },
            ):
                errors = validate_production_skill_set(root, self.skill_set)
            self.assertTrue(
                any("locale keys must be non-empty strings" in error for error in errors),
                errors,
            )

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
