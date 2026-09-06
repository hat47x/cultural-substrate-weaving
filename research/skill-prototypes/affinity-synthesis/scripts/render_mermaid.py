from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "affinity-map":
        raise ValueError("input is not an affinity-map")
    if not isinstance(data.get("cards"), list) or not isinstance(data.get("groups"), list):
        raise ValueError("cards and groups must be arrays")
    return data


def mermaid_text(value: object) -> str:
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return " ".join(text.splitlines())


def by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in items if "id" in item}


def relation_connector(direction: str) -> str:
    return {
        "directed": "-->",
        "reciprocal": "<-->",
        "unspecified": "---",
    }.get(direction, "---")


def relation_label(item: dict[str, Any]) -> str:
    label = f'{item.get("id", "R?")}｜{item.get("predicate", "")}'
    state = str(item.get("state", "")).strip()
    if state:
        label += f" [{state}]"
    return mermaid_text(label)


def render_group_map(data: dict[str, Any]) -> str:
    lines = ["flowchart LR"]
    groups = by_id(data.get("groups", []))

    for gid, group in groups.items():
        label = mermaid_text(f'{gid}｜{group.get("label", "")}')
        lines.append(f'    {gid}["{label}"]')

    questions = by_id(data.get("questions", []))
    for qid, question in questions.items():
        label = mermaid_text(f'{qid}?｜{question.get("text", "")}')
        lines.append(f'    {qid}["{label}"]')

    if groups or questions:
        lines.append("")

    for relation in data.get("relations", []):
        source = str(relation.get("from", ""))
        target = str(relation.get("to", ""))
        if not source or not target:
            continue
        connector = relation_connector(str(relation.get("direction", "unspecified")))
        lines.append(
            f'    {source} {connector}|"{relation_label(relation)}"| {target}'
        )

    for question in data.get("questions", []):
        qid = str(question.get("id", ""))
        for origin in question.get("arises_from", []):
            origin = str(origin)
            if origin in groups and qid:
                lines.append(
                    f'    {origin} -.->|"question / not asserted relation"| {qid}'
                )

    if data.get("layout"):
        lines.append("")
        lines.append(
            "    %% layout metadata exists in the semantic record; "
            "Mermaid does not preserve free positioning"
        )

    return "\n".join(lines) + "\n"


def render_membership_map(data: dict[str, Any]) -> str:
    lines = ["flowchart TB"]
    cards = by_id(data.get("cards", []))
    groups = by_id(data.get("groups", []))
    grouped_cards: set[str] = set()

    for gid, group in groups.items():
        label = mermaid_text(f'{gid}｜{group.get("label", "")}')
        lines.append(f'    subgraph SG_{gid}["{label}"]')
        lines.append(f'        {gid}_anchor["{label}"]')
        for member in group.get("members", []):
            member = str(member)
            if member in cards:
                grouped_cards.add(member)
                text = mermaid_text(f'{member}｜{cards[member].get("text", "")}')
                lines.append(f'        {member}["{text}"]')
            elif member in groups:
                child_label = mermaid_text(
                    f'{member}｜{groups[member].get("label", "")}'
                )
                lines.append(f'        REF_{gid}_{member}["{child_label}"]')
            else:
                missing = mermaid_text(f"{member}｜unresolved reference")
                lines.append(f'        REF_{gid}_{member}["{missing}"]')
        lines.append("    end")

    for cid, card in cards.items():
        if cid not in grouped_cards:
            text = mermaid_text(f'{cid}｜{card.get("text", "")}')
            lines.append(f'    {cid}["{text}"]')

    for crosslink in data.get("resonances", []):
        source = str(crosslink.get("from", ""))
        target = str(crosslink.get("to", ""))
        if not source or target not in groups:
            continue
        note = mermaid_text(
            f'{crosslink.get("id", "X?")}｜resonance / not membership｜'
            f'{crosslink.get("note", "")}'
        )
        lines.append(
            f'    {source} -.->|"{note}"| {target}_anchor'
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render affinity-map JSON as Mermaid source."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--view", choices=("group", "membership"), default="group")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    data = load_map(args.input)
    output = (
        render_group_map(data)
        if args.view == "group"
        else render_membership_map(data)
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
