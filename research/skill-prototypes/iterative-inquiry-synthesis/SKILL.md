---
name: iterative-inquiry-synthesis
description: 材料が複数roundで増える調査・分析・設計・創作で、一回の統合結果を固定せず、新材料が触れた意味構造だけを再開し、問い・残差・履歴・停止／再開条件を追跡する。単発の親和統合、固定taxonomy分類、domain固有の調査法そのものには使わない。
---

# Iterative Inquiry Synthesis

Status: research candidate Agent Skill realization

一回の統合を最終結論として固定せず、後から来た材料が**どこを変え、どこを変えず、何を未解決として残したか**を追跡する。

このSkillは**one-round synthesisの内部手順を所有しない**。利用できる場合は `affinity-synthesis` または同じMethod Definitionを満たすcompatible realizationを各roundの統合に使う。

## When to use

次のような仕事で使う。

- 調査・分析・設計・創作が複数roundにわたり、後から材料が増える。
- 前roundの結果にgap / conflict / singleton / unresolvedが残り、それが後の材料で意味を持つ可能性がある。
- 新材料が来るたびに全体を再構成するのではなく、既存構造との差分を追いたい。
- 問いそのものが材料によって変化する可能性がある。
- 長期作業で、何が変わり何が残ったかを外部成果物として追跡したい。

## When not to use

次では優先しない。

- 一回のsynthesisで十分。
- 同じ固定datasetを、問いも材料も変わらないまま再実行するだけ。
- domain固有のsearch strategy、法務・医療判断、product prioritization等が中心。
- predeterminedなround数を回すこと自体が目的になっている。

## Core Round

private chain-of-thoughtではなく、外部から検査できるartifactを残す。

1. **Receive delta**
   - 新しいsource、observation、counterexample、execution result、constraint change等を受け取る。
2. **Locate touched semantic artifacts**
   - 新材料が実際に触れるcard / group / relation / resonance / residual / questionだけを前roundから持ち込む。
   - stable semantic handleがあれば再利用する。
3. **State the current inquiry**
   - 今roundで何を見分けたいか、何を理解したいかを一文で置く。
   - 前roundの問いが今も正しいとは仮定しない。
4. **Run one synthesis realization**
   - 新材料と必要なprior materialだけを、compatible one-round synthesisへ渡す。
   - どのrealizationを使ったか記録する。
5. **Inspect structural delta**
   - 何が新しく立ったか。
   - 何が変わったか。
   - 何を実際に再検査し、意味上は変わらなかったか。
   - 何が弱まり、撤回されたか。
6. **Separate semantic and representation delta**
   - card meaning / membership / label / relation / resonance / residual / questionの変化と、wording / renderer / line wrapping / layoutだけの変化を分ける。
7. **Externalize residuals**
   - gap / conflict / singleton / unresolved / weak relation等を残す。
8. **Decide continuation boundary**
   - 残った問いを実際に判別できる材料があるか。
   - 今の目的にもう一roundが有効か。
   - 次はdomain判断・人間の価値判断・外部actionなのか。
9. **Freeze a round snapshot**
   - 前roundを上書きせず、今回のdeltaとreturn pointを追加する。

## Round Contract

必要に応じて次を外部化する。

- round id
- current inquiry / purpose
- input delta
- reopened prior artifact refs / touched semantic IDs
- synthesis realization id / name
- representation / schema ref if available
- output artifact refs
- residual refs
- semantic structural delta
- representation-only delta if relevant
- possible next inquiry / verification target
- stop / continue / handoff reason

保存形式は固定しない。

### Compact delta notation

stable IDがある場合、次の記号で**change operation**を表せる。

```text
+  newly emerged
~  changed
=  touched and explicitly checked, but semantically unchanged
-  withdrawn / no longer supported
?  unresolved / residual remains
```

例:

```text
+ C115 := "新材料から立った意味単位"
~ G03 := members + {C115}; label "旧表札" -> "改訂表札"
= G04 :: "新材料を照合したが意味核は維持"
- R02 :: "以前の向きは現在の材料では支持されない"
+ R05: G03 -- G07 :: "新しく立った関係predicate"
? Q08 :: "現在の材料ではまだ判別できない"
```

この記号は変化を表す。card / groupの意味分類ではない。

## Stable Semantic Handles

one-round synthesis側に `C / G / R / X / U / Q` 等のstable IDがある場合、意味上の同一性が保たれる間はroundを跨いで再利用する。

- 文言を整えただけで新IDへ振り直さない。
- 同じIDでも意味のある変更は `~` として記録できる。
- split / mergeで同一性が失われる場合は新IDを立て、旧IDからのderivationを残す。

ID prefixは分類体系ではなく参照handleである。

## Semantic Delta Is Not Diagram Delta

node位置、edge routing、automatic layout、折返し、色、shape等の変更を新しい意味発見と数えない。

representation変更によって新relation candidateに気づくことはある。その場合も、candidateとしてsemantic recordとsource materialへ戻して確認してから昇格する。

視覚的近接をrelationへ、上下配置をhierarchy / causalityへ自動変換しない。

## Do Not Rebuild Without Cause

新材料が来たこと自体を、全group / relation再構築の理由にしない。

まず確認する。

- 新材料は既存の意味核を変えるか。
- 局所追加で足りるか。
- 独立した新しい訴えを立てるか。
- 既存conflictを解く、または深めるか。

旧構造が材料をなお十分に表すなら、それを保ち、意味のあるdeltaだけを記録する。

## Residuals Are Reopenable Anchors

未解決だからという理由でresidualを削除しない。

例:

- gap: 後で確認する価値のある空白・関係不足。
- conflict: 現材料では整合しない差。
- singleton: まだ他と組にならない訴え。
- unresolved: 現材料では判別できない区別。

閉じたtaxonomyではない。

今の問いに無関係なら背景化し、後の材料が実際に触れたときだけ再開する。

## Question Shift

問いは前後左右へ動いてよい。

問題解決では、状況把握、問題設定、本質追求、構想、具体化、手順化、検証等の動きが現れることがあるが、固定stage gateにはしない。

問いが変わった場合、過去roundの問いを後から書き換えない。何が問いを動かしたか、旧構造のどこが今も使えるかを残す。

## Stop Conditions

complete explanationやresidual zeroを成功条件にしない。

停止してよい例:

- 今の問いに対し、追加roundが意味のある構造変化を生まなくなった。
- 未解決は残るが、現時点で判別可能な新証拠がない。
- 目的に必要な理解粒度へ達した。
- 次がdomain decision / human value judgment / external actionである。
- 追加探索costが期待される認知gainを上回る。
- 外部条件で一度閉じる必要がある。

## Restart Conditions

次のような理由があれば再開する。

- new source / observation
- counterexample
- environment change
- contact with an old residual
- explicit revisit
- a different cognitive field or framework exposes a new question
- previously unavailable compatible synthesis realization becomes available

過去の停止を失敗扱いせず、触れた箇所だけを再開する。

## External Exploration Routes

文化体系、web research、domain skill、human interview、experimentなどは、次roundの材料や問いを得る**外部探索経路**として利用できる。

それぞれが出した仮説やcorrespondenceを、独立した観察事実へ自動昇格させない。

外部探索由来のものをone-round synthesisへ渡す場合は、origin / operation / incoming status or roleを、target-side source materialと区別できる状態で渡す。これらのmetadataをgrouping geometryや独立support数へ変換しない。

特に `cultural-substrate-weaving` を使う場合、文化体系から得た問い・対応候補は、その由来を保ったまま対象材料へ返す。後から対象側の資料で独立に支持された場合も、最初のframework由来を履歴から消さず、新しいtarget-side supportを別に記録する。

## Quality Checklist

- [ ] round数を目的化していない。
- [ ] 前roundを上書きせず、差分として追跡できる。
- [ ] 新材料が触れない部分まで無理由に再構成していない。
- [ ] stable IDがある場合、意味上同一なものを無理由に振り直していない。
- [ ] 外部探索由来の問い・仮説・correspondenceを、origin / statusを失ってtarget-side factへ混ぜていない。
- [ ] 使用したsynthesis realizationを追跡できる。必要なのに利用できなかった場合は未実行として区別している。
- [ ] semantic deltaとwording / renderer / layoutだけの差を区別した。
- [ ] diagram proximity / hierarchyをsemantic relationへ自動変換していない。
- [ ] gap / conflict / singleton / unresolvedを次の観察事実と混同していない。
- [ ] question shiftを失敗または進捗点数へ単純変換していない。
- [ ] stop理由が外部から説明可能である。
- [ ] private chain-of-thoughtではなく外部成果物を保存している。

## Progressive References

- 方法の不変条件: `references/METHOD.md`
- 標準round記録とdelta notation: `references/ROUND-TEMPLATE.md`
- Layer 1との境界とsemantic representation: 利用可能な場合はcompanion Skill `affinity-synthesis` のMethod Definition / representation contractを参照する。sibling filesystem pathの存在は前提にしない。

## Boundary

このSkillは、何が真実か、どの意思決定を採るべきか、どのactionを実行すべきかを自動決定しない。

役割は、**問いと材料と統合結果の履歴を壊さず、必要なときに次の認知roundへ接続すること**である。
