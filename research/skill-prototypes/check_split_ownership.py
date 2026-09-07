from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(relative: str, markers: tuple[str, ...], errors: list[str]) -> None:
    value = text(relative)
    for marker in markers:
        if marker not in value:
            errors.append(f"{relative}: required split-ownership marker missing: {marker}")


def forbid(relative: str, markers: tuple[str, ...], errors: list[str]) -> None:
    value = text(relative)
    for marker in markers:
        if marker in value:
            errors.append(f"{relative}: stale monolithic ownership wording remains: {marker}")


def main() -> None:
    errors: list[str] = []

    require(
        "src/ja-JP/ROUTER.md",
        (
            "CSWはそれらの内部アルゴリズムを所有しない",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
            "実行していない親和統合やmulti-round orchestrationを実行済みとは称しない",
            "対象が体系を押し返す不一致・抵抗・逆転",
            "対応 ≠ 統合",
        ),
        errors,
    )
    forbid(
        "src/ja-JP/ROUTER.md",
        (
            "本スキルは二つの能力を組み合わせる",
            "KJ法による統合",
        ),
        errors,
    )
    require(
        "src/ja-JP/core/cognitive-stance.md",
        (
            "一致より、緊張から何が生まれるかを見る",
            "止揚（Aufhebung）",
            "正・反・合の固定段階",
            "cross_field_emergent",
        ),
        errors,
    )
    require(
        "src/ja-JP/core/principles-and-constraints.md",
        (
            "対象と体系の差・抵抗・矛盾が接触によってどう変形するか",
            "適合よりも不一致・抵抗・相互修正から生じたものを含む",
            "対立を自動的に「解決済み」にするラベルではない",
        ),
        errors,
    )
    require(
        "src/ja-JP/methods/integration.md",
        (
            "接続契約",
            "compatible realization",
            "CSWはこれらの内部アルゴリズムを独自に再実装しない",
            "target_side_tension:",
            "framework_side_claim_or_operation:",
            "cross_field_candidate:",
            "これはLayer 1に弁証法や文化体系処理を実装させるためではない",
        ),
        errors,
    )
    require(
        "src/ja-JP/methods/transformation.md",
        (
            "対象と体系の緊張を変換材料にする",
            "一致、不一致、抵抗、逆転、欠落、過剰、相互修正",
            "正 → 反 → 合",
            "第三構造としない",
        ),
        errors,
    )
    require(
        "src/ja-JP/core/iteration.md",
        (
            "round delta",
            "compatible iterative realization",
            "CSWはこれらを別系統のround管理として再実装しない",
        ),
        errors,
    )

    require(
        "src/en-US/ROUTER.md",
        (
            "CSW does not own those internal algorithms",
            "affinity-synthesis",
            "iterative-inquiry-synthesis",
            "Do not claim that affinity synthesis or multi-round orchestration was executed when it was not",
            "the target pushing back against the framework through misfit, resistance, reversal, or excess",
            "Correspondence != synthesis",
        ),
        errors,
    )
    forbid(
        "src/en-US/ROUTER.md",
        (
            "This skill combines two capabilities",
            "Integration through KJ",
        ),
        errors,
    )
    require(
        "src/en-US/core/cognitive-stance.md",
        (
            "Look for what tension produces, not only for fit",
            "sublation (Aufhebung)",
            "fixed thesis-antithesis-synthesis stage model",
            "cross_field_emergent",
        ),
        errors,
    )
    require(
        "src/en-US/core/principles-and-constraints.md",
        (
            "observe how difference, resistance, or contradiction changes through contact",
            "misfit, resistance, and mutual revision rather than only by agreement",
            "automatically declares a contradiction resolved",
        ),
        errors,
    )
    require(
        "src/en-US/methods/integration.md",
        (
            "This document does not implement affinity synthesis itself",
            "compatible realization",
            "CSW does not independently re-implement these internal algorithms",
            "target_side_tension:",
            "framework_side_claim_or_operation:",
            "cross_field_candidate:",
            "This does not ask Layer 1 to implement dialectics or cultural-framework interpretation",
        ),
        errors,
    )
    require(
        "src/en-US/methods/transformation.md",
        (
            "Use target-framework tension as transformation material",
            "fit, misfit, resistance, reversal, absence, excess, and mutual revision",
            "thesis -> antithesis -> synthesis",
            "Do not call a simple midpoint between target and framework a third structure",
        ),
        errors,
    )
    require(
        "src/en-US/core/iteration.md",
        (
            "This document does not implement multi-round inquiry orchestration itself",
            "compatible realization",
            "CSW does not independently re-implement this general round governance",
        ),
        errors,
    )

    require(
        "research/skill-prototypes/affinity-synthesis/SKILL.en.md",
        (
            "Status: research English realization",
            "This Skill owns **one synthesis round**",
            "Join when semantic unity must be preserved; split when epistemic state must be preserved",
            "membership",
            "secondary resonance",
        ),
        errors,
    )
    forbid(
        "research/skill-prototypes/affinity-synthesis/SKILL.en.md",
        (
            "thesis-antithesis-synthesis",
            "sublation",
            "Aufhebung",
            "target-framework tension",
        ),
        errors,
    )
    require(
        "research/skill-prototypes/affinity-synthesis/references/METHOD.en.md",
        (
            "I1. Material-led structure",
            "I14. Rendering is a projection, not the method authority",
            "A realization may be replaced by an existing external Skill",
        ),
        errors,
    )
    forbid(
        "research/skill-prototypes/affinity-synthesis/references/METHOD.en.md",
        (
            "thesis-antithesis-synthesis",
            "sublation",
            "Aufhebung",
        ),
        errors,
    )
    require(
        "research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md",
        (
            "Status: research English realization",
            "does not own the one-round synthesis algorithm",
            "Semantic delta is not diagram delta",
            "Stable semantic handles",
        ),
        errors,
    )
    require(
        "research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.en.md",
        (
            "I1. A round is a delta, not a restart",
            "I14. Semantic delta and representation delta are distinct",
            "Layer 2 does not reimplement Layer 1 grouping or labeling algorithms",
        ),
        errors,
    )

    require(
        "research/skill-prototypes/evals/CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md",
        (
            "対象と体系の緊張、不一致、抵抗、相互修正から生じる情報",
            "Hegelian stage modelをそのままruntimeへ導入する意味ではない",
            "tension may end without synthesis",
            "framework agreement can be less informative than disagreement",
        ),
        errors,
    )

    require(
        "AGENTS.md",
        (
            "one canonical runtime skill plus two research-stage sibling method prototypes",
            "affinity-synthesis (research prototype)",
            "iterative-inquiry-synthesis (research prototype)",
            "do not move their internal algorithms back into `src/`",
        ),
        errors,
    )
    forbid(
        "AGENTS.md",
        (
            "The skill has two core capabilities",
            "KJ carding, grouping, integration, gap discovery, and transformation checks | Writing craft",
        ),
        errors,
    )

    require(
        "README.md",
        (
            "このresearch branchでは方法分離を試験中です",
            "これはまだ公開済みの三Skill構成を意味しません",
            "英語の `SKILL.en.md` と `METHOD.en.md` の初期版",
            "English (`en-US`) | translated draft",
        ),
        errors,
    )
    require(
        "README.en.md",
        (
            "This research branch is testing a method split",
            "This does not mean that a three-Skill distribution has already been publicly released",
            "initial English `SKILL.en.md` and `METHOD.en.md` drafts",
            "English (`en-US`) | Translated draft",
        ),
        errors,
    )

    require(
        "adapters/microsoft-copilot/ja-JP/instructions.md",
        (
            "親和統合コアの最小互換手順を埋め込んでいます",
            "これはCSW本体が材料統合アルゴリズムを所有するという意味ではなく",
            "完全なmulti-round orchestrationではありません",
        ),
        errors,
    )
    forbid(
        "adapters/microsoft-copilot/ja-JP/instructions.md",
        ("文化的体系による構造探索とKJ法による統合の中核だけを扱います",),
        errors,
    )
    require(
        "adapters/microsoft-copilot/en-US/instructions.md",
        (
            "This limited profile embeds a minimal compatible material-synthesis fallback",
            "That does not mean CSW itself owns the material-synthesis algorithm",
            "This is not complete multi-round orchestration",
        ),
        errors,
    )
    forbid(
        "adapters/microsoft-copilot/en-US/instructions.md",
        ("It keeps the core of cultural-framework exploration and KJ integration",),
        errors,
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("Split ownership regression check passed")


if __name__ == "__main__":
    main()
