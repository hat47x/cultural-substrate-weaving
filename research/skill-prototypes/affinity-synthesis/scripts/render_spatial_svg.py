from __future__ import annotations

import argparse
import html
import json
import math
import textwrap
from pathlib import Path
from typing import Any

WIDTH = 1200
HEIGHT = 800
NODE_W = 330
NODE_H = 120
QUESTION_W = 300
QUESTION_H = 96
MARGIN_X = 70
MARGIN_Y = 60
FONT_FAMILY = "'Noto Sans CJK JP','Noto Sans JP','Yu Gothic',sans-serif"


def load_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "affinity-map":
        raise ValueError("input is not an affinity-map")
    return data


def index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in items if "id" in item}


def svg_text(value: object) -> str:
    return html.escape(str(value), quote=True)


def lines(text: str, width: int = 22, max_lines: int = 4) -> list[str]:
    wrapped = textwrap.wrap(
        text,
        width=width,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]
    if len(wrapped) <= max_lines:
        return wrapped
    clipped = wrapped[:max_lines]
    clipped[-1] = clipped[-1][:-1] + "…" if clipped[-1] else "…"
    return clipped


def display_text(item: dict[str, Any], canonical_key: str) -> str:
    compact = str(item.get("display_label", "")).strip()
    return compact or str(item.get(canonical_key, ""))


def position(ref: str, positions: dict[str, Any]) -> tuple[float, float]:
    raw = positions.get(ref)
    if not isinstance(raw, dict):
        raise ValueError(f"spatial projection requires a position for {ref}")
    x = float(raw["x"])
    y = float(raw["y"])
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise ValueError(f"position for {ref} must be normalized to 0..1")
    px = MARGIN_X + x * (WIDTH - 2 * MARGIN_X)
    py = MARGIN_Y + y * (HEIGHT - 2 * MARGIN_Y)
    return px, py


def rect_edge_point(
    source: tuple[float, float],
    target: tuple[float, float],
    width: float,
    height: float,
) -> tuple[float, float]:
    sx, sy = source
    tx, ty = target
    dx = tx - sx
    dy = ty - sy
    if dx == 0 and dy == 0:
        return source
    scale_x = (width / 2) / abs(dx) if dx else math.inf
    scale_y = (height / 2) / abs(dy) if dy else math.inf
    scale = min(scale_x, scale_y)
    return sx + dx * scale, sy + dy * scale


def node_size(ref: str, questions: dict[str, Any]) -> tuple[int, int]:
    return (QUESTION_W, QUESTION_H) if ref in questions else (NODE_W, NODE_H)


def render(data: dict[str, Any]) -> str:
    groups = index(data.get("groups", []))
    questions = index(data.get("questions", []))
    layout = data.get("layout", {})
    positions = layout.get("positions", {}) if isinstance(layout, dict) else {}
    if not isinstance(positions, dict):
        raise ValueError("layout.positions must be an object")

    drawable = {**groups, **questions}
    centers: dict[str, tuple[float, float]] = {
        ref: position(ref, positions) for ref in drawable
    }

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "  <defs>",
        '    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#222"/>',
        "    </marker>",
        "  </defs>",
        '  <rect x="0" y="0" width="100%" height="100%" fill="white"/>',
        f'  <text x="40" y="38" font-family="{FONT_FAMILY}" font-size="16" fill="#333">Spatial projection — positions are layout data, not semantic relations</text>',
    ]

    # Explicit relations are drawn before nodes so labels and nodes stay readable.
    # The diagram may use display_label; predicate remains canonical in the semantic record.
    for relation in data.get("relations", []):
        source = str(relation.get("from", ""))
        target = str(relation.get("to", ""))
        if source not in centers or target not in centers:
            continue
        sw, sh = node_size(source, questions)
        tw, th = node_size(target, questions)
        start = rect_edge_point(centers[source], centers[target], sw, sh)
        end = rect_edge_point(centers[target], centers[source], tw, th)
        direction = str(relation.get("direction", "unspecified"))
        marker_end = ' marker-end="url(#arrow)"' if direction in {"directed", "reciprocal"} else ""
        marker_start = ' marker-start="url(#arrow)"' if direction == "reciprocal" else ""
        out.append(
            f'  <line x1="{start[0]:.1f}" y1="{start[1]:.1f}" x2="{end[0]:.1f}" y2="{end[1]:.1f}" stroke="#222" stroke-width="2"{marker_start}{marker_end}/>'
        )
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        label = f'{relation.get("id", "R?")}｜{display_text(relation, "predicate")}'
        label_lines = lines(label, width=18, max_lines=2)
        box_w = 230
        box_h = 18 * len(label_lines) + 14
        out.append(
            f'  <rect x="{mx - box_w/2:.1f}" y="{my - box_h/2:.1f}" width="{box_w}" height="{box_h}" rx="8" fill="white" stroke="#777" stroke-width="1"/>'
        )
        for i, line in enumerate(label_lines):
            y = my - (len(label_lines) - 1) * 9 + i * 18 + 5
            out.append(
                f'  <text x="{mx:.1f}" y="{y:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="12" fill="#222">{svg_text(line)}</text>'
            )

    # Question-origin links are explicitly labelled as non-asserted semantic relations.
    for question in questions.values():
        qid = str(question.get("id", ""))
        if qid not in centers:
            continue
        for origin in question.get("arises_from", []):
            origin = str(origin)
            if origin not in centers:
                continue
            sw, sh = node_size(origin, questions)
            qw, qh = node_size(qid, questions)
            start = rect_edge_point(centers[origin], centers[qid], sw, sh)
            end = rect_edge_point(centers[qid], centers[origin], qw, qh)
            out.append(
                f'  <line x1="{start[0]:.1f}" y1="{start[1]:.1f}" x2="{end[0]:.1f}" y2="{end[1]:.1f}" stroke="#777" stroke-width="1.5" stroke-dasharray="7 6"/>'
            )
            mx = (start[0] + end[0]) / 2
            my = (start[1] + end[1]) / 2
            label = "question provenance / not asserted relation"
            label_w = 270
            out.append(
                f'  <rect x="{mx - label_w/2:.1f}" y="{my - 11:.1f}" width="{label_w}" height="22" rx="5" fill="white"/>'
            )
            out.append(
                f'  <text x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="11" fill="#555">{label}</text>'
            )

    for gid, group in groups.items():
        cx, cy = centers[gid]
        x = cx - NODE_W / 2
        y = cy - NODE_H / 2
        out.append(
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{NODE_W}" height="{NODE_H}" rx="18" fill="white" stroke="#222" stroke-width="2"/>'
        )
        out.append(
            f'  <text x="{cx:.1f}" y="{y + 25:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#111">{svg_text(gid)}</text>'
        )
        for i, line in enumerate(lines(str(group.get("label", "")), width=20, max_lines=4)):
            out.append(
                f'  <text x="{cx:.1f}" y="{y + 50 + i*18:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="14" fill="#222">{svg_text(line)}</text>'
            )

    for qid, question in questions.items():
        cx, cy = centers[qid]
        x = cx - QUESTION_W / 2
        y = cy - QUESTION_H / 2
        out.append(
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{QUESTION_W}" height="{QUESTION_H}" rx="18" fill="white" stroke="#666" stroke-width="1.5" stroke-dasharray="8 6"/>'
        )
        out.append(
            f'  <text x="{cx:.1f}" y="{y + 25:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="14" font-weight="700" fill="#333">{svg_text(qid)}?</text>'
        )
        for i, line in enumerate(lines(display_text(question, "text"), width=19, max_lines=3)):
            out.append(
                f'  <text x="{cx:.1f}" y="{y + 49 + i*18:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="13" fill="#333">{svg_text(line)}</text>'
            )

    out.append('  <text x="40" y="770" font-family="sans-serif" font-size="13" fill="#555">Edge display labels are projections; canonical predicates remain in the semantic record.</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a free-position group-level SVG projection from affinity-map JSON.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    data = load_map(args.input)
    output = render(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
