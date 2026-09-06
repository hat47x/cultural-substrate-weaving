# CSW thin migration audit

Date: 2026-09-06
Status: research migration audit

## Purpose

現行monolithic CSWの `methods/integration.md` と `core/iteration.md` を薄くするとき、単なる削除によって有用な方法知・来歴・安全境界が失われないかを責務単位で監査する。

paired regression:

- `research/skill-prototypes/evals/THREE-LAYER-PAIRED-RUN-2026-09-06.md`

replacement candidates:

- `research/skill-prototypes/migration/thin-csw-integration-candidate.md`
- `research/skill-prototypes/migration/thin-csw-iteration-candidate.md`

## 1. `methods/integration.md` ownership map

| Current responsibility / content | Future owner | Migration state | Notes |
|---|---|---|---|
| KJ法の系譜・主要書誌・商標注意 | Layer 1 evidence / release docs | carried over | `affinity-synthesis/evidence/KJ-LINEAGE-CARRYOVER.md`へ移管inventoryを追加 |
| KJ法／親和図法／質的統合法の位置づけ | Layer 1 METHOD / evidence | already represented | `references/METHOD.md` + `evidence/dossier.md` |
| 材料を分類名へ先に押し込めない | Layer 1 | already represented | material-led structure / cluster before naming |
| 意味の生命を保ったカード境界 | Layer 1 | already represented | meaning-bearing unit |
| epistemic seam | Layer 1 | already represented | I3 |
| 理由のまだ分からない注意・違和感を残す | Layer 1 | represented | singleton / residual / unresolved |
| 対立・両義性を早く均さない | Layer 1 | represented | conflict preservation |
| 弱化・ぼかし・行為者脱落・確度変更の監査 | Layer 1 | represented | source-return failure modes |
| カード化・表札化・上位統合の共通核 | Layer 1 | represented | same integration kernel across granularity |
| 核を抜く／伏せて立てる／戻す | Layer 1 realization / evidence | represented | SKILL + dossier; Methodは抽象核を保持 |
| provenance / discovery route / derivation | Layer 1 | represented | provenance audit / lineage |
| derived / reposted materialの二重計上防止 | Layer 1 | represented | no false independent repetition |
| 束ね／表札 | Layer 1 | represented | grouping / label |
| 配置／関係predicate | Layer 1 | represented | relational structure |
| A型的図解とB型叙述の往復 | Layer 1 | represented | diagram ↔ narrative check |
| membership / relation / resonance / layoutの区別 | Layer 1 | represented | I13 + Representation Grammar |
| inherited / emergent / residual監査 | Layer 1 | represented | I7 |
| 外部文化体系由来候補を観察事実と同じ地位へ置かない | **CSW connection + Layer 1 input status** | must remain in CSW | thin integration candidateで保持 |
| cultural-framework interpretationを対象へ戻す | **CSW** | must remain in CSW | thin integration candidateで保持 |
| compatible KJ/affinity realizationがない場合のfallback | **CSW connection** | new explicit boundary | false claim of executionを禁止 |

### Integration conclusion

現行 `methods/integration.md` の方法本体はLayer 1へ移管可能である。

CSWに残す必要があるのは、KJ法の内部手順ではなく、**文化体系由来材料をどの認識状態で渡し、統合後にどの帰属で受け取るか**という接続である。

## 2. `core/iteration.md` ownership map

| Current responsibility / content | Future owner | Migration state | Notes |
|---|---|---|---|
| 基本単位をroundとして扱う | Layer 2 | represented | METHOD Purpose / Round Kernel |
| material delta | Layer 2 | represented | I1 |
| 新材料と関係する古い残差・artifactだけを戻す | Layer 2 | represented | I2 |
| 新材料だけを理由に既存島を全再構築しない | Layer 2 | represented | local reopen |
| 既存構造を正解として固定しない | Layer 2 | represented | I3 |
| question shift | Layer 2 | represented | I6 |
| structural delta | Layer 2 | represented | I4 |
| append-only history | Layer 2 | represented | I9 |
| residualを再開anchorとして残す | Layer 2 | represented | I5 |
| continue / stop / handoff | Layer 2 | represented | I7/I8 |
| stable semantic handles | Layer 2 | represented | I13 |
| semantic delta vs representation delta | Layer 2 | represented | I14 |
| synthesis realization binding | Layer 2 | represented | I10 |
| 文化体系から得たものの認識状態を保持 | **CSW + Layer 2 external-output boundary** | shared boundary | Layer 2 I11 + thin iteration candidate |
| framework contact change | **CSW handoff -> Layer 2 delta** | must remain at connection | thin iteration candidateで保持 |
| framework probeがno-useful-incrementでも正常終了 | **CSW** | must remain in CSW | thin iteration candidateで保持 |
| 一定数の文化体系／full depthを完了条件にしない | **CSW** | must remain in CSW | thin iteration candidateで保持 |
| KJと文化体系を混ぜないという帰属原則 | **CSW principles** | remains canonical | `core/principles-and-constraints.md` |

### Iteration conclusion

現行 `core/iteration.md` のmulti-round一般論はLayer 2へ移管可能である。

CSWに残す必要があるのは、**framework contactによって何が新しいdeltaとして生じたかを、由来付きでLayer 2へ渡すこと**である。

## 3. `core/principles-and-constraints.md` retention audit

このファイルはthin migration後もCSW canonicalに残す。

特に移管しない核:

- 決定権の所在
- 二重の忠実性
- 帰属の原則
- `target_supported / framework_generated / cross_field_emergent / unresolved`
- 対象固有性
- 委ねられた範囲
- 保存と現在の注意の分離
- 意味固定の遅延
- 可能性と採用の分離
- 認知・価値・事実の分離
- 新しい価値／抑制規則に高い正当化閾値を置くこと

これらはKJ／Affinity Synthesis一般の責務ではなく、文化体系を認知場として利用するCSWの境界を定めている。

## 4. Gaps found by migration audit

### G1. KJ legacy references could disappear from the repository surface

現行 `integration.md` を短い接続文へ置換すると、KJ法の主要書誌・商標注意がCSW側から消える。

対応:

- `affinity-synthesis/evidence/KJ-LINEAGE-CARRYOVER.md` を追加した。
- public promotion前に一次／公式情報で再確認する。

Status: **covered for migration; external verification remains a promotion gate.**

### G2. Thin connection can become a hidden hard dependency

CSW本文を単に「affinity-synthesisを使う」と書くと、独立SkillがないplatformでCSW自体が動けなくなる。

対応:

- compatible realizationがない場合のfallbackをthin candidateへ明記した。
- 実行していないKJ／親和統合／multi-round orchestrationを実行済みと称さない。

Status: **covered.**

### G3. Metadata can overwhelm creative attention

分離後、`origin / verification / stable ID / realization` を前景化しすぎると、創作の場面・身体・温度より管理情報が目立つ危険がある。

対応:

- metadataは保存・監査層に厚く保持する。
- grouping geometryや現在の注意の第一軸にしない。
- creative paired runでframework語彙「器」が原カードを上書きしないことを確認した。

Status: **covered as design principle; continue living-task observation.**

### G4. Layer boundaries can become procedural dogma

責務分離は内部所有権を明確にするためのものであり、ユーザー作業を必ず三段階のUIへ分断するためではない。

対応:

- composite realizationでは三Skillを連続実行してよい。
- 成果物上で意味・来歴・変換責任へ戻れればよい。
- Layerを跨ぐ自然な往復そのものを禁止しない。

Status: **covered in migration guidance; should be tested in composite runtime later.**

## 5. Replacement size / responsibility effect

thin候補では、CSWから詳細なカード化・束ね・表札・図解・B型叙述・round ledgerの説明を外す。

削減の目的はtoken削減そのものではない。

期待する効果:

1. CSWがcultural-framework explorationへ集中する。
2. one-round synthesisを単独で改善・置換できる。
3. multi-round orchestrationを単独で改善・置換できる。
4. KJ系統の技法改善が、文化体系側のruntime文面を肥大化させない。
5. failureをLayer単位でevalできる。

## 6. Pre-replacement gates

research branch上で現行canonical sourceを置換する前に必要なgate:

- [x] Layer 1 Method Definition exists.
- [x] Layer 1 representation / hierarchy / lineage regression exists.
- [x] 114-card synthetic scale regression exists.
- [x] Layer 2 Method Definition exists.
- [x] Layer 2 delta-reopen eval cases exist.
- [x] CSW handoff cases exist.
- [x] analysis real-material paired comparison exists.
- [x] creative real-material paired comparison exists.
- [x] three-layer paired comparison exists.
- [x] thin integration candidate exists.
- [x] thin iteration candidate exists.
- [x] KJ legacy source carry-over inventory exists.
- [ ] current source vs thin candidate semantic-retention machine/manual checklist is recorded.
- [ ] ja-JP runtime routing references are checked against the new thin files.
- [ ] en-US parity strategy is decided before public promotion.
- [ ] build/generated artifact impact is tested in a local checkout or CI-capable environment.

## 7. Decision

**Do not delete the current canonical files yet.**

The next safe step is a source-to-candidate semantic-retention checklist and router/build impact audit. If those pass, replace the Japanese canonical `methods/integration.md` and `core/iteration.md` on the research branch, then run the repository build/validation path before any merge or release promotion.
