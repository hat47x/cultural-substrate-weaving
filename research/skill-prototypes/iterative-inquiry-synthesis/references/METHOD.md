# Iterative Inquiry Synthesis — Method Definition

Status: research candidate

## Purpose

一回の統合結果を固定結論へせず、そこから現れた未解決・対立・空白・新材料を、必要な箇所だけ次の問いと統合roundへ戻す。

この方法の目的はround数を増やすことではない。

> **何が変わったか、何が変わらなかったか、何がなお分からないかを壊さず、意味のある差分がある間だけ探索を継続できる状態を作る。**

## Scope

この方法はmulti-round inquiry orchestrationを所有する。

所有するもの:

- current inquiry / purpose
- input delta
- prior artifact reopening
- synthesis realization binding
- structural delta
- residuals / unresolved
- continuation / stop / handoff reason
- append-only round history
- restart conditions

所有しないもの:

- one-round synthesis algorithm
- web/search strategyそのもの
- domain expertise
- recommendation / decision authority
- action execution
- private chain-of-thought

## Relationship to existing iterative research skills

Autonomous research / autoresearch系Skillから、次の運用上の長所を参照する。

- goal / current objectiveを明示する。
- iterationごとに外部成果物を記録する。
- append-only ledgerを持つ。
- recovery pointを残す。
- stop conditionsを明示する。
- evidence / source stateを次roundへ持ち越せる。

一方、次は本方法の不変条件にはしない。

- measurable scalar metricの必須化
- one-change-per-experiment
- max iterationsを使い切るまで自律継続
- machine-checkable successだけを正常停止とすること
- research search backlogを必須とすること
- autonomous executionを既定とすること

本方法は探索・創作・分析・設計など、単一metricへ還元できないinquiryも扱う。

## Inputs

- current inquiry / question
- previous round snapshot or artifact references
- new material / counterexample / changed constraint / external result
- existing residuals
- optional prior synthesis structure

## Outputs

- round snapshot
- reopened artifact refs
- synthesis realization binding
- structural delta
- newly emerged meaning / relation / question
- preserved unchanged structure
- withdrawn or weakened prior interpretation
- residuals
- possible next inquiry
- stop / continue / handoff reason

## Invariants

### I1. Round is a delta, not a restart

新材料が入っただけで全履歴を最初から再要約しない。

まず、その差分がどのartifact、group、relation、residualへ触れるかを見る。

### I2. Reopen only what is touched unless a global contradiction appears

差分が局所なら局所を再開する。

全体構造を壊す反証・前提変更・問いの変更がある場合のみ、より広いreopenを行う。

### I3. Old structure has no immunity

既存島・表札・仮説を保存すること自体を目的にしない。

新材料が核を変えるなら、split / merge / relabel / withdrawできる。

「既存を安易に壊さない」と「既存を正解扱いする」は別である。

### I4. Structural delta is explicit

各round後に少なくとも次を区別できるようにする。

- newly emerged
- changed
- unchanged despite new material
- weakened / withdrawn
- unresolved

変化がないことも成果であり得る。

### I5. Residuals are reopenable anchors

gap / conflict / singleton / unresolvedを「未完成だから削除する」対象にしない。

後のmaterial deltaが触れたときにreopenできるanchorとして保持する。

### I6. Question shift is versioned, not rewritten

問いが変わったとき、過去roundの問いを現在の問いへ書き換えない。

何が問いを変えたか、以前の理解の何がなお有効かを残す。

### I7. Continuation requires a reason

次roundを開始するには、外部から説明できる理由が必要である。

例:

- new material exists
- a residual can now be checked
- a contradiction needs discrimination
- narrative produced an unverified relation
- environmental conditions changed
- user explicitly asks to revisit
- another cognitive field exposed a concrete new question

「まだround数が少ない」は理由にしない。

### I8. Stopping with unresolved material is valid

次の場合、未解決を残したまま正常に停止できる。

- 追加材料が現在取得できない。
- 追加roundが実質的な構造変化を生まない。
- 現在の利用目的に必要な粒度へ達した。
- 次に必要なのが人間の価値判断、domain decision、external actionである。
- 追加探索の費用が期待される認知増分を上回る。

`gap == 0` や完全説明を終了条件にしない。

### I9. Append-only history, current-state projection

過去roundを破壊的に更新しない。

現在の見解をprojectionとして持ってよいが、どのroundで何が変わったかへ戻れるようにする。

### I10. Method realization is explicit

各roundで何の統合方法を使ったかを追跡できる。

異なるrealizationへ切り替えた場合、その変更自体がoutput差へ影響し得ることを残す。

### I11. External exploration outputs keep their epistemic status

web research、interview、experiment、cultural framework等から得たものを、元の認識状態を消して既存事実へ混ぜない。

探索経路は材料を供給する。truth statusを自動決定しない。

### I12. No private chain-of-thought as history

保存するのは、問い、材料、成果物、差分、残差、判断理由等の外部から意味のあるartifactである。

モデル内部のtoken-by-token reasoningを方法履歴の正本にしない。

## Round Kernel

```text
receive delta
  ↓
locate touched artifacts
  ↓
state current inquiry
  ↓
reopen locally or globally with reason
  ↓
run one compatible synthesis realization
  ↓
compare with prior structure
  ↓
record new / changed / unchanged / withdrawn / residual
  ↓
continue | stop | handoff
  ↓
append round snapshot
```

## AI-era advantage and risk

生成AIは大量の再読・再統合を低コストで行えるため、過去の人間作業よりroundを回しやすい。

この利点は同時に危険でもある。

- 毎round全面再構成して履歴を漂流させる。
- 文面が変わっただけなのに「新発見」と数える。
- 何度も処理した派生物を独立supportとして重くする。
- 完了感を得るためにresidualを消す。
- 終わらない探索を「深さ」と誤認する。

本方法は、**再計算能力を全面再生成ではなく差分再開へ使う**ことを生成AI向けの中心補正とする。

## Relationship to Affinity Synthesis

`affinity-synthesis` は一回のmeaning integrationを担当する。

`iterative-inquiry-synthesis` は、そのinput/output/residualをround間で扱う。

Layer 2が独自のgrouping / labeling algorithmを再実装しない。

## Relationship to Cultural Substrate Weaving

CSWは外部探索routeの一つとして、文化体系からquestion / contrast / correspondence candidateを返す。

Layer 2はその由来を保ったまま次round materialへ接続する。

文化体系由来candidateをtarget-supported observationへ自動昇格させない。

## Failure modes

- new materialが来るたびに全体を再構築する。
- old structureを守るため新材料を既存島へ押し込む。
- question shiftを過去の失敗として履歴から消す。
- round数やtoken量を進捗とみなす。
- unresolvedを埋めるため推測を事実化する。
- stopを「諦め」とみなし無限に探索する。
- synthesis realization変更の影響をmaterial changeと混同する。
- 外部探索routeの仮説をsource factへ昇格させる。

## Realization boundary

このMethod Definitionは、特定のfilesystem layout、JSON schema、autonomous agent loop、検索tool、最大round数、時間budget、モデルを要求しない。

Agent Skill realizationは必要に応じてround templateやledgerを実装できる。
