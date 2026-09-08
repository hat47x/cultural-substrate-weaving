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

from validate_research_public_name_projection_inventory import (  # noqa: E402
    validate_projection_inventory,
)

INVENTORY_PATH = (
    ROOT
    / "research"
    / "skill-prototypes"
    / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"
)
PROMOTION_PLAN_PATH = (
    "research/skill-prototypes/"
    "P4-PRODUCTION-SOURCE-AND-BUILDER-PROMOTION-PLAN-2026-09-07.md"
)
LAYER1_CASES_PATH = "research/skill-prototypes/affinity-synthesis/evals/CASES.md"
LAYER1_DOSSIER_PATH = "research/skill-prototypes/affinity-synthesis/evidence/dossier.md"


class ResearchPublicNameProjectionInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, inventory: dict, fragment: str) -> None:
        errors = validate_projection_inventory(ROOT, inventory)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def content_item(self, inventory: dict, path: str) -> dict:
        return next(item for item in inventory["content_projection"] if item["path"] == path)

    def test_current_inventory_is_valid(self) -> None:
        self.assertEqual(validate_projection_inventory(ROOT, self.inventory), [])

    def test_production_name_must_remain_material_led_synthesis(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["production_name"] = "affinity-synthesis"
        self.assert_has_error(inventory, "production_name must remain material-led-synthesis")

    def test_missing_expected_runtime_marker_requires_audit(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["content_projection"][0]["required_markers"] = [
            "name: does-not-exist"
        ]
        self.assert_has_error(inventory, "marker changed and requires audit")

    def test_packaged_layer1_support_docs_are_projection_sensitive(self) -> None:
        for path in (LAYER1_CASES_PATH, LAYER1_DOSSIER_PATH):
            item = self.content_item(self.inventory, path)
            self.assertEqual(item["class"], "packaged-progressive-support")
            self.assertEqual(item["action"], "rewrite-explicit-installable-name")
            self.assertIn("`affinity-synthesis`", item["required_markers"])

    def test_packaged_layer1_support_projection_cannot_be_removed(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["content_projection"] = [
            item
            for item in inventory["content_projection"]
            if item.get("path") != LAYER1_DOSSIER_PATH
        ]
        self.assert_has_error(
            inventory,
            "missing promotion-critical content projection paths",
        )

    def test_promotion_plan_is_guarded_against_stale_production_paths(self) -> None:
        item = self.content_item(self.inventory, PROMOTION_PLAN_PATH)
        self.assertIn("src/skills/material-led-synthesis/", item["required_markers"])
        self.assertIn("src/skills/affinity-synthesis/", item["forbidden_markers"])
        self.assertIn(
            "adapters/openai-skill/<locale>/affinity-synthesis/",
            item["forbidden_markers"],
        )

    def test_forbidden_projection_marker_requires_audit(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        item = self.content_item(inventory, PROMOTION_PLAN_PATH)
        item["forbidden_markers"] = ["src/skills/material-led-synthesis/"]
        self.assert_has_error(inventory, "forbidden marker requires audit")

    def test_forbidden_projection_markers_must_be_strings(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        item = self.content_item(inventory, PROMOTION_PLAN_PATH)
        item["forbidden_markers"] = [None]
        self.assert_has_error(inventory, "forbidden_markers must contain non-empty strings")

    def test_layer2_method_projection_cannot_be_removed_from_inventory(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        target = (
            "research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.en.md"
        )
        inventory["content_projection"] = [
            item for item in inventory["content_projection"] if item.get("path") != target
        ]
        self.assert_has_error(
            inventory,
            "missing promotion-critical content projection paths",
        )

    def test_promotion_plan_projection_cannot_be_removed_from_inventory(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["content_projection"] = [
            item
            for item in inventory["content_projection"]
            if item.get("path") != PROMOTION_PLAN_PATH
        ]
        self.assert_has_error(
            inventory,
            "missing promotion-critical content projection paths",
        )

    def test_bundle_contains_must_still_expose_research_id_before_projection(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["structured_projection"][0]["field"] = "missing-field"
        self.assert_has_error(inventory, "unsupported structured projection field")

    def test_bundle_structured_projection_cannot_be_removed(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["structured_projection"] = inventory["structured_projection"][1:]
        self.assert_has_error(
            inventory,
            "missing promotion-critical structured projection paths",
        )

    def test_production_path_projection_must_not_point_into_research(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["path_projection"][0]["production_pattern"] = (
            "research/skill-prototypes/material-led-synthesis/{locale}/"
        )
        self.assert_has_error(inventory, "production path must not point into research")

    def test_global_string_replacement_remains_forbidden(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["note"] = "rename everything globally"
        self.assert_has_error(inventory, "must forbid global string replacement")


if __name__ == "__main__":
    unittest.main()
