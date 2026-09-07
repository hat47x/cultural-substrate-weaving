from __future__ import annotations

import tempfile
from collections import Counter
from pathlib import Path

from generate_large_fixture import build
from render_hierarchy import render as render_hierarchy
from render_lineage import LineageGraph
from validate_map import validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "references" / "TEMPLATE.md"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def direct_card_membership_counts(data: dict) -> Counter[str]:
    cards = {str(card["id"]) for card in data.get("cards", [])}
    counts: Counter[str] = Counter()
    for group in data.get("groups", []):
        for member in group.get("members", []):
            member = str(member)
            if member in cards:
                counts[member] += 1
    return counts


def check_reader_facing_overview() -> None:
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert_true(
        "Reader-facing Overview — fill last" in text,
        "standard output must keep the reader-facing overview as a post-synthesis projection",
    )
    assert_true(
        "Member count" in text and "truth" in text and "importance" in text,
        "overview must state that member count is descriptive rather than truth/importance",
    )
    assert_true(
        "Anchor refs" in text and "navigation" in text,
        "overview anchor refs must remain navigation rather than evidence substitution",
    )
    assert_true(
        "Residuals that change the reading" in text,
        "overview must keep residuals visible to summary-only readers",
    )
    assert_true(
        "Weight (H/M/L)" not in text,
        "standard output must not import affinity-map weight scoring as a default semantic field",
    )


def main() -> None:
    data = build()

    errors, warnings = validate(data)
    assert_true(not errors, f"large fixture has semantic errors: {errors}")
    assert_true(not warnings, f"large fixture has semantic warnings: {warnings}")

    assert_true(len(data.get("cards", [])) == 114, "fixture must contain 114 cards")
    assert_true(len(data.get("groups", [])) == 13, "fixture must contain 10 leaf + 3 higher groups")

    membership = direct_card_membership_counts(data)
    assert_true(len(membership) == 114, "every card must appear in a direct leaf membership")
    assert_true(set(membership.values()) == {1}, "every card must have exactly one direct leaf membership")

    hierarchy = render_hierarchy(data, include_relations=True)
    assert_true(
        "higher-order membership / not semantic relation" in hierarchy,
        "hierarchy projection must distinguish membership from semantic relation",
    )
    assert_true("%% roots: G_ROOT" in hierarchy, "recursive fixture must resolve one root")

    collapsed = LineageGraph(data, "groups")
    collapsed.walk("N001")
    collapsed_source = collapsed.mermaid()

    expanded = LineageGraph(data, "cards")
    expanded.walk("N001")
    expanded_source = expanded.mermaid()

    assert_true("cards collapsed" in collapsed_source, "group-detail lineage must collapse leaf cards")
    assert_true("cards collapsed" not in expanded_source, "card-detail lineage must expand cards")
    assert_true(
        len(collapsed_source.splitlines()) < len(expanded_source.splitlines()),
        "collapsed lineage must be smaller than fully expanded lineage",
    )

    invalid = {
        "format": "affinity-map",
        "version": "0.2",
        "cards": [{"id": "C001", "text": "one"}],
        "groups": [
            {"id": "G01", "label": "one", "members": ["G02", "C001"]},
            {"id": "G02", "label": "two", "members": ["G01"]},
        ],
        "narratives": [
            {"id": "N001", "text": "orphan narrative", "basis": ["G404"]}
        ],
    }
    invalid_errors, invalid_warnings = validate(invalid)
    assert_true(
        any("group membership cycle" in error for error in invalid_errors),
        "validator must reject recursive membership cycles",
    )
    assert_true(
        any("narrative N001 basis ref does not resolve" in warning for warning in invalid_warnings),
        "validator must expose unresolved narrative lineage",
    )

    check_reader_facing_overview()

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "hierarchy.mmd"
        path.write_text(hierarchy, encoding="utf-8")
        assert_true(path.stat().st_size > 0, "generated hierarchy source must be non-empty")

    print("Representation regression checks passed")
    print(f"collapsed lineage lines: {len(collapsed_source.splitlines())}")
    print(f"expanded lineage lines: {len(expanded_source.splitlines())}")


if __name__ == "__main__":
    main()
