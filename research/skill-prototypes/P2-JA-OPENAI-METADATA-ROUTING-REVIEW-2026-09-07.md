# Research Skill Suite — ja-JP OpenAI Metadata Routing Review 2026-09-07

Status: same-authoring-session routing review; not host-behavior evidence

## Purpose

ja-JP companion OpenAI metadata prototypeが、三Skillの責務分離を入口文面で弱めていないかを確認する。

対象:

- `cultural-substrate-weaving`
- `affinity-synthesis`
- `iterative-inquiry-synthesis`

見るものはSkill本体の性能ではなく、OpenAI metadataのdisplay name / short description / default promptが典型的な依頼をどのSkillへ案内するかである。

## Baseline roles

### Cultural Substrate Weaving

文化的体系を通常分析とは異なる認知資源として使い、問い・対応候補・構造候補を供給し、対象側で検証する。

### Affinity Synthesis

異種の材料を、先にtaxonomyを置かず、一回のmaterial-led synthesisとして外部化する。

### Iterative Inquiry Synthesis

前roundを上書きせず、新材料が触れた箇所を再開し、one-round synthesisを互換realizationへ委ねながら複数roundをつなぐ。

## Case 1 — 一回だけ異種資料を統合する

Input intent:

> 20本のインタビュー、会議メモ、観察記録を一度まとめたい。先にカテゴリ表は作らず、材料から意味のまとまりと矛盾を立ち上げたい。

Expected primary entry: **Affinity Synthesis**

理由:

- 一回の統合で足りる。
- multi-round orchestrationは不要。
- 文化体系探索も不要。
- 「先に分類せず」「意味単位・束・関係・残差」というmetadataが直接対応する。

Result: **PASS**

## Case 2 — 既存統合へ新資料を追加する

Input intent:

> 先週まとめた構造へ、新しいヒアリング5件が届いた。全体をゼロから作り直さず、影響した箇所と残った問いだけを更新したい。

Expected primary entry: **Iterative Inquiry Synthesis**

理由:

- 前roundが明示される。
- delta / touched region / reopenが中心である。
- 必要な局所統合はAffinity等のLayer 1 realizationへ委ねられる。

Result: **PASS**

## Case 3 — 文化体系から通常分析にない問いを得る

Input intent:

> 現状の資料だけでは見落としている関係がありそうだ。易・タロット等を真実判定に使わず、別の構造候補や問いを供給する認知資源として当て、対象資料へ戻して確かめたい。

Expected primary entry: **Cultural Substrate Weaving**

理由:

- 要求の中心が文化体系による探索である。
- framework-generated candidateを対象へ戻す境界が必要である。
- companion metadataには文化体系を入れていない。

Result: **PASS**

## Case 4 — framework由来の問いを次roundへつなぐ

Input intent:

> CSWで出た問い自体は対象事実ではない。追加資料を集め、対象側で支持されるものとされないものを分けながら、既存の統合構造へ差分として返したい。

単一Skillを万能入口にしない。

```text
CSW
  framework-generated question / candidate
        ↓ attribution retained
Iterative
  round / delta / reopen orchestration
        ↓ one-round synthesis when needed
Affinity
  material-led local synthesis
        ↓
Iterative
  residual / next inquiry / stop-handoff record
```

Result: **PASS WITH HANDOFF REQUIREMENT**

## Cross-case observations

### Short descriptions are asymmetric enough

Affinityは「一回の統合」、Iterativeは「新材料が触れた箇所だけを再開」「ラウンド間で追跡」を前面に出す。同じ「統合」という語を使っても役割境界は見える。

### Companion prompts do not copy CSW cultural-framework wording

Affinity / Iterativeへ「文化体系」「KJ法による増分」「対象側で検証」を一式コピーしていない。旧CSWの総合責務を各Skillへ再複製する形を避けている。

### Iterative explicitly delegates one-round synthesis

「必要な一回統合は利用可能な互換realizationへ委ね」と明示することで、Layer 2がLayer 1 algorithmまで所有する読みを抑える。

### Affinity does not promise inquiry-cycle completion

Affinityは残差を外部化するところまでであり、残差を必ず次の問いへ変換してroundを回すとは書かない。

## Residual risk

interactive profileではAffinity / Iterativeともimplicit invocationを許可する。metadata文面の役割分離が、実hostのrouting precision / recallへそのまま反映されるとは限らない。

また現行production CSW metadataはpre-split canonical Skillを説明している。canonical migration後にはCSW自身のshort description/default prompt再監査が必要である。

## Evidence classification

このreviewで言えること:

- metadata文章の責務境界は4ケースで整合する。
- obviousなcross-layer wording contaminationは見つからない。
- 複合ケースではhandoffを要求する設計になっている。

このreviewで言えないこと:

- OpenAI hostが実際に正しいSkillを自動選択する。
- implicit invocationのprecision/recallが十分である。
- production metadataとして承認済みである。
- canonical splitが安全に実施可能である。

## Decision

**Authoring-level routing boundary: provisional pass.**

ja-JP companion OpenAI metadataはresearch `prototype` のまま維持する。次に必要なのはhost executionまたは独立評価であり、同じauthoring sessionで文言をさらに増やすことではない。

Claude/Codexについてはbundle-level metadataが `existing-baseline / review-required` なので、次の静的研究対象は三Skill bundle向けdescription/display境界である。
