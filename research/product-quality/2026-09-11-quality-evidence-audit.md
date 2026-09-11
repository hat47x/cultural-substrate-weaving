# E0 — 品質証拠カバレッジ監査

- 実施日: 2026-09-11
- audit id: `PQ-E0-20260911-01`
- 基準commit: `f4370bea759fcb83a4eeae352b325f8feaea39d5`
- 種別: repository evidence audit
- 対象: 現行`develop/v0.5.0`上で確認できる品質証拠
- 制約: repository上の契約・test・research recordを対象とした監査であり、今回新たなモデル実行は行っていない

## 1. 監査目的

プロダクト品質プログラムのE0として、現在すでに何を検証できていて、どの品質要求がまだ主に「設計上の意図」に留まっているかを確認する。

この監査では、証拠の**量**ではなく種類を区別する。

- deterministic contractが存在する
- static semantic retentionが存在する
- controlled behavioral executionが存在する
- natural-work observationが存在する

static validatorが多数あることを、実際のモデル行動が十分検証済みという意味には読み替えない。

## 2. 確認した主要資産

### 方法・評価の正本

- `src/ja-JP/ROUTER.md`
- `src/ja-JP/core/`
- `src/ja-JP/governance/evaluation.md`
- `src/ja-JP/methods/`

`governance/evaluation.md`は、単一の総合品質スコアではなく、課題に適した局所評価、framework agreementと成功の分離、misfit/resistanceの情報価値、target supportとprovenanceの区別を要求している。今回の品質モデルはこの境界を維持する。

### deterministic / repository checks

- `Makefile`
- `scripts/validate.py`
- `scripts/validate_research_*.py`
- `tests/`
- `i18n/translation-manifest.json`
- `research/skill-prototypes/`

現行repositoryは、正本・生成物・翻訳・research/production境界・promotion前提・projection等について多数の決定論的checkを持つ。特にv0.5系のMethod分離では、productionへ研究状態を漏らさないこと、current authorityを個別スクリプトへ複製しないこと、promotionを明示的gateで扱うことが継続して強化されている。

### static semantic / activation fixtures

- `evals/semantic-retention.json`
- `tests/test_semantic_retention.py`
- `evals/activation-cases.json`

`test_semantic_retention.py`は、buildされた成果物に要求phraseが保持されることを機械的に確認する。これは重要な回帰検知だが、モデルがその意味に従って振る舞うことを検証するtestではない。

`activation-cases.json`は、局所的debug、onboarding文書、設計review、self-reference、full activation等の具体例と期待される読み込み深度を持つ。発動設計の具体性はあるが、この監査で確認した範囲では、それ自体はモデル実行結果ではない。

### natural-work observations

- `.living-lab/README.md`
- `research/living-lab/observations/2026-08-30-round-001.json`
- `research/living-lab/observations/2026-09-04-round-002.json`

Living Labはschema 0.2で、natural work、measurement provenance、retrospective/prospective、`target_signal`等を区別する設計になっている。現時点で確認できた公開観測roundは2件であり、長期的傾向を確定するにはまだ小さい。これは欠点というより、観測件数をKPI化せず自然利用を待つ設計の結果でもある。

### 分離Method関連

- `docs/ja/maintainers/skill-improvement-direction.md`
- `docs/ja/maintainers/v05-cognitive-prompt-roadmap.md`
- `research/skill-prototypes/`

v0.5の中心的変更であるthin-CSW化と`affinity-synthesis` / `iterative-inquiry-synthesis`の分離について、ownership、production projection、translation、promotion等の構造契約は厚くなっている。一方、今回確認した主要資産からは、**CSWから両Methodへ実際に引き渡して一連の成果物を作り、来歴・残差・決定権が末端まで保持されたことを確認するend-to-end behavioral evidence**はまだ主要な品質証拠として確立していない。

## 3. 品質要求別の初回評価

評価語は次の意味で使う。

- **strong-static**: deterministic/static evidenceが比較的厚い
- **partial**: 設計・fixture・一部観測はあるが、主要failure modeのbehavioral evidenceが不足
- **sparse**: 要求としては重要だが、今回確認した資産では直接証拠が少ない

これは製品の優劣スコアではない。

| Requirement | 初回評価 | 現在の主な証拠 | 主な空白 |
|---|---|---|---|
| PQ-01 証拠境界 | partial | 正本、evaluation、semantic retention、research gate | framework-only候補を含むadversarial behavioral probe |
| PQ-02 決定権境界 | partial | 正本、authority refactor、validator群 | 過剰委任に見えるprompt下での実行証拠 |
| PQ-03 固定depth/round回避 | partial | activation設計、iteration設計、activation cases | controlled executionでの過剰適用比較 |
| PQ-04 発動/非発動を勝敗化しない | partial | Living Lab schema、activation設計 | paired behavioral observation |
| PQ-05 Method handoff完全性 | partial | split ownership / promotion / projection contracts | **end-to-end handoff behavioral evidence** |
| PQ-06 局所再開 | sparse | iteration設計、iterative inquiry prototype | delayed materialを使った再開実験 |
| PQ-07 領域品質の非代替 | partial | evaluation/authority境界 | domain fixtureを用いた実行証拠 |
| PQ-08 platform意味同等性 | partial | adapters、生成・package checks | cross-platform behavioral parity |
| PQ-09 多言語同期 | strong-static | manifest、translation validator、review/promotion gate | 高リスク語義の継続的独立reviewは運用課題 |
| PQ-10 観測・操作負荷 | sparse | Living Labの低介入方針 | overheadの局所測定 |
| PQ-11 観測来歴 | strong-static / early-natural | Living Lab schema、research status/provenance | behavioral experiment用の統一実施記録はこれから |
| PQ-12 回帰可能性 | strong-static for known contracts / partial-behavior | tests、validators、semantic retention | behavioral failureを最小fixture化するloop |

## 4. 監査で見えた構造

### 4.1 repository correctnessは強いが、product behaviorとは別物

現行CSWは「何を正本とするか」「何をproductionへ出してよいか」「翻訳・生成物がどう同期するか」といったrepository correctnessをかなり強く検査している。これは重要な基盤である。

一方、利用者が実際に得る品質は、モデルがその契約を読んでどう振る舞うかにも依存する。たとえば、文面に「framework由来候補をtarget factへ昇格させない」と残っていることと、魅力的な仮説を与えられたモデルが本当に境界を守れることは別の命題である。

したがって次の前進は、static ruleをさらに大量追加することより、重要な境界に絞ったcontrolled behavioral evidenceを得ることにある。

### 4.2 v0.5の最大リスクはMethod分離そのもののhandoff

thin-CSW化には、CSWがKJ処理や反復更新まで抱え込まないという設計上の利点がある。しかし分離は新しいfailure surfaceも作る。

- CSWで付いたprovenanceが次のMethodで消える
- affinity synthesisが孤立・矛盾を「まとまりの悪さ」として除去する
- iterative inquiryへ採用済み成果だけが渡り、残差や戻り先が失われる
- downstream Methodがauthor-pendingな候補を確定扱いする
- 後続roundが局所更新ではなく全体再構築へ戻る

これらはrepository projectionの正しさだけでは検出しにくい。そのためE3を第一優先とする判断は妥当である。

### 4.3 Living Labをcontrolled experimentへ変質させない

Living Labは自然作業の縦断観測として価値がある。E1〜E5をLiving Labへ無理に載せると、観測のために仕事を作ることになり、既存設計を壊す。

controlled probeは`research/product-quality/`へ分離し、Living Labは自然に生じた長期的な採用・修正・撤回・再利用を見る。この二つは相互補完するが代替しない。

## 5. 次に実施すべき実験

### Priority 1 — E3 split-method handoff integrity

理由:

- v0.5のアーキテクチャ変更に直接対応する。
- PQ-01/PQ-02/PQ-05/PQ-06を一度に観測できる。
- failureが出た場合、Method Definition、handoff packet、CSW routerのどこを直すべきか切り分けやすい。
- production promotion前に確認する価値が高い。

固定protocolを`experiment-001-handoff-integrity.md`へ作成する。

### Priority 2 — E1 authority / provenance adversarial probe

E3でhandoff形式そのものが安定した後、その形式へ圧力をかける。特に「良さそうなframework-only仮説」「公開まで一任したように読める曖昧な依頼」「author-pending候補」を混ぜる。

### Priority 3 — E4 delayed reactivation

E3の最終成果物へ後日材料を追加し、局所的に再開できるかを見る。E3と完全に別のfixtureを増やすより、同一packetを時間方向へ延長した方が比較しやすい。

## 6. 今回の実施結果

E0として、品質要求と既存repository evidenceを対応づけた。

**確認できた前進点**

- deterministicなrepository/release/research境界は品質基盤として比較的厚い。
- semantic-retentionとactivation-caseという静的fixtureがすでに存在し、behavioral experimentの入力設計へ再利用できる。
- Living Labは自然利用・provenanceの観測面として分離できている。

**主要な未測定領域**

- split Method間のend-to-end handoff behavior
- authority/provenanceへのadversarial pressure
- delayed local reactivation
- cross-platform behavioral parity
- 利用者負荷の局所測定

この監査結果を受け、最初のbehavioral experimentはE3とする。今回のcommitではprotocolまで固定するが、**新規モデルrunを行ったとは扱わない**。最初のrunはprotocol自身の曖昧さも検出するengineering trialとして実施する。

## 7. 判定

現段階で新しい大規模eval frameworkを導入する必要はない。

先にE3を一度実行し、記録上不足するfieldと実際に発生するfailure modeを確認する。その結果、複数runで機械可読化する価値がある項目だけを`evals/`やvalidatorへ昇格させる。

この順序により、「品質を測る仕組み」を作る作業が「品質を高める作業」そのものを上回ることを避ける。
