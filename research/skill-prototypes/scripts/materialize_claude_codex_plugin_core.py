#!/usr/bin/env python3
"""Materialize a research Claude/Codex multi-Skill plugin core outside the repository.

The current production plugin lets Claude Code and Codex share one `skills/`
tree. This pre-production probe verifies that the research suite can preserve
that shared tree while composing host-specific plugin manifests from the
reviewed/prototype bundle metadata. It intentionally does not generate README,
marketplace catalogs, archives, or release assets.
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

from materialize_skill_tree import _safe_output_root, materialize_skill_tree  # noqa: E402
from plan_adapter_metadata import plan_adapter_metadata  # noqa: E402

READY_BUNDLE_METADATA = {"prototype", "reviewed"}
REPOSITORY_URL = "https://github.com/hat47x/cultural-substrate-weaving"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def _locale_short(locale: str) -> str:
    try:
        return {"ja-JP": "ja", "en-US": "en"}[locale]
    except KeyError as exc:
        raise ValueError(f"unsupported locale short name: {locale}") from exc


def _tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _bundle_plan(metadata_plan: dict, locale: str, distribution: str) -> dict:
    try:
        plan = metadata_plan["locales"][locale]["distributions"][distribution]
    except KeyError as exc:
        raise ValueError(f"unknown bundle plan for {locale}/{distribution}") from exc

    if plan.get("runtime_state") != "buildable":
        raise ValueError(
            f"{distribution} runtime bundle is not buildable: {plan.get('runtime_state')!r}"
        )
    if plan.get("metadata_state") not in READY_BUNDLE_METADATA:
        raise ValueError(
            f"{distribution} bundle metadata is not materializable: "
            f"{plan.get('metadata_state')!r}"
        )
    if plan.get("source_kind") != "research-prototype" and plan.get("metadata_state") != "reviewed":
        raise ValueError(
            f"{distribution} bundle metadata has no approved research source: "
            f"{plan.get('source_kind')!r}"
        )
    return plan


def _bundle_metadata(root: Path, claude_plan: dict, codex_plan: dict) -> tuple[dict, str]:
    claude_source = claude_plan.get("source")
    codex_source = codex_plan.get("source")
    if not isinstance(claude_source, str) or claude_source != codex_source:
        raise ValueError("Claude/Codex bundle metadata sources diverge")

    source = (root / claude_source).resolve()
    repository = root.resolve()
    if not source.is_file() or not source.is_relative_to(repository):
        raise ValueError(f"bundle metadata source is missing or outside repository: {claude_source!r}")

    value = _load_json(source)
    if value.get("invocation_policy") != "explicit":
        raise ValueError("Claude/Codex research bundle must preserve explicit invocation policy")

    for field in ("plugin_name", "display", "description", "contains"):
        if value.get(field) != claude_plan.get("catalog_entry", {}).get(field):
            raise ValueError(f"Claude bundle plan drifts from prototype field: {field}")
        if value.get(field) != codex_plan.get("catalog_entry", {}).get(field):
            raise ValueError(f"Codex bundle plan drifts from prototype field: {field}")

    return value, source.relative_to(root).as_posix()


def materialize_claude_codex_plugin_core(
    *,
    locale: str,
    output_root: Path,
    root: Path = ROOT,
) -> dict:
    """Materialize one shared Claude/Codex plugin core outside the repository."""

    suite = _load_json(root / SUITE_PATH.relative_to(ROOT))
    metadata = _load_json(root / METADATA_PATH.relative_to(ROOT))

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        claude_tree = temp / "claude"
        codex_tree = temp / "codex"

        claude_result = materialize_skill_tree(
            locale=locale,
            distribution_name="claude_plugin",
            output_root=claude_tree,
            root=root,
        )
        codex_result = materialize_skill_tree(
            locale=locale,
            distribution_name="codex_plugin",
            output_root=codex_tree,
            root=root,
        )

        if _tree_snapshot(claude_tree) != _tree_snapshot(codex_tree):
            raise ValueError("Claude/Codex research Skill trees diverge")

        metadata_plan = plan_adapter_metadata(suite, metadata, root)
        claude_plan = _bundle_plan(metadata_plan, locale, "claude_plugin")
        codex_plan = _bundle_plan(metadata_plan, locale, "codex_plugin")
        bundle, metadata_source = _bundle_metadata(root, claude_plan, codex_plan)

        output = _safe_output_root(output_root, root)
        plugin_root = output / bundle["plugin_name"]
        skills_source = claude_tree / "skills"
        if not skills_source.is_dir():
            raise ValueError("research Claude/Codex bundle has no shared skills/ tree")
        shutil.copytree(skills_source, plugin_root / "skills")

        current_version = _version(root)
        claude_manifest = {
            "name": bundle["plugin_name"],
            "description": bundle["description"],
            "version": current_version,
            "author": {"name": "hat47x"},
            "homepage": REPOSITORY_URL,
            "repository": REPOSITORY_URL,
            "license": "MIT",
        }
        _write_json(plugin_root / ".claude-plugin" / "plugin.json", claude_manifest)

        codex_manifest = {
            "name": bundle["plugin_name"],
            "version": current_version,
            "description": bundle["description"],
            "author": {"name": "hat47x"},
            "homepage": REPOSITORY_URL,
            "repository": REPOSITORY_URL,
            "license": "MIT",
            "keywords": ["analysis", "design", "writing", "architecture", _locale_short(locale)],
            "skills": "./skills/",
            "interface": {
                "displayName": bundle["display"],
                "shortDescription": bundle["description"],
                "developerName": "hat47x",
                "category": "Productivity",
            },
        }
        _write_json(plugin_root / ".codex-plugin" / "plugin.json", codex_manifest)

    return {
        "schema": "csw.research-claude-codex-plugin-core/v1",
        "locale": locale,
        "plugin_name": bundle["plugin_name"],
        "metadata_source": metadata_source,
        "metadata_state": claude_plan.get("metadata_state"),
        "contains": list(bundle["contains"]),
        "shared_skill_tree": True,
        "claude_subtree_state": claude_result.get("subtree_state"),
        "codex_subtree_state": codex_result.get("subtree_state"),
        "output_root": str(output),
        "plugin_root": str(plugin_root),
        "note": (
            "Research plugin core only. README, marketplace catalogs, archives, "
            "production generated artifacts, and release assets were not generated."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        result = materialize_claude_codex_plugin_core(
            locale=args.locale,
            output_root=args.output,
        )
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, ValueError) as exc:
        print(f"research Claude/Codex plugin core materialization failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
