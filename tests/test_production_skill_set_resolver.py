from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_production_skill_set_legacy_parity import validate_legacy_parity  # noqa: E402
from common import manifest as legacy_manifest  # noqa: E402
from production_skill_set import resolve_production_skills  # noqa: E402


class ProductionSkillSetResolverTests(unittest.TestCase):
    def test_current_resolver_matches_legacy_manifest_exactly(self) -> None:
        resolved = resolve_production_skills(ROOT)
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["id"], "cultural-substrate-weaving")
        self.assertEqual(resolved[0]["source_manifest"], "src/manifest.json")
        self.assertEqual(resolved[0]["manifest"], legacy_manifest())
        self.assertEqual(validate_legacy_parity(ROOT), [])

    def test_resolver_preserves_descriptor_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            self._write_manifest(root / "src" / "one.json", "one")
            self._write_manifest(root / "src" / "two.json", "two")
            self._write_descriptor(
                root,
                [
                    {"id": "two", "source_manifest": "src/two.json"},
                    {"id": "one", "source_manifest": "src/one.json"},
                ],
            )

            resolved = resolve_production_skills(root)
            self.assertEqual([item["id"] for item in resolved], ["two", "one"])

    def test_resolver_fails_closed_on_invalid_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            self._write_manifest(root / "src" / "manifest.json", "cultural-substrate-weaving")
            (root / "src" / "skill-set.json").write_text(
                json.dumps(
                    {
                        "schema": "csw.production-skill-set/v1",
                        "skills": [
                            {
                                "id": "cultural-substrate-weaving",
                                "source_manifest": "src/manifest.json",
                                "research_state": "candidate",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "invalid production Skill-set"):
                resolve_production_skills(root)

    def test_legacy_bridge_blocks_multi_skill_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "src").mkdir()
            self._write_manifest(root / "src" / "one.json", "one")
            self._write_manifest(root / "src" / "two.json", "two")
            self._write_descriptor(
                root,
                [
                    {"id": "one", "source_manifest": "src/one.json"},
                    {"id": "two", "source_manifest": "src/two.json"},
                ],
            )

            errors = validate_legacy_parity(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("requires exactly one Skill", errors[0])
            self.assertIn("replace this gate intentionally", errors[0])

    @staticmethod
    def _write_manifest(path: Path, skill_id: str) -> None:
        path.write_text(
            json.dumps(
                {
                    "name": skill_id,
                    "canonical_locale": "ja-JP",
                    "locales": {"ja-JP": {}},
                }
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _write_descriptor(root: Path, skills: list[dict]) -> None:
        (root / "src" / "skill-set.json").write_text(
            json.dumps(
                {
                    "schema": "csw.production-skill-set/v1",
                    "skills": skills,
                }
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
