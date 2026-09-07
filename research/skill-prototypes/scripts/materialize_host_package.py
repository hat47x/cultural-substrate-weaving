#!/usr/bin/env python3
"""Materialize research Skill trees plus minimal host package metadata.

This is a pre-production probe. It writes only to a repository-external empty
output root, reuses the Skill-tree materializer, and adds package-local host
metadata for OpenAI Skill, Claude plugin, or Codex plugin shapes. It does not
create marketplace catalogs, README files, archives, release manifests, or
release assets.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
SCRIPTS_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from common import locale_short  # noqa: E402
from materialize_skill_tree import (  # noqa: E402
    _target_path,
    _validated_inputs,
    materialize_skill_tree,
)

SUPPORTED_DISTRIBUTIONS = {"openai_skill", "claude_plugin", "codex_plugin"}
OPENAI_PROFILES = {"interactive", "metered"}
READY_OPENAI_METADATA = {"existing", "prototype"}
READY_BUNDLE_METADATA = {"prototype", "reviewed"}
REPOSITORY_URL = "https://github.com/hat47x/cultural-substrate-weaving"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _repository_version(root: Path) -> str:
    value = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not value:
        raise ValueError("VERSION must not be empty")
    return value


def _prepare_openai_metadata(
    *,
    root: Path,
    suite: dict,
    metadata: dict,
    locale: str,
    profile: str | None,
) -> list[dict]:
    if profile not in OPENAI_PROFILES:
        raise ValueError("openai_skill host materialization requires profile=interactive or metered")

    declared = metadata["distributions"]["openai_skill"]["skills"]
    mappings: list[dict] = []
    for skill in suite.get("skills", []):
        if not isinstance(skill, dict):
            continue
        skill_id = skill.get("id")
        if not isinstance(skill_id, str):
            continue
        realization = skill.get("locale_realizations", {}).get(locale)
        if not isinstance(realization, dict) or realization.get("status") == "planned":
            raise ValueError(f"OpenAI runtime is not materializable for {skill_id}/{locale}")
        target = realization.get("package_targets", {}).get("openai_skill")
        if not isinstance(target, dict) or not isinstance(target.get("skill_name"), str):
            raise ValueError(f"OpenAI package target is missing for {skill_id}/{locale}")

        entry = declared.get(skill_id, {}).get(locale, {}).get(profile)
        if not isinstance(entry, dict):
            raise ValueError(f"OpenAI metadata declaration is missing for {skill_id}/{locale}/{profile}")
        status = entry.get("status")
        if status not in READY_OPENAI_METADATA:
            raise ValueError(
                f"OpenAI metadata for {skill_id}/{locale}/{profile} is not host-materializable: {status!r}"
            )
        source_relative = entry.get("source")
        if not isinstance(source_relative, str):
            raise ValueError(f"OpenAI metadata source is missing for {skill_id}/{locale}/{profile}")
        source = (root / source_relative).resolve()
        if not source.is_file() or not source.is_relative_to(root.resolve()):
            raise ValueError(
                f"OpenAI metadata source is missing or outside repository for {skill_id}/{locale}/{profile}"
            )
        mappings.append(
            {
                "skill_id": skill_id,
                "skill_name": target["skill_name"],
                "source": source_relative,
                "source_path": source,
            }
        )

    return mappings


def _load_bundle_metadata(
    *,
    root: Path,
    metadata: dict,
    distribution_name: str,
    locale: str,
) -> tuple[dict, str]:
    config = metadata["distributions"][distribution_name]
    locale_entry = config["locales"][locale]
    status = locale_entry.get("status")
    if status not in READY_BUNDLE_METADATA:
        raise ValueError(f"bundle metadata is not host-materializable: {status!r}")

    if status == "prototype":
        source_relative = locale_entry.get("prototype_source")
        if not isinstance(source_relative, str):
            raise ValueError(f"bundle prototype source is missing for {distribution_name}/{locale}")
        source = (root / source_relative).resolve()
        if not source.is_file() or not source.is_relative_to(root.resolve()):
            raise ValueError(
                f"bundle prototype source is missing or outside repository for {distribution_name}/{locale}"
            )
        value = _load_json(source)
        return value, source_relative

    source_relative = config.get("source")
    if not isinstance(source_relative, str):
        raise ValueError(f"reviewed bundle metadata source is missing for {distribution_name}/{locale}")
    source = (root / source_relative).resolve()
    if not source.is_file() or not source.is_relative_to(root.resolve()):
        raise ValueError(
            f"reviewed bundle metadata source is missing or outside repository for {distribution_name}/{locale}"
        )
    catalog = _load_json(source)
    value = catalog.get(locale)
    if not isinstance(value, dict):
        raise ValueError(f"reviewed bundle metadata does not contain locale {locale}")
    return value, source_relative


def _require_bundle_fields(bundle: dict, locale: str) -> None:
    for field in ("plugin_name", "display", "description"):
        value = bundle.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"bundle metadata {locale} must declare {field}")


def _claude_manifest(bundle: dict, current_version: str) -> dict:
    return {
        "name": bundle["plugin_name"],
        "description": bundle["description"],
        "version": current_version,
        "author": {"name": "hat47x"},
        "homepage": REPOSITORY_URL,
        "repository": REPOSITORY_URL,
        "license": "MIT",
    }


def _codex_manifest(bundle: dict, current_version: str, locale: str) -> dict:
    return {
        "name": bundle["plugin_name"],
        "version": current_version,
        "description": bundle["description"],
        "author": {"name": "hat47x"},
        "homepage": REPOSITORY_URL,
        "repository": REPOSITORY_URL,
        "license": "MIT",
        "keywords": ["analysis", "design", "writing", "architecture", locale_short(locale)],
        "skills": "./skills/",
        "interface": {
            "displayName": bundle["display"],
            "shortDescription": bundle["description"],
            "developerName": "hat47x",
            "category": "Productivity",
        },
    }


def materialize_host_package(
    *,
    locale: str,
    distribution_name: str,
    output_root: Path,
    profile: str | None = None,
    root: Path = ROOT,
) -> dict:
    """Materialize one research host-package shape outside the repository."""

    if distribution_name not in SUPPORTED_DISTRIBUTIONS:
        raise ValueError(f"unsupported host-package distribution: {distribution_name}")
    if distribution_name != "openai_skill" and profile is not None:
        raise ValueError("profile is only valid for openai_skill host materialization")

    suite, metadata = _validated_inputs(root)
    if locale not in suite.get("locales", {}):
        raise ValueError(f"unknown research suite locale: {locale}")

    openai_mappings: list[dict] | None = None
    bundle: dict | None = None
    bundle_source: str | None = None
    if distribution_name == "openai_skill":
        openai_mappings = _prepare_openai_metadata(
            root=root,
            suite=suite,
            metadata=metadata,
            locale=locale,
            profile=profile,
        )
    else:
        bundle, bundle_source = _load_bundle_metadata(
            root=root,
            metadata=metadata,
            distribution_name=distribution_name,
            locale=locale,
        )
        _require_bundle_fields(bundle, locale)

    tree_result = materialize_skill_tree(
        locale=locale,
        distribution_name=distribution_name,
        output_root=output_root,
        root=root,
        allow_partial=False,
    )
    output = Path(tree_result["output_root"]).resolve()
    host_files: list[dict] = []

    if distribution_name == "openai_skill":
        assert openai_mappings is not None
        for mapping in openai_mappings:
            target_relative = f"{mapping['skill_name']}/agents/openai.yaml"
            target = _target_path(output, target_relative)
            if target.exists():
                raise ValueError(f"host metadata target already exists: {target_relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(mapping["source_path"], target)
            host_files.append(
                {
                    "skill_id": mapping["skill_id"],
                    "source": mapping["source"],
                    "target": target_relative,
                    "action": "copy",
                }
            )
    else:
        assert bundle is not None
        current_version = _repository_version(root)
        if distribution_name == "claude_plugin":
            target_relative = ".claude-plugin/plugin.json"
            manifest = _claude_manifest(bundle, current_version)
        else:
            target_relative = ".codex-plugin/plugin.json"
            manifest = _codex_manifest(bundle, current_version, locale)
        target = _target_path(output, target_relative)
        if target.exists():
            raise ValueError(f"host metadata target already exists: {target_relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        host_files.append(
            {
                "source": bundle_source,
                "target": target_relative,
                "action": "render",
            }
        )

    return {
        "schema": "csw.research-host-package-materialization/v1",
        "locale": locale,
        "distribution": distribution_name,
        "profile": profile if distribution_name == "openai_skill" else None,
        "output_root": str(output),
        "skill_tree": tree_result,
        "host_files": host_files,
        "note": (
            "Research host-package probe only. Package-local host metadata was added, but no "
            "marketplace catalog, README, archive, release manifest, or release asset was generated."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True)
    parser.add_argument(
        "--distribution",
        required=True,
        choices=sorted(SUPPORTED_DISTRIBUTIONS),
    )
    parser.add_argument("--profile", choices=sorted(OPENAI_PROFILES))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        result = materialize_host_package(
            locale=args.locale,
            distribution_name=args.distribution,
            output_root=args.output,
            profile=args.profile,
        )
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, ValueError) as exc:
        print(f"research host-package materialization failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
