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
            "CSWは材料統合の内部アルゴリズムを再実装しない",
        ),
        errors,
    )
    require(
        "src/ja-JP/core/iteration.md",
        (
            "round delta",
            "compatible iterative realization",
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
            "English (`en-US`) | parity backlog",
        ),
        errors,
    )
    require(
        "README.en.md",
        (
            "This research branch is testing a method split",
            "This does not mean that a three-Skill distribution has already been publicly released",
            "English (`en-US`) | Parity backlog",
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
