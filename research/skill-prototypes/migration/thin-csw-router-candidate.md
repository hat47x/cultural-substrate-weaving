# 文化的体系を認知場として開き、対象へ戻して確かめる — thin CSW router candidate

Status: research replacement candidate for `src/ja-JP/ROUTER.md`
Date: 2026-09-06

**外部体系から得た構造は対象へ返して確かめる。対象側の材料で独立に支えられた部分だけを対象所見とし、体系から生じた問い・仮説・構成資源は由来を保つ。**

本スキルは、文化的体系を答えや分類器として使うのではなく、対象を見るための一時的な認知場として開く。

位置、関係、状態、遷移、周期、象徴、境界、経路など、通常分析とは異なる構造候補を得たら、対象材料へ戻して、何が支えられ、何が支えられず、何が新しい問いとして残るかを確かめる。

材料の親和統合や複数roundの差分再開が必要な場合、利用可能なら専用のcompatible realizationへ委ねる。CSWはそれらの内部アルゴリズムを所有しない。

- one-round material synthesis: `affinity-synthesis` またはcompatible Method realization
- multi-round delta / reopen orchestration: `iterative-inquiry-synthesis` またはcompatible Method realization

compatible realizationがない環境でも、CSW自体の文化体系探索、帰属保持、対象側へのverification handoffは行える。ただし、実行していない親和統合やmulti-round orchestrationを実行済みとは称しない。

本スキル自体は領域固有知識を収録しない。必要な領域知識・品質基準・専門手順は、呼び出し側のコンテキスト、利用可能な資料、または併用する領域スキルから受け取る。

本スキルを使う範囲、文化体系の利用量、読み込み深度、停止・採否・公開などの決定権は、本スキルの静的規則には置かない。依頼者・著者の指定、上位の設定・指示、または実行AIへ与えられた委任に従う。

## 認知姿勢

対象から自分の読みを修正され得る位置に置く。

これは知識や仮説を捨てることではない。十分に材料へ触れた後は大胆に考えてよいが、新しく生じた意味を元材料が最初から語っていた事実へ書き換えない。

詳細は `core/cognitive-stance.md` を読む。

## 最小実行手順

1. **外部利用条件を受け取る**：依頼範囲、目的、判断の留保先、実行AIへ委ねられた裁量を確認する。
2. **認知姿勢を置く**：`core/cognitive-stance.md` に従い、自分の説明を対象より上位へ固定しない。
3. **基準線と保持事項を置く**：元材料、対象固有の事実・例外、領域固有手法だけの出力を確認する。
4. **必要なら材料統合へ委ねる**：多数・異種の材料から構造を立ち上げる必要があれば、`methods/integration.md` の接続契約からcompatible synthesis realizationへ渡す。
5. **文化体系を開く**：外部利用条件と委任範囲に応じて `not_loaded / probe / preview / full / enacted` 等を使い分ける。
6. **探索する**：文化体系から問い・関係・状態・遷移・対応候補を得る。体系固有構造を汎用語へ早く薄めない。
7. **対象へ返す**：`target_supported / framework_generated / cross_field_emergent / unresolved` を混同せず保持する。
8. **必要ならround deltaへ渡す**：新しいframework contactが旧artifactや残差へ触れるなら、`core/iteration.md` の接続契約からcompatible iterative realizationへ渡す。
9. **実作業へ反映する**：成果物、判断材料、調査方針、残差、再開条件へ反映する。区切りや採否は外部利用条件に従う。

文化体系の利用数、全文読解、体系固有操作の実行量を、それ自体で成功度とする規則は置かない。

## 重要な区別

- **状態記録 ≠ 決定権**：来歴、証拠状態、利用深度を区別して残すことと、その区別から採否・停止・公開を決めることを分ける。
- **保存 ≠ 現在の注意**：正本は厚く残し、今回前景化する範囲は必要に応じて選ぶ。
- **探索 ≠ 帰属**：体系から問いを得ることと、対象にその構造があると主張することを分ける。
- **de-binding ≠ 証拠**：体系語彙を外して文が成立しても、対象側の独立supportが増えたことにはならない。
- **利用状態 ≠ 成否評価**：読み込み状態や不採用は探索状態であり、それ自体を成否評価にしない。
- **framework output ≠ synthesis authority**：文化体系から来た候補は、親和統合へ渡す材料にはなれるが、groupingや表札を先に決める権威ではない。
- **synthesis result ≠ framework verification**：同島、近接、relation、resonanceが生じても、それ自体では文化体系の妥当性を独立検証しない。

## 参照ファイルを選ぶ

| 判断・処理 | 読むファイル |
|---|---|
| 対象へ入る認知姿勢 | [00-cognitive-stance.md](core/cognitive-stance.md) |
| 利用範囲、読み込み深度 | [00-activation.md](core/activation.md) |
| 決定権、帰属、二重の忠実性、保存原則 | [00-principles-and-constraints.md](core/principles-and-constraints.md) |
| 新framework contactをround deltaへ渡す | [00-iteration.md](core/iteration.md) |
| 対象範囲、基準線、事実整理 | [01-scope-and-facts.md](methods/scope-and-facts.md) |
| 体系の選定、探索／帰属利用 | [02-system-selection.md](methods/system-selection.md) |
| 割当、遷移、採用後検査、出口 | [02a-framework-application.md](methods/framework-application.md) |
| 関係種別、欠落と接続、複数体系 | [03-transformation.md](methods/transformation.md) |
| 人間の身体反応をTaihekiで探索 | [05-human-and-taiheki.md](domains/human-and-taiheki.md) |
| 判断来歴、長期event | [08-governance-and-records.md](governance/governance-and-records.md) |
| 最終評価 | [09-evaluation.md](governance/evaluation.md) |
| 多数・異種材料の親和統合への接続 | [10-integration.md](methods/integration.md) |

## 読み込み方

一括読み込みを前提にしない。

- 認知姿勢が必要なら `core/cognitive-stance.md`。
- 利用深度を扱うなら `core/activation.md`。
- cultural frameworkの候補選択・native operationが必要なら該当methodを読む。
- one-round synthesisが必要なら接続契約からcompatible realizationへ委ねる。
- multi-round再開が必要なら接続契約からcompatible iterative realizationへ委ねる。

対象固有の情報は静的Skillへ吸収せず、動的材料として扱う。
