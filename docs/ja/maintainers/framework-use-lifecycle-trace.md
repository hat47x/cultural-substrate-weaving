# framework use lifecycle trace

- Status: Research observation template / no runtime rule change
- Date: 2026-08-30
- Related: `framework-loading-depth-observation.md`, `kj-atlas-case001-longitudinal-companion.md`, `v39-deepseek-api-validation.md`

## 目的

文化体系について、**候補に上がったこと、資料を読んだこと、体系固有の操作を使ったこと、対象側の成果へ採用されたこと**を別々に記録する。

これらを同じ「frameworkを使った」にまとめると、次の区別が失われる。

- 候補には上がったが、不採用条件によって読む前に棄却した。
- 詳細を読んだが、対象側の増分が無く操作しなかった。
- 操作は試したが、forcingや不適合を検出して対象側へ採用しなかった。
- framework由来の問いが、後の資料で対象側の所見として残った。

このtraceは実行手順ではない。`candidate → loaded → operated → adopted`を必須の段階として進ませるものではなく、**実際に何が起きたかを後から混同しないための来歴**である。

## 記録単位

一つのframework候補について、観察上意味がある場合だけ一行または短いブロックを残す。候補を大量列挙することを目的にしない。

### `candidate`

その体系が候補に上がった理由を対象側の言葉で残す。

- 対象のどの問い・空白・関係に反応したか。
- 明示指定か、探索中に自然に候補化したか。
- 不採用条件をどこに置いたか。

候補に上がっただけなら、ここで止めてよい。

### `loaded`

実際にworking contextへ入れた範囲を残す。

- `none`
- `selection_only`
- `application_rule`
- `framework_detail`
- `multiple_frameworks`

可能なら参照した資料・ファイル・外部sourceを記す。`framework-loading-depth-observation.md`の定義を使う。

### `operated`

体系固有の操作を実際に行ったかを残す。

- `none`
- 操作名または短い説明
- 何を対象材料として操作したか
- 途中で止めた場合はその理由

資料を読んだだけなら`none`でよい。操作しなかったことを欠落として扱わない。

### `adopted`

frameworkを外した後にも対象側へ残ったものだけを記録する。

例:

- 新しい問い
- 新しい調査先
- 関係候補
- 反証条件
- KJ再編
- 設計・文章・判断への実採用

何も残らなければ`none`とする。framework内部の説明が増えただけなら採用に数えない。

### `stop_reason`

途中で深めなかった、または採用しなかった理由を短く残す。

例:

- 不採用条件に該当した。
- 同種性を確保できなかった。
- baselineとの差分が無かった。
- 詳細loading後にframework語彙だけが増えた。
- forcing / provenance loss / target distortionを検出した。
- 現在の問いには浅い利用で十分だった。

## 短い記録例

```text
framework: 五行
candidate: 自己改善loopの「促進」と「抑制」を別の関係動詞で見る候補として浮上
loaded: selection_only
operated: none
adopted: feedback loopの抑制側を確認する調査問い
stop_reason: 分類器としての同種性がないため詳細対応へ進まない
```

```text
framework: 易
candidate: 状態遷移の不在を検査できる可能性
loaded: application_rule
operated: none
adopted: none
stop_reason: 独立した割当規約を用意できず、遷移試行へ進めない
```

## 長期ラウンドでの読み方

このtraceを即時の成功率へ集計しない。

後のラウンドで見るのは、たとえば次である。

- `candidate`だけ残した問いが後の資料で再活性化したか。
- `loaded`を深くしたことでanchoringが長く残らなかったか。
- `operated`した内容のうち、対象へ戻した後にも何が残ったか。
- `adopted`した所見が実成果へ移ったか、後から撤回・再編されたか。
- `stop_reason`が別ケースでも再現し、routing改善に使えるか。

## KJ Atlas Case 001での扱い

独立A〜D比較のarmや処置を増やさない。

B/Dで文化体系を扱った場合、必要ならこのtraceを**実験者側の補助来歴**として残す。blind reviewerへは、armやframeworkを推測させる情報を渡さない。

Case 001の独立B/Dは事前登録済みのskill snapshotに固定されている。新しいCSW文書やこのtraceをarmのmodel/operator inputへ追加しない。**run出力と既存run recordを固定した後に、既に残っている記録から実験者が補助traceを作る。** traceを書くために追加質問、追加framework探索、再実行を行わない。これにより、現在の方法論改善が凍結済み比較条件へ逆流することを防ぐ。

長期companion laneでは、`framework_use`だけでは区別が不足する重要ラウンドに限ってこのtraceを添える。こちらは独立A〜Dとは別のprospective観察であり、使用した`method_ref`を記録する。

## 方法論正本への昇格条件

このtrace自体は研究用記録であり、`src/<locale>/`のruntime規則ではない。

複数の異なる実課題で、たとえば

- 候補化だけで十分な問いが繰り返し得られる。
- 詳細loading後のanchoringが繰り返し問題になる。
- operationを省いた方が対象固有性を保てる。
- 特定のstop reasonが再現し、現行routingでは防げない。

といった所見が出た場合にだけ、最小のruntime変更を検討する。

## 現時点の判定

現段階で必要なのは、framework利用を新しい固定階層へ変えることではない。

> **候補化・読み込み・操作・採用を別々に観察し、どこで有用な増分が生まれ、どこでforcingやanchoringが生じたかを長期的に追えるようにする。**

この区別を保ったまま実データを蓄積し、規則化は後から行う。
