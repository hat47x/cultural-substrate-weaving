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

from validate_research_release_composition_plan import (  # noqa: E402
    validate_release_composition_plan,
)

BASE = ROOT / "research" / "skill-prototypes"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
PLAN_PATH = BASE / "P4-RELEASE-INTERNAL-COMPOSITION-PLAN-2026-09-07.md"
PACKAGE_PATH = ROOT / "scripts" / "package.py"


class ResearchReleaseCompositionPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.plan_text = PLAN_PATH.read_text(encoding="utf-8")
        self.package_text = PACKAGE_PATH.read_text(encoding="utf-8")

    def errors(
        self,
        *,
        descriptor: dict | None = None,
        plan_text: str | None = None,
        package_text: str | None = None,
    ) -> list[str]:
        return validate_release_composition_plan(
            self.descriptor if descriptor is None else descriptor,
            self.plan_text if plan_text is None else plan_text,
            self.package_text if package_text is None else package_text,
        )

    def assert_has_error(self, fragment: str, **kwargs) -> None:
        errors = self.errors(**kwargs)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_release_composition_contract_is_valid(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_three_skill_release_shape_flag_cannot_be_disabled(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        descriptor["release_shape"]["openai_package_contains_three_standalone_skills"] = False
        self.assert_has_error(
            "openai_package_contains_three_standalone_skills",
            descriptor=descriptor,
        )

    def test_layer1_public_directory_cannot_disappear_from_release_plan(self) -> None:
        plan_text = self.plan_text.replace("material-led-synthesis/", "missing-layer1/")
        self.assert_has_error(
            "missing OpenAI Skill directory: material-led-synthesis",
            plan_text=plan_text,
        )

    def test_openai_skill_directory_follows_descriptor_target_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        layer1["targets"]["openai_skill"] = "material-led-release"
        plan_text = self.plan_text + "\nmaterial-led-release/\n"
        errors = self.errors(descriptor=descriptor, plan_text=plan_text)
        self.assertFalse(
            any("missing OpenAI Skill directory: material-led-release" in error for error in errors),
            errors,
        )

    def test_claude_skill_subtree_follows_descriptor_target_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        csw = next(
            item
            for item in descriptor["skills"]
            if item["research_id"] == "cultural-substrate-weaving"
        )
        csw["targets"]["claude_plugin"] = "weave-next"
        csw["targets"]["codex_plugin"] = "weave-next"
        plan_text = self.plan_text.replace("    weave/", "    weave-next/")
        self.assertEqual(self.errors(descriptor=descriptor, plan_text=plan_text), [])

    def test_codex_targets_must_match_claude_subtree_targets(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        layer1["targets"]["codex_plugin"] = "material-led-codex-only"
        self.assert_has_error(
            "Codex release Skill targets must match Claude subtree targets",
            descriptor=descriptor,
        )

    def test_research_layer1_id_cannot_reenter_as_installable_release_directory(self) -> None:
        plan_text = self.plan_text + "\naffinity-synthesis/\n  SKILL.md\n"
        self.assert_has_error("stale/forbidden marker", plan_text=plan_text)

    def test_renamed_research_id_forbidden_marker_follows_descriptor_authority(self) -> None:
        descriptor = copy.deepcopy(self.descriptor)
        layer1 = next(
            item for item in descriptor["skills"] if item["research_id"] == "affinity-synthesis"
        )
        layer1["research_id"] = "legacy-affinity-research"
        plan_text = self.plan_text + "\nlegacy-affinity-research/\n  SKILL.md\n"
        self.assert_has_error(
            "stale/forbidden marker",
            descriptor=descriptor,
            plan_text=plan_text,
        )

    def test_current_openai_package_filename_family_cannot_change_silently(self) -> None:
        package_text = self.package_text.replace(
            "cultural-substrate-weaving-openai-interactive-{suffix}-v{v}.zip",
            "method-suite-openai-interactive-{suffix}-v{v}.zip",
        )
        self.assert_has_error("package filename family", package_text=package_text)

    def test_separate_codex_release_zip_kind_is_rejected(self) -> None:
        package_text = self.package_text + (
            '\npackages / f"cultural-substrate-weaving-codex-plugin-{suffix}-v{v}.zip"\n'
        )
        self.assert_has_error("separate Codex release ZIP kind", package_text=package_text)

    def test_release_plan_cannot_claim_a_separate_codex_zip(self) -> None:
        plan_text = self.plan_text + (
            "\ncultural-substrate-weaving-codex-plugin-<locale>-v<version>.zip\n"
        )
        self.assert_has_error("stale/forbidden marker", plan_text=plan_text)


if __name__ == "__main__":
    unittest.main()
