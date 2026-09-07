# Iterative Inquiry Synthesis — Carry-forward / Handoff Recheck 2026-09-08

Status: **same-authoring-model specification recheck; not an independent model evaluation**

## Purpose

Layer 1 → Layer 2 handoff capsuleの検討と外部iterative research Skill比較から、次の区別がLayer 2のMethod Definitionレベルで必要だと分かった。

```text
preserve / carry forward
    !=
reopen now
    !=
continue another round
```

このrecordは、2026-09-08時点の `references/METHOD.md` / `METHOD.en.md` / `SKILL*.md` / `ROUND-TEMPLATE*.md` / `evals/CASES.md` にその境界が反映されたかを同一authoring modelで仕様上再確認する。

ここでの `COVERED BY SPECIFICATION` は実modelの挙動を証明しない。

## Triggering findings

### 1. Handoff capsuleの役割

one-round synthesisは、semantic identity、provenance、residual、possible next checksを次roundへ渡す必要がある。

しかしcarry-forward list全体をLayer 2が毎回reopenすると、生成AIの低コスト再生成能力が局所差分を全面再構築へ膨らませる。

### 2. Residualの役割

residualは「未完成だから消すもの」ではなく、後の材料が触れたときに戻れるanchorである。

同時に、residualが存在することだけでは次roundを実行する理由にならない。

### 3. English Method parity drift

Japanese Method DefinitionはI15として、compatible one-round synthesis realization不在時にLayer 2が即興統合して「実行済み」と称さない境界を持っていた。

一方、English draftは一時点でI14までしかなく、Round kernelも無条件にcompatible synthesis realizationをrunする表現になっていた。

これはMethod Definition parityの実際のdrift事例であるため、English I15を復元し、bilingual invariant parity checkを別途追加した。

## Post-change Method Definition

### I15 — Missing synthesis realization stays explicit

Japanese / Englishとも、少なくとも次を区別する。

1. synthesis不要でdelta/historyだけを更新する。
2. synthesisが必要だがcompatible realization不在で、未実行のままstop / handoffする。
3. caller等が別realizationを明示し、そのbindingを記録して実行する。

### I16 — Carry-forward state is not reopen or continuation authority

Japanese / Englishとも、持越しstateをreopen命令やcontinuation命令として扱わない。

- current deltaを先に読む。
- deltaが実際に触れたsubsetだけをreopenする。
- untouched artifactを「carriedされている」という理由で `= checked unchanged` にしない。
- residualやpossible next checkの存在だけでcontinueしない。
- 特定handoff schemaやID形式へMethod Definitionをhard-codeしない。

## Contract Case 10 recheck

`evals/CASES.md` Case 10は次を固定する。

### Prior carried state

- `G80`
- `G81`
- `X80`
- `Q80`
- `U80`
- possible next check

### Delta A

新sourceは `G80`, `Q80` のみに触れる。

Expected:

- reopen `G80`, `Q80`
- do not reopen `G81`, `X80`, `U80` merely because carried
- do not mark untouched items as `=`
- use arrival of the new source, not existence of an old candidate, as the reopen reason

**COVERED BY SPECIFICATION**

### Delta B

新semantic materialはなく、representationだけが変わり、`Q80`, `U80` は残る。

Expected:

- preserve `Q80`, `U80` as reopenable anchors
- normal stop is allowed
- representation change remains representation-only
- keep a later reopen condition

**COVERED BY SPECIFICATION**

## External-Skill evidence alignment

今回の外部比較では、次のmechanismをLayer 2へ選択的に取り込む方針とした。

Adopt:

- explicit current objective
- append-only ledger
- recovery / resume point
- evidence/material refs
- explicit stop conditions

Adapt:

- operational budgets
- stall detection
- dossiers
- early user review

Reject as universal Method invariant:

- mandatory scalar metric
- one-change-per-experiment
- machine-checkable success only for normal stopping
- max iterationsを使い切るまでの継続
- never ask / never pause autonomy directive
- universal search backlog
- universal automatic rollback

この比較から、round数そのものをtruth / confidence / independent supportへ変換する根拠は得ていない。

## Parity check added

`iterative-inquiry-synthesis/scripts/check_method_parity.py` は、日英Method Definitionについて少なくとも次を静的に確認する設計になった。

- I1〜I16のID集合が双方に存在する。
- I15 markerが双方に存在する。
- I16 markerが双方に存在する。
- required synthesisを実行済みと偽らないmarkerが双方に存在する。
- preserve / reopen / continueの三分離markerが双方に存在する。
- round countをtruth/confidence/supportへ変換しないmarkerが双方に存在する。

これは自然な英訳や独立査読の代替ではない。Method surfaceの重大な欠落を早期検出するstatic regressionである。

## Remaining evaluation need

このrecheck後も未検証なのは少なくとも次である。

1. 長い履歴で、modelがcarry-forward list全体を再活性化せず局所reopenを守れるか。
2. global contradiction時に必要十分な範囲へ広げられるか。
3. residualが多数残る状況で、不要な自動continueを抑止できるか。
4. compatible synthesis realizationを意図的に利用不能にしたhostで、即興統合を抑止できるか。
5. synthesis realization切替の差をmaterial deltaと分離できるか。
6. English Method/runtimeの独立review。
7. complete checkoutでresearch checksが実行成功するか。

## Decision

**The carry-forward / reopen / continuation boundary is now explicit at Method, runtime, template, and fixture levels. English I15 parity drift has been corrected at text level. Empirical behavior and complete-checkout execution remain unverified.**

このrecheckだけをproduction promotionの根拠にはしない。
