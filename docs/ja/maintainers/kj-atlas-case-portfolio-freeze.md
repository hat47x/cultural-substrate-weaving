# KJ Atlas Case 001〜003 portfolio freeze

- Status: Research synchronization / no runtime rule change
- Date: 2026-08-30
- Related: `kj-atlas-cognitive-coevolution.md`, `kj-atlas-case001-longitudinal-companion.md`, `framework-use-lifecycle-trace.md`
- External experiment: `hat47x/kj-atlas` PR #2805

## 目的

KJ Atlas側で事前登録・凍結されたCase 001〜003の比較条件を、cultural-substrate-weaving側からも追跡できるようにする。

この文書は実験結果ではない。Case選定、source snapshot、skill snapshot、arm treatment、review順序が**最初の有効なCase 001 runより前に固定されたこと**を記録し、後から現在のCSW方法論を比較条件へ逆流させないためのmaintainer記録である。

## 凍結されたcase portfolio

KJ Atlas側では、少なくとも3つの異なる開発課題を同じ4arm構造で比較する。

| Case | 主領域 | 固定された問いの中心 |
|---|---|---|
| 001 | Product / value | KJ Atlasの存在目的と一次利用仕事 |
| 002 | AI governance / product behavior | AI提案・自動化と人間判断・確認・有益な摩擦の境界 |
| 003 | Architecture / operations / adoption | local/offline/self-hostによるデータ統制とcollaborationの境界 |

Case 001の結果を見てCase 002/003を有利な問題へ差し替えないことが事前登録されている。原則として001→002→003を実施し、問いが閉じた、source snapshotを成立させられない、重大な安全・権限上の理由がある場合にだけdeviationを残す。

## 共通snapshot

Cases 001〜003は次を共通に固定している。

- KJ Atlas product snapshot: `hat47x/kj-atlas@2232b3bb26647e5c4a083f55bdbf83c161698649`
- B/D用CSW snapshot: `hat47x/cultural-substrate-weaving@3988e12e5f7f316f377d3391e9486c8467a111d5`
- B/Dへ渡すCSW source: frozen manifestで指定されたcanonical `src/ja-JP`のみ
- A/CへCSW sourceを渡さない
- Round 1ではarm固有の外部Web検索を行わない
- C/Dは空starterから始め、結論・カード・束・表札を事前投入しない

CSWのfrozen commit `3988e12e...` は `VERSION 0.2.0` の比較条件である。現在の`develop/v0.4.0`やv0.3.0以降の方法論、maintainer文書、evaluation文書をB/Dのmodel/operator inputへ追加しない。

## 4armと実行順序

比較条件は次を維持する。

| Arm | 外部表象 | CSW |
|---|---|---|
| A | 通常チャット/文書 | なし |
| B | 通常チャット/文書 | frozen skill snapshot |
| C | KJ Atlas | なし |
| D | KJ Atlas | frozen skill snapshot |

KJ Atlas側のfreeze registerではarm execution orderを `C → D → B → A` としている。この順序も結果を見て変更しない。

## raw resultとreviewの境界

実験側で重要な順序は次である。

1. armごとのraw resultを固定する。
2. blind reviewer向けpackageを作る。
3. blind reviewを完了する。
4. その後にunblindなmethod/arm比較を行う。

invalid、negative、no-increment resultを削除しない。

`framework-use-lifecycle-trace.md`など、現在のCSW側で追加した実験者用来歴は**raw resultと既存run recordを固定した後**にだけ作る。traceを書くための追加質問、追加framework探索、再実行は行わない。

## CSW側の二つの時間線

### 比較実験線

Cases 001〜003のA〜Dでは、frozen CSW `0.2.0`を使う。現在の改善を途中投入しない。

### 長期companion線

本チャットや将来の実作業では、その時点のactive developを使ってよい。ただし独立A〜Dとは別のprospective観察として扱い、`method_ref`を記録する。

この二つを混ぜない。

## cross-caseで初めて判定するもの

単一ケースの勝敗を、CSWの価値・欠陥・方法変更の根拠へ直結させない。

Case 001〜003を横断して初めて、少なくとも次を確認する。

- CSWの増分が特定の領域や一つの文化体系だけに依存していないか。
- Arm Dの組合せが正の相互作用なのか、方法過多による負の相互作用なのか。
- 根拠保持・異論保持・再訪・依存校正などの改善が、単なる論点数増加ではないか。
- 同じskill-side method defectが異なるケースでも再現するか。
- loading、forcing、framework capture、provenance loss等の問題がどの条件で再現するか。

## 方法論正本への昇格ゲート

`src/<locale>/`を変更する候補にできるのは、既存の帰属ゲートを通り、かつcross-caseで同じ方法欠陥が再現した場合に限る。

単一ケースで出た所見は、まず次のいずれかとして保持する。

- case固有の観察
- caller/domain context
- KJ Atlas product/UI
- model挙動
- experiment design
- 未決

複数ケースで同じCSW固有の欠陥が再現しなければ、runtime規則を増やさない。

## 現時点の状態

KJ Atlas PR #2805では、Case 001〜003の問い、source manifest、starter、launch packet、shared validator、blind-review infrastructure、portfolio freezeまで準備されている。

一方、現時点でPR差分にはA〜Dの実run recordはまだ含まれていない。したがって、ここから導けるのは「比較条件がより強く固定された」という実験設計上の更新だけであり、CSWの効果や方法欠陥について新しい実証結果はまだない。

> **今は方法論を増やす段階ではなく、凍結した異質3ケースから実データが出るまで比較条件を守る段階である。**
