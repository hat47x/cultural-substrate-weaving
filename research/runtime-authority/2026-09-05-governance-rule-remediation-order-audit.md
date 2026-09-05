# 規則過剰時の固定修正順序監査

日付: 2026-09-05
対象: `src/ja-JP/governance/governance-and-records.md` / `src/en-US/governance/governance-and-records.md`

## 対象規則

現行末尾には次の順序規則がある。

> 規則が過剰に作用する場合は、適用条件を狭める、優先順位を下げる、補助扱いへ移す、機能を確認したうえで削除する、という順で調整する。動的材料を減らすことで、規則整理の代わりにしない。

英語版:

> When rules become overactive, narrow their conditions, lower their priority, move them to auxiliary status, then remove them if their function cannot be shown. Do not use deletion of dynamic material as a substitute for rule maintenance.

問題は、四つの修正手段そのものではなく、それらを常にこの順番で適用する根拠があるかである。

## 履歴

### v0.1.0 初回公開

`cd580449e942e7b80786dd70eb9c963f41287296` の初回公開時点から、既に次の4段階リストが存在した。

1. 適用条件を狭める。
2. 優先順位を下げる。
3. 補助パターンへ移す。
4. 担っていた機能を確認したうえで削除する。

初回コミットは方法論全体の公開であり、この順序を比較・測定した記録や外部典拠は示していない。

### 2026-08-09

`2b39432ae98fd0fae6a5f2a000dea1138850dd5f` は、判断起源・保持事項・採否状態・重複計上の扱いを governance に追加した。同コミットの実測は framework removal check に関するもので、規則修正の4段階順序は既存文として残っただけである。

### 2026-08-23

`3988e12e5f7f316f377d3391e9486c8467a111d5` はスキルを二つの核心能力へ縮約した。この際、4項目の箇条書きを

> 適用条件を狭める、優先順位を下げる、補助扱いへ移す、機能を確認して削除する、の順で調整する。

という一文へ圧縮した。意味は維持され、順序の有効性は新たに検証されていない。

後続の governance 改定は、観測と評価の分離、判断主体と根拠、event記録などを強化したが、この4段階順序を比較した測定は確認できない。

## 分離すべきもの

### 保持する

- 規則の過剰作用を検出・記録できること。
- 適用条件の限定、優先順位調整、補助扱いへの移行、削除という修正手段を利用できること。
- 削除を選ぶ場合、規則が担っていた機能を確認すること。
- 動的材料を削ることで静的規則の整理を代替しないこと。

### 固定しない

- 四つの修正手段を常に同じ順序で試すこと。
- 前段を実施しない限り次段へ進めないこと。
- 「削除は最後」という順序それ自体を成功条件にすること。

例えば、局所条件だけが誤っていれば条件限定が適切であり得る一方、規則自体の機能が失われているなら、優先順位変更や補助化を経由することに独立した価値は確認されていない。

## runtime改定案

JA:

> 規則が過剰に作用する場合は、その原因と利用条件に応じて、適用条件の限定、優先順位の調整、補助扱いへの移行、削除を選べる。削除する場合は、担っていた機能を確認する。動的材料を減らすことで、規則整理の代わりにしない。

EN:

> When rules become overactive, choose among narrowing their conditions, changing their priority, moving them to auxiliary status, or removing them according to the cause and use conditions. Before removal, identify the function the rule carried. Do not use deletion of dynamic material as a substitute for rule maintenance.

この変更は修正手段を失わせず、未検証の固定順序だけを外す。

## 非目標

- 規則の過剰作用を放置すること。
- 動的材料保護を弱めること。
- 規則削除を自動化すること。
- 新しい固定回数、固定閾値、修正アルゴリズムを追加すること。
