from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RuntimeManifestStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            (ROOT / "src" / "manifest.json").read_text(encoding="utf-8")
        )
        self.canonical_root = ROOT / "src" / self.manifest["canonical_locale"]

    def test_modules_cover_all_canonical_non_router_markdown_once(self) -> None:
        canonical_files = {
            str(path.relative_to(self.canonical_root))
            for path in self.canonical_root.rglob("*.md")
        }
        expected_modules = canonical_files - {self.manifest["router"]}
        module_sources = [module["source"] for module in self.manifest["modules"]]

        self.assertEqual(len(module_sources), len(set(module_sources)))
        self.assertEqual(set(module_sources), expected_modules)

    def test_knowledge_groups_cover_all_modules_once(self) -> None:
        module_sources = [module["source"] for module in self.manifest["modules"]]
        grouped_sources = [
            source
            for group in self.manifest["knowledge_groups"].values()
            for source in group
        ]

        self.assertEqual(len(grouped_sources), len(set(grouped_sources)))
        self.assertEqual(set(grouped_sources), set(module_sources))


if __name__ == "__main__":
    unittest.main()
