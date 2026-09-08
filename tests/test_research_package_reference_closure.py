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
    package_local_references,
    validate_in_memory_package_reference_closure,
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

    def test_shared_parser_normalizes_and_deduplicates_package_local_refs(self) -> None:
        text = (
            "Read `references/METHOD.md` and "
            "[the same method](references/METHOD.md#invariants). "
            "Also inspect `evals/CASES.md`. "
            "Ignore `https://example.com/references/REMOTE.md` and `src/manifest.json`."
        )
        self.assertEqual(
            package_local_references(text),
            {"references/METHOD.md", "evals/CASES.md"},
        )

    def test_in_memory_projected_package_closure_accepts_valid_tree(self) -> None:
        files = {
            "SKILL.md": "Read `references/METHOD.md`.\n",
            "references/METHOD.md": "[Detail](DETAIL.md)\n",
            "references/DETAIL.md": "detail\n",
        }
        self.assertEqual(
            validate_in_memory_package_reference_closure(
                files,
                "SKILL.md",
                label="projected fixture",
            ),
            [],
        )

    def test_in_memory_projected_runtime_rejects_stale_locale_suffix_reference(self) -> None:
        files = {
            "SKILL.md": "Read `references/METHOD.en.md`.\n",
            "references/METHOD.md": "method\n",
        }
        errors = validate_in_memory_package_reference_closure(
            files,
            "SKILL.md",
            label="projected fixture",
        )
        self.assertTrue(
            any(
                "runtime reference is missing" in error
                and "references/METHOD.en.md" in error
                for error in errors
            ),
            errors,
        )

    def test_in_memory_projected_markdown_link_rejects_missing_target(self) -> None:
        files = {
            "SKILL.md": "Read `references/METHOD.md`.\n",
            "references/METHOD.md": "[Detail](DETAIL.md)\n",
        }
        errors = validate_in_memory_package_reference_closure(
            files,
            "SKILL.md",
            label="projected fixture",
        )
        self.assertTrue(
            any(
                "packaged Markdown link is missing" in error
                and "references/DETAIL.md" in error
                for error in errors
            ),
            errors,
        )

    def test_in_memory_projected_markdown_link_cannot_escape_package_root(self) -> None:
        files = {
            "SKILL.md": "Read `references/METHOD.md`.\n",
            "references/METHOD.md": "[Outside](../../outside.md)\n",
        }
        errors = validate_in_memory_package_reference_closure(
            files,
            "SKILL.md",
            label="projected fixture",
        )
        self.assertTrue(
            any("packaged Markdown link escapes package root" in error for error in errors),
            errors,
        )

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

    def test_packaged_markdown_link_target_must_be_declared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "skill"
            refs = package / "references"
            refs.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                "Read `references/METHOD.md`.\n",
                encoding="utf-8",
            )
            (refs / "METHOD.md").write_text(
                "[Detail](DETAIL.md)\n",
                encoding="utf-8",
            )
            (refs / "DETAIL.md").write_text("detail\n", encoding="utf-8")
            manifest = self._fixture_manifest(
                ["SKILL.md", "references/METHOD.md"]
            )
            errors = validate_package_reference_closure(root, manifest)
            self.assertTrue(
                any("packaged Markdown link target is not included" in error for error in errors),
                errors,
            )

    def test_packaged_markdown_link_cannot_escape_package_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "skill"
            refs = package / "references"
            refs.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                "Read `references/METHOD.md`.\n",
                encoding="utf-8",
            )
            (refs / "METHOD.md").write_text(
                "[Outside](../../outside.md)\n",
                encoding="utf-8",
            )
            (root / "outside.md").write_text("outside\n", encoding="utf-8")
            manifest = self._fixture_manifest(
                ["SKILL.md", "references/METHOD.md"]
            )
            errors = validate_package_reference_closure(root, manifest)
            self.assertTrue(
                any("packaged Markdown link escapes package root" in error for error in errors),
                errors,
            )

    def test_external_markdown_link_does_not_become_package_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "skill"
            refs = package / "references"
            refs.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                "Read `references/METHOD.md`.\n",
                encoding="utf-8",
            )
            (refs / "METHOD.md").write_text(
                "[External](https://example.com/detail.md)\n",
                encoding="utf-8",
            )
            manifest = self._fixture_manifest(
                ["SKILL.md", "references/METHOD.md"]
            )
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
    def _fixture_manifest(files: list[str]) -> dict:
        return {
            "skills": [
                {
                    "id": "fixture-skill",
                    "locale_realizations": {
                        "ja-JP": {
                            "status": "prototype",
                            "runtime_entry": "skill/SKILL.md",
                            "package_source": {
                                "mode": "explicit_files",
                                "root": "skill",
                                "files": files,
                            },
                        }
                    },
                }
            ]
        }

    @staticmethod
    def _files(manifest: dict, skill_id: str, locale: str) -> list[str]:
        skill = next(skill for skill in manifest["skills"] if skill["id"] == skill_id)
        return skill["locale_realizations"][locale]["package_source"]["files"]


if __name__ == "__main__":
    unittest.main()
