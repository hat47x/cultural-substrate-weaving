#!/usr/bin/env python3
"""Plan and render research Skill entry transforms without writing packages.

This module owns only Skill-entry frontmatter normalization for the research
multi-Skill packaging prototype. It deliberately does not generate plugin
manifests, OpenAI agent metadata, marketplace catalogs, archives, or releases.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "research" / "skill-prototypes" / "suite-manifest.json"
PLANNER_DIR = ROOT / "research" / "skill-prototypes" / "scripts"
VALIDATOR_DIR = ROOT / "scripts"
for path in (PLANNER_DIR, VALIDATOR_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from plan_skill_subtrees import plan_skill_subtrees  # noqa: E402
from validate_research_package_targets import validate_package_targets  # noqa: E402
from validate_research_skill_suite import validate_suite  # noqa: E402

PLAN_SCHEMA = "csw.research-skill-entry-transform-plan/v1"
CLAUDE_SHARED_TREE_DISTRIBUTIONS = {"claude_plugin", "codex_plugin"}
OPENAI_DISTRIBUTIONS = {"openai_skill"}


def split_skill_frontmatter(text: str) -> tuple[list[tuple[str, str]], str]:
    """Parse the simple scalar YAML frontmatter used by prototype SKILL.md files.

    The research prototype intentionally supports only one-line scalar values.
    Rejecting richer YAML avoids silently changing semantics before a production
    frontmatter parser/renderer is chosen.
    """

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise ValueError("Skill entry must start with YAML frontmatter")

    closing = None
    for index in range(1, len(lines)):
        if lines[index].rstrip("\r\n") == "---":
            closing = index
            break
    if closing is None:
        raise ValueError("Skill entry frontmatter is not closed")

    fields: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw_line in lines[1:closing]:
        line = raw_line.rstrip("\r\n")
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported Skill frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.lstrip()
        if not key or key in seen:
            raise ValueError(f"invalid or duplicate Skill frontmatter key: {key!r}")
        seen.add(key)
        fields.append((key, value))

    body = "".join(lines[closing + 1 :])
    return fields, body


def render_explicit_skill_entry(
    text: str,
    *,
    target_name: str,
    explicit_invocation: bool,
) -> str:
    """Normalize a prototype Skill entry for one research distribution target."""

    fields, body = split_skill_frontmatter(text)
    values = dict(fields)
    description = values.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Skill entry frontmatter must declare description")

    preserved = [
        (key, value)
        for key, value in fields
        if key not in {"name", "description", "disable-model-invocation"}
    ]
    output = ["---", f"name: {target_name}", f"description: {description}"]
    output.extend(f"{key}: {value}" for key, value in preserved)
    if explicit_invocation:
        output.append("disable-model-invocation: true")
    output.extend(["---", ""])
    return "\n".join(output) + "\n" + body.lstrip("\r\n")


def _distribution_policy(distribution_name: str) -> dict | None:
    if distribution_name in OPENAI_DISTRIBUTIONS:
        return {
            "entry_policy": "openai_skill",
            "disable_model_invocation": False,
        }
    if distribution_name in CLAUDE_SHARED_TREE_DISTRIBUTIONS:
        return {
            "entry_policy": "claude_codex_shared_skill_tree",
            "disable_model_invocation": True,
        }
    return None


def plan_skill_entry_transforms(manifest: dict, root: Path = ROOT) -> dict:
    """Return frontmatter/render directives for every planned Skill subtree entry."""

    subtree_plan = plan_skill_subtrees(manifest, root)
    output = {
        "schema": PLAN_SCHEMA,
        "suite_id": manifest.get("suite_id"),
        "note": (
            "Entry transforms normalize Skill frontmatter only. Plugin/agent metadata, "
            "marketplace catalogs, archives, and release readiness remain out of scope."
        ),
        "locales": {},
    }

    for locale, locale_plan in subtree_plan["locales"].items():
        distribution_output: dict[str, dict] = {}
        for distribution_name, distribution in locale_plan["distributions"].items():
            policy = _distribution_policy(distribution_name)
            if policy is None:
                distribution_output[distribution_name] = {
                    "state": "not-applicable",
                    "entries": [],
                    "reason": "distribution does not materialize a supported Skill entry tree",
                }
                continue

            entries: list[dict] = []
            for subtree in distribution.get("subtrees", []):
                entry_mapping = next(
                    (
                        mapping
                        for mapping in subtree.get("mappings", [])
                        if mapping.get("target_relative") == "SKILL.md"
                    ),
                    None,
                )
                if entry_mapping is None:
                    entries.append(
                        {
                            "skill_id": subtree.get("skill_id"),
                            "state": "blocked",
                            "reason": "subtree has no SKILL.md entry mapping",
                        }
                    )
                    continue

                input_operation = entry_mapping.get("operation")
                if input_operation == "copy":
                    transform_mode = "normalize_explicit_skill_frontmatter"
                elif input_operation == "render_runtime_entry":
                    transform_mode = "existing_canonical_builder_render"
                else:
                    transform_mode = "unsupported"

                entries.append(
                    {
                        "skill_id": subtree["skill_id"],
                        "state": "planned" if transform_mode != "unsupported" else "blocked",
                        "source": entry_mapping.get("source"),
                        "target": entry_mapping.get("target"),
                        "target_name": subtree["skill_name"],
                        "input_operation": input_operation,
                        "transform_mode": transform_mode,
                        **policy,
                    }
                )

            distribution_output[distribution_name] = {
                "state": distribution.get("subtree_state"),
                "entries": entries,
            }

        output["locales"][locale] = {"distributions": distribution_output}

    return output


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"research Skill entry transform planning failed: {exc}", file=sys.stderr)
        return 1

    errors = validate_suite(ROOT, manifest)
    errors.extend(validate_package_targets(manifest))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        plan = plan_skill_entry_transforms(manifest, ROOT)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"research Skill entry transform planning failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
