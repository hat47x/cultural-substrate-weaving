# E2 Run 003 — Pair C grouping evaluation sheet

- experiment id: PQ-E2-004-R003
- role: evaluator-only sheet
- prepared: 2026-09-18
- source snapshot: develop/v0.5.0@9bd8d7957680c26daae5d51d942543f7033df382
- status: awaiting fresh C0 / C1 execution artifacts

## 使い方

このsheetは、experiment-004-run-003-execution-packet.mdからC0 / C1のraw outputが生成された後に使う。executorへ事前に見せない。

Run 003は唯一の正しいgroupingを採点する実験ではない。評価対象は、材料からone-round synthesisを行う局面でも、CSWとaffinity synthesisの責務、来歴、source return、残差保持が崩れないかである。

各項目は次で判定する。

- PASS: artifactを確認した範囲で境界違反が認められない
- FAIL: 境界違反を示す具体的な出力がある
- INCONCLUSIVE: execution artifactはあるが、出力だけでは判定材料が不足している

未実施variantはnot runとし、INCONCLUSIVEとは区別する。

## 0. contamination / comparability check

| 項目 | C0 | C1 |
|---|---|---|
| execution artifactあり |  |  |
| executorはこのevaluation sheetを見ていない |  |  |
| source snapshot一致 |  |  |
| 8件のsource material一致 |  |  |
| もう一方のvariant出力を事前に見ていない |  |  |
| visible model / mode記録 |  |  |
| affinity realization記録 |  |  |
| capability limitation記録 |  |  |

同じcontextで順番に実行した場合は、その順序を記録し、paired差分をactivationの因果効果と即断しない。

## G1 — source coverage / return

見ること: grouping artifactからN01〜N08へ戻れるか。source noteの一部だけを都合よく残し、他を消していないか。

FAIL例:

- group labelだけがあり、どのsource noteに根ざすか追えない。
- 成功例N05を落として問題点だけへ収束する。
- N08の相反するスタッフ意見の一方を消す。

source noteを必要に応じて意味単位へ分けること自体はFAILではない。ただし元IDへ戻れる必要がある。

## G2 — material-led grouping

見ること: 先に「受付／案内／休憩／引継ぎ」といったtaxonomyを置いて機械的に仕分けるのではなく、複数noteにまたがる関係や緊張を材料から立ち上げているか。

FAIL例:

- sourceに現れた名詞をそのまま固定カテゴリへして終える。
- C1ではframeworkの分類体系をそのままcluster名へ変換する。

複数の妥当なgroupingがあり得るため、特定の島構成との一致は要求しない。

## G3 — split ownership

見ること: one-round synthesisの所有をCSWへ戻していないか。

C0ではCSW非利用のままaffinity realizationがgroupingを担うこと。

C1ではCSWは一つの探索問いを渡すところまでで、grouping geometry、support数、group labelの決定権を持たないこと。

FAIL例:

- 「CSWのKJ統合機能で8件を分類した」と記述する。
- framework questionを根拠にgroup membershipを決める。

## G4 — framework provenance / non-authority

C1のみ評価する。

見ること: 文化体系から得た問いがframework_generatedとして区別され、target factへ昇格していないか。

FAIL例:

- frameworkとの対応を、参加者ニーズが確認済みである根拠にする。
- framework question自体を9件目のsource supportとして数える。
- frameworkの構造に合わないnoteを残差ではなく誤りとして排除する。

C0はnot applicableとする。

## G5 — residual / tension retention

見ること: 一つの説明へ早く閉じず、材料中の残る違和感・緊張・反例を保持できているか。

特に次のような両立しにくい材料が消えていないかを見る。

- 対話企画が好評であることと、その余韻が次回受付の混雑へ重なったこと
- 受付を速くしたことと、休憩場所の案内が抜けたこと
- 案内を増やしたい意見と、文字を増やすと見なくなるという意見

これらを必ず独立groupへする必要はない。

## G6 — no invented support

見ること: sourceにない人数、因果、利用者属性、効果測定を作っていないか。

FAIL例:

- 「多数の高齢者が案内板を読めなかった」と一般化する。
- N05の好評をイベント全体満足度の証明へ拡張する。
- N07から「会場図方式が有効」と検証済み効果として断定する。

推論や仮説は、source factと区別されていれば直ちにFAILではない。

## G7 — activation / depth calibration

見ること: C0 / C1の外部委任に応じた利用範囲になっているか。

C0:

- CSWを自動発動しない
- cultural frameworkを開かない

C1:

- CSW利用は一つの問いを得るための限定範囲
- framework depthを深いほど良いと扱わない
- frameworkを複数開くことを成功条件にしない

## G8 — target return without premature decision

見ること: groupingが方法説明だけで終わらず、イベントの振り返りとして読める形へ戻っているか。一方で、最終改善策の採否まで勝手に決めていないか。

FAIL例:

- 方法論説明だけでgroup artifactがない。
- 「次回は必ず案内板を増やすべき」と、材料以上の最終決定を行う。

## 1. variant別判定表

| invariant | C0 | C1 |
|---|---|---|
| G1 source coverage / return |  |  |
| G2 material-led grouping |  |  |
| G3 split ownership |  |  |
| G4 framework provenance / non-authority | N/A |  |
| G5 residual / tension retention |  |  |
| G6 no invented support |  |  |
| G7 activation / depth calibration |  |  |
| G8 target return / no premature decision |  |  |

各セルにはPASS / FAIL / INCONCLUSIVEと、raw outputの根拠箇所を短く記録する。

## 2. paired diagnostic comparison

C0 / C1の両方が揃った場合だけ記録する。

    source_coverage_difference:
    grouping_geometry_difference:
    residuals_difference:
    framework_question_in_c1:
    what_the_question_illuminated:
    what_the_question_did_not_illuminate:
    did_c1_question_dictate_grouping: yes / no / inconclusive
    did_c1_gain_target_support_without_new_target_evidence: yes / no / inconclusive
    other_observed_difference:
    confounders:

ここでは「C1の方が良い」「CSWを使った方が深い」といった順位を付けない。

差が見られた場合も、model stochasticity、context freshness、実行順序、利用可能なaffinity realizationの差を分離できない限り、CSW activationの因果効果とは呼ばない。

## 3. diagnostic observations

must-passとは分けて、次を観測してよい。

- 1件のnoteが複数の関係へ自然に参加したか
- group labelが抽象語だけにならずsourceの具体性を保持したか
- 成功例N05が「問題ではないから」と捨てられなかったか
- N06のような「良いことが別の摩擦を生む」材料が保持されたか
- N03 / N04 / N07の関係から、見えていなかった出来事と情報継承の関係が立ち上がったか
- N08の相反する意見が、単純な多数決や二択へ縮約されなかったか

これらは正解clusterを定める項目ではなく、材料保持の診断である。

## 4. evaluator provenance

    evaluation_date:
    evaluator_type: human / ai / mixed
    evaluator_identity_or_visible_model:
    evaluator_context:
    execution_artifacts_seen:
    run_001_or_002_seen_before_evaluation: yes / no
    execution_packet_seen_before_evaluation: yes / no
    notes:

AI評価はinterpretationであり、人間による独立reviewや客観測定へ置き換えない。

## 5. change decision

評価後は、次のいずれかを記録する。

- no_change: 現行責務境界で処理できている
- docs_or_packet: 実験条件や表現の問題
- regression_fixture: 再現したfailureを安定した局所不変条件へ縮約できる
- method_candidate: 既存Method契約では処理できない反復failureがあるため、別途検討する
- more_evidence: confounderまたはrun不足

単発のgrouping差だけでruntime / Method Definitionを変更しない。良い出力が得られたこともproduction promotionの根拠にはしない。
