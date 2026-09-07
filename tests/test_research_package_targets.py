from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_package_targets import validate_package_targets  # noqa: E402

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
CLAUDE_LOCALES_PATH = ROOT / "adapters" / "claude-code" / "locales.json"


class ResearchPackageTargetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def skill(self, manifest: dict, skill_id: str) -> dict:
        return next(skill for skill in manifest["skills"] if skill["id"] == skill_id)

    def assert_has_error(self, manifest: dict, fragment: str) -> None:
        errors = validate_package_targets(manifest)
        self.assertTrue(any(fragment in error for error in errors), f"expected {fragment!r}; got {errors!r}")

    def test_current_package_targets_are_internally_consistent(self) -> None:
        self.assertEqual(validate_package_targets(self.manifest), [])

    def test_realized_locale_requires_package_targets(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        self.skill(manifest, "affinity-synthesis")["locale_realizations"]["en-US"].pop("package_targets")
        self.assert_has_error(manifest, "realized locale en-US must declare package_targets")

    def test_planned_locale_cannot_carry_stale_package_targets(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        targets = copy.deepcopy(iterative["locale_realizations"]["en-US"]["package_targets"])
        iterative["locale_realizations"]["en-US"] = {"status": "planned", "package_targets": targets}
        self.assert_has_error(manifest, "planned locale en-US must not declare package_targets")

    def test_package_targets_must_cover_skill_tree_distributions_exactly(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        affinity["locale_realizations"]["ja-JP"]["package_targets"].pop("codex_plugin")
        self.assert_has_error(manifest, "package_targets must match Skill-tree distributions; missing=['codex_plugin']")

    def test_unsafe_target_name_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["locale_realizations"]["ja-JP"]["package_targets"]["openai_skill"]["skill_name"] = "../iterative-inquiry-synthesis"
        self.assert_has_error(manifest, "has unsafe skill_name")

    def test_target_name_collision_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        affinity = self.skill(manifest, "affinity-synthesis")
        iterative = self.skill(manifest, "iterative-inquiry-synthesis")
        iterative["locale_realizations"]["ja-JP"]["package_targets"]["claude_plugin"]["skill_name"] = affinity["locale_realizations"]["ja-JP"]["package_targets"]["claude_plugin"]["skill_name"]
        self.assert_has_error(manifest, "distribution claude_plugin target skill_name collision")

    def test_current_openai_targets_use_installable_names(self) -> None:
        for skill in self.manifest["skills"]:
            for locale, realization in skill["locale_realizations"].items():
                if realization["status"] == "planned":
                    continue
                self.assertEqual(realization["package_targets"]["openai_skill"]["skill_name"], skill["installable_name"], f"{skill['id']} {locale}")

    def test_csw_claude_and_codex_targets_match_existing_adapter(self) -> None:
        adapter_locales = json.loads(CLAUDE_LOCALES_PATH.read_text(encoding="utf-8"))
        csw = self.skill(self.manifest, "cultural-substrate-weaving")
        for locale, adapter in adapter_locales.items():
            expected = adapter["skill_name"]
            realization = csw["locale_realizations"][locale]
            self.assertEqual(realization["package_targets"]["claude_plugin"]["skill_name"], expected)
            self.assertEqual(realization["package_targets"]["codex_plugin"]["skill_name"], expected)

    def test_bilingual_sibling_targets_are_stable_candidate_names(self) -> None:
        for skill_id in ("affinity-synthesis", "iterative-inquiry-synthesis"):
            skill = self.skill(self.manifest, skill_id)
            for locale in ("ja-JP", "en-US"):
                targets = skill["locale_realizations"][locale]["package_targets"]
                self.assertEqual({entry["skill_name"] for entry in targets.values()}, {skill_id})


if __name__ == "__main__":
    unittest.main()
