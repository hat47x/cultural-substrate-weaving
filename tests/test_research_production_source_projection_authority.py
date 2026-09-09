from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from preview_production_source_projection import (  # noqa: E402
    project_production_source_contents,
    validate_projected_contents,
)


class ResearchProductionSourceProjectionAuthorityTests(unittest.TestCase):
    def test_projection_selection_follows_source_plan_state_not_research_id(self) -> None:
        plan = {
            "skills": [
                {
                    "research_id": "existing-canonical-skill",
                    "production_name": "existing-canonical-skill",
                    "state": "existing-canonical-manifest",
                    "locales": {
                        "ja-JP": {
                            "runtime_entry": "must-not-be-projected/SKILL.md",
                            "mappings": [
                                {
                                    "source": "missing/SKILL.md",
                                    "target": "must-not-be-projected/SKILL.md",
                                    "target_relative": "SKILL.md",
                                    "content_transforms": [],
                                }
                            ],
                        }
                    },
                },
                {
                    "research_id": "old-skill",
                    "production_name": "new-skill",
                    "state": "planned-locale-tree-promotion",
                    "locales": {
                        "ja-JP": {
                            "runtime_entry": "src/skills/new-skill/ja-JP/SKILL.md",
                            "mappings": [
                                {
                                    "source": "old/SKILL.md",
                                    "target": "src/skills/new-skill/ja-JP/SKILL.md",
                                    "target_relative": "SKILL.md",
                                    "content_transforms": ["rewrite-frontmatter-name-only"],
                                }
                            ],
                        }
                    },
                },
            ]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "old" / "SKILL.md"
            source.parent.mkdir(parents=True)
            source.write_text("---\nname: old-skill\n---\n# Friendly Display\n", encoding="utf-8")

            projected = project_production_source_contents(plan, root=root)

        self.assertEqual(
            set(projected),
            {"src/skills/new-skill/ja-JP/SKILL.md"},
        )
        self.assertIn(
            "name: new-skill",
            projected["src/skills/new-skill/ja-JP/SKILL.md"]["content"],
        )
        self.assertEqual(validate_projected_contents(projected, plan), [])


if __name__ == "__main__":
    unittest.main()
