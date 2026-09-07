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
REPRESENTATION_PATH = ROOT / "references" / "REPRESENTATION.md"


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


def check_relation_readback_contract() -> None:
    representation = REPRESENTATION_PATH.read_text(encoding="utf-8")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    assert_true(
        "Explicit relations must survive proposition read-back" in representation,
        "representation grammar must keep proposition read-back for explicit semantic relations",
    )
    assert_true(
        "read-backは監査操作" in representation,
        "relation read-back must remain an audit operation rather than duplicated canonical meaning",
    )
    assert_true(
        "Questionable / missing relation candidate" in representation,
        "representation grammar must keep questionable relations as question candidates",
    )
    assert_true(
        "missing linkの**問い**" in representation,
        "missing-link notation must remain a question rather than a relation assertion",
    )

    assert_true(
        "Read-back audit" in template,
        "standard output relation inventory must expose read-back audit status",
    )
    assert_true(
        "Questionable relation / missing-link candidates" in template,
        "standard output must keep questionable relations separate from relation assertions",
    )
    assert_true(
        "ここにあるものは `R` ではない" in template,
        "questionable-link candidates must not be represented as explicit R relations",
    )
    assert_true(
        "support / refute" in template,
        "questionable-link inventory must state what would support or refute a candidate",
    )


def check_questionable_relation_metadata() -> None:
    valid_candidate = {
        "format": "affinity-map",
        "version": "0.2",
        "sources": [{"id": "S01", "ref": "source"}],
        "cards": [
            {"id": "C001", "text": "one", "source_refs": ["S01"]},
            {"id": "C002", "text": "two", "source_refs": ["S01"]},
        ],
        "groups": [
            {"id": "G01", "label": "group one", "members": ["C001"]},
            {"id": "G02", "label": "group two", "members": ["C002"]},
        ],
        "questions": [
            {
                "id": "Q01",
                "text": "Is there a relation between the groups?",
                "arises_from": ["G01", "G02"],
                "candidate_relation_between": ["G01", "G02"],
                "would_clarify_refs": ["C001", "S01"],
                "handling": "keep as question",
            }
        ],
    }
    errors, warnings = validate(valid_candidate)
    assert_true(not errors, f"valid questionable relation candidate has errors: {errors}")
    assert_true(not warnings, f"valid questionable relation candidate has warnings: {warnings}")

    same_endpoint = {
        **valid_candidate,
        "questions": [
            {
                "id": "Q01",
                "text": "self relation?",
                "candidate_relation_between": ["G01", "G01"],
            }
        ],
    }
    same_errors, _ = validate(same_endpoint)
    assert_true(
        any("two distinct semantic nodes" in error for error in same_errors),
        "questionable relation candidate must reject identical endpoints",
    )

    unknown_endpoint = {
        **valid_candidate,
        "questions": [
            {
                "id": "Q01",
                "text": "unknown relation?",
                "candidate_relation_between": ["G01", "G404"],
            }
        ],
    }
    unknown_errors, _ = validate(unknown_endpoint)
    assert_true(
        any("candidate relation endpoint does not resolve" in error for error in unknown_errors),
        "questionable relation candidate must reject unknown semantic endpoints",
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
    check_relation_readback_contract()
    check_questionable_relation_metadata()

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "hierarchy.mmd"
        path.write_text(hierarchy, encoding="utf-8")
        assert_true(path.stat().st_size > 0, "generated hierarchy source must be non-empty")

    print("Representation regression checks passed")
    print(f"collapsed lineage lines: {len(collapsed_source.splitlines())}")
    print(f"expanded lineage lines: {len(expanded_source.splitlines())}")


if __name__ == "__main__":
    main()
