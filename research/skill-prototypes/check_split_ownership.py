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
        "src/ja-JP/methods/integration.md",
        (
            "接続契約",
            "compatible realization",
            "CSWはこれらの内部アルゴリズムを独自に再実装しない",
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
        "src/en-US/methods/integration.md",
        (
            "This document does not implement affinity synthesis itself",
            "compatible realization",
            "CSW does not independently re-implement these internal algorithms",
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
    require(
        "research/skill-prototypes/affinity-synthesis/references/METHOD.en.md",
        (
            "I1. Material-led structure",
            "I14. Rendering is a projection, not the method authority",
            "A realization may be replaced by an existing external Skill",
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
