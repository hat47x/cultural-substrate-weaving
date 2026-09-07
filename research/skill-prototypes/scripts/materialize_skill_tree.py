#!/usr/bin/env python3
"""Materialize research Skill trees outside the repository.

This is a pre-production probe. It materializes only Skill subtrees from the
research suite contracts, applies the already-planned Skill-entry transforms,
and refuses to write anywhere inside the repository. It does not create plugin
manifests, marketplace metadata, archives, or release artifacts.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
SUITE_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
METADATA_PATH = ROOT / "research" / "skill-prototypes" / "adapter-metadata-plan.json"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
SCRIPTS_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, SCRIPTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build import skill_frontmatter  # noqa: E402
from common import replace_router_links  # noqa: E402
from plan_adapter_metadata import plan_adapter_metadata  # noqa: E402
from plan_skill_entry_transforms import (  # noqa: E402
    plan_skill_entry_transforms,
    render_explicit_skill_entry,
)
from plan_skill_subtrees import plan_skill_subtrees  # noqa: E402
from validate_research_adapter_metadata import validate_adapter_metadata  # noqa: E402
from validate_research_package_targets import validate_package_targets  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402

SUPPORTED_DISTRIBUTIONS = {"openai_skill", "claude_plugin", "codex_plugin"}
READY_OPENAI_METADATA = {"existing", "prototype"}
READY_BUNDLE_METADATA = {"prototype", "reviewed"}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validated_inputs(root: Path) -> tuple[dict, dict]:
    suite = _load_json(root / SUITE_PATH.relative_to(ROOT))
    metadata = _load_json(root / METADATA_PATH.relative_to(ROOT))
    errors = validate_suite(root, suite)
    errors.extend(validate_package_targets(suite))
    errors.extend(validate_adapter_metadata(root, metadata))
    if errors:
        raise ValueError("invalid research packaging inputs: " + "; ".join(errors))
    return suite, metadata


def _safe_output_root(output_root: Path, root: Path) -> Path:
    resolved = output_root.resolve()
    repository = root.resolve()
    if resolved == repository or repository in resolved.parents:
        raise ValueError("research materializer output_root must be outside the repository")
    if resolved.exists():
        if not resolved.is_dir():
            raise ValueError("research materializer output_root exists and is not a directory")
        if any(resolved.iterdir()):
            raise ValueError("research materializer output_root must be empty")
    else:
        resolved.mkdir(parents=True)
    return resolved


def _target_path(output_root: Path, target: str) -> Path:
    pure = PurePosixPath(target)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe materialization target: {target!r}")
    path = output_root.joinpath(*pure.parts).resolve()
    if not path.is_relative_to(output_root):
        raise ValueError(f"materialization target escapes output root: {target!r}")
    return path


def _metadata_ready(
    metadata_coverage: dict,
    distribution_name: str,
    skill_ids: set[str],
) -> tuple[bool, str | None]:
    if distribution_name == "openai_skill":
        item_map = {
            item["skill_id"]: item
            for item in metadata_coverage.get("items", [])
            if isinstance(item, dict) and isinstance(item.get("skill_id"), str)
        }
        for skill_id in sorted(skill_ids):
            item = item_map.get(skill_id)
            if not isinstance(item, dict):
                return False, f"metadata coverage has no OpenAI entry for {skill_id}"
            if item.get("metadata_state") not in READY_OPENAI_METADATA:
                return (
                    False,
                    f"OpenAI metadata for {skill_id} is not materializable: "
                    f"{item.get('metadata_state')!r}",
                )
        return True, None

    state = metadata_coverage.get("metadata_state")
    if state not in READY_BUNDLE_METADATA:
        return False, f"bundle metadata is not materializable: {state!r}"
    return True, None


def _render_canonical_entry(
    *,
    root: Path,
    suite: dict,
    skill_id: str,
    locale: str,
    source: Path,
    target_name: str,
    explicit_invocation: bool,
) -> str:
    skill = next(
        skill
        for skill in suite["skills"]
        if isinstance(skill, dict) and skill.get("id") == skill_id
    )
    realization = skill["locale_realizations"][locale]
    package_source = realization["package_source"]
    if package_source.get("mode") != "canonical_manifest":
        raise ValueError(f"{skill_id} canonical render requires canonical_manifest source")

    config = _load_json(root / package_source["manifest"])
    router = source.read_text(encoding="utf-8")
    description = config["locales"][locale]["description"]
    return (
        skill_frontmatter(
            target_name,
            description,
            claude_explicit=explicit_invocation,
        )
        + replace_router_links(router, config["modules"])
    )


def materialize_skill_tree(
    *,
    locale: str,
    distribution_name: str,
    output_root: Path,
    root: Path = ROOT,
    allow_partial: bool = False,
) -> dict:
    """Materialize one research Skill-tree distribution outside the repository."""

    if distribution_name not in SUPPORTED_DISTRIBUTIONS:
        raise ValueError(f"unsupported Skill-tree materialization distribution: {distribution_name}")

    suite, metadata = _validated_inputs(root)
    if locale not in suite.get("locales", {}):
        raise ValueError(f"unknown research suite locale: {locale}")

    subtree_plan = plan_skill_subtrees(suite, root)
    entry_plan = plan_skill_entry_transforms(suite, root)
    metadata_plan = plan_adapter_metadata(suite, metadata, root)

    distribution = subtree_plan["locales"][locale]["distributions"][distribution_name]
    state = distribution.get("subtree_state")
    if state == "collision":
        raise ValueError(f"Skill subtree plan has target collisions: {distribution.get('collisions')!r}")
    if state == "blocked":
        raise ValueError("Skill subtree plan is blocked")
    if state == "partial" and not allow_partial:
        raise ValueError(
            "Skill subtree plan is partial; pass allow_partial=True only for an explicit research probe"
        )
    if state not in {"planned", "partial"}:
        raise ValueError(f"Skill subtree plan is not materializable: {state!r}")

    subtrees = distribution.get("subtrees", [])
    skill_ids = {
        subtree["skill_id"]
        for subtree in subtrees
        if isinstance(subtree, dict) and isinstance(subtree.get("skill_id"), str)
    }
    metadata_coverage = metadata_plan["locales"][locale]["distributions"][distribution_name]
    ready, reason = _metadata_ready(metadata_coverage, distribution_name, skill_ids)
    if not ready:
        raise ValueError(reason or "adapter metadata is not materializable")

    entries = {
        entry["skill_id"]: entry
        for entry in entry_plan["locales"][locale]["distributions"][distribution_name].get(
            "entries", []
        )
        if isinstance(entry, dict) and isinstance(entry.get("skill_id"), str)
    }

    output = _safe_output_root(output_root, root)
    written: list[dict] = []
    seen_targets: set[str] = set()

    for subtree in subtrees:
        skill_id = subtree["skill_id"]
        entry = entries.get(skill_id)
        if not isinstance(entry, dict) or entry.get("state") != "planned":
            raise ValueError(f"Skill entry transform is not planned for {skill_id}")

        for mapping in subtree.get("mappings", []):
            target_rel = mapping["target"]
            if target_rel in seen_targets:
                raise ValueError(f"duplicate materialization target: {target_rel}")
            seen_targets.add(target_rel)

            source = (root / mapping["source"]).resolve()
            if not source.is_file() or not source.is_relative_to(root.resolve()):
                raise ValueError(f"materialization source is missing or outside repository: {mapping['source']}")
            target = _target_path(output, target_rel)
            target.parent.mkdir(parents=True, exist_ok=True)

            if mapping.get("target_relative") == "SKILL.md":
                if entry.get("target") != target_rel:
                    raise ValueError(
                        f"Skill entry transform target mismatch for {skill_id}: "
                        f"{entry.get('target')!r} != {target_rel!r}"
                    )
                mode = entry.get("transform_mode")
                if mode == "normalize_explicit_skill_frontmatter":
                    text = render_explicit_skill_entry(
                        source.read_text(encoding="utf-8"),
                        target_name=entry["target_name"],
                        explicit_invocation=bool(entry["disable_model_invocation"]),
                    )
                elif mode == "existing_canonical_builder_render":
                    text = _render_canonical_entry(
                        root=root,
                        suite=suite,
                        skill_id=skill_id,
                        locale=locale,
                        source=source,
                        target_name=entry["target_name"],
                        explicit_invocation=bool(entry["disable_model_invocation"]),
                    )
                else:
                    raise ValueError(f"unsupported Skill entry transform for {skill_id}: {mode!r}")
                target.write_text(text, encoding="utf-8")
                action = "render"
            else:
                shutil.copyfile(source, target)
                action = "copy"

            written.append(
                {
                    "skill_id": skill_id,
                    "source": mapping["source"],
                    "target": target_rel,
                    "action": action,
                }
            )

    return {
        "schema": "csw.research-skill-tree-materialization/v1",
        "locale": locale,
        "distribution": distribution_name,
        "subtree_state": state,
        "partial": state == "partial",
        "output_root": str(output),
        "files": written,
        "note": (
            "Research Skill-tree materialization only. No plugin/marketplace manifest, archive, "
            "production adapter, or release artifact was generated."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True)
    parser.add_argument("--distribution", required=True, choices=sorted(SUPPORTED_DISTRIBUTIONS))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    try:
        result = materialize_skill_tree(
            locale=args.locale,
            distribution_name=args.distribution,
            output_root=args.output,
            allow_partial=args.allow_partial,
        )
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, ValueError) as exc:
        print(f"research Skill-tree materialization failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
