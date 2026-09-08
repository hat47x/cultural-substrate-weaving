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

from plan_production_source_promotion import plan_production_source_promotion  # noqa: E402
from preview_production_source_projection import (  # noqa: E402
    ProjectionError,
    apply_content_transforms,
    build_preview,
    project_production_source_contents,
    validate_projected_contents,
)

BASE = ROOT / "research" / "skill-prototypes"
SUITE_PATH = BASE / "suite-manifest.json"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
MIGRATION_PATH = BASE / "P4-PUBLIC-NAME-MIGRATION-CONTRACT.json"
INVENTORY_PATH = BASE / "P4-PUBLIC-NAME-PROJECTION-INVENTORY.json"


class ResearchProductionSourceProjectionPreviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))
        self.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        self.plan = plan_production_source_promotion(
            self.suite,
            self.descriptor,
            self.migration,
            self.inventory,
        )
        self.projected = project_production_source_contents(self.plan)

    def target(self, suffix: str) -> dict:
        return next(item for path, item in self.projected.items() if path.endswith(suffix))

    def test_current_projection_is_valid(self) -> None:
        self.assertEqual(validate_projected_contents(self.projected, self.plan), [])
        preview = build_preview()
        self.assertEqual(preview["schema"], "csw.production-source-content-preview/v1")
        self.assertFalse(preview["writes_production_source"])
        self.assertTrue(preview["files"])
        self.assertTrue(all("content" not in item for item in preview["files"]))

    def test_layer1_frontmatter_changes_but_display_title_remains_affinity_synthesis(self) -> None:
        ja = self.projected["src/skills/material-led-synthesis/ja-JP/SKILL.md"]["content"]
        en = self.projected["src/skills/material-led-synthesis/en-US/SKILL.md"]["content"]
        for text in (ja, en):
            self.assertIn("name: material-led-synthesis", text)
            self.assertNotIn("name: affinity-synthesis", text)
            self.assertIn("# Affinity Synthesis", text)

    def test_layer1_japanese_progressive_support_uses_production_installable_name(self) -> None:
        for target in (
            "src/skills/material-led-synthesis/ja-JP/evals/CASES.md",
            "src/skills/material-led-synthesis/ja-JP/evidence/dossier.md",
        ):
            text = self.projected[target]["content"]
            self.assertIn("`material-led-synthesis`", text)
            self.assertNotIn("`affinity-synthesis`", text)

    def test_layer2_english_runtime_rewrites_installable_name_and_package_local_refs(self) -> None:
        text = self.projected[
            "src/skills/iterative-inquiry-synthesis/en-US/SKILL.md"
        ]["content"]
        self.assertIn("`material-led-synthesis`", text)
        self.assertNotIn("`affinity-synthesis`", text)
        self.assertIn("companion Skill `material-led-synthesis`", text)
        self.assertNotIn("../affinity-synthesis/", text)
        self.assertIn("references/METHOD.md", text)
        self.assertIn("references/ROUND-TEMPLATE.md", text)
        self.assertNotIn(".en.md", text)

    def test_projected_runtime_rejects_missing_reference_added_after_transform(self) -> None:
        projected = copy.deepcopy(self.projected)
        target = "src/skills/iterative-inquiry-synthesis/en-US/SKILL.md"
        projected[target]["content"] += "\nRead `references/DOES-NOT-EXIST.md` when needed.\n"
        errors = validate_projected_contents(projected, self.plan)
        self.assertTrue(
            any(
                "projected package runtime reference is missing after transforms" in error
                and "references/DOES-NOT-EXIST.md" in error
                for error in errors
            ),
            errors,
        )

    def test_projected_runtime_rejects_dropped_known_reference_target(self) -> None:
        projected = copy.deepcopy(self.projected)
        del projected["src/skills/material-led-synthesis/ja-JP/references/TEMPLATE.md"]
        errors = validate_projected_contents(projected, self.plan)
        self.assertTrue(
            any(
                "projected package runtime reference is missing after transforms" in error
                and "references/TEMPLATE.md" in error
                for error in errors
            ),
            errors,
        )

    def test_layer2_method_rewrites_realization_identifier_not_method_display_term(self) -> None:
        for locale in ("ja-JP", "en-US"):
            text = self.projected[
                f"src/skills/iterative-inquiry-synthesis/{locale}/references/METHOD.md"
            ]["content"]
            self.assertIn("material-led-synthesis", text)
            self.assertNotIn("`affinity-synthesis`", text)
        en = self.projected[
            "src/skills/iterative-inquiry-synthesis/en-US/references/METHOD.md"
        ]["content"]
        self.assertIn("## Relationship to Affinity Synthesis", en)

    def test_any_projected_package_file_rejects_old_backtick_installable_id(self) -> None:
        projected = copy.deepcopy(self.projected)
        target = "src/skills/material-led-synthesis/ja-JP/evals/CASES.md"
        projected[target]["content"] += "\nlegacy `affinity-synthesis` identifier\n"
        errors = validate_projected_contents(projected, self.plan)
        self.assertTrue(
            any("retains research installable identifier" in error for error in errors),
            errors,
        )

    def test_any_projected_package_file_rejects_research_sibling_path(self) -> None:
        projected = copy.deepcopy(self.projected)
        target = "src/skills/material-led-synthesis/ja-JP/evidence/dossier.md"
        projected[target]["content"] += "\n../affinity-synthesis/\n"
        errors = validate_projected_contents(projected, self.plan)
        self.assertTrue(
            any("retains research sibling filesystem path" in error for error in errors),
            errors,
        )

    def test_projection_is_in_memory_and_does_not_create_production_source(self) -> None:
        self.assertFalse((ROOT / "src/skills/material-led-synthesis").exists())
        self.assertFalse((ROOT / "src/skills/iterative-inquiry-synthesis").exists())

    def test_unknown_transform_is_rejected(self) -> None:
        with self.assertRaisesRegex(ProjectionError, "unsupported production source content transform"):
            apply_content_transforms(
                "sample",
                ["unknown-transform"],
                source="sample.md",
                production_name="material-led-synthesis",
            )

    def test_required_transform_marker_cannot_silently_disappear(self) -> None:
        with self.assertRaisesRegex(ProjectionError, "required marker missing"):
            apply_content_transforms(
                "no installable reference here",
                ["rewrite-explicit-installable-name"],
                source="sample.md",
                production_name="iterative-inquiry-synthesis",
            )


if __name__ == "__main__":
    unittest.main()
