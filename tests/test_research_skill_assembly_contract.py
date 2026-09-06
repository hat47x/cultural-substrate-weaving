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


class ResearchSkillAssemblyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def assert_has_error(self, manifest: dict, fragment: str) -> None:
        errors = validate_suite(ROOT, manifest)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_unknown_assembly_mode_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        self.skill(manifest, "affinity-synthesis")["assembly"]["mode"] = "future-mode"
        self.assert_has_error(manifest, "assembly mode must be one of")

    def test_router_modules_requires_source_manifest(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        csw = self.skill(manifest, "cultural-substrate-weaving")
        csw["assembly"].pop("source_manifest")
        self.assert_has_error(manifest, "assembly source_manifest must be a non-empty")

    def test_router_modules_source_manifest_stays_inside_skill_source_root(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        csw = self.skill(manifest, "cultural-substrate-weaving")
        csw["assembly"]["source_manifest"] = "CHANGELOG.md"
        self.assert_has_error(manifest, "assembly source_manifest is outside source_root")

    def test_direct_skill_does_not_accept_router_source_manifest(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["assembly"]["source_manifest"] = "research/skill-prototypes/affinity-synthesis/SKILL.md"
        self.assert_has_error(manifest, "direct_skill assembly must not declare source_manifest")


if __name__ == "__main__":
    unittest.main()
