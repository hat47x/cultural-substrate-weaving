#!/usr/bin/env python3
"""Materialize research OpenAI Skill packages outside the repository.

This extends the research Skill-tree materializer by composing per-profile
`agents/openai.yaml` metadata around each realized Skill tree. It is a
pre-production probe only: it never writes to production `dist/`, generated
plugin directories, or release assets.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
if str(PLANNER_DIR) not in sys.path:
    sys.path.insert(0, str(PLANNER_DIR))

from materialize_skill_tree import (  # noqa: E402
    _load_json,
    _safe_output_root,
    _target_path,
    materialize_skill_tree,
)
from plan_adapter_metadata import plan_adapter_metadata  # noqa: E402

READY_METADATA_STATES = {"existing", "prototype"}
PROFILES = ("interactive", "metered")


def _skill_target_name(suite: dict, skill_id: str, locale: str) -> str:
    if not isinstance(suite, dict):
        raise ValueError("research skill suite must be an object")
    skills = suite.get("skills")
    if not isinstance(skills, list):
        raise ValueError("research skill suite skills must be a list")
    skill = next(
        (
            item
            for item in skills
            if isinstance(item, dict) and item.get("id") == skill_id
        ),
        None,
    )
    if not isinstance(skill, dict):
        raise ValueError(f"research skill suite entry is missing: {skill_id}")
    realizations = skill.get("locale_realizations")
    if not isinstance(realizations, dict):
        raise ValueError(f"research skill locale realizations are missing: {skill_id}")
    realization = realizations.get(locale)
    if not isinstance(realization, dict):
        raise ValueError(f"research skill locale realization is missing: {skill_id}/{locale}")
    package_targets = realization.get("package_targets")
    if not isinstance(package_targets, dict):
        raise ValueError(f"research skill package targets are missing: {skill_id}/{locale}")
    openai = package_targets.get("openai_skill")
    if not isinstance(openai, dict):
        raise ValueError(f"OpenAI package target is missing: {skill_id}/{locale}")
    skill_name = openai.get("skill_name")
    if not isinstance(skill_name, str) or not skill_name:
        raise ValueError(f"OpenAI package skill_name is missing: {skill_id}/{locale}")
    return skill_name


def _metadata_source(root: Path, profile_entry: dict, skill_id: str, profile: str) -> Path:
    if not isinstance(profile_entry, dict):
        raise ValueError(f"OpenAI metadata profile entry must be an object: {skill_id}/{profile}")
    state = profile_entry.get("status")
    source = profile_entry.get("source")
    if state not in READY_METADATA_STATES or not isinstance(source, str):
        raise ValueError(
            f"OpenAI metadata is not materializable for {skill_id}/{profile}: {state!r}"
        )

    candidate = (root / source).resolve()
    repository = root.resolve()
    if not candidate.is_file() or not candidate.is_relative_to(repository):
        raise ValueError(
            f"OpenAI metadata source is missing or outside repository for "
            f"{skill_id}/{profile}: {source!r}"
        )
    return candidate


def materialize_openai_packages(
    *,
    locale: str,
    output_root: Path,
    root: Path = ROOT,
    allow_partial: bool = False,
) -> dict:
    """Materialize realized OpenAI packages for one locale outside the repository."""

    suite = _load_json(root / SUITE_PATH.relative_to(ROOT))
    metadata = _load_json(root / METADATA_PATH.relative_to(ROOT))

    with tempfile.TemporaryDirectory() as temp_dir:
        stage = Path(temp_dir) / "skill-trees"
        tree_result = materialize_skill_tree(
            locale=locale,
            distribution_name="openai_skill",
            output_root=stage,
            root=root,
            allow_partial=allow_partial,
        )

        metadata_plan = plan_adapter_metadata(suite, metadata, root)
        try:
            openai_plan = metadata_plan["locales"][locale]["distributions"]["openai_skill"]
        except KeyError as exc:
            raise ValueError(f"unknown research suite locale: {locale}") from exc

        coverage = openai_plan.get("metadata_coverage")
        if coverage not in {"complete-for-realized", "prototype-for-realized"}:
            raise ValueError(f"OpenAI metadata coverage is not materializable: {coverage!r}")

        items = {
            item["skill_id"]: item
            for item in openai_plan.get("items", [])
            if isinstance(item, dict) and isinstance(item.get("skill_id"), str)
        }
        realized_skill_ids = sorted(
            skill_id
            for skill_id, item in items.items()
            if item.get("runtime_state") == "buildable"
        )
        if not realized_skill_ids:
            raise ValueError("OpenAI package materialization has no realized Skills")

        output = _safe_output_root(output_root, root)
        written: list[dict] = []
        for profile in PROFILES:
            for skill_id in realized_skill_ids:
                item = items[skill_id]
                profile_entry = item.get("profiles", {}).get(profile)
                if not isinstance(profile_entry, dict):
                    raise ValueError(f"OpenAI metadata has no {profile} profile for {skill_id}")

                source_tree_name = _skill_target_name(suite, skill_id, locale)
                source_tree = _target_path(stage, source_tree_name)
                if not source_tree.is_dir():
                    raise ValueError(
                        f"materialized OpenAI Skill tree is missing for {skill_id}: "
                        f"{source_tree_name!r}"
                    )

                metadata_source = _metadata_source(
                    root,
                    profile_entry,
                    skill_id,
                    profile,
                )

                target_root = _target_path(
                    output,
                    f"{profile}/{source_tree_name}",
                )
                shutil.copytree(source_tree, target_root)
                metadata_target = target_root / "agents" / "openai.yaml"
                metadata_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(metadata_source, metadata_target)

                written.append(
                    {
                        "skill_id": skill_id,
                        "profile": profile,
                        "target": target_root.relative_to(output).as_posix(),
                        "metadata_state": profile_entry.get("status"),
                        "metadata_source": metadata_source.relative_to(root).as_posix(),
                    }
                )

    return {
        "schema": "csw.research-openai-package-materialization/v1",
        "locale": locale,
        "runtime_state": openai_plan.get("runtime_state"),
        "metadata_coverage": coverage,
        "partial": bool(tree_result.get("partial")),
        "profiles": list(PROFILES),
        "output_root": str(output),
        "packages": written,
        "note": (
            "Research OpenAI package materialization only. No production dist tree, "
            "generated plugin, archive, release manifest, or release asset was generated."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    try:
        result = materialize_openai_packages(
            locale=args.locale,
            output_root=args.output,
            allow_partial=args.allow_partial,
        )
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, ValueError) as exc:
        print(f"research OpenAI package materialization failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
