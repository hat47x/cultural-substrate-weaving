from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from common import project_reference_links


class ReferenceProjectionTests(unittest.TestCase):
    def setUp(self):
        self.modules = [
            {"source": "frameworks/portfolio.md", "skill_reference": "04-portfolio.md"},
            {"source": "frameworks/yijing.md", "skill_reference": "04-yijing.md"},
            {"source": "methods/perspective-analysis.md", "skill_reference": "02b-perspective-analysis.md"},
            {"source": "domains/body.md", "skill_reference": "07-body.md"},
        ]

    def test_flat_projection_resolves_sibling_parent_and_root_pointers(self):
        source = "[Yi](yijing.md#changes) [Body](../domains/body.md) `methods/perspective-analysis.md`"
        projected = project_reference_links(source, self.modules, "frameworks/portfolio.md")
        self.assertEqual(projected, "[Yi](04-yijing.md#changes) [Body](07-body.md) `02b-perspective-analysis.md`")

    def test_external_urls_and_unregistered_assets_are_preserved(self):
        source = "[Source](https://example.org/methods/perspective-analysis.md) [Other](unregistered.md)"
        self.assertEqual(project_reference_links(source, self.modules, "frameworks/portfolio.md"), source)

    def test_group_projection_handles_legacy_flat_aliases(self):
        modules = [{"source": "methods/perspective-analysis.md", "skill_reference": "01-perspectives.md", "aliases": ["02b-perspective-analysis.md"]}]
        source = "`methods/perspective-analysis.md` and `02b-perspective-analysis.md`"
        self.assertEqual(project_reference_links(source, modules, "methods/application.md"), "`01-perspectives.md` and `01-perspectives.md`")
