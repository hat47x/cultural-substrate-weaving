# Affinity Synthesis — Evaluation Cases

Status: research fixtures

このfixtureは「唯一の正解文」を固定するためではない。realizationを変更したとき、方法の不変条件が壊れていないかを比較するために使う。

各caseでは、最終テーマ名の一致より、**何を壊さなかったか**を評価する。

## Case 1 — 一つの体験を過剰分割しない

### Input

> 会議の前から胸が詰まる感じがしていた。開始後、説明を求められた瞬間に頭が真っ白になり、答えられない自分を見てさらに焦った。終わって席に戻ると、しばらく手が震えていた。

### Tempting failure

文ごと、出来事ごとに「胸が詰まる」「頭が真っ白」「焦る」「手が震える」の4カードへ機械分割する。

### Expected preservation

- 全体が一つの連続した体験・身体運動として意味を持つ可能性を検討する。
- 必要なら複数カードにできるが、長さや文数だけを理由に分けない。
- 身体感覚と出来事の時間的連続が失われない。

### Fail if

- 最小断片化が自動で行われる。
- 「会議不安」のような一般カテゴリだけへ置換され、具体的運動が消える。

## Case 2 — 観察と推論の継ぎ目を潰さない

### Input

A: 「担当者は説明中に三度資料を見直し、質問には『確認します』と答えた。」

B: 「担当者は内容を理解していなかったのだと思う。」

### Expected preservation

- Aは観察／報告された行動として扱える。
- BはAから伸ばした解釈・推論として区別する。
- 「担当者は理解していなかった」と一枚の事実カードへ統合しない。
- AとBの関係自体は保持してよい。

### Fail if

- 推論を確認済み事実へ格上げする。
- 逆に、推論であるという理由だけでBを捨てる。

## Case 3 — 派生物を独立反復として数えない

### Input lineage

- S1: 原資料「停電は14:05から14:37まで発生した」
- P1: S1を引用したSNS投稿
- C1: S1から作ったカード「32分間停電した」
- C2: P1を検索で見つけ、そこから再び作ったカード「32分間停電した」
- S2: 独立した監視ログ「14:05 DOWN / 14:37 UP」

### Expected preservation

- C1とC2を二つの独立支持として扱わない。
- P1はS1へのdiscovery routeになり得るが、転載しただけなら独立corroborationではない。
- S2は独立資料としてcorroborationに数え得る。

### Fail if

- 「同じ内容が三件あるから強いテーマ」と判断する。
- discovery routeとsource provenanceを同一視する。

## Case 4 — 強い表札で矛盾を洗い流さない

### Input cards

- C1: 「利用者は通知があると作業を思い出せると話した。」
- C2: 「別の利用者は通知が多いほどアプリを開かなくなると話した。」
- C3: 「通知をすべて切った利用者もいた。」

### Tempting label

「通知はユーザー体験に重要である」

### Expected preservation

- 上記表札は広すぎ、相反する作用を隠す可能性を指摘する。
- 一つの束に置く場合でも、通知が支援と回避の両方向に働く緊張を残す。
- 材料が別束を要求するなら分ける。

### Fail if

- 「通知の重要性」という抽象カテゴリで差を消す。
- 多数派／少数派だけで一方を削除する。

## Case 5 — 叙述が因果を発明しない

### Relational map input

- G1: 「締切直前に問い合わせが集中する」
- G2: 「回答担当者の残業が増える」
- G3: 「問い合わせテンプレートは任意利用である」

関係は、G1とG2が近接して観察されていることだけが支持されている。G3との関係は未確認。

### Tempting narrative

「テンプレートが任意であるため問い合わせが締切直前に集中し、その結果担当者の残業が増えている。」

### Expected preservation

- G1→G2の因果も、G3→G1の因果も、元材料が支持しないなら断定しない。
- 文章化で因果仮説が生じた場合は、未検証関係としてMapとsourceへ戻す。

### Fail if

- 読みやすい文章を作るために因果鎖を完成させる。

## Case 6 — 理由の分からない違和感を仮説へ強制しない

### Input

> 仕様書を何度読み直しても、この節だけ何か引っかかる。ただ、何がおかしいのかはまだ言葉にできない。

### Expected preservation

- 「理由はまだ分からないが、この節が気になる」という意味単位として残せる。
- すぐに「仕様矛盾がある」「セキュリティ上の問題がある」等へ仮説化しない。
- 後で別材料と接触したときに再開できる残差として扱える。

### Fail if

- 説明できないため削除する。
- もっともらしい原因を補って確定的カードにする。

## Case 7 — Map ↔ Narrative の差分を失敗と決めつけない

### Input

Map上ではG1とG2の間に直接リンクを置いていなかったが、叙述を書いている途中で「両者は同じ時期に制度変更の影響を受けているのではないか」という関係候補が生じた。

### Expected preservation

- Narrative側に新しい意味が生じたこと自体を禁止しない。
- その関係を「元材料が最初から語っていた」と書き換えない。
- sourceへ戻り、支持されればMapへ反映し、支持されなければhypothesis / unresolvedとして残す。

### Fail if

- 差分があるだけでNarrativeを削除する。
- 逆に差分を検査せず確定関係へ昇格させる。

## Case 8 — Affinity Mappingへ委譲できる近接タスク

### Input task

「この80件の自由記述を、創発的なテーマへまとめ、各テーマに代表コメントを付けてください。関係図や文章化は不要です。」

### Expected behavior

- `affinity-synthesis` 全体を実行する必要はないと判断できる。
- 導入済みの専用Affinity Mapping Skillがあれば、そちらへ委譲可能とする。
- 外部Skillがない場合でも、必要以上に関係図・叙述・複数ラウンドを増やさない。

### Fail if

- 自分の方法を使うこと自体を目的化し、不要な工程を強制する。

## Case 9 — 一枚が複数groupへ響いても複製しない

### Existing groups

G1:
> 身体が今受け取れる量を知る。

G2:
> 言葉や待つことが、切れた関係をもう一度通す。

### Input card

C1:
> 相手が長く話し終えるまで待ち、話し終わった後に温かい飲み物を運んだ。

### Expected handling

C1は、身体・生活量へ配慮するG1にも、話し終えるまで待つG2にも自然に響き得る。

必要なら、たとえば次のように扱う。

```text
C1
  primary placement → G2
  secondary resonance → G1
```

または材料全体のgeometryによって逆でもよい。

重要なのは、C1をC1a/C1bとして複製し、二つの独立supportにしないことである。

### Expected preservation

- 最も強い主配置を選べる。
- 別groupへの意味上の響きをcross-linkとして残せる。
- secondary resonanceがgroup size / frequency / corroboration countを増やさない。
- 一つの主配置へ決めきれない場合、その不確定性を残せる。

### Fail if

- 一枚を複製して独立した二カードとして数える。
- 一つのgroupへ置いた瞬間に、他groupとの関係を消す。
- 全カードを一意分類できたこと自体を成功基準にする。

## Cross-realization comparison

realization A/Bを比較する場合は、少なくとも次を記録する。

| Metric | A | B | Notes |
|---|---|---|---|
| source fidelity | | | |
| overfragmentation | | | |
| overcompression | | | |
| premature taxonomy | | | |
| epistemic seam preservation | | | |
| derivation double-counting | | | |
| singleton / conflict preservation | | | |
| multi-affinity without duplication | | | |
| invented causality / interior state | | | |
| provenance round-trip | | | |
| map ↔ narrative consistency | | | |
| unnecessary method activation | | | |

数値化が不自然な項目を無理に点数へしない。差分の性質を記述し、重大なinvariant violationが一つでもある場合は平均点で相殺しない。
