# Sāṅkhyaと通常のdata lineage / SRE observabilityの能力比較

Status: 同一の架空対象に対する机上比較。独立レビュー、実DB/ログ検証、runtime採否判断ではない。

## 固定対象と強い通常baseline

[注文成功率の表示低下という固定対象](../worked-examples/sankhya-layer-observer.md)のO1–O6を、Sāṅkhya側と通常手法側へ同じように与える。業務成功率の低下はUI上の観測であり、実トランザクション成功率の低下や分類器変更の因果は未確認。

**文化体系名を出さない初回の依頼**：「10:00の設定変更後に部署別ダッシュボードで成功率が低下している。gateway countersは同じ傾向を示さない。成功率がどの処理で算出され、実処理の変化を表すか調べてください。」

この依頼から自然に選ばれる専門技法は、metric definition監査、event-to-dashboard data lineage、ETL/aggregationの変換検査、filter/permissionの点検、productionのlogs/traces/metrics照合、および時刻をそろえた前後比較である。

OpenTelemetryのobservabilityはtraces/metrics/logsを異なる観測信号として扱い、測定値を実態の説明そのものと同一視しない。Google SREのtroubleshootingは、症状を集め、仮説の区別と検査を行う。この通常の仕事に、古典哲学の構造を前提とする必要はない。

## 操作ごとの比較

| CSWのde-bound操作 | 通常手法で自然に行うこと | 対象O1–O6での問い | 能力面の結論 |
| --- | --- | --- | --- |
| layer-backtracking | data lineage: metric→集計→分類→正規化→event→実処理 | どの段階で成功の定義や分母が変わるか | 大きく重複 |
| production-tree | transform graphと依存・入力出力契約 | 表示値はどの版のSQL、filter、定義に依存するか | 大きく重複 |
| observer-process-split | 観測指標とbusiness transactionを区別し、閲覧者filterを確認 | 部署A/Bは同じ対象と時刻を測っているか | 大きく重複 |
| mixture-view | 複数要因仮説・欠損/定義/実処理の切分け | 何が独立に計測・反証できるか | 対象変数がなければ撤回、三guṇaの固定対応をしない |
| upstream-inversion | RCAで「症状」や「原因候補」自身の上流依存を追跡 | 10:00の分類変更は処理結果の変化か測定系の変化か | 大きく重複 |

単に「現れた指標の層だけを見る」という弱いordinary baselineを作らない。O3で観測値の生成系列が明示され、O4で分類設定変更が明示されている以上、普通の調査は**初めから**その系列とmetric definitionを点検できる。

## 機能面と発見面を混同しない

この文書が示すのは、**強い通常手法が同じ対象へ返す問いを再現できる**という能力上の重複である。通常手法が歴史上のSāṅkhyaのpurūṣa/prakṛtiと等価だとは主張しない。

また「同じ問いを後から専門技法で作れる」だけなら発見価値は未決である。しかし今回は指標とETLという対象設定そのものが自然な専門技法を選ばせるため、**体系接触前に同じ問いを開ける可能性が高い**。これは今のところ文献・設計に基づく分析者の推論であって、別担当者の初回回答を観測した結果ではない。詳細は[発見価値の検討](sankhya-discovery-value.md)。

## 出典と文化的境界

- Internet Encyclopedia of Philosophy, *Sankhya*: https://iep.utm.edu/sankhya/
- Īśvarakṛṣṇa, *Sāṃkhyakārikā* (GRETIL): https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_IzvarakRSNa-sAMkhyakArikA-alt.htm
- Google SRE, *Effective Troubleshooting*: https://sre.google/sre-book/effective-troubleshooting/
- OpenTelemetry, *Observability Primer*: https://opentelemetry.io/docs/concepts/observability-primer/

IEPの記述する観照者と生成自然の区別、25のtattva、guṇaは対象事実ではない。抽象した問いを使えても、古典的な因果・認識・解脱の理論をソフトウェアの設計標準や権威として持ち込まない。

**結論：** 同じ架空の対象では通常手法との能力重複が大きい。採用状態は変更せず、独立の無接触レビューと対象記録の照合が未取得であることを保持する。
