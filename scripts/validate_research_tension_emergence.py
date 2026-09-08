#!/usr/bin/env python3
"""Validate CSW target-framework tension / cross-field emergence boundaries.

This research check keeps tension-derived emergence as a CSW contact/attribution
responsibility, verifies it through runtime and evaluation, and prevents it from
becoming a mandatory Layer-1 or Layer-2 synthesis/orchestration algorithm.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED: dict[str, tuple[str, ...]] = {
    "src/ja-JP/ROUTER.md": (
        "体系との一致だけでなく、対象が体系を押し返す不一致・抵抗・逆転にも注意し",
        "**対応 ≠ 統合**",
        "第三構造が生じても、対象側の独立supportなしに事実へ昇格させない",
    ),
    "src/en-US/ROUTER.md": (
        "misfit, resistance, reversal, or excess",
        "**Correspondence != synthesis**",
        "Do not promote a third structure to target-side fact without independent target-side support",
    ),
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
    "src/ja-JP/governance/evaluation.md": (
        "## 一致より、情報を生んだ緊張を見る",
        "止揚を成功quotaにしない",
        "第三構造が生じなかった場合も、それを失敗として捏造で埋めていない",
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
    "src/en-US/governance/evaluation.md": (
        "## Look for informative tension rather than fit alone",
        "Do not make sublation a success quota",
        "When no third structure emerged, the result was not fabricated merely to make the exploration look successful",
    ),
    "docs/ja/maintainers/csw-tension-emergence-and-aufhebung-contract.md": (
        "文化体系が**都合のよい解釈資源**になりやすい",
        "アウフヘーベンを成功quotaや必須stageにしない",
        "対象との抵抗によって新しい差・問い・構造を立ち上げる認知場",
    ),
    "research/skill-prototypes/evals/CSW-TENSION-EMERGENCE-CASES.md": (
        "Framework fit is not itself a success condition",
        "Generic compromise masquerading as Aufhebung",
        "Tension without synthesis",
        "without turning those distinctions into a fixed stage sequence or success quota",
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
    "research/skill-prototypes/evals/CSW-HANDOFF-CASES.md": (
        "cross-field emergence is neither source fact nor pure framework output",
        "cross_field_emergent",
        "framework妥当性の追加supportとして数えない",
    ),
}

FORBIDDEN_OUTSIDE_CSW: dict[str, tuple[str, ...]] = {
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
    "research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md": (
        "止揚",
        "アウフヘーベン",
        "正・反・合",
    ),
    "research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md": (
        "sublation",
        "Aufhebung",
        "thesis-antithesis-synthesis",
    ),
    "research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.md": (
        "止揚",
        "アウフヘーベン",
        "正・反・合",
    ),
    "research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.en.md": (
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

    for relative, markers in FORBIDDEN_OUTSIDE_CSW.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"non-CSW boundary asset missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                errors.append(
                    f"{relative}: CSW-specific tension/sublation vocabulary leaked outside CSW ownership: {marker}"
                )

    # The handoff contract must carry the generating tension, not only a polished third statement.
    trio = (
        "target_side_tension:",
        "framework_side_claim_or_operation:",
        "cross_field_candidate:",
    )
    for locale in ("ja-JP", "en-US"):
        integration = _read(f"src/{locale}/methods/integration.md")
        if not all(marker in integration for marker in trio):
            errors.append(
                f"{locale} CSW -> Layer-1 handoff must preserve the full tension lineage trio"
            )

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
