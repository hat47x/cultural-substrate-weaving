# Marshallese wave navigation と通常の障害調査・可観測性の能力比較

Status: 2026-10-17 bounded runtime requalification / desk comparison, **not** independent experiment or adoption verdict.

## 比較の固定条件

[既存の正例](../worked-examples/marshallese-wave-navigation.md)の架空の分散処理障害を、そのまま比較対象とする。

- O1: queue Q-Aに入るジョブは正常に完了する。
- O2: service S-Bへのhandoff後にretry数が振動し始める。
- O3: S-Cへ到達する処理もあり、全経路が遮断されているわけではない。
- O4: 静的トポロジー図にはS-B→S-Cが記載される。
- O5: live traceでは一部のrequestにproxy P-Xが挟まる。
- O6: 特定deployment zoneを通るrequestのlatency spikeが強くなる。
- O7: P-Xやzoneがretryの原因だとは立証されていない。

対象に元々与えられたO4とO5の差を隠したり、計測がないふりをしたりしない。「現在の地図を作り直すことだけが通常手法」という弱いbaselineを採らない。

## 体系との接触前から選ばれる通常手法

**入口の依頼**：「S-B以降のretry振動と遅延を、現在のtrace・metrics・logsから調査してください。」

この依頼からSREのeffective troubleshooting、distributed tracing、request/spanごとの経路分析、メトリクスとの相関、比較仮説、実行時経路と設計図との差分照合へ進むことは自然である。

- Google SRE, *Effective Troubleshooting*：observationsを集め、hypothesisを作り、検査し、scopeを狭める。componentのmetrics、logs、request tracingを利用する。
- OpenTelemetry, *Observability Primer* / *Signals*：分散traceは実際のrequestが辿るservice間のpathをspan群で表す。metricsとlogsは別の証拠面を与える。

**重要な制限：** spanがない部分、samplingで欠けたrequest、instrumentation外のproxyは、traceから不存在と結論できない。metricsの相関も、原因の証明ではない。

## 固有操作と強い通常baselineの対応

| CSWが借りる操作 | 通常の障害調査がex anteに選ぶ操作 | 同じO1–O7での対象へ返す問い | 現時点の境界 |
| --- | --- | --- | --- |
| relative-route-model | traceから観測済みpartial request pathを復元する | P-Xはどのrequest/zoneで現れるか。観測していない区間は何か | 大きく重複。partial routeはOTelで自然 |
| cue-sequence-wayfinding | request/spanごとの時系列とconditional troubleshooting | retryが増える直前・直後のspan/eventは何か | 重複。stepwise diagnosisで再現 |
| model-environment-return | 静的architectureとruntime traceを照合する | 図では直結なのに、どの条件でP-X経由になるか | O4/O5が既に明示されており、通常側で自然 |
| disturbance-as-signal | latency、retry、zoneの異常相関を分けて診断する | spikeはzone/P-X/失敗requestに偏るか。成功例にもあるか | 重複。異常値を証拠手掛かりとして扱う |
| embodied-abstract-complementarity | design/runbookとlive telemetryを別の証拠として扱う | 図のモデルと実測が違う場合、どちらを何の根拠に使うか | 対象上は再現可能。ただし文化の身体的熟達とは同一でない |

「グラフがノードとエッジを描くだけである」という弱い比較では、強い差があるように見える。しかし**実務の普通手法はグラフ単独ではなく、観測、trace、時系列、仮説、照合、再試験を含む**。このbaselineにすると、既存正例の五操作はほぼ通常の障害調査で再現可能である。

## P-X仮説をどう取り扱うか

- traceでP-Xを通るrequestが一部に存在することはO5が支持する。
- P-Xが失敗の原因であることはO5/O6では決まらない。
- 成功requestにもP-Xが挟まるなら「P-Xの有無だけで失敗が決まる」という仮説が弱まる。
- sampling、request属性、zone、retry policy、時刻、service versionなどは追加確認事項であり、**与件に実在が証明された値ではない**。

この分析に航海知の由来を持ち込む必要はない。関連する問いが体系を利用して出せても、体系固有の発見とは数えない。

## 比較した範囲と比較していない範囲

- **実施したこと：** 同じ仮想O1–O7に対する、強い通常のSRE/OTel手法との机上での能力対応づけ。
- **未実施：** 異なるreviewerによる初回分析、独立したframework-contact実験、実装・ログでのP-X因果確認、実際の現場の波知覚との比較。
- **未判断：** runtime維持／降格、別の対象での潜在的な発見価値、文化体系の歴史的・実践的価値。

## 出典

- Google, *Site Reliability Engineering — Effective Troubleshooting*: https://sre.google/sre-book/effective-troubleshooting/
- Google SRE Workbook, *Monitoring*: https://sre.google/workbook/monitoring/
- OpenTelemetry, *Observability Primer*: https://opentelemetry.io/docs/concepts/observability-primer/
- OpenTelemetry, *Signals*: https://opentelemetry.io/docs/concepts/signals/
- Smithsonian Ocean, *Navigating the Waters with Micronesian Stick Charts*: https://ocean.si.edu/human-connections/history-cultures/navigating-waters-micronesian-stick-charts
- Genz (2016), *Resolving Ambivalence in Marshallese Navigation*: https://escholarship.org/uc/item/43h1d0d7

Stick chartをリアルタイムに読む縮尺地図と捉えず、公開資料で再現できない航海者の実践知・家族内知識を推測しない。CSWの抽象的な認知操作と航海文化を同一視しない。
