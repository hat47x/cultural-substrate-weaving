from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_research_package_reference_closure import (  # noqa: E402
    validate_package_reference_closure,
)

MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


class ResearchPackageReferenceClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def package_files(self, skill_id: str, locale: str = "ja-JP") -> list[str]:
        skill = next(skill for skill in self.manifest["skills"] if skill["id"] == skill_id)
        return skill["locale_realizations"][locale]["package_source"]["files"]

    def assert_has_error(self, manifest: dict, fragment: str) -> None:
        errors = validate_package_reference_closure(ROOT, manifest)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_explicit_package_references_are_closed(self) -> None:
        self.assertEqual(validate_package_reference_closure(ROOT, self.manifest), [])

    def test_affinity_template_reference_must_be_packaged(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        files = self._files(manifest, "affinity-synthesis", "ja-JP")
        files.remove("references/TEMPLATE.md")
        self.assert_has_error(manifest, "references/TEMPLATE.md")

    def test_affinity_eval_reference_must_be_packaged(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        files = self._files(manifest, "affinity-synthesis", "ja-JP")
        files.remove("evals/CASES.md")
        self.assert_has_error(manifest, "evals/CASES.md")

    def test_iterative_round_template_reference_must_be_packaged(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        files = self._files(manifest, "iterative-inquiry-synthesis", "ja-JP")
        files.remove("references/ROUND-TEMPLATE.md")
        self.assert_has_error(manifest, "references/ROUND-TEMPLATE.md")

    def test_english_affinity_method_reference_must_be_packaged(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        files = self._files(manifest, "affinity-synthesis", "en-US")
        files.remove("references/METHOD.en.md")
        self.assert_has_error(manifest, "references/METHOD.en.md")

    def test_english_iterative_round_template_reference_must_be_packaged(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        files = self._files(manifest, "iterative-inquiry-synthesis", "en-US")
        files.remove("references/ROUND-TEMPLATE.en.md")
        self.assert_has_error(manifest, "references/ROUND-TEMPLATE.en.md")

    def test_declared_markdown_second_hop_reference_must_be_packaged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_root = root / "research" / "skill"
            (package_root / "references").mkdir(parents=True)
            (package_root / "evidence").mkdir(parents=True)
            (package_root / "SKILL.md").write_text(
                "See `references/METHOD.md`.\n",
                encoding="utf-8",
            )
            (package_root / "references" / "METHOD.md").write_text(
                "Design evidence is in `evidence/dossier.md`.\n",
                encoding="utf-8",
            )
            (package_root / "evidence" / "dossier.md").write_text(
                "research evidence\n",
                encoding="utf-8",
            )

            manifest = {
                "skills": [
                    {
                        "id": "example",
                        "locale_realizations": {
                            "ja-JP": {
                                "status": "prototype",
                                "runtime_entry": "research/skill/SKILL.md",
                                "package_source": {
                                    "mode": "explicit_files",
                                    "root": "research/skill",
                                    "files": ["SKILL.md", "references/METHOD.md"],
                                },
                            }
                        },
                    }
                ]
            }

            errors = validate_package_reference_closure(root, manifest)
            self.assertTrue(
                any("evidence/dossier.md" in error for error in errors),
                errors,
            )

            manifest["skills"][0]["locale_realizations"]["ja-JP"]["package_source"][
                "files"
            ].append("evidence/dossier.md")
            self.assertEqual(validate_package_reference_closure(root, manifest), [])

    def test_canonical_manifest_realizations_are_out_of_scope(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        skill = next(
            skill for skill in manifest["skills"] if skill["id"] == "cultural-substrate-weaving"
        )
        self.assertEqual(
            skill["locale_realizations"]["ja-JP"]["package_source"]["mode"],
            "canonical_manifest",
        )
        self.assertEqual(validate_package_reference_closure(ROOT, manifest), [])

    @staticmethod
    def _files(manifest: dict, skill_id: str, locale: str) -> list[str]:
        skill = next(skill for skill in manifest["skills"] if skill["id"] == skill_id)
        return skill["locale_realizations"][locale]["package_source"]["files"]


if __name__ == "__main__":
    unittest.main()