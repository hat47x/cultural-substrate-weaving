from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_host_package import materialize_host_package  # noqa: E402

METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
SKILL_NAMES = (
    "cultural-substrate-weaving",
    "affinity-synthesis",
    "iterative-inquiry-synthesis",
)


def file_snapshot(root: Path, *, exclude: set[str] | None = None) -> dict[str, bytes]:
    excluded = exclude or set()
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() not in excluded
    }


class ResearchHostPackageCrossSurfaceParityTests(unittest.TestCase):
    def materialize(
        self,
        locale: str,
        distribution: str,
        *,
        profile: str | None = None,
    ) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "package"
        materialize_host_package(
            locale=locale,
            distribution_name=distribution,
            output_root=output,
            profile=profile,
            root=ROOT,
        )
        return output, temp

    def test_openai_profiles_share_identical_skill_tree_except_host_metadata(self) -> None:
        for locale in ("ja-JP", "en-US"):
            interactive, interactive_temp = self.materialize(
                locale,
                "openai_skill",
                profile="interactive",
            )
            metered, metered_temp = self.materialize(
                locale,
                "openai_skill",
                profile="metered",
            )
            self.addCleanup(interactive_temp.cleanup)
            self.addCleanup(metered_temp.cleanup)

            for skill_name in SKILL_NAMES:
                self.assertEqual(
                    file_snapshot(
                        interactive / skill_name,
                        exclude={"agents/openai.yaml"},
                    ),
                    file_snapshot(
                        metered / skill_name,
                        exclude={"agents/openai.yaml"},
                    ),
                    f"OpenAI profile changed Skill content for {locale}/{skill_name}",
                )

    def test_openai_metadata_is_byte_identical_to_declared_source(self) -> None:
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        declared = metadata["distributions"]["openai_skill"]["skills"]

        for locale in ("ja-JP", "en-US"):
            for profile in ("interactive", "metered"):
                output, temp = self.materialize(
                    locale,
                    "openai_skill",
                    profile=profile,
                )
                self.addCleanup(temp.cleanup)

                for skill_name in SKILL_NAMES:
                    source_relative = declared[skill_name][locale][profile]["source"]
                    source = ROOT / source_relative
                    packaged = output / skill_name / "agents" / "openai.yaml"
                    self.assertEqual(
                        packaged.read_bytes(),
                        source.read_bytes(),
                        f"OpenAI metadata drift for {skill_name}/{locale}/{profile}",
                    )

    def test_claude_and_codex_share_identical_skill_tree(self) -> None:
        for locale in ("ja-JP", "en-US"):
            claude, claude_temp = self.materialize(locale, "claude_plugin")
            codex, codex_temp = self.materialize(locale, "codex_plugin")
            self.addCleanup(claude_temp.cleanup)
            self.addCleanup(codex_temp.cleanup)

            self.assertEqual(
                file_snapshot(claude / "skills"),
                file_snapshot(codex / "skills"),
                f"Claude/Codex Skill tree diverged for {locale}",
            )

    def test_materialized_bundle_manifests_preserve_prototype_wording_and_version(self) -> None:
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        for locale in ("ja-JP", "en-US"):
            bundle_source = metadata["distributions"]["claude_plugin"]["locales"][locale][
                "prototype_source"
            ]
            bundle = json.loads((ROOT / bundle_source).read_text(encoding="utf-8"))

            claude, claude_temp = self.materialize(locale, "claude_plugin")
            codex, codex_temp = self.materialize(locale, "codex_plugin")
            self.addCleanup(claude_temp.cleanup)
            self.addCleanup(codex_temp.cleanup)

            claude_manifest = json.loads(
                (claude / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
            )
            codex_manifest = json.loads(
                (codex / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )

            self.assertEqual(claude_manifest["name"], bundle["plugin_name"])
            self.assertEqual(codex_manifest["name"], bundle["plugin_name"])
            self.assertEqual(claude_manifest["description"], bundle["description"])
            self.assertEqual(codex_manifest["description"], bundle["description"])
            self.assertEqual(codex_manifest["interface"]["displayName"], bundle["display"])
            self.assertEqual(codex_manifest["interface"]["shortDescription"], bundle["description"])
            self.assertEqual(claude_manifest["version"], version)
            self.assertEqual(codex_manifest["version"], version)


if __name__ == "__main__":
    unittest.main()
