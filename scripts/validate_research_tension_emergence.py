#!/usr/bin/env python3
"""Validate CSW target-framework tension / cross-field emergence boundaries.

This research check keeps the new tension-derived emergence principle inside CSW
and prevents it from becoming a mandatory Layer-1 synthesis algorithm.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED: dict[str, tuple[str, ...]] = {
    "src/ja-JP/core/cognitive-stance.md": (
        "## 一致より、緊張から何が生まれるかを見る",
        "止揚（Aufhebung）",
        "正・反・合の固定段階",
        "cross_field_emergent",
    ),
    "src/ja-JP/core/principles-and-constraints.md": (
        "対象と体系の差・抵抗・矛盾が接触によってどう変形するか",
        "適合よりも不一致・抵抗・相互修正から生じたものを含む",
        "対立を自動的に「解決済み」にするラベルではない",
    ),
    "src/ja-JP/methods/transformation.md": (
        "## 対象と体系の緊張を変換材料にする",
        "preserved_from_target:",
        "preserved_from_framework:",
        "negated_or_revised:",
        "newly_recomposed:",
        "第三構造としない",
    ),
    "src/ja-JP/methods/integration.md": (
        "target_side_tension:",
        "framework_side_claim_or_operation:",
        "cross_field_candidate:",
        "これはLayer 1に弁証法や文化体系処理を実装させるためではない",
    ),
    "src/en-US/core/cognitive-stance.md": (
        "## Look for what tension produces, not only for fit",
        "sublation (Aufhebung)",
        "fixed thesis-antithesis-synthesis stage model",
        "cross_field_emergent",
    ),
    "src/en-US/core/principles-and-constraints.md": (
        "observe how difference, resistance, or contradiction changes through contact",
        "misfit, resistance, and mutual revision rather than only by agreement",
        "automatically declares a contradiction resolved",
    ),
    "src/en-US/methods/transformation.md": (
        "## Use target-framework tension as transformation material",
        "preserved_from_target:",
        "preserved_from_framework:",
        "negated_or_revised:",
        "newly_recomposed:",
        "Do not call a simple midpoint between target and framework a third structure",
    ),
    "src/en-US/methods/integration.md": (
        "target_side_tension:",
        "framework_side_claim_or_operation:",
        "cross_field_candidate:",
        "This does not ask Layer 1 to implement dialectics or cultural-framework interpretation",
    ),
    "research/skill-prototypes/evals/CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md": (
        "対象と体系の緊張、不一致、抵抗、相互修正から生じる情報",
        "Hegelian stage modelをそのままruntimeへ導入する意味ではない",
        "clean correspondence is not automatically the most informative result",
        "do not repair the target to save the framework",
        "do not weaken the framework into a convenient metaphor",
        "sublation preserves consequential difference",
        "tension may end without synthesis",
        "framework agreement can be less informative than disagreement",
    ),
}

FORBIDDEN_IN_LAYER1: dict[str, tuple[str, ...]] = {
    "research/skill-prototypes/affinity-synthesis/SKILL.md": (
        "止揚",
        "アウフヘーベン",
        "正・反・合",
    ),
    "research/skill-prototypes/affinity-synthesis/SKILL.en.md": (
        "sublation",
        "Aufhebung",
        "thesis-antithesis-synthesis",
    ),
    "research/skill-prototypes/affinity-synthesis/references/METHOD.md": (
        "止揚",
        "アウフヘーベン",
        "正・反・合",
    ),
    "research/skill-prototypes/affinity-synthesis/references/METHOD.en.md": (
        "sublation",
        "Aufhebung",
        "thesis-antithesis-synthesis",
    ),
}


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def validate() -> list[str]:
    errors: list[str] = []

    for relative, markers in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"required tension/emergence asset missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing tension/emergence marker: {marker}")

    for relative, markers in FORBIDDEN_IN_LAYER1.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Layer-1 boundary asset missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                errors.append(
                    f"{relative}: CSW-specific tension/sublation vocabulary leaked into Layer 1: {marker}"
                )

    # The handoff contract must carry the generating tension, not only a polished third statement.
    ja_integration = _read("src/ja-JP/methods/integration.md")
    trio = (
        "target_side_tension:",
        "framework_side_claim_or_operation:",
        "cross_field_candidate:",
    )
    if not all(marker in ja_integration for marker in trio):
        errors.append("Japanese CSW -> Layer-1 handoff must preserve the full tension lineage trio")

    en_integration = _read("src/en-US/methods/integration.md")
    if not all(marker in en_integration for marker in trio):
        errors.append("English CSW -> Layer-1 handoff must preserve the full tension lineage trio")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Research target-framework tension / emergence contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
