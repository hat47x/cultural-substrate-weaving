# Iterative Inquiry Synthesis — Fallback Boundary Recheck 2026-09-06

Status: **same-authoring-model specification recheck; not an independent model evaluation**

`DRY-RUN-2026-09-06.md` のCase 9で見つかった、compatible one-round synthesis realization不在時のfallback gapについて、修正後のMethod DefinitionとAgent Skill realizationを再確認する。

元dry-runは修正前の記録として保持し、結果を書き換えない。

## Original gap

research suiteでは `iterative-inquiry-synthesis` が `hard_dependency: false` である一方、one-round synthesisが必要なのにcompatible realizationが利用できない場合の扱いが明示されていなかった。

危険は、Layer 2が独自のgrouping / labeling / return-checkを即興し、それをcompatible one-round synthesisが実行されたかのように扱うことだった。

## Post-fix Method Definition

`references/METHOD.md` はI15として次を区別する。

1. one-round synthesisが不要で、差分・履歴管理だけを行うround。
2. synthesisが必要だがcompatible realizationが利用できず、未実行のままstop / handoffするround。
3. caller等が別realizationを明示し、そのbindingを記録して実行するround。

利用不能を永続停止にはせず、後からcompatible realizationが利用可能になれば未実行deltaへ戻れる。

Round Kernelも、synthesisの必要性とrealization availabilityを区別する。

## Post-fix Agent Skill realization

`SKILL.md` は同じ境界を次へ反映した。

- Skill冒頭のownership説明
- Core Roundのsynthesis realization binding
- Stop Conditions
- Restart Conditions
- Quality Checklist

Layer 2へone-round synthesis algorithmをコピーしていない。

## Case 9 recheck

### Required behavior

- Layer 1/2 ownership separation: COVERED BY SPECIFICATION
- compatible realization binding recorded: COVERED BY SPECIFICATION
- Layer 2-specific grouping algorithm prohibited: COVERED BY SPECIFICATION
- no compatible realization available → explicit not-run / stop / handoff: COVERED BY SPECIFICATION
- synthesis not needed → delta/history-only round distinguishable: COVERED BY SPECIFICATION
- later realization availability can reopen the pending delta: COVERED BY SPECIFICATION

### Invalid behavior now explicitly rejected

- compatible realization不在時にLayer 2独自の統合を即興し、`affinity-synthesis` 等の実行結果として扱う。
- synthesis未実行なのにoutput artifactを統合済み成果として記録する。
- realization availabilityの一時的欠如を、Method Definition上の永続的失敗へ変える。

## Residual evaluation need

このrecheckは**文面上の境界が閉じたことだけ**を確認する。

まだ実行評価が必要である。

- compatible realizationを意図的に利用不能にした環境で、Agentが即興統合せずhandoffできるか。
- one-round synthesis不要のroundで、不要なLayer 1呼び出しを強制しないか。
- 後でrealizationが利用可能になったとき、pending delta / reopen refsへ正しく戻れるか。
- callerが別realizationを指定したとき、その変更をmaterial deltaと混同しないか。

## Decision

**The specification gap identified by the authoring dry run is closed at the research Method/Skill text level. Empirical behavior remains unverified.**

canonical CSW runtimeの縮小やsuite build migrationへ進む根拠にはまだしない。
