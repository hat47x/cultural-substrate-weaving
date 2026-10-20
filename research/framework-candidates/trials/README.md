# 初回レビュー用の固定入力

状態：入力と手順のみ準備済み。独立レビュー、実際の業務検証、効果判定は未実施。

## 目的

Llull後期Arsに由来する体系的な問いの生成が、体系との接触前の通常の要件レビューに比べ、新しい問いを生むか検討する。そのため、体系名を提示しない初回レビューの原記録を、後の比較と区別して保管する。

## 入力と生成

- `requirements-review-target-v1.json`：仮想業務システムの対象条件。研究用の内部情報を含むため、レビューの配布には使わない。
- `reviewer-packet-v1.md`：通常の要件レビュー用に生成した依頼文。研究体系の名称や期待される答えは含めない。
- `../scripts/precontact_review_packet.py`：元入力のレビュー用項目だけから依頼文を生成し、可視入力のSHA-256を付ける。分析・採点はしない。

再生成コマンド：

```sh
python research/framework-candidates/scripts/precontact_review_packet.py research/framework-candidates/trials/requirements-review-target-v1.json --output /tmp/reviewer-packet-v1.md
```

レビュー担当には配布用依頼文のみを渡す。元JSONの研究情報、既存のLlull比較資料、期待される質問は先に提示しない。この措置だけでは、担当者や使用モデルが既に持つ知識を消去できず、独立性を保証しない。

## 結果を取得するときに記録する欄

| 段階 | 記録 |
| --- | --- |
| 通常レビューの前 | 配布入力のSHA-256、実施日時、レビュー環境、既知の研究文脈 |
| 通常レビュー | 最初に選んだ分析方法と理由、質問の原文、追加資料が必要な点 |
| 体系接触 | 同じ対象から追加で出た候補、由来、通常側との重複、使わない判断 |
| 対象へ戻す | 仕様・試験等の根拠、支持・反証・未確認・構造上不可能の別 |
| 事後の比較 | 通常の専門手法での再現可能性と、初回にその手法が自然に選ばれたかを別々に記録 |

この段階では結果欄を埋めない。元の初回質問を後から書き換えない。問いの数、組合せの網羅、資料ファイルの存在だけで発見効果や体系の採用可否を判定しない。

参照：[Llullと通常の組合せ分析](../comparisons/llull-ars-vs-ordinary-combinatorial-review.md)、[Llullの発見価値の検討](../comparisons/llull-ars-discovery-value.md)。

## 初回回答を受け取った場合の記録

回答の原文は、書き換えず別ファイルへ保存する。回答が存在しない現時点では、実施記録を作成しない。

`../scripts/record_trial_response.py` は、元入力の可視項目の指紋、回答本文のSHA-256、回答ファイルの場所、回答者が申告した方法と事前接触状況を**未評価の原記録**としてJSON化する。回答本文はメタデータへ複製しない。

```sh
python research/framework-candidates/scripts/record_trial_response.py \
  research/framework-candidates/trials/requirements-review-target-v1.json \
  /path/to/raw-response.md \
  --phase unprimed-baseline \
  --method-as-reported "回答者が最初に選んだ方法" \
  --exposure-as-reported unknown \
  --output /path/to/response-provenance.json
```

`--phase framework-contact` は体系接触後の回答を別に記録する場合に用いる。回答者が「体系を知らなかった」と申告しても、それは第三者による独立性確認ではない。作成される `status: raw-response-captured-unassessed` は、発見、正確性、実務有効性、体系の採用判断を示さない。

回答原文に機密情報・個人情報が含まれる場合は、公開リポジトリに保存しない。公開可能な検証用材料と、アクセス管理を要する実務証拠を区別する。

## 既存評価との関係

`research/efficacy-cheap-llm/` には、体系なしの比較条件（B0）を含む以前の合成課題研究がある。ただし、その課題、依頼文、比較設定は本試行と異なる。以前のB0結果をこの固定入力に対する独立レビュー結果として転用しない。以前の研究で観測した、体系選択の偏りや根拠のない構造の強制を検討する材料として参照するにとどめる。

## 二経路の記録整合性を点検する（回答取得後のみ）

通常レビューと体系接触後の回答を取得したら、両方の原文ファイルおよび `record_trial_response.py` の記録JSONを指定して、`audit_trial_pair.py` を実行できる。

```sh
python research/framework-candidates/scripts/audit_trial_pair.py \
  --target research/framework-candidates/trials/requirements-review-target-v1.json \
  --baseline-record /path/to/baseline-provenance.json \
  --baseline-response /path/to/baseline-raw.md \
  --contact-record /path/to/contact-provenance.json \
  --contact-response /path/to/contact-raw.md \
  --output /path/to/pair-audit.json
```

この読み取り専用監査は、二つの回答が同じ固定入力を指し、記録された段階と生データのSHA-256が一致するかを確認する。対象の変更、段階の取り違え、回答バイト列の変更、報告方法の欠落を個別に表示する。また、通常レビューで体系への事前接触を申告している場合、接触歴が不明な場合、同一回答が両経路に使われている場合は注意として表示する。

`trace-complete` は**記録上の整合性が取れた**という意味に限る。盲検、別担当による独立性、実施順序、実際の発見、ターゲット側の裏付けは保証しない。回答の質問が同義か、体系接触後に本質的な認知作業が増えたかは、原文と対象資料を別途比較する。

本監査のテストは合成回答のみで実施する。現時点でレビュー回答そのものは存在しないため、`pair-audit.json` や判定結果を仮作成して実証済みとは記載しない。

## Marshallese wave navigation：独立した通常レビューの入力

[従来の分散処理障害の正例](../worked-examples/marshallese-wave-navigation.md)のO1–O7をそのまま含む、別対象の[固定入力](marshallese-observability-target-v1.json)を追加した。初回分析の対象にはSREのtrace・retry・zone情報が初めから含まれる。通常手法を不自然に弱めるために観測情報を削除しない。

この入力JSONには研究上の内部情報を含むため、レビュー担当には**生成したMarkdownだけ**を渡す。次のコマンドで生成する。

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/marshallese-observability-target-v1.json \
  --output /tmp/marshallese-initial-review.md
```

結果を取得した場合は、元回答の生バイト列を `record_trial_response.py` で保存し、同じ入力の体系接触後の回答と `audit_trial_pair.py` で照合できる。ここに示すコマンドは**試験を実施したという記録ではない**。

初回にOpenTelemetry、distributed tracing、SRE troubleshootingを自然に選んで同じ問いを出した場合には、その重複を削らず記録する。体系接触後にできた問いの数だけで発見の優劣を決めない。[通常手法との机上比較](../comparisons/marshallese-vs-ordinary-observability.md)および[発見仮説](../comparisons/marshallese-discovery-value.md)を参照する。

## Sāṅkhya：成功率ダッシュボードの初回レビュー入力

[生成層・観測者の仮想事例](../worked-examples/sankhya-layer-observer.md)のO1–O6を固定した、[入力JSON](sankhya-dashboard-target-v1.json)を追加した。内部には体系を識別できる研究メタデータがあるため、**JSONをそのまま無接触レビューの担当者へ渡さない**。

既存の共通生成器で、表示対象の項目だけを使った配布用Markdownを生成する：

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/sankhya-dashboard-target-v1.json \
  --output /tmp/sankhya-initial-review.md
```

部署別表示差、分類設定変更、event→集計→filterの系列は与件として保持する。通常レビューから情報を削り、体系がないと分からない課題へ作り替えてはいけない。

回答が取得された場合のみ、原文のバイト列を `record_trial_response.py` で記録し、同じ入力条件の別レビューと `audit_trial_pair.py` で追跡する。これらのツールは独立性や発見の有効性を証明しない。**現時点でSāṅkhya対象の初回レビュー回答は未取得**。

関連：[通常のdata lineageとの比較](../comparisons/sankhya-vs-ordinary-data-lineage-review.md)、[発見価値の机上検討](../comparisons/sankhya-discovery-value.md)。

## Rasa：保存失敗画面の通常UXレビュー

[元のRasa構成例](../worked-examples/rasa-expression-reception.md)にある、大量明細を入力した直後の赤い保存失敗画面・エラー文言・唯一のOKボタンをそのまま使い、[固定入力](rasa-save-error-target-v1.json)を追加した。画面内容や利用者の反応が不明である部分を補わず、普通のUXレビューに同じ情報を与える。

内部JSONには研究体系を識別できる非配布メタデータが含まれる。初回レビュー担当には、次の生成器で可視項目だけを書き出したMarkdownを渡す。

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/rasa-save-error-target-v1.json \
  --output /tmp/rasa-initial-review.md
```

初回の担当者が通常のエラー回復・画面設計・利用者調査を選び、Rasa接触時と同じ問いを既に挙げた場合はそのまま記録する。本人が感情を報告していない限り、体験・困惑・不快感を観測事実としない。

回答が取得された場合は、元の回答バイト列と実施条件を既存の `record_trial_response.py` で保持し、同一入力を使った後続の体系接触後の出力と `audit_trial_pair.py` で整合性を点検する。**この文書は独立レビュー実施報告ではない**。

参照：[通常のUIレビューとの能力比較](../comparisons/rasa-vs-ordinary-ui-review.md)、[体系接触前の発見価値](../comparisons/rasa-discovery-value.md)。

## 易経：二経路の状態遷移レビュー

[6位置の仮想移行例](../worked-examples/yijing-positioned-transition.md)を同一の対象として使う[固定入力](yijing-two-path-rollout-target-v1.json)を追加した。位置3→4と4→3では最終構成が一致しても中間状態が異なること、実システムの安全性は未確認であることを与件に明記している。

内部JSONの `internal_research_context` にある文化体系名や期待される発見は、初回担当者へ渡さない。共通のpacket生成器で、依頼文に必要な項目だけ出力する：

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/yijing-two-path-rollout-target-v1.json \
  --output /tmp/yijing-initial-review.md
```

**固定された2bitの反転順序が可換であること**と、データ移行操作・状態遷移・rollbackに副作用があるかを混同しない。通常レビュー担当が最初からstate-transition testing、状態機械、feature flagの依存確認を選んだ場合、同じ問いをそのまま初回記録へ残す。後から回答を編集して易経固有の発見を作らない。

独立した回答を実際に取得した場合のみ、既存の回答原文保存と二経路の整合性監査を適用する。入力の準備は盲検成立・効果測定の実施とは異なる。

関連：[通常の状態遷移テストとの比較](../comparisons/yijing-vs-ordinary-state-transition-review.md)、[体系接触前の発見価値](../comparisons/yijing-discovery-value.md)。

## Maya calendars：二つの定期処理の初回レビュー

[6時間周期と10時間周期の構成例](../worked-examples/tzolkin-coupled-cycle.md)を同一条件で使う[固定入力](tzolkin-coupled-schedules-target-v1.json)を追加した。通常側にもA/Bの周期、t=30での再同時実行、因果未確認という情報を同じように与える。

元JSONの `internal_research_context` には研究体系の識別情報があるため、初回レビュー担当へJSONそのものを渡さない。共通生成器で可視項目だけを出力する：

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/tzolkin-coupled-schedules-target-v1.json \
  --output /tmp/tzolkin-initial-review.md
```

初回担当がscheduler設定、LCM、offset、time-series seasonalityを自然に選ぶ場合、その事実を後から弱めない。「片方の周期だけ戻ること」と「複合位相が戻ること」を普通の分析ですでに区別できていれば、Maya calendar接触後の同じ問いを追加発見と数えない。

同じschedule位相が戻っても、release version、queue、traffic等が同一とは限らない。時刻の一致を因果や「完全に同じ状況」の証拠にしない。

回答を実際に取得した場合のみ、既存の `record_trial_response.py` と `audit_trial_pair.py` で原文・入力指紋・段階を記録する。**現時点では独立した初回回答は未取得**。

関連：[通常の周期分析との比較](../comparisons/tzolkin-vs-ordinary-periodicity-review.md)、[接触前の発見価値](../comparisons/tzolkin-discovery-value.md)。
