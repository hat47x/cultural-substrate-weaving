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
