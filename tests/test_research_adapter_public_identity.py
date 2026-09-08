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

from validate_research_adapter_public_identity import (  # noqa: E402
    renamed_skill_ids,
    validate_adapter_public_identity,
    validate_host_visible_text,
)

BASE = ROOT / "research" / "skill-prototypes"
DESCRIPTOR_PATH = BASE / "P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json"
ADAPTER_PLAN_PATH = BASE / "adapter-metadata-plan.json"


class ResearchAdapterPublicIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.descriptor = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
        self.adapter_plan = json.loads(ADAPTER_PLAN_PATH.read_text(encoding="utf-8"))

    def test_current_host_visible_metadata_has_no_renamed_research_id_leak(self) -> None:
        self.assertEqual(
            validate_adapter_public_identity(ROOT, self.descriptor, self.adapter_plan),
            [],
        )

    def test_layer1_research_id_maps_to_material_led_public_name(self) -> None:
        mapping = renamed_skill_ids(self.descriptor)
        self.assertEqual(mapping.get("affinity-synthesis"), "material-led-synthesis")

    def test_exact_hyphenated_research_id_is_rejected_in_host_visible_prose(self) -> None:
        errors = validate_host_visible_text(
            "fixture",
            "Use affinity-synthesis for this task.",
            {"affinity-synthesis": "material-led-synthesis"},
        )
        self.assertTrue(any("leaks renamed research id" in error for error in errors), errors)

    def test_display_term_affinity_synthesis_remains_allowed(self) -> None:
        self.assertEqual(
            validate_host_visible_text(
                "fixture",
                "Use Affinity Synthesis for this task.",
                {"affinity-synthesis": "material-led-synthesis"},
            ),
            [],
        )

    def test_research_contains_field_is_not_treated_as_host_visible_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openai.yaml").write_text(
                'interface:\n  display_name: "Affinity Synthesis"\n',
                encoding="utf-8",
            )
            (root / "bundle.json").write_text(
                json.dumps(
                    {
                        "description": "Three complementary Skills for cultural exploration and synthesis.",
                        "contains": ["affinity-synthesis"],
                    }
                ),
                encoding="utf-8",
            )
            descriptor = {
                "skills": [
                    {
                        "research_id": "affinity-synthesis",
                        "proposed_installable_name": "material-led-synthesis",
                    }
                ]
            }
            adapter_plan = {
                "distributions": {
                    "openai_skill": {
                        "skills": {
                            "affinity-synthesis": {
                                "ja-JP": {
                                    "interactive": {"source": "openai.yaml"}
                                }
                            }
                        }
                    },
                    "claude_plugin": {
                        "locales": {
                            "ja-JP": {"prototype_source": "bundle.json"}
                        }
                    },
                }
            }
            self.assertEqual(
                validate_adapter_public_identity(root, descriptor, adapter_plan),
                [],
            )

    def test_openai_and_bundle_description_leaks_are_both_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Invoke affinity-synthesis."\n',
                encoding="utf-8",
            )
            (root / "bundle.json").write_text(
                json.dumps(
                    {
                        "description": "Bundle includes affinity-synthesis.",
                        "contains": ["affinity-synthesis"],
                    }
                ),
                encoding="utf-8",
            )
            descriptor = {
                "skills": [
                    {
                        "research_id": "affinity-synthesis",
                        "proposed_installable_name": "material-led-synthesis",
                    }
                ]
            }
            adapter_plan = {
                "distributions": {
                    "openai_skill": {
                        "skills": {
                            "affinity-synthesis": {
                                "ja-JP": {
                                    "interactive": {"source": "openai.yaml"}
                                }
                            }
                        }
                    },
                    "claude_plugin": {
                        "locales": {
                            "ja-JP": {"prototype_source": "bundle.json"}
                        }
                    },
                }
            }
            errors = validate_adapter_public_identity(root, descriptor, adapter_plan)
            self.assertGreaterEqual(
                sum("leaks renamed research id" in error for error in errors),
                2,
                errors,
            )


if __name__ == "__main__":
    unittest.main()
