# Marshallese wave navigation — 接触前の方法選択と発見価値

状態：2026-10-17の定性的な机上検討。独立した無接触レビュー、盲検、ログ実測、採用判断は未実施。

## 検証する仮説

「普通の分析は地図を完成させ、ずれを雑音として扱う」という想定だけでは、[既存の正例](../worked-examples/marshallese-wave-navigation.md)の発見価値を示せない。対象はすでにservice handoff、retryの振動、live traceと静的トポロジーのずれ、zone別のlatency差を含んでいる。

**区別する二つの問い：**

1. **能力の重複**：Marshallese wave navigationの抽象操作に接触した後、通常のSRE/observabilityでも同じ問いを再現できるか。
2. **発見への寄与**：体系に触れる**前**の普通の依頼を受け、担当者がその分析方法と問いを自然に選ぶか。

[能力比較](marshallese-vs-ordinary-observability.md)では、通常手法との重複が広いことを示した。以下はその手法の事前選択を検討する。

## 経路A：障害調査という自然な入口

体系や「航海」の語彙を与えない初回依頼：

> queue Q-Aに続くservice S-Bでretryが振動する。静的構成図ではS-B→S-Cだが、一部のlive tracesではP-Xが挟まり、特定zoneでlatencyが大きい。原因は未確定。最初に何を調べますか。

この情報なら、普通のSRE担当者はmetrics/logs/distributed tracing、requestごとの経路比較、成功・失敗群での差、計測欠落の確認、設計図とruntime実態の差分、仮説検査を選べる。

したがって、この対象では「通常の入口なら必ずglobal mapしか見ない」「disturbanceをただ捨てる」という**弱く構成した対照は採用しない**。通常の入口から同じ認知仕事へ至る可能性は高い。これは実測した頻度ではなく、標準のSRE手法と対象条件に基づく机上判断である。

## 経路B：文化体系への接触

Smithsonianの公開資料では、stick chartsは航海中に逐次読むliteral mapではなく、陸上で学習・記憶する模型として説明される。Genz (2016)は複数の航海知の学派、実践の中で必要な情報を選択すること、研究者・当事者の解釈にある不確実性を扱う。

CSWが借りる、(a) 教材モデルと現場観察を混同しない、(b) 局所的cueを順に追う、(c) disturbanceを情報候補として扱う、という操作は、対象側では次の問いになる。

- 静的図のS-B→S-Cと、traceに現れるP-X経由が異なる条件は何か。
- retry/latency振動はservice境界、zone、request属性ごとにどう異なるか。
- 既存モデルが無い区間を、根拠のあるlocal tracesだけでどこまで記述できるか。

ただしこれらは**もともと普通の障害調査から選べる問い**でもあり、接触後に思い付いたという事実だけで「固有の発見」とは数えない。

## 第二の構成例でも通常の入口を弱くしない

[別の正例](../worked-examples/marshallese-wave-navigation-non-navigation.md)は、runbookの期待checkpointとlive telemetryのずれを扱うdeploymentである。ここでも普通のrelease readiness、runbook-vs-actual確認、段階的なcanary観察やrollback判断は自然な入口に入る。体系接触による追加発見の実証はまだない。

## 表に残す判定

| 対象側の問い | 初回から自然に選ばれる専門手法 | 体系接触後の作用 | 現時点の扱い |
| --- | --- | --- | --- |
| 一部requestでP-Xを通る経路 | distributed tracing | relative-route | 重複が強い |
| retryの順序と次の調査点 | SRE hypothesis / trace timeline | cue-sequence | 重複が強い |
| static topologyとlive routeの差 | runtime trace vs design diff | model/environment return | すでに与件で差が明示 |
| latencyやretryの乱れを手掛かりへ | metrics correlation / isolation | disturbance-as-signal | 通常分析でも自然 |
| 計測の穴がある部分の保留 | observability/sampling gap review | abstract/situated complementarity | 体系固有と判定できない |

この結果は**能力面の重複に加え、初回選択でも重複する可能性が大きい**という厳しい見通しを示す。ただし独立した初回回答を得ていないため、実測したdiscovery overlapや正式なruntime降格決定ではない。

## 発見価値を保留したまま再検討できる条件

将来の別対象については、原文を固定した無接触レビューが、普通の方法を自然に選びながらも、ある特定の**事前の模型・局所cue・状況からの再観測の断絶**を見落としたか、対象側に証拠を戻して比較する余地がある。

しかし、後から「普通の分析者は見ないはず」と仕立てた課題や、体系から生成した回答を元の依頼に埋め込む課題は、発見価値の検証に使えない。仮想例の問いが具体的でも、対象側の実装・測定値・行動観察は別に要る。

**非活性化条件：** 通常のtracing/SRE、telemetry-vs-runbook、checkpoints、conditional diagnosisが同じ問いを最初から立てている場合。[負例](../worked-examples/marshallese-wave-navigation-negative-boundary.md)を参照。

## 文化・出典の境界

Smithsonianの一般向け説明を、すべての家族・航海学校に共通する航法文法とは扱わない。Genzの研究には相違する波の説明、現場で用いる情報の選択性が含まれる。「局所的な手掛かり」の抽象化はCSW自身の設計操作であり、当事者の実際の航海技能を再現しない。実際の海上航行や安全判断への使用も不可。

出典：
- Smithsonian Ocean: https://ocean.si.edu/human-connections/history-cultures/navigating-waters-micronesian-stick-charts
- Genz, *Resolving Ambivalence in Marshallese Navigation* (2016): https://escholarship.org/uc/item/43h1d0d7
- Google SRE, *Effective Troubleshooting*: https://sre.google/sre-book/effective-troubleshooting/
- OpenTelemetry, *Observability Primer*: https://opentelemetry.io/docs/concepts/observability-primer/
- Google SRE Workbook, *Monitoring*: https://sre.google/workbook/monitoring/

**結果：** `readiness: adopted` と `discovery_hypothesis.evidence_state: unreviewed_hypothesis` を変更するには至らない。現段階の成果は、弱い「グラフだけ」比較から実務で自然なSRE比較へ、検証仮説を厳格化したことである。
