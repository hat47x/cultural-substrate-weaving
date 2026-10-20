# 独立初回レビュー：配布・回収・比較の引継ぎ

状態：実施準備。回答者の確保・配布・回収・独立性確認は**未実施**。既存の試験契約や判定基準を変更しない。

## 最初の対象

`tzolkin-coupled-schedules-target-v1.json` の架空の二つの定期処理（6時間・10時間）を使う。体系の歴史・day sign・期待される発見を伝えることはしない。周期とlatency spikeの関係は未検証であり、初回担当者が普通のscheduler・time-series手法を選ぶことを妨げない。

## 配布前に実施者が確認すること

1. 配布資料は元JSONではなく、`precontact_review_packet.py` が出力したMarkdownだけとする。配布前に体系名・研究用内部メタデータが含まれないことを人手でも確認する。
2. 担当者またはモデルの会話履歴に、対象の文化体系・比較文書・期待される問いが含まれていないかを確認する。確認不能な場合は「不明」と記録し、独立性を保証しない。
3. 配布したMarkdown、配布時刻、使用環境・モデル、担当者が申告した分析方法と接触歴を保存する。個人情報や秘密を公開repoへ書かない。
4. 初回回答は修正せず原文として保存する。後から追加質問・補足をした場合は、初回回答と区別して保存する。

## 配布用ファイルの生成

リポジトリルートから実行する。

```sh
python research/framework-candidates/scripts/precontact_review_packet.py \
  research/framework-candidates/trials/tzolkin-coupled-schedules-target-v1.json \
  --output /tmp/csw-coupled-schedules-unprimed.md
```

`/tmp/csw-coupled-schedules-unprimed.md` **だけ**を初回担当者に渡す。元JSONには `internal_research_context` がある。

## 初回回答を取得した後

原文を例えば非公開の `/path/to/unprimed-raw.md` に保存し、次を実行する。

```sh
python research/framework-candidates/scripts/record_trial_response.py \
  research/framework-candidates/trials/tzolkin-coupled-schedules-target-v1.json \
  /path/to/unprimed-raw.md \
  --phase unprimed-baseline \
  --method-as-reported "担当者が申告した最初の方法" \
  --exposure-as-reported unknown \
  --output /path/to/unprimed-provenance.json
```

`--exposure-as-reported` は実際の申告に応じて `unknown` / `reported-none` / `reported-prior-contact` から選ぶ。`reported-none` でも独立性が外部検証されたことにはならない。

体系接触後の回答を取得した場合に限り、同じ対象を `--phase framework-contact` で別途記録し、既存の `audit_trial_pair.py` に両原文・両記録を渡す。監査の `trace-complete` はSHAと記録の整合性だけを意味する。

## 事後の比較（未実施）

- **問いの同義性**：表現だけ異なる既出の問いを追加発見としない。
- **自然な通常手法**：初回回答にscheduler設定、offset、LCM、time-series分析が出ていれば、その事実を保持する。
- **新規性と対象支持**：体系接触後の問いが新しくても、ログ・仕様・測定等で検証できるかを別に扱う。
- **非活性化**：通常側で必要な問いが既に出ていれば、文化体系を使用しない判断を認める。
- **解釈の限界**：少数例・同一モデル・自己申告の接触歴・未検証の因果から、体系の一般的な効果や採用／降格を決定しない。

この文書の存在はレビュー回答の存在を意味しない。独立した回答を取得するまで `unreviewed_hypothesis` を維持する。
