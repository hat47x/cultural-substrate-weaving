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

from plan_production_adapter_metadata_promotion import (  # noqa: E402
    plan_production_adapter_metadata_promotion,
    validate_production_adapter_metadata_promotion_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
LOCALE_CATALOG_PATH = ROOT / "adapters" / "claude-code" / "locales.json"


class ResearchAdapterBundleWordingAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.locale_catalog = json.loads(LOCALE_CATALOG_PATH.read_text(encoding="utf-8"))

    def test_locale_bundle_distributions_must_share_prototype_source_per_locale(self) -> None:
        adapter_plan = copy.deepcopy(self.adapter_plan)
        adapter_plan["distributions"]["codex_plugin"]["locales"]["en-US"][
            "prototype_source"
        ] = adapter_plan["distributions"]["claude_plugin"]["locales"]["ja-JP"][
            "prototype_source"
        ]

        with self.assertRaisesRegex(
            ValueError,
            "locale_bundle distributions must share prototype source per locale",
        ):
            plan_production_adapter_metadata_promotion(
                adapter_plan,
                self.descriptor,
                self.locale_catalog,
            )

    def test_generated_bundle_plan_cannot_change_declared_prototype_source(self) -> None:
        plan = plan_production_adapter_metadata_promotion(
            self.adapter_plan,
            self.descriptor,
            self.locale_catalog,
        )
        mutated = copy.deepcopy(plan)
        en = next(
            item
            for item in mutated["locale_bundle_promotions"]
            if item["locale"] == "en-US"
        )
        en["prototype_source"] = "research/skill-prototypes/OTHER.json"

        errors = validate_production_adapter_metadata_promotion_plan(
            mutated,
            self.descriptor,
            self.locale_catalog,
            adapter_plan=self.adapter_plan,
        )

        self.assertTrue(
            any("locale-bundle prototype source mismatch: en-US" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
