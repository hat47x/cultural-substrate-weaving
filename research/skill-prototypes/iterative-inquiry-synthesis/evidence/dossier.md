# Iterative Inquiry Synthesis — External Evidence Dossier

Status: research evidence / engineering-pattern comparison

## Purpose

このdossierは、`iterative-inquiry-synthesis` のMethod Definitionが、既存のautonomous research / iterative search系Agent Skillから何を借り、何を借りず、どこを生成AI向けに組み替えたかを明示する。

ここで比較する対象は主に次である。

1. `wjgoarxiv/autoresearch-skill`
2. `hoanganhduc/coding-system-rebuild` の `autonomous-research-loop`
3. `wielandbrendel/ralph_search`

この資料は、これらのSkillがLayer 2より優れている／劣っているという総合評価ではない。各Skillは目的が異なる。

- autoresearch: measurable metricとsearch spaceを持つ自律実験ループ
- autonomous-research-loop: bounded autonomy、ledger、evidence gate、recoveryを重視するresearch orchestration
- ralph-search: candidate backlog / dossierを中心にしたsystematic search automation
- iterative-inquiry-synthesis: 意味構造の差分再開、問い・残差・semantic identity・stop/restart履歴を扱う汎用multi-round inquiry orchestration

したがって、既存Skillの表面的なworkflowをコピーするのではなく、Layer 2の責務へ移植可能なmechanismだけを Adopt / Adapt / Reject / Defer で扱う。

## Source snapshots used in this review

### S1 — `wjgoarxiv/autoresearch-skill`

Reviewed source:

- repository: `wjgoarxiv/autoresearch-skill`
- file: `SKILL.md`
- observed main branch blob SHA during review: `8e2215f812269deb80a2dfc538faaf898766a165`

Relevant mechanisms observed:

- explicit goal / metric / constraints / search space / history
- Understand → Hypothesize → Experiment → Evaluate → Log & Iterate
- append iteration history to external files
- target metric / max iterations as loop stop conditions
- one specific testable change per experiment
- autonomous directive to continue without asking until a terminal condition
- stuck / pivot detection based on consecutive non-improving iterations

### S2 — `hoanganhduc/coding-system-rebuild` autonomous research loop

Reviewed source:

- repository: `hoanganhduc/coding-system-rebuild`
- file: `agents/opencode/skills/autonomous-research-loop/SKILL.md`
- observed search snapshot commit during review: `3fb032a54624be7d3608c9765eb093ba4352ba56`

Relevant mechanisms observed:

- concrete goal
- success criteria
- hard budgets
- append-only `iterations.jsonl`
- `recovery.md` with resume point / blockers / next safe action / evidence gaps
- evidence gates
- explicit iteration decision states
- bounded autonomous modes
- strong machine-checkable-success / budget-oriented stop policy in the reviewed realization

### S3 — `wielandbrendel/ralph_search`

Reviewed source:

- repository: `wielandbrendel/ralph_search`
- file: `SKILL.md`
- observed search snapshot commit during review: `5dca744329646c514cba235deeb2b28ab6d892fd`

Relevant mechanisms observed:

- persisted search folder as cross-session state
- backlog-driven candidate selection
- per-item dossiers
- notes / learnings accumulation
- stall detection
- early user review before spending many more iterations
- search-specific scoring and coverage checks

## Comparative decision table

| External mechanism | Decision | Layer 2 treatment | Reason |
|---|---|---|---|
| Explicit current goal / objective | **Adopt** | `current inquiry / purpose` | Roundの焦点が曖昧だとdeltaと無関係な全体再生成へ流れやすい。 |
| Append-only iteration ledger | **Adopt** | append-only round history | 過去の問いや解釈を現在形で上書きしないために必要。 |
| Recovery / resume point | **Adopt** | round handoff / return point / reopen condition | context compactionや中断後に全面再読せず再開できる。 |
| Evidence/material refs per iteration | **Adopt** | input refs / output refs / provenance / realization binding | 何が変化を生んだかを追跡するために必要。 |
| Explicit stop conditions | **Adopt** | continuation / stop / handoff boundary | round数を進捗そのものにしない。 |
| Hard operational budgets | **Adapt** | host/runtime constraintとして利用可能 | 時間・token・cost制約は有用だが、Method Definitionの意味論的不変条件ではない。 |
| Scalar metric | **Reject as universal invariant** | metric-bearing taskでは任意利用可能 | 創作・設計・探索・意味統合は単一scalarへ還元できない。 |
| Machine-checkable success as normal-stop requirement | **Reject as universal invariant** | 利用できるtaskでは補助的に利用 | unresolvedを残した正常停止を不可能にしてしまう。 |
| One-change-per-experiment | **Reject as universal invariant** | 実験realization固有の制約としては可 | semantic inquiryでは一つのnew sourceが複数relation/groupへ同時に触れることがある。 |
| Max iterationsを使い切るまで継続 | **Reject** | continuationには毎round外部理由を要求 | budgetは上限であって「使い切るべき深さ」ではない。 |
| Never ask / never pause autonomy directive | **Reject as method default** | host/user intentが明示した場合だけautonomous realizationで採用可能 | Layer 2はinquiry methodであり、autonomy policyそのものではない。 |
| Stall detection | **Adapt** | fixed N回ではなく「meaningful semantic deltaが生じない」ことを見る | wordingやrenderer差を改善扱いしないためsemantic delta基準へ変換する。 |
| Search backlog | **Reject as universal invariant** | web/search routeの局所realizationで利用可能 | interview、設計、創作、文化体系探索等ではbacklogが自然な中心表現とは限らない。 |
| Per-item dossiers | **Adapt** | domain/search-specific evidence artifactとして利用可能 | 汎用round状態はitem-centricとは限らない。 |
| Early user review | **Adapt** | interaction policy / host realizationのquality gate | user reviewは重要だが、非対話hostや既知の目的ではMethod Definition必須ではない。 |
| Multi-agent/panel review | **Defer** | independent review realizationとして追加可能 | panel構成はLayer 2の意味論的不変条件ではなくhost能力に依存する。 |
| Automatic rollback of unsuccessful experiment | **Reject as universal invariant** | code/optimization realizationでは有効 | 意味探索では「失敗した解釈」自体がresidual/historyとして価値を持つ。破壊的rollbackは履歴を失わせる。 |

## What Layer 2 specifically learns from each source

### From autoresearch: loop visibility, not optimization semantics

最も有用なのは、各iterationにgoal、history、evaluation、logを持たせ、外部状態を介して次へ進む構造である。

一方、Layer 2は次を取り込まない。

- `metric` が常に中心であるという前提
- experimentが常にone-changeであるという前提
- non-improving iterationを改善探索のpivot回数で定義すること
- target / max iterations以外では基本的に止まらないautonomy directive

Layer 2で「改善」に相当するものは単純なscore増加ではない。

例えば次はすべて正当なround resultである。

- 既存structureが新材料でも維持された。
- relationが弱まった。
- 以前一つだったgroupがsplitした。
- questionが変化した。
- unresolvedが残り、現時点では追加証拠が無いことが分かった。
- one-round synthesisが不要だった。

したがって、autoresearchのloop shapeは参考になるが、metric-driven progress semanticsは移植しない。

## From autonomous-research-loop: external control state and recovery

Layer 2に最も強く取り込みたいmechanismは次である。

- append-only iteration record
- recovery point
- remaining gaps
- explicit decision state
- evidence/source refs
- concrete next objective

これは現在のMethod Definitionの次と直接対応する。

- I4 Structural delta is explicit
- I7 Continuation requires a reason
- I9 Append-only history, current-state projection
- I10 Method realization is explicit
- I11 External exploration outputs keep their epistemic status

ただし、reviewed realizationのstrong enforcement policyはそのまま採用しない。

特に、正常な早期stopをmachine-checkable proofへ強く限定し、plateau / evidence gapを原則continueへ戻す設計は、Layer 2のI8と目的が異なる。

Layer 2では、

> **未解決が残ること** と **もう一roundを行う理由があること** は別である。

このため、evidence gapは時にstop reasonであり、後から新材料が来たときのrestart anchorになる。

## From Ralph Search: durable research artifacts and early direction checks

Ralph Searchからは、検索対象に適した次の設計が有用である。

- backlog
- dossiers
- search notes
- logs
- stall detection
- early review

ただしこれらは`iterative-inquiry-synthesis`のcore stateに昇格させない。

理由は、Layer 2の対象がcandidate searchに限られないためである。

例えば創作では「候補一件ごとのdossier」は不自然であり、KJ系意味統合ではbacklogより `residual / question / touched semantic handle` の方が再開点として自然である。

したがってRalph Searchは、Layer 2の上に載る**search-route realizationのよい参照例**と位置づける。

## Central synthesis: iteration state must not become semantic authority

三つの外部Skillはいずれも、iterationを外部状態として記録する点で参考になる。

Layer 2ではここへ次の補正を加える。

### 1. Carried state is not automatically active state

前roundから持ち越されたgroup、relation、residual、question、candidateは、存在するという理由だけで次roundのreopen対象にならない。

新しいdeltaが実際に触れたsubsetだけをreopenする。

これは大量の履歴を容易に再処理できる生成AIで特に重要である。すべてのcarried stateを毎回再読・再生成すると、過去構造が少しずつ漂流する。

### 2. Residual is not a continuation command

unresolved、gap、singletonが存在することは、その意味を保存する理由ではある。

しかし、それだけでは追加roundを開始する理由にならない。

区別する。

```text
preserve as reopenable anchor
    !=
reopen now
    !=
continue another round
```

### 3. More rounds do not imply more truth

このreviewから、反復回数そのものがtruth、confidence、independent supportを増やすという根拠は得ていない。

むしろ生成AIでは、同じ派生材料を何度も再処理することで、

- 反復表現を独立supportと誤認する
- 自分で生成したhypothesisを後roundでsource factのように読む
- wording polishをsemantic convergenceと誤認する

危険がある。

Layer 2はround countをconfidence scoreに変換しない。

### 4. Realization changes are confounders

同じ材料でもmodel / Skill / prompt / rendererが変わればoutput差が生じ得る。

そのため、iteration historyにはmaterial deltaだけでなく、使ったone-round synthesis realizationを残す。

外部Skillのfile-based persistenceを、Layer 2ではsemantic provenanceまで含む形へ広げる。

## Relationship to the current Method Definition

この比較は、現在のMethod Definitionの方向を概ね支持するが、有効性を証明しない。

特に次の不変条件は外部Skill比較から合理性を補強される。

- I1 Round is a delta, not a restart
- I4 Structural delta is explicit
- I7 Continuation requires a reason
- I8 Stopping with unresolved material is valid
- I9 Append-only history, current-state projection
- I10 Method realization is explicit
- I11 External exploration outputs keep their epistemic status
- I13 Stable semantic handles survive when identity survives
- I14 Semantic delta and representation delta are not the same
- I15 Missing synthesis realization stays explicit

また、handoff capsule設計から次のsemantic invariantをMethod Definitionへ追加する価値がある。

> **Carry-forward state is not reopen or continuation authority.**
>
> Prior state may preserve semantic identity, provenance, residuals, and possible checks. A later round still decides what to reopen from the current delta, and a residual or candidate alone does not require continuation.

この原則は特定のJSON field名やfilesystem layoutを要求しないため、Method Definitionレベルへ置ける。

## Evidence limits

このdossierの根拠は、公開Agent Skillの設計・実装文書を比較した**engineering/practitioner evidence**である。

次を証明しない。

- Layer 2を使うと分析のtruthが上がる。
- round数を増やすほどaccuracyが改善する。
- delta-based reopeningがすべてのtaskでfull rebuildより優れる。
- 既存三SkillよりLayer 2が総合的に優れている。
- 現在のAgent Skill realizationが異なるmodel/hostでも不変条件を守る。

現在のreal-task paired comparisonもsame-model sequential evaluationであり、独立・blinded・randomizedではない。

したがってpublic promotion前には、少なくとも次が残る。

- long-history local-reopen behavior
- global contradiction behavior
- missing compatible synthesis realization behavior
- realization-switch confounder handling
- independent English review
- complete-checkout repository checks

## Current decision

**Keep the Layer 2 split and continue research. Do not replace it wholesale with any of the three reviewed Skills.**

理由は、既存Skillに欠陥があるからではなく、ownershipが異なるためである。

- metric-driven autonomous experimentation → autoresearch系が強い
- bounded autonomous research control → autonomous-research-loop系が強い
- systematic candidate search → ralph-search系が強い
- semantic delta / residual / local reopening / question history across heterogeneous inquiry → Layer 2が保持すべき固有責務

外部Skillの強みは、対応するroute/realizationで再利用する。Layer 2 coreへは、goal、ledger、recovery、evidence refs、stop reasonsのような移植可能なmechanismだけを残す。
