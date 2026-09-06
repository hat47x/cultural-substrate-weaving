from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "affinity-map":
        raise ValueError("input is not an affinity-map")
    return data


def index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(item["id"]): item
        for item in items
        if isinstance(item, dict) and item.get("id")
    }


def mermaid_text(value: object) -> str:
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return " ".join(text.splitlines())


def display_label(item: dict[str, Any]) -> str:
    return str(
        item.get("display_label")
        or item.get("label")
        or item.get("text")
        or item.get("id", "")
    )


def render(data: dict[str, Any], include_relations: bool = False) -> str:
    groups = index(data.get("groups", []))
    cards = index(data.get("cards", []))
    child_groups = {
        str(member)
        for group in groups.values()
        for member in group.get("members", [])
        if str(member) in groups
    }
    roots = [gid for gid in groups if gid not in child_groups]

    lines = ["flowchart TB"]
    for gid, group in groups.items():
        direct_cards = sum(
            1 for member in group.get("members", []) if str(member) in cards
        )
        direct_groups = sum(
            1 for member in group.get("members", []) if str(member) in groups
        )
        counts: list[str] = []
        if direct_cards:
            counts.append(f"{direct_cards} cards")
        if direct_groups:
            counts.append(f"{direct_groups} groups")
        suffix = f" ({', '.join(counts)})" if counts else ""
        label = mermaid_text(f"{gid}｜{display_label(group)}{suffix}")
        lines.append(f'    {gid}["{label}"]')

    lines.append("")
    for parent, group in groups.items():
        for member in group.get("members", []):
            child = str(member)
            if child in groups:
                lines.append(
                    f'    {parent} -->|"higher-order membership / not semantic relation"| {child}'
                )

    if include_relations:
        lines.append("")
        lines.append(
            "    %% explicit semantic relations; visually distinct from higher-order membership"
        )
        for relation in data.get("relations", []):
            source = str(relation.get("from", ""))
            target = str(relation.get("to", ""))
            if source not in groups or target not in groups:
                continue
            label = relation.get("display_label") or relation.get("predicate") or relation.get("id", "R?")
            edge = mermaid_text(
                f'{relation.get("id", "R?")}｜relation｜{label}'
            )
            lines.append(f'    {source} -.->|"{edge}"| {target}')

    lines.append("")
    lines.append("    %% roots: " + ", ".join(roots))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render recursive higher-order group membership as Mermaid."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--with-relations", action="store_true")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    output = render(load(args.input), include_relations=args.with_relations)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
