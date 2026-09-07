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


class ResearchPublicNameProjectionInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def assert_has_error(self, inventory: dict, fragment: str) -> None:
        errors = validate_projection_inventory(ROOT, inventory)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

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

    def test_bundle_contains_must_still_expose_research_id_before_projection(self) -> None:
        inventory = copy.deepcopy(self.inventory)
        inventory["structured_projection"][0]["field"] = "missing-field"
        self.assert_has_error(inventory, "unsupported structured projection field")

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
