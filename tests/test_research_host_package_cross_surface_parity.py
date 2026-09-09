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

from materialize_host_package import (  # noqa: E402
    READY_BUNDLE_METADATA,
    READY_OPENAI_METADATA,
    materialize_host_package,
)

METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"


def file_snapshot(root: Path, *, exclude: set[str] | None = None) -> dict[str, bytes]:
    excluded = exclude or set()
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() not in excluded
    }


def suite() -> dict:
    return json.loads(SUITE_PATH.read_text(encoding="utf-8"))


def metadata_plan() -> dict:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def declared_openai_profiles(metadata: dict | None = None) -> tuple[str, ...]:
    source = metadata_plan() if metadata is None else metadata
    config = source.get("distributions", {}).get("openai_skill")
    if not isinstance(config, dict):
        raise AssertionError("adapter metadata plan must declare openai_skill")
    profiles = config.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise AssertionError("OpenAI adapter metadata plan must declare profiles")
    return tuple(profiles)


def target_mappings(locale: str, distribution: str) -> tuple[tuple[str, str], ...]:
    mappings: list[tuple[str, str]] = []
    for skill in suite().get("skills", []):
        if not isinstance(skill, dict):
            continue
        skill_id = skill.get("id")
        realization = skill.get("locale_realizations", {}).get(locale)
        if not isinstance(skill_id, str) or not isinstance(realization, dict):
            continue
        if realization.get("status") == "planned":
            continue
        target = realization.get("package_targets", {}).get(distribution)
        if not isinstance(target, dict) or not isinstance(target.get("skill_name"), str):
            raise AssertionError(f"missing package target for {skill_id}/{locale}/{distribution}")
        mappings.append((skill_id, target["skill_name"]))
    return tuple(mappings)


def runtime_target_complete(locale: str, distribution: str) -> bool:
    skills = [skill for skill in suite().get("skills", []) if isinstance(skill, dict)]
    if not skills:
        return False
    for skill in skills:
        skill_id = skill.get("id")
        realization = skill.get("locale_realizations", {}).get(locale)
        if not isinstance(skill_id, str) or not isinstance(realization, dict):
            return False
        if realization.get("status") == "planned":
            return False
        target = realization.get("package_targets", {}).get(distribution)
        if not isinstance(target, dict) or not isinstance(target.get("skill_name"), str):
            return False
    return True


def host_metadata_ready(locale: str, distribution: str) -> bool:
    metadata = metadata_plan()
    config = metadata.get("distributions", {}).get(distribution)
    if not isinstance(config, dict):
        return False

    if distribution == "openai_skill":
        declared = config.get("skills")
        if not isinstance(declared, dict):
            return False
        for skill_id, _ in target_mappings(locale, distribution):
            locale_entry = declared.get(skill_id, {}).get(locale)
            if not isinstance(locale_entry, dict):
                return False
            for profile in declared_openai_profiles(metadata):
                entry = locale_entry.get(profile)
                if not isinstance(entry, dict) or entry.get("status") not in READY_OPENAI_METADATA:
                    return False
        return True

    locale_entry = config.get("locales", {}).get(locale)
    return isinstance(locale_entry, dict) and locale_entry.get("status") in READY_BUNDLE_METADATA


def materializable_locales(distribution: str) -> tuple[str, ...]:
    return tuple(
        locale
        for locale in suite().get("locales", {})
        if runtime_target_complete(locale, distribution)
        and host_metadata_ready(locale, distribution)
    )


def shared_materializable_locales(*distributions: str) -> tuple[str, ...]:
    if not distributions:
        return ()
    sets = [set(materializable_locales(distribution)) for distribution in distributions]
    return tuple(sorted(set.intersection(*sets)))


def declared_bundle_metadata(metadata: dict, distribution: str, locale: str) -> dict:
    config = metadata["distributions"][distribution]
    locale_entry = config["locales"][locale]
    status = locale_entry["status"]

    if status == "prototype":
        source = ROOT / locale_entry["prototype_source"]
        return json.loads(source.read_text(encoding="utf-8"))

    if status == "reviewed":
        source = ROOT / config["source"]
        catalog = json.loads(source.read_text(encoding="utf-8"))
        return catalog[locale]

    raise AssertionError(
        f"{distribution}/{locale} is not expected to be host-materializable: {status!r}"
    )


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
        profiles = sorted(declared_openai_profiles())
        for locale in materializable_locales("openai_skill"):
            outputs: dict[str, Path] = {}
            for profile in profiles:
                output, temp = self.materialize(locale, "openai_skill", profile=profile)
                self.addCleanup(temp.cleanup)
                outputs[profile] = output

            baseline_profile = profiles[0]
            for _, skill_name in target_mappings(locale, "openai_skill"):
                baseline = file_snapshot(
                    outputs[baseline_profile] / skill_name,
                    exclude={"agents/openai.yaml"},
                )
                for profile in profiles[1:]:
                    self.assertEqual(
                        baseline,
                        file_snapshot(
                            outputs[profile] / skill_name,
                            exclude={"agents/openai.yaml"},
                        ),
                        f"OpenAI profile changed Skill content for {locale}/{skill_name}: "
                        f"{baseline_profile} != {profile}",
                    )

    def test_openai_metadata_is_byte_identical_to_declared_source(self) -> None:
        metadata = metadata_plan()
        declared = metadata["distributions"]["openai_skill"]["skills"]

        for locale in materializable_locales("openai_skill"):
            for profile in sorted(declared_openai_profiles(metadata)):
                output, temp = self.materialize(
                    locale,
                    "openai_skill",
                    profile=profile,
                )
                self.addCleanup(temp.cleanup)

                for skill_id, skill_name in target_mappings(locale, "openai_skill"):
                    source_relative = declared[skill_id][locale][profile]["source"]
                    source = ROOT / source_relative
                    packaged = output / skill_name / "agents" / "openai.yaml"
                    self.assertEqual(
                        packaged.read_bytes(),
                        source.read_bytes(),
                        f"OpenAI metadata drift for {skill_id}/{locale}/{profile}",
                    )

    def test_claude_and_codex_share_declared_skill_tree(self) -> None:
        for locale in shared_materializable_locales("claude_plugin", "codex_plugin"):
            claude, claude_temp = self.materialize(locale, "claude_plugin")
            codex, codex_temp = self.materialize(locale, "codex_plugin")
            self.addCleanup(claude_temp.cleanup)
            self.addCleanup(codex_temp.cleanup)

            claude_names = {name for _, name in target_mappings(locale, "claude_plugin")}
            codex_names = {name for _, name in target_mappings(locale, "codex_plugin")}
            self.assertEqual(claude_names, codex_names)
            self.assertEqual(
                {path.name for path in (claude / "skills").iterdir() if path.is_dir()},
                claude_names,
            )
            self.assertEqual(
                {path.name for path in (codex / "skills").iterdir() if path.is_dir()},
                codex_names,
            )
            self.assertEqual(
                file_snapshot(claude / "skills"),
                file_snapshot(codex / "skills"),
                f"Claude/Codex Skill tree diverged for {locale}",
            )

    def test_materialized_bundle_manifests_preserve_declared_wording_and_version(self) -> None:
        metadata = metadata_plan()
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        for locale in shared_materializable_locales("claude_plugin", "codex_plugin"):
            claude_bundle = declared_bundle_metadata(metadata, "claude_plugin", locale)
            codex_bundle = declared_bundle_metadata(metadata, "codex_plugin", locale)
            for field in ("plugin_name", "description", "display"):
                self.assertEqual(
                    claude_bundle[field],
                    codex_bundle[field],
                    f"Claude/Codex declared bundle wording diverged for {locale}/{field}",
                )

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

            self.assertEqual(claude_manifest["name"], claude_bundle["plugin_name"])
            self.assertEqual(codex_manifest["name"], codex_bundle["plugin_name"])
            self.assertEqual(claude_manifest["description"], claude_bundle["description"])
            self.assertEqual(codex_manifest["description"], codex_bundle["description"])
            self.assertEqual(codex_manifest["interface"]["displayName"], codex_bundle["display"])
            self.assertEqual(
                codex_manifest["interface"]["shortDescription"],
                codex_bundle["description"],
            )
            self.assertEqual(claude_manifest["version"], version)
            self.assertEqual(codex_manifest["version"], version)


if __name__ == "__main__":
    unittest.main()
