# KJ Atlas Case 001〜003の比較条件を凍結する

- Status: Research synchronization / no runtime rule change
- Date: 2026-08-30
- Related: `kj-atlas-cognitive-coevolution.md`, `kj-atlas-case001-longitudinal-companion.md`, `framework-use-lifecycle-trace.md`
- External experiment: `hat47x/kj-atlas` PR #2805

## 目的

KJ Atlas側で事前登録し、すでに凍結したCase 001〜003の比較条件を、cultural-substrate-weaving側からも追跡できるようにする。

この文書は実験結果を記すものではない。Caseの選定、source snapshot、skill snapshot、arm treatment、review順序が**最初の有効なCase 001 runより前に固定されたこと**を記録するためのmaintainer文書である。後から現在のCSW方法論を比較条件へ逆流させないことが主な目的となる。

## 凍結したCaseの構成

KJ Atlas側では、性質の異なる少なくとも3つの開発課題を、同じ4-arm構造で比較する。

| Case | 主領域 | 固定した問いの中心 |
|---|---|---|
| 001 | Product / value | KJ Atlasの存在目的と一次利用仕事 |
| 002 | AI governance / product behavior | AI提案・自動化と、人間の判断・確認・有益な摩擦との境界 |
| 003 | Architecture / operations / adoption | local/offline/self-hostによるデータ統制とcollaborationの境界 |

Case 001の結果を見た後で、Case 002/003を都合のよい問題へ差し替えないことも事前登録している。原則として001→002→003の順に実施する。問いそのものが閉じた、source snapshotを成立させられない、重大な安全上・権限上の理由がある、といった場合に限ってdeviationを記録する。

## 共通で固定したsnapshot

Cases 001〜003では、次を共通条件として固定している。

- KJ Atlas product snapshot: `hat47x/kj-atlas@2232b3bb26647e5c4a083f55bdbf83c161698649`
- B/D用CSW snapshot: `hat47x/cultural-substrate-weaving@3988e12e5f7f316f377d3391e9486c8467a111d5`
- B/Dへ渡すCSW source: frozen manifestで指定したcanonical `src/ja-JP`のみ
- A/CにはCSW sourceを渡さない
- Round 1では、arm固有の外部Web検索を行わない
- C/Dは空のstarterから始め、結論、カード、束、表札を事前投入しない

CSWのfrozen commit `3988e12e...` は、`VERSION 0.2.0`時点の比較条件である。現在の`develop/v0.4.0`や、v0.3.0以降で追加した方法論、maintainer文書、evaluation文書をB/Dのmodel/operator inputへ追加しない。

## 4-arm条件と実行順序

比較条件は次のまま維持する。

| Arm | 外部表象 | CSW |
|---|---|---|
| A | 通常チャット/文書 | なし |
| B | 通常チャット/文書 | frozen skill snapshot |
| C | KJ Atlas | なし |
| D | KJ Atlas | frozen skill snapshot |

KJ Atlas側のfreeze registerでは、armの実行順序を`C → D → B → A`としている。この順序も、途中結果を見て変更しない。

## raw resultとreviewを分ける

実験側では、次の順序を守る。

1. armごとのraw resultを固定する。
2. blind reviewer向けpackageを作る。
3. blind reviewを完了する。
4. その後に、unblindなmethod/arm比較を行う。

invalid、negative、no-incrementのresultも削除しない。

`framework-use-lifecycle-trace.md`など、現在のCSW側で追加した実験者向けの来歴は、**raw resultと既存run recordを固定した後**にだけ作る。来歴を書くための追加質問、追加の文化体系探索、再実行は行わない。

## CSW側では二つの時間線を分ける

### 比較実験の時間線

Cases 001〜003のA〜Dでは、frozen CSW `0.2.0`を使う。現在の改善を途中から投入しない。

### 長期companionの時間線

本チャットや将来の実作業では、その時点のactive developを使ってよい。ただし、独立A〜Dとは別のprospective観察として扱い、`method_ref`を記録する。

この二つの時間線を混ぜない。

## cross-caseで初めて判断すること

単一ケースの勝敗を、CSWの価値、欠陥、方法変更の根拠へ直結させない。

Case 001〜003を横断した時点で、少なくとも次を確認する。

- CSWの増分が、特定の領域や一つの文化体系だけに依存していないか。
- Arm Dの組合せが正の相互作用なのか、方法を重ねすぎたことによる負の相互作用なのか。
- 根拠保持、異論保持、再訪、依存校正などの改善が、単なる論点数の増加にすぎないのではないか。
- 同じskill-side method defectが、異なるケースでも繰り返し現れるか。
- loading、forcing、framework capture、provenance lossなどの問題が、どの条件で再現するか。

## 方法論正本へ昇格させる条件

`src/<locale>/`を変更する候補にできるのは、既存の帰属ゲートを通り、さらにcross-caseで同じ方法上の欠陥が繰り返し現れた場合に限る。

単一ケースで得た所見は、まず次のいずれかとして保持する。

- case固有の観察
- caller/domain context
- KJ Atlas product/UI
- model挙動
- experiment design
- 未決

複数ケースで同じCSW固有の欠陥が再現しなければ、runtime規則を増やさない。

## 現時点の状態

KJ Atlas PR #2805では、Case 001〜003の問い、source manifest、starter、launch packet、shared validator、blind-review infrastructure、portfolio freezeまで準備されている。

一方、現時点のPR差分には、A〜Dの実run recordはまだ含まれていない。そのため、ここから言えるのは「比較条件がより強く固定された」という実験設計上の更新だけであり、CSWの効果や方法上の欠陥について新しい実証結果はまだない。

> **今は方法論を増やす段階ではない。凍結した性質の異なる3ケースから実データが得られるまで、比較条件を守る段階である。**
