from __future__ import annotations

import argparse
import json
from pathlib import Path


GROUP_SIZES = [14, 20, 8, 9, 10, 18, 11, 7, 13, 4]
GROUP_IDS = [f"G_{letter}" for letter in "ABCDEFGHIJ"]


def build() -> dict:
    cards: list[dict] = []
    groups: list[dict] = []
    current = 1

    for group_id, size in zip(GROUP_IDS, GROUP_SIZES):
        members: list[str] = []
        for _ in range(size):
            card_id = f"C{current:03d}"
            current += 1
            members.append(card_id)
            cards.append(
                {
                    "id": card_id,
                    "text": f"synthetic scale card {card_id}",
                }
            )
        groups.append(
            {
                "id": group_id,
                "label": f"Leaf group {group_id[-1]}",
                "members": members,
            }
        )

    groups.extend(
        [
            {
                "id": "G_SERIES_1",
                "label": "Higher-order series 1",
                "members": ["G_A", "G_F", "G_G", "G_J"],
            },
            {
                "id": "G_SERIES_2",
                "label": "Higher-order series 2",
                "members": ["G_B", "G_C", "G_H", "G_I"],
            },
            {
                "id": "G_ROOT",
                "label": "Whole synthesis",
                "members": ["G_SERIES_1", "G_SERIES_2", "G_D", "G_E"],
            },
        ]
    )

    return {
        "format": "affinity-map",
        "version": "0.2",
        "subject": {
            "question": "Synthetic 114-card recursive grouping stress fixture",
            "scope": "structure/load test only; carries no project source text",
        },
        "cards": cards,
        "groups": groups,
        "relations": [
            {
                "id": "R001",
                "from": "G_SERIES_1",
                "to": "G_SERIES_2",
                "direction": "unspecified",
                "predicate": "synthetic relation between the two higher-order series",
                "display_label": "series relation",
                "basis": ["G_SERIES_1", "G_SERIES_2"],
            }
        ],
        "narratives": [
            {
                "id": "N001",
                "text": "synthetic narrative claim derived from the whole synthesis",
                "display_label": "whole narrative",
                "basis": ["G_ROOT", "R001"],
            }
        ],
        "questions": [
            {
                "id": "Q001",
                "text": "what should be reopened next?",
                "arises_from": ["N001"],
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic 114-card recursive affinity-map fixture."
    )
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
