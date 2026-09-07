# Research Skill Suite — ja-JP OpenAI Metadata Routing Review 2026-09-07

Status: same-authoring-session routing review; not host-behavior evidence

## Purpose

ja-JP companion OpenAI metadata prototypeが、三Skillの責務分離を入口文面で弱めていないかを確認する。

対象:

- `cultural-substrate-weaving`
- `affinity-synthesis`
- `iterative-inquiry-synthesis`

見るものはSkill本体の性能ではなく、OpenAI metadataの、

- display name
- short description
- default prompt

が、典型的な依頼をどのSkillへ案内するかである。

このreviewはsame-authoring-sessionで行うため、独立評価ではない。

## Baseline roles

### Cultural Substrate Weaving

主役割:

> 文化的体系を通常分析とは異なる認知資源として使い、問い・対応候補・構造候補を供給し、対象側で検証する。

OpenAI default prompt:

> 領域固有手法の基準線を置き、文化的体系とKJ法による増分だけを対象側で検証してください。

現行canonical CSWはまだKJ統合も内包しているため、この文面は現行runtimeの説明として読む。将来split後のproduction wordingは別途再設計が必要である。

### Affinity Synthesis

主役割:

> 異種の材料を、先にtaxonomyを置かず、一回の材料主導統合として外部化する。

prototype default prompt:

> 元材料の来歴と認識状態を保ち、先に分類体系を置かず、一回の親和統合として意味単位・束・関係・残差を立ち上げてください。

### Iterative Inquiry Synthesis

主役割:

> 前roundを上書きせず、新材料が触れた箇所を再開し、one-round synthesisを互換realizationへ委ねながら複数roundをつなぐ。

prototype default prompt:

> 前ラウンドを上書きせず、新材料が触れた箇所だけを再開し、必要な一回統合は利用可能な互換realizationへ委ね、残差・次の問い・停止理由を追跡してください。

## Case 1 — 一回だけ異種資料を統合する

### Input intent

> 20本のインタビュー、会議メモ、観察記録を一度まとめたい。先にカテゴリ表は作らず、材料から意味のまとまりと矛盾を立ち上げたい。

### Expected primary entry

**Affinity Synthesis**

理由:

- 一回の統合で足りる。
- 問いのmulti-round orchestrationは要求されていない。
- 文化体系による探索も要求されていない。
- 「先に分類せず」「意味単位・束・関係・残差」というmetadataが依頼意図と直接対応する。

### Wrong primary routes

CSW:
- 文化体系による構造供給という追加能力を不要に持ち込む。

Iterative:
- 前roundが存在せず、差分reopenも不要である。

### Review result

**PASS — Affinity metadataが最も狭く一致する。**

## Case 2 — 既存統合へ新資料を追加する

### Input intent

> 先週まとめた構造へ、新しいヒアリング5件が届いた。全体をゼロから作り直さず、影響した箇所と残った問いだけを更新したい。

### Expected primary entry

**Iterative Inquiry Synthesis**

理由:

- 前roundが明示される。
- delta/touched region/reopenが中心である。
- 必要なone-round integrationはLayer 1へ委ねる必要がある。
- metadataの「新材料が触れた箇所だけを再開」「前ラウンドを上書きせず」が直接対応する。

### Companion use

局所的な再統合が必要なら **Affinity Synthesis** をone-round realizationとして併用する。

### Wrong primary routes

Affinity単独:
- 一回の統合結果は作れるが、round history / reopen / stop reasonの所有者にならない。

CSW:
- 文化体系探索はこの依頼の必要条件ではない。

### Review result

**PASS — Iterative metadataがLayer 2入口を明示し、Affinityへの委任も保つ。**

## Case 3 — 文化体系から通常分析にない問いを得る

### Input intent

> 現状の資料だけでは見落としている関係がありそうだ。易・タロット等を真実判定に使わず、別の構造候補や問いを供給する認知資源として当て、対象資料へ戻して確かめたい。

### Expected primary entry

**Cultural Substrate Weaving**

理由:

- 要求の中心が文化体系による探索である。
- framework-generated candidateを対象へ戻す境界が必要である。
- Affinity/Iterative metadataには文化体系を入れていないため、companionが誤って主入口へ出にくい。

### Companion use

探索後に多数の対象材料を一回統合する必要があればAffinityへ渡せる。

複数roundで新資料を追加するならIterativeへhandoffできる。

### Wrong primary routes

Affinity:
- 材料統合はできるが、文化体系による探索を所有しない。

Iterative:
- round orchestrationはできるが、文化体系から問いを供給しない。

### Review result

**PASS — companion metadataがCSWの探索能力を横取りしていない。**

## Case 4 — framework由来の問いを次roundへつなぐ

### Input intent

> CSWで「複数周期の交差を見る」という問いが出た。その問い自体は対象事実ではない。追加資料を集め、対象側で支持されるものとされないものを分けながら、既存の統合構造へ差分として返したい。

### Expected route

単一Skillを主役に固定しない。

推奨される責務の流れ:

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

### Why no single metadata entry should claim the whole task

CSWだけに寄せると:
- multi-round historyとLayer 1分離を旧単一Skillへ戻しやすい。

Affinityだけに寄せると:
- framework-generated originを単なるsource cardへ平板化しやすい。

Iterativeだけに寄せると:
- framework explorationやone-round groupingをLayer 2が自前実装しやすい。

### Review result

**PASS WITH HANDOFF REQUIREMENT — metadata分離は複合ケースで単一万能Skillを作らない。**

## Cross-case observations

### 1. Short descriptions are sufficiently asymmetric

Affinity:

> 異種の材料を先に分類せず、一回の統合…

Iterative:

> 新材料が触れた箇所だけを再開し…ラウンド間で追跡…

同じ「統合」という語を含むが、one-round と reopened multi-round の差が見える。

### 2. Default prompts do not copy CSW's cultural-framework language

companion promptには「文化体系」「KJ法による増分」「対象側で検証」を一式コピーしていない。

このため、Skill分離後も旧CSWの総合責務を各companionへ複製する形にはなっていない。

### 3. Iterative explicitly names delegation

> 必要な一回統合は利用可能な互換realizationへ委ね

という文言があることで、Layer 2が「統合」という語を理由にLayer 1 algorithmまで所有する読みを抑えている。

### 4. Affinity does not promise question-cycle completion

Affinity promptは残差を外部化するところまでであり、残差を必ず次の問いへ変換してroundを回すとは書いていない。

これはLayer 2境界を保つ。

## Residual risk

### Implicit invocation is not yet observed

interactive profileではAffinity/Iterativeとも `allow_implicit_invocation: true` である。

metadata文面上の役割は分離できていても、実hostがどのsignalを重く見るかは未観測である。

特にCase 1とCase 2の境界で、

- 「資料を統合したい」だけでIterativeが過剰起動しないか。
- 「新資料が来た」というだけでAffinityではなくIterativeへ適切に寄るか。

はhost executionが必要である。

### Current CSW metadata still describes the pre-split canonical Skill

CSW production runtimeはまだKJ統合を内包している。

したがって現在のCSW metadataとcompanion prototypeを並べた状態は、**将来production三Skill routingの完成形ではない**。

canonical migration後にはCSW short description/default promptから旧KJ統合責務をどこまで外すかを再監査する必要がある。

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

ja-JP companion OpenAI metadataはresearch `prototype` のまま維持する。

次に必要なのはhost executionまたは独立評価であり、同じauthoring sessionで文言をさらに増やすことではない。

一方、Claude/Codexについてはまだbundle-level metadataが `existing-baseline / review-required` なので、次の静的研究対象は三Skill bundle向けdescription/displayの境界である。
