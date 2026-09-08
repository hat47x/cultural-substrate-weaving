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

from plan_production_source_promotion import (  # noqa: E402
    PLAN_SCHEMA,
    _locale_tree_source_prefixes,
    plan_production_source_promotion,
    validate_production_source_promotion_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
SUITE_PATH = BASE / "suite-manifest.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
MIGRATION_PATH = BASE / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
INVENTORY_PATH = BASE / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"


class ResearchProductionSourcePromotionAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        cls.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        cls.migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
        cls.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def test_current_locale_tree_prefixes_come_from_suite_and_descriptor(self) -> None:
        prefixes = _locale_tree_source_prefixes(self.suite, self.descriptor)
        descriptor_by_id = {
            item["research_id"]: item
            for item in self.descriptor["skills"]
        }
        expected = {
            skill["source_root"].rstrip("/") + "/"
            for skill in self.suite["skills"]
            if descriptor_by_id[skill["id"]]["production_source"]["mode"] == "locale_tree"
        }
        self.assertEqual(set(prefixes), expected)

    def test_current_plan_accepts_locale_neutral_source_shared_across_locales(self) -> None:
        plan = plan_production_source_promotion(
            self.suite,
            self.descriptor,
            self.migration,
            self.inventory,
        )
        errors = validate_production_source_promotion_plan(
            plan,
            self.descriptor,
            self.inventory,
            suite=self.suite,
        )
        self.assertEqual(errors, [])

        layer1 = next(item for item in plan["skills"] if item["research_id"] == "affinity-synthesis")
        shared_source = "research/skill-prototypes/affinity-synthesis/references/affinity-map.schema.json"
        occurrences = sum(
            1
            for locale_plan in layer1["locales"].values()
            for mapping in locale_plan["mappings"]
            if mapping["source"] == shared_source
        )
        self.assertEqual(occurrences, 2)

    def test_new_locale_tree_source_root_needs_no_python_prefix_update(self) -> None:
        suite = copy.deepcopy(self.suite)
        descriptor = copy.deepcopy(self.descriptor)
        suite["skills"].append(
            {
                "id": "new-synthesis",
                "source_root": "research/skill-prototypes/new-synthesis",
            }
        )
        descriptor["skills"].append(
            {
                "research_id": "new-synthesis",
                "production_source": {"mode": "locale_tree"},
            }
        )
        self.assertIn(
            "research/skill-prototypes/new-synthesis/",
            _locale_tree_source_prefixes(suite, descriptor),
        )

    def test_canonical_manifest_route_is_source_mode_driven_not_research_id_driven(self) -> None:
        suite = {
            "skills": [
                {
                    "id": "alternate-core",
                    "source_root": "src",
                    "locale_realizations": {},
                }
            ]
        }
        descriptor = {
            "skills": [
                {
                    "research_id": "alternate-core",
                    "proposed_installable_name": "alternate-core",
                    "production_source": {
                        "mode": "canonical_manifest",
                        "manifest": "src/manifest.json",
                    },
                }
            ]
        }
        migration = {"research_to_production_name": {"alternate-core": "alternate-core"}}
        plan = plan_production_source_promotion(suite, descriptor, migration, {"content_projection": []})
        self.assertEqual(plan["skills"][0]["state"], "existing-canonical-manifest")
        self.assertEqual(plan["skills"][0]["locales"], {})
        self.assertEqual(
            validate_production_source_promotion_plan(
                plan,
                descriptor,
                {"content_projection": []},
                suite=suite,
            ),
            [],
        )

    def test_descriptor_name_is_the_only_public_name_authority_in_validator(self) -> None:
        descriptor = {
            "skills": [
                {
                    "research_id": "affinity-synthesis",
                    "proposed_installable_name": "different-valid-name",
                    "production_source": {
                        "mode": "locale_tree",
                        "root_pattern": "src/skills/different-valid-name/{locale}",
                    },
                }
            ]
        }
        plan = {
            "schema": PLAN_SCHEMA,
            "status": "design-only",
            "selection_basis": "research locale package_source.files",
            "skills": [
                {
                    "research_id": "affinity-synthesis",
                    "production_name": "different-valid-name",
                    "state": "planned-locale-tree-promotion",
                    "source": descriptor["skills"][0]["production_source"],
                    "locales": {
                        "ja-JP": {
                            "production_source_mode": "locale_tree",
                            "production_root": "src/skills/different-valid-name/ja-JP",
                            "runtime_entry": "src/skills/different-valid-name/ja-JP/SKILL.md",
                            "target_collision": False,
                            "mappings": [
                                {
                                    "source": "research/skill-prototypes/affinity-synthesis/SKILL.md",
                                    "source_relative": "SKILL.md",
                                    "target_relative": "SKILL.md",
                                    "content_transforms": [],
                                }
                            ],
                        }
                    },
                }
            ],
        }
        errors = validate_production_source_promotion_plan(plan, descriptor)
        self.assertEqual(errors, [])

    def test_inventory_coverage_uses_declared_locale_tree_source_root(self) -> None:
        suite = {
            "skills": [
                {
                    "id": "new-synthesis",
                    "source_root": "research/skill-prototypes/new-synthesis",
                }
            ]
        }
        descriptor = {
            "skills": [
                {
                    "research_id": "new-synthesis",
                    "proposed_installable_name": "new-synthesis",
                    "production_source": {
                        "mode": "locale_tree",
                        "root_pattern": "src/skills/new-synthesis/{locale}",
                    },
                }
            ]
        }
        plan = {
            "schema": PLAN_SCHEMA,
            "status": "design-only",
            "selection_basis": "research locale package_source.files",
            "skills": [
                {
                    "research_id": "new-synthesis",
                    "production_name": "new-synthesis",
                    "state": "planned-locale-tree-promotion",
                    "source": descriptor["skills"][0]["production_source"],
                    "locales": {
                        "ja-JP": {
                            "production_source_mode": "locale_tree",
                            "production_root": "src/skills/new-synthesis/ja-JP",
                            "runtime_entry": "src/skills/new-synthesis/ja-JP/SKILL.md",
                            "target_collision": False,
                            "mappings": [
                                {
                                    "source": "research/skill-prototypes/new-synthesis/SKILL.md",
                                    "source_relative": "SKILL.md",
                                    "target_relative": "SKILL.md",
                                    "content_transforms": [],
                                }
                            ],
                        }
                    },
                }
            ],
        }
        inventory = {
            "content_projection": [
                {
                    "path": "research/skill-prototypes/new-synthesis/references/METHOD.md",
                    "action": "rewrite-something",
                }
            ]
        }
        errors = validate_production_source_promotion_plan(
            plan,
            descriptor,
            inventory,
            suite=suite,
        )
        self.assertTrue(
            any("promotion-sensitive source declared by projection inventory is missing" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
