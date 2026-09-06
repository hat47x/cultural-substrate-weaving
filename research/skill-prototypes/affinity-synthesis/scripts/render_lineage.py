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


def short(value: object, limit: int = 42) -> str:
    text = " ".join(str(value).splitlines())
    return text if len(text) <= limit else text[: limit - 1] + "…"


class LineageGraph:
    def __init__(self, data: dict[str, Any], detail: str) -> None:
        self.detail = detail
        self.sections = {
            key: index(data.get(key, []))
            for key in (
                "sources",
                "cards",
                "groups",
                "relations",
                "narratives",
                "residuals",
                "questions",
            )
        }
        self.nodes: dict[str, tuple[str, str]] = {}
        self.edges: list[tuple[str, str, str]] = []
        self.visited: set[str] = set()

    def kind(self, ref: str) -> str | None:
        for kind, items in self.sections.items():
            if ref in items:
                return kind
        return None

    def add_node(self, ref: str, label: str, kind: str) -> None:
        self.nodes[ref] = (label, kind)

    def walk(self, ref: str) -> None:
        if ref in self.visited:
            return
        self.visited.add(ref)
        kind = self.kind(ref)
        if not kind:
            self.add_node(ref, ref, "unknown")
            return

        item = self.sections[kind][ref]
        text = (
            item.get("display_label")
            or item.get("label")
            or item.get("text")
            or item.get("ref")
            or ref
        )
        self.add_node(ref, f"{ref}｜{short(text)}", kind)

        if kind == "sources":
            return

        if kind == "cards":
            if self.detail == "cards":
                for parent in item.get("source_refs", []):
                    parent = str(parent)
                    self.walk(parent)
                    self.edges.append((parent, ref, "source → card"))
                for parent in item.get("derivation_refs", []):
                    parent = str(parent)
                    self.walk(parent)
                    self.edges.append((parent, ref, "derives"))
            return

        if kind == "groups":
            card_members = [
                str(member)
                for member in item.get("members", [])
                if str(member) in self.sections["cards"]
            ]
            group_members = [
                str(member)
                for member in item.get("members", [])
                if str(member) in self.sections["groups"]
            ]
            for parent in group_members:
                self.walk(parent)
                self.edges.append((parent, ref, "higher-order membership"))
            if self.detail == "cards":
                for parent in card_members:
                    self.walk(parent)
                    self.edges.append((parent, ref, "membership"))
            elif card_members:
                virtual = f"{ref}__cards"
                self.add_node(
                    virtual,
                    f"{len(card_members)} cards collapsed",
                    "collapsed",
                )
                self.edges.append((virtual, ref, "membership summary"))
            return

        if kind == "relations":
            parents = [item.get("from"), item.get("to"), *item.get("basis", [])]
            for parent in parents:
                if parent:
                    parent = str(parent)
                    self.walk(parent)
                    self.edges.append((parent, ref, "relation basis"))
            return

        if kind == "narratives":
            for parent in item.get("basis", []):
                parent = str(parent)
                self.walk(parent)
                self.edges.append((parent, ref, "narrative basis"))
            return

        if kind == "residuals":
            for parent in item.get("refs", []):
                parent = str(parent)
                self.walk(parent)
                self.edges.append((parent, ref, "residual ref"))
            return

        if kind == "questions":
            for parent in item.get("arises_from", []):
                parent = str(parent)
                self.walk(parent)
                self.edges.append((parent, ref, "question provenance"))

    def mermaid(self) -> str:
        lines = ["flowchart LR"]
        for ref, (label, kind) in self.nodes.items():
            quoted = mermaid_text(label)
            if kind == "narratives":
                shape = f'[["{quoted}"]]'
            elif kind == "relations":
                shape = f'{{{{"{quoted}"}}}}'
            elif kind in {"questions", "residuals"}:
                shape = f'("{quoted}")'
            else:
                shape = f'["{quoted}"]'
            lines.append(f"    {ref}{shape}")

        lines.append("")
        seen: set[tuple[str, str, str]] = set()
        for source, target, label in self.edges:
            key = (source, target, label)
            if key in seen:
                continue
            seen.add(key)
            lines.append(
                f'    {source} -->|"{mermaid_text(label)}"| {target}'
            )
        return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render backward lineage for one affinity-map artifact."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--focus", required=True)
    parser.add_argument(
        "--detail",
        choices=("groups", "cards"),
        default="groups",
        help="groups collapses direct card members; cards expands them and their source refs",
    )
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    graph = LineageGraph(load(args.input), args.detail)
    graph.walk(args.focus)
    output = graph.mermaid()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
