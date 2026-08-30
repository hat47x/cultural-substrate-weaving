from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("ja-JP", "en-US")
MANIFEST = json.loads((ROOT / "src/manifest.json").read_text(encoding="utf-8"))
EXPECTED_REFERENCES = {module["skill_reference"] for module in MANIFEST["modules"]}
REPOSITORY_ONLY_PARTS = {"docs", "evals", "tests", ".github", "maintainers"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def markdown_filenames(path: Path) -> set[str]:
    return {item.name for item in path.glob("*.md") if item.is_file()}


def local_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        links.append(target)
    return links


def generated_skill_paths() -> list[Path]:
    paths: list[Path] = []
    for locale in LOCALES:
        for profile in ("interactive", "metered"):
            paths.append(
                ROOT
                / f"dist/{locale}/openai-skill/{profile}/cultural-substrate-weaving/SKILL.md"
            )
    for plugin_root in sorted((ROOT / "plugins").glob("cultural-substrate-weaving-*")):
        paths.extend(sorted((plugin_root / "skills").glob("*/SKILL.md")))
    return paths


class MultilingualBuildTests(unittest.TestCase):
    def test_openai_profiles_exist_for_each_locale(self):
        for locale in LOCALES:
            for profile in ("interactive", "metered"):
                self.assertTrue(
                    (ROOT / f"dist/{locale}/openai-skill/{profile}/cultural-substrate-weaving/SKILL.md").exists()
                )

    def test_locale_source_trees_are_parallel(self):
        ja = {
            str(path.relative_to(ROOT / "src/ja-JP"))
            for path in (ROOT / "src/ja-JP").rglob("*.md")
        }
        en = {
            str(path.relative_to(ROOT / "src/en-US"))
            for path in (ROOT / "src/en-US").rglob("*.md")
        }
        self.assertEqual(ja, en)

    def test_claude_marketplace_contains_both_locales(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {plugin["name"] for plugin in marketplace["plugins"]},
            {"cultural-substrate-weaving-ja", "cultural-substrate-weaving-en"},
        )

    def test_m365_instruction_limit_for_each_locale(self):
        for locale in LOCALES:
            path = ROOT / f"dist/{locale}/microsoft-copilot/agent-project/appPackage/declarativeAgent.json"
            agent = json.loads(path.read_text(encoding="utf-8"))
            self.assertLessEqual(len(agent["instructions"]), 8000)

    def test_gpt_knowledge_group_count_for_each_locale(self):
        for locale in LOCALES:
            files = list((ROOT / f"dist/{locale}/chatgpt-gpt/knowledge").glob("*.md"))
            self.assertEqual(len(files), 4)

    def test_skill_frontmatter_uses_expected_language_description(self):
        ja = (ROOT / "dist/ja-JP/openai-skill/metered/cultural-substrate-weaving/SKILL.md").read_text(encoding="utf-8")
        en = (ROOT / "dist/en-US/openai-skill/metered/cultural-substrate-weaving/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("文化的体系", ja)
        self.assertIn("KJ法", ja)
        self.assertIn("cultural frameworks", en)
        self.assertIn("KJ", en)

    def test_openai_reference_sets_match_manifest(self):
        for locale in LOCALES:
            for profile in ("interactive", "metered"):
                references = (
                    ROOT
                    / f"dist/{locale}/openai-skill/{profile}/cultural-substrate-weaving/references"
                )
                self.assertEqual(
                    markdown_filenames(references),
                    EXPECTED_REFERENCES,
                    f"unexpected OpenAI reference set for {locale}/{profile}",
                )

    def test_generated_plugin_reference_sets_match_manifest(self):
        plugin_roots = sorted((ROOT / "plugins").glob("cultural-substrate-weaving-*"))
        self.assertTrue(plugin_roots)
        for plugin_root in plugin_roots:
            skill_roots = [path for path in (plugin_root / "skills").iterdir() if path.is_dir()]
            self.assertEqual(len(skill_roots), 1, f"unexpected skill count in {plugin_root}")
            self.assertEqual(
                markdown_filenames(skill_roots[0] / "references"),
                EXPECTED_REFERENCES,
                f"unexpected plugin reference set in {plugin_root}",
            )

    def test_generated_skill_local_links_resolve_inside_package(self):
        skill_paths = generated_skill_paths()
        self.assertEqual(len(skill_paths), 6)
        for skill_path in skill_paths:
            package_root = skill_path.parent.resolve()
            text = skill_path.read_text(encoding="utf-8")
            for target in local_markdown_links(text):
                path_part = target.split("#", 1)[0]
                if not path_part:
                    continue
                resolved = (skill_path.parent / path_part).resolve()
                self.assertTrue(
                    resolved.is_relative_to(package_root),
                    f"local link escapes runtime package in {skill_path}: {target}",
                )
                self.assertTrue(
                    resolved.is_file(),
                    f"broken local link in {skill_path}: {target}",
                )
                if Path(path_part).parts and Path(path_part).parts[0] == "references":
                    self.assertIn(
                        Path(path_part).name,
                        EXPECTED_REFERENCES,
                        f"unmanifested reference link in {skill_path}: {target}",
                    )

    def test_repository_only_material_is_not_emitted_as_runtime_files(self):
        offenders: list[str] = []
        for runtime_root in (ROOT / "dist", ROOT / "plugins"):
            for path in runtime_root.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(runtime_root)
                if REPOSITORY_ONLY_PARTS.intersection(relative.parts):
                    offenders.append(f"{runtime_root.name}/{relative}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
