#!/usr/bin/env python3
"""Check semantic invariant parity between Japanese and English Layer 2 methods.

This is intentionally narrower than translation review. It verifies that the
same numbered invariant surface exists in both research Method Definitions and
that the two high-risk boundaries discovered during split research remain
explicit. It does not require sentence-by-sentence translation identity.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JA_METHOD = ROOT / "references" / "METHOD.md"
EN_METHOD = ROOT / "references" / "METHOD.en.md"
EXPECTED_IDS = tuple(range(1, 17))
INVARIANT_RE = re.compile(r"^### I(\d+)\.\s+(.+?)\s*$", re.MULTILINE)


def invariant_entries(text: str) -> list[tuple[int, str]]:
    return [(int(number), title) for number, title in INVARIANT_RE.findall(text)]


def invariant_map(entries: list[tuple[int, str]]) -> dict[int, str]:
    return dict(entries)


def validate_texts(ja: str, en: str) -> list[str]:
    errors: list[str] = []
    ja_entries = invariant_entries(ja)
    en_entries = invariant_entries(en)
    ja_map = invariant_map(ja_entries)
    en_map = invariant_map(en_entries)

    expected = set(EXPECTED_IDS)
    for locale, entries, mapping in (
        ("ja-JP", ja_entries, ja_map),
        ("en-US", en_entries, en_map),
    ):
        counts = Counter(number for number, _ in entries)
        duplicates = sorted(number for number, count in counts.items() if count > 1)
        if duplicates:
            errors.append(f"{locale} Method has duplicate invariant ids: {duplicates}")

        missing = sorted(expected - set(mapping))
        extra = sorted(set(mapping) - expected)
        if missing or extra:
            errors.append(
                f"{locale} Method invariant ids drifted; missing={missing}, extra={extra}"
            )

        if len(entries) != len(EXPECTED_IDS):
            errors.append(
                f"{locale} Method must expose exactly {len(EXPECTED_IDS)} numbered invariant headings; "
                f"found={len(entries)}"
            )

    if set(ja_map) != set(en_map):
        errors.append(
            "Japanese and English Method Definitions do not expose the same invariant ids"
        )

    high_risk_markers = {
        "ja-JP": (
            (ja, "### I15. Missing synthesis realization stays explicit"),
            (ja, "### I16. Carry-forward state is not reopen or continuation authority"),
            (ja, "必要な統合を実行済みと称さず"),
            (ja, "preserve / carry forward"),
            (ja, "reopen now"),
            (ja, "continue another round"),
            (ja, "反復回数そのものをtruth、confidence、independent supportの増加へ変換しない"),
        ),
        "en-US": (
            (en, "### I15. Missing synthesis realization stays explicit"),
            (en, "### I16. Carry-forward state is not reopen or continuation authority"),
            (en, "Do not claim a required synthesis ran"),
            (en, "preserve / carry forward"),
            (en, "reopen now"),
            (en, "continue another round"),
            (en, "Round count itself is not converted into greater truth, confidence, or independent support"),
        ),
    }
    for locale, checks in high_risk_markers.items():
        for text, marker in checks:
            if marker not in text:
                errors.append(f"{locale} Method missing parity marker: {marker!r}")

    return errors


def validate() -> list[str]:
    ja = JA_METHOD.read_text(encoding="utf-8")
    en = EN_METHOD.read_text(encoding="utf-8")
    return validate_texts(ja, en)


def main() -> int:
    try:
        errors = validate()
    except OSError as exc:
        print(f"iterative method parity check failed to read source: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Iterative Inquiry Method invariant parity passed (I1-I16)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
