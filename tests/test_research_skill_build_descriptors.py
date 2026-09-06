from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
sys.path.insert(0, str(PLANNER_DIR))

from plan_build_descriptors import plan_build_descriptors  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchSkillBuildDescriptorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def descriptors(self, manifest: dict, locale: str) -> dict[str, dict]:
        plan = plan_build_descriptors(manifest)
        return {
            item["skill_id"]: item
            for item in plan["locales"][locale]["skills"]
        }

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def test_current_suite_normalizes_three_skills_for_both_locales(self) -> None:
        plan = plan_build_descriptors(self.manifest)
        self.assertEqual(set(plan["locales"]), {"ja-JP", "en-US"})
        self.assertEqual(len(plan["locales"]["ja-JP"]["skills"]), 3)
        self.assertEqual(len(plan["locales"]["en-US"]["skills"]), 3)
        for locale in ("ja-JP", "en-US"):
            for descriptor in plan["locales"][locale]["skills"]:
                self.assertTrue(descriptor["research_only"])
                self.assertFalse(descriptor["release_readiness_asserted"])
                self.assertEqual(descriptor["state"], "buildable-input")

    def test_english_affinity_descriptor_uses_explicit_locale_package_references(self) -> None:
        affinity = self.descriptors(self.manifest, "en-US")["affinity-synthesis"]
        self.assertEqual(affinity["assembly_mode"], "direct_skill")
        self.assertTrue(affinity["method_source"].endswith("/METHOD.en.md"))
        self.assertIn(
            "research/skill-prototypes/affinity-synthesis/references/REPRESENTATION.md",
            affinity["package_reference_sources"],
        )
        self.assertIn(
            "research/skill-prototypes/affinity-synthesis/references/affinity-map.schema.json",
            affinity["package_reference_sources"],
        )
        self.assertNotIn(
            "research/skill-prototypes/affinity-synthesis/references/METHOD.md",
            affinity["package_reference_sources"],
        )
        self.assertNotIn(
            "research/skill-prototypes/affinity-synthesis/references/TEMPLATE.md",
            affinity["package_reference_sources"],
        )
        self.assertNotIn(
            "research/skill-prototypes/affinity-synthesis/references/HIERARCHY-AND-LINEAGE.md",
            affinity["package_reference_sources"],
        )

    def test_english_iterative_descriptor_keeps_explicit_optional_round_template(self) -> None:
        iterative = self.descriptors(self.manifest, "en-US")["iterative-inquiry-synthesis"]
        self.assertEqual(iterative["assembly_mode"], "direct_skill")
        self.assertTrue(iterative["method_source"].endswith("/METHOD.en.md"))
        self.assertIn(
            "research/skill-prototypes/iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md",
            iterative["package_reference_sources"],
        )

    def test_csw_descriptor_preserves_router_modules_assembly_boundary(self) -> None:
        csw = self.descriptors(self.manifest, "ja-JP")["cultural-substrate-weaving"]
        self.assertEqual(csw["assembly_mode"], "router_modules")
        self.assertEqual(csw["source_manifest"], "src/manifest.json")
        self.assertEqual(csw["package_reference_sources"], [])
        self.assertIsNone(csw["method_source"])

    def test_planned_realization_becomes_blocked_input(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["en-US"] = {"status": "planned"}

        descriptor = self.descriptors(manifest, "en-US")["affinity-synthesis"]
        self.assertEqual(descriptor["state"], "blocked-input")
        self.assertIsNone(descriptor["runtime_source"])
        self.assertEqual(descriptor["package_reference_sources"], [])


if __name__ == "__main__":
    unittest.main()
