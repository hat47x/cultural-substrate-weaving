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

from build import canonical_reference_files, write_skill_tree  # noqa: E402
from common import replace_router_links  # noqa: E402

MANIFEST = json.loads((ROOT / "src" / "manifest.json").read_text(encoding="utf-8"))


def legacy_frontmatter(name: str, description: str, *, explicit: bool = False) -> str:
    lines = ["---", f"name: {name}", f"description: {description}"]
    if explicit:
        lines.append("disable-model-invocation: true")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


class GenericSkillTreeWriterTests(unittest.TestCase):
    def test_writer_uses_resolved_name_description_body_and_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_a = root / "source-a.md"
            source_b = root / "source-b.md"
            source_a.write_text("alpha\n", encoding="utf-8")
            source_b.write_text("beta\n", encoding="utf-8")
            target = root / "skill"

            write_skill_tree(
                target,
                name="example-skill",
                description="example description",
                body="# Body\n\nResolved body.\n",
                references=[
                    (source_a, "00-a.md"),
                    (source_b, "10-b.md"),
                ],
            )

            entry = (target / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(entry.startswith("---\nname: example-skill\n"))
            self.assertIn("description: example description", entry)
            self.assertIn("# Body\n\nResolved body.\n", entry)
            self.assertNotIn("disable-model-invocation:", entry)
            self.assertEqual((target / "references" / "00-a.md").read_bytes(), b"alpha\n")
            self.assertEqual((target / "references" / "10-b.md").read_bytes(), b"beta\n")

    def test_explicit_invocation_is_only_a_frontmatter_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "skill"
            write_skill_tree(
                target,
                name="example-skill",
                description="example description",
                body="# Body\n",
                references=[],
                explicit_invocation=True,
            )

            entry = (target / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(entry.count("disable-model-invocation: true"), 1)
            self.assertTrue(entry.endswith("# Body\n"))

    def test_canonical_reference_files_preserve_manifest_order_and_names(self) -> None:
        references = canonical_reference_files("ja-JP", MANIFEST)
        expected = [
            (
                ROOT / "src" / "ja-JP" / module["source"],
                module["skill_reference"],
            )
            for module in MANIFEST["modules"]
        ]
        self.assertEqual(references, expected)

    def test_writer_does_not_require_csw_specific_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "affinity-synthesis"
            write_skill_tree(
                target,
                name="affinity-synthesis",
                description="one-round material-led synthesis",
                body="# Affinity Synthesis\n",
                references=[],
            )
            entry = (target / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("name: affinity-synthesis", entry)
            self.assertNotIn("cultural-substrate-weaving", entry)

    def test_current_csw_openai_tree_matches_legacy_rendering_formula(self) -> None:
        for locale in ("ja-JP", "en-US"):
            source_root = ROOT / "src" / locale
            router = (source_root / MANIFEST["router"]).read_text(encoding="utf-8")
            body = replace_router_links(router, MANIFEST["modules"])
            description = MANIFEST["locales"][locale]["description"]

            with tempfile.TemporaryDirectory() as temp_dir:
                target = Path(temp_dir) / "cultural-substrate-weaving"
                write_skill_tree(
                    target,
                    name="cultural-substrate-weaving",
                    description=description,
                    body=body,
                    references=canonical_reference_files(locale, MANIFEST),
                )

                expected_entry = (
                    legacy_frontmatter("cultural-substrate-weaving", description) + body
                ).encode("utf-8")
                self.assertEqual((target / "SKILL.md").read_bytes(), expected_entry)

                expected_references = {
                    module["skill_reference"]: (source_root / module["source"]).read_bytes()
                    for module in MANIFEST["modules"]
                }
                actual_references = {
                    path.name: path.read_bytes()
                    for path in (target / "references").glob("*.md")
                }
                self.assertEqual(actual_references, expected_references)

    def test_current_csw_claude_tree_matches_legacy_rendering_formula(self) -> None:
        for locale in ("ja-JP", "en-US"):
            source_root = ROOT / "src" / locale
            router = (source_root / MANIFEST["router"]).read_text(encoding="utf-8")
            body = replace_router_links(router, MANIFEST["modules"])
            description = MANIFEST["locales"][locale]["description"]

            with tempfile.TemporaryDirectory() as temp_dir:
                target = Path(temp_dir) / "weave"
                write_skill_tree(
                    target,
                    name="weave",
                    description=description,
                    body=body,
                    references=canonical_reference_files(locale, MANIFEST),
                    explicit_invocation=True,
                )

                expected_entry = (
                    legacy_frontmatter("weave", description, explicit=True) + body
                ).encode("utf-8")
                self.assertEqual((target / "SKILL.md").read_bytes(), expected_entry)


if __name__ == "__main__":
    unittest.main()
