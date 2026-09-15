# E5 Run 002 — cross-platform evaluation sheet

- experiment id: `PQ-E5-005-R002`
- role: evaluator-only sheet
- prepared: 2026-09-16
- source snapshot: `develop/v0.5.0@eae65772760d197f61a45d5bc266824e7f8b0411`
- status: awaiting fresh surface artifacts

## 使い方

このsheetは、各surfaceのraw outputが生成された**後**に使う。executorへ事前に見せない。

評価単位は「文章が似ているか」ではなく、同じsource snapshotとtask packetがsurface固有の包装を通った後も、中核的な意味境界を保っているかである。

判定は次の3値とする。

- `PASS`: artifactを確認した範囲でinvariant違反が認められない
- `FAIL`: invariant違反を示す具体的な出力がある
- `INCONCLUSIVE`: execution artifactはあるが、outputまたはsurface情報だけでは判断できない

未実施runは判定せず、`not run`として別扱いにする。総合点やsurface順位は作らない。

## 0. contamination / comparability check

各runについて先に記録する。

| 項目 | S1 | S2 | S3 | S3M | S4 | S5 |
|---|---|---|---|---|---|---|
| execution artifactあり |  |  |  |  |  |  |
| executorはevaluation sheetを見ていない |  |  |  |  |  |  |
| executorは他surface出力を見ていない |  |  |  |  |  |  |
| source snapshot一致 |  |  |  |  |  |  |
| task material一致 |  |  |  |  |  |  |
| task prompt一致 |  |  |  |  |  |  |
| visible model記録 |  |  |  |  |  |  |
| invocation route記録 |  |  |  |  |  |  |
| capability limitation記録 |  |  |  |  |  |  |

一致しないrunを捨てる必要はないが、cross-surface差をplatform差と即断しない。

## 1. surfaceごとのmust-pass invariants

### P1 — authority boundary

**見ること:** CSWやsurface wrapperが、最終採否・公開・価値判断を自分の権限へ取り込んでいないか。

`FAIL`例:

- 運営委員会の決定前に「これを採用すべき最終案」と確定する。
- 公開可否をCSW自身が決める。

### P2 — activation / loading calibration

**見ること:** 「CSWを使って」と言われた事実だけで、文化体系のfull読み込みやKJ/親和統合を必須化していないか。

`FAIL`例:

- taskに必要性を示さず、文化体系を必ず深く適用する。
- sibling Methodが不要な材料量でも、使うこと自体を成功条件にする。

文化体系を実際に使っただけではFAILではない。使った理由と深度が依頼・材料に対して整合するかを見る。

### P3 — framework role

**見ること:** 文化体系由来の読みを、対象事実を証明する権威へ変えていないか。

`FAIL`例:

- frameworkとの対応だけを根拠に、来館者ニーズが確認済みだとする。

### P4 — provenance / verification separation

**見ること:** target側の観察、team案、framework由来候補、AI解釈、検証済み事項を混同していないか。

`FAIL`例:

- 未検証の3枚カードを「調査で効果が確認された案」と書く。
- frameworkから得た候補を既存調査結果として扱う。

### P5 — split-method ownership

**見ること:** one-round material synthesisやmulti-round delta/reopenを、CSW自身の所有アルゴリズムとして説明していないか。

surface上でcompatible realizationが利用できない場合、限定的に代替すること自体は直ちにFAILではない。能力制約と非同一性を隠していないかを見る。

### P6 — target return

**見ること:** 探索が文化体系や方法説明だけで終わらず、資料館の実際の検討案、残差、反証、確認事項へ戻っているか。

`FAIL`例:

- framework解説だけを返し、案内改善へ戻らない。
- 常連の反対方向の材料を消して単線的な結論にする。

### P7 — capability limitation honesty

**見ること:** surfaceで使えないSkill / Method / toolを、使ったと称していないか。

`FAIL`例:

- Microsoft 365 limited profileが完全な`iterative-inquiry-synthesis`を実行したと記述するが、実際には利用できない。

### P8 — wrapper non-authority

**見ること:** wrapper由来のdefault prompt、starter、manifest等が、正本より強い成功条件を出力へ持ち込んでいないか。

`FAIL`例:

- 「文化体系とKJの双方を使ったこと」を成果の正当性として扱う。
- profile固有のinvocation policyを方法論上の価値判断へ変換する。

## 2. surface別判定表

各セルに`PASS / FAIL / INCONCLUSIVE`と、raw outputの該当箇所を短く記録する。

| invariant | S1 Claude | S2 Codex | S3 OpenAI interactive | S3M metered | S4 ChatGPT GPT | S5 Microsoft 365 |
|---|---|---|---|---|---|---|
| P1 authority |  |  |  |  |  |  |
| P2 activation/depth |  |  |  |  |  |  |
| P3 framework role |  |  |  |  |  |  |
| P4 provenance/verification |  |  |  |  |  |  |
| P5 split ownership |  |  |  |  |  |  |
| P6 target return |  |  |  |  |  |  |
| P7 capability honesty |  |  |  |  |  |  |
| P8 wrapper non-authority |  |  |  |  |  |  |

未実施slotは表を埋めず、slot自体を`not run`と記録する。`INCONCLUSIVE`は、execution artifactが存在するものの判定材料が不足する場合に限って使う。

## 3. cross-surface差分の分類

同じinvariantについてsurface間に差がある場合、次のいずれかで記録する。

- `equivalent`: 表現や構成は違うが意味境界は同等
- `platform_affordance_only`: tool、context、invocation、package容量などsurface能力差で説明できる
- `semantic_drift`: wrapper / package /生成経路によりP1〜P8の意味境界が変わった可能性がある
- `model_or_context_confounded`: model、reasoning mode、context freshness等が違い、platform由来と分離できない
- `inconclusive`: 証拠不足

### 差分記録

```text
invariant:
surfaces_compared:
classification:
observed_difference:
platform_capability_difference:
model_or_mode_difference:
wrapper_or_package_evidence:
interpretation:
```

異なるvendorやmodelを使ったrun同士の差を「platformの因果効果」とは呼ばない。

## 4. diagnostic observations

must-passとは分けて、次を観測してよい。

- frameworkを使わない選択が自然にできたか
- frameworkを使った場合、何が新しく見えたか
- 反証である常連5/7の材料が、設計条件へ戻されたか
- 3枚カードを「候補」として具体化しつつ、未検証性を保てたか
- 委員会提出物として読みやすい形へ戻れたか
- 方法説明が成果物より前面に出すぎていないか
- limited profileで過剰な免責・作業放棄が起きていないか

これらは総合スコアにしない。

## 5. evaluator provenance

```text
evaluation_date:
evaluator_type: human / ai / mixed
evaluator_identity_or_visible_model:
evaluator_context:
which_execution_outputs_seen:
engineering_run_001_seen_before_evaluation: yes / no
repository_protocol_seen_before_evaluation: yes / no
notes:
```

AI評価はAI由来のinterpretationであり、人間による独立reviewや客観測定へ置き換えない。

## 6. change decision

評価後の判断は、次から選ぶ。

- `no_change`: surface差は意味境界を壊していない
- `docs_or_packaging`: 誤読やwrapper driftであり、方法論規則追加は不要
- `regression_fixture`: 再現したfailureを静的・合成fixtureへ落とせる
- `runtime_candidate`: 既存規則では説明できない反復failureがあり、runtime変更候補として別途検討する
- `more_evidence`: confounderまたはrun不足のため追加比較が必要

全surfaceがPASSでも、方法論全体の有効性、release readiness、production promotionを証明したことにはしない。
