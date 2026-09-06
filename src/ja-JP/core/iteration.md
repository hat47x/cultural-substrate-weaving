# Framework contactとround handoff

新しい材料や別の文化体系との接触によって作業を再開するときに読む。

この文書はmulti-round inquiry orchestrationそのものを実装しない。差分再開、stable artifact、question shift、append-only round history等は専用Method / compatible realizationへ委ね、CSWは文化体系との接触で何が新たに生じたかを由来付きで渡す。

## 責務境界

複数roundの再開・差分管理が必要な場合は、利用可能なら `iterative-inquiry-synthesis` または同じMethod Definitionを満たすcompatible realizationを用いる。

反復探索側へ委ねるもの:

- input delta
- touched-artifact reopen
- local / global reopen decision with reason
- stable semantic IDs across rounds
- structural delta
- question shift
- semantic delta vs representation delta
- append-only history
- residual / reopen condition
- continue / stop / handoff reason

CSWはこれらを別系統のround管理として再実装しない。

## 新しいframework contactはdeltaとして渡す

後の時点で、

- 別の文化体系
- 同じ体系の別位置
- 別のnative operation
- previewからfullへの深度変更
- 再照射による別の問い

から新しい候補が生じた場合、過去の全材料を自動的に再統合しない。

少なくとも必要に応じて次をdeltaとして渡す。

```text
new material / question:
origin / framework ref:
possibly touched prior artifact / residual:
framework contact change:
```

どこまでreopenするかは反復探索Methodへ委ねる。

## framework contactの結果が空でもよい

文化体系をprobe / previewした結果、対象側へ戻す新しい問い・対比・残差が生じなかった場合、それを正常な結果として扱う。

例えば:

```text
framework contact: no_useful_increment
material delta: none
reopen request: none
```

文化体系を使ったこと自体を理由に、洞察や次roundを作らない。

## 帰属をround間で保つ

文化体系由来候補が後の対象側材料で支持・反証・修正された場合も、問いがどこから生じたかの由来を消さない。

`origin` と `verification` を別に保持できる。

```text
meaning: <現在の意味>
origin: framework_generated
verification: target_supported | unresolved | contradicted / weakened等
verification_basis: <target-side refs>
```

後から支持されたことを理由に、過去roundへ遡って「最初から対象事実だった」と書き換えない。

反証された場合も、体系を守るために対象側材料を弱めない。

## 反復探索realizationがない場合

compatible Layer 2 realizationが利用できない環境でも、CSWは一回の探索結果として、

- 新しく生じたframework候補
- 由来
- target-sideで確認すべきこと
- 戻り先
- unresolved / reopen condition

を返せる。

ただし、append-only round history、touched-artifact reopen、structural delta等を実際に運用していないなら、multi-round orchestrationを実行済みとは称しない。

## CSW側に残すevent

長期履歴の一般event taxonomyは反復探索／governance側へ委ねる。

CSW固有に重要なのは、文化体系との接触が変わったことを後から辿れることである。

必要なら `framework_contact_change` 相当のeventを記録する。

例:

```text
framework: FW-A -> FW-B
change: preview position changed / native operation changed / no-useful-increment
produced: F5, Q2
handed_to: iterative inquiry round N
```

このevent自体を有用性・正しさの評価にしない。

## 停止と再開

CSW固有の完了条件として、一定数の文化体系、一定round数、`full` depth、体系固有操作の実行を要求しない。

再開の契機として文化体系から具体的な新しい問いが生じた場合、その問いをLayer 2へ渡す。

追加のframework contactが対象側の問い・材料配置・成果物・判断を動かさない場合は、`no_useful_increment`を保ったまま止まってよい。

停止・採用・行動への移行の決定権は `core/principles-and-constraints.md` の委任境界に従う。

## 最小handoff

反復探索へ渡すときは、現在のtaskに必要な範囲で次を含める。

- current inquiry
- new framework-derived material / question
- origin / framework ref
- touched candidate refs if known
- unresolved / verification need
- return-to-target condition

過去round全文を複製しない。

## CSW固有の正本

この接続より上位の原則は `core/principles-and-constraints.md` に置く。

とくに、可能性と採用、認知と事実、保存と現在の注意を混同しない。
