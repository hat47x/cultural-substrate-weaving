---
name: iterative-inquiry-synthesis
description: Orchestrates repeated inquiry rounds in which new material is synthesized, residual gaps and conflicts become explicit next questions, and later evidence is returned to the prior material state without overwriting history. Use for long-running research, analysis, or creative inquiry that needs repeated collect → synthesize → inspect residuals → recollect cycles. Do not use for a single synthesis round or as a domain-specific research method.
---

# Iterative Inquiry Synthesis

一回の統合結果を結論として固定せず、そこから現れた空白、対立、孤立、未解決、新しい材料を次の問いへ返す。

このSkillは**統合アルゴリズムそのものを所有しない**。各ラウンドの材料統合には、利用可能なら `affinity-synthesis` または同じMethod Definitionを満たす別realizationを使う。

## When to Use

- 調査・設計・創作・分析が複数回の資料追加を前提としている。
- 前回の統合から、次に確認すべきgap / conflict / singleton / unresolved questionが生じている。
- 新しい資料が届くたびに、既存構造を全部捨てず差分として再評価したい。
- 問いそのものが材料によって変化し得る。
- 長期作業で、何が変わり何が残ったかを追跡したい。

## When NOT to Use

- 一組の材料を一度だけ統合すれば足りる。
- 決められたデータセットへ同じ処理を再実行するだけで、問いや材料状態が変わらない。
- domain-specificな検索戦略、法的判断、医療判断、製品優先度等そのものが必要である。
- 「必ずNラウンド回す」こと自体が目的になっている。

## Core Round

各ラウンドでは次の外部成果物だけを扱う。private chain-of-thoughtを保存しない。

1. **Receive delta**
   - 新しい資料、観察、反証、実行結果、依頼条件の変更を受け取る。
2. **Reopen only what the delta touches**
   - 関係する旧カード、旧group、residual、unresolvedを前景へ戻す。
   - 長期履歴を毎回すべて再要約しない。
3. **State the current inquiry**
   - 今回何を確かめるroundかを一文で置く。
   - 前回の問いがそのまま妥当とは限らない。
4. **Run one synthesis realization**
   - 新材料と必要な旧材料を、一回の統合方法へ渡す。
   - 複数の統合方法を無自覚に混ぜない。使用realizationを記録する。
5. **Inspect structural delta**
   - 何が新しく生じたか。
   - 何が変わったか。
   - 何が変わらなかったか。
   - 何が消えたか。消えた理由は何か。
6. **Externalize residuals**
   - gap / conflict / singleton / unresolved / weakly-supported relationを明示する。
7. **Decide continuation boundary**
   - 次に確かめられる材料があるか。
   - 現在の目的に追加roundが必要か。
   - 人間の価値判断・domain decision・外部actionへ渡す段階か。
8. **Freeze a round snapshot**
   - 前roundを上書きせず、今回の差分と戻り先を残す。

## Round Contract

各roundで最低限追跡できるようにする。

- round id
- current inquiry / purpose
- input delta
- reopened prior artifact refs
- synthesis realization id or name
- output artifact refs
- residual refs
- structural delta
- possible next inquiry / verification target
- stop / continue reason

形式は固定しない。必要なら `references/ROUND-TEMPLATE.md` を使う。

## Do Not Rebuild Without Cause

新材料が来ただけで、既存の島・表札・関係を全面再構成しない。

まず問う。

- 新材料は既存の核を本当に変えるか。
- 既存groupへ局所追補できるか。
- 新しい独立した訴えが立ったか。
- 既存の対立を解いたか、むしろ深めたか。

既存構造がなお材料をよく表しているなら、その構造を保ったまま差分だけを追加できる。

## Residuals Are Reopenable Anchors

残差は未完成だから消すものではない。

- gap: 次に何を確かめればよいかを示す空所。
- conflict: 両立しない材料が残っていること。
- singleton: まだ他と結ばれない独立した訴え。
- unresolved: 現材料では判別できない問い。

現在の問いと関係しなければ背景へ置く。後の材料が触れたときにreopenする。

## Question Shift

問題解決型では、現状把握、問題提起、本質追及、構想、具体策、手順化、検証などの問いを使える。

ただし固定stage-gateにはしない。必要に応じて戻り、飛び、局所的に深掘りする。

問いが変わった場合は、以前のroundが誤りだったと自動判定しない。新材料によってinquiry frameが変わった出来事として記録する。

## Stop Conditions

完全な説明やgapゼロを完了条件にしない。

次のいずれかで停止できる。

- 追加roundが現在の問いに実質的な構造変化を生まなくなった。
- 残差はあるが、現在取得できる材料では解けない。
- 利用目的に必要な粒度へ到達した。
- 次に必要なのがdomain decision / human value judgment / external actionである。
- 追加探索の費用が、期待される認知上の改善を上回る。
- 外部利用条件が終了を要求する。

## Restart Conditions

- new source / observation
- counterexample
- environment change
- contact with an old residual
- explicit revisit
- a different cognitive field or framework exposes a new question

過去の停止を失敗扱いせず、触れた箇所だけを再開する。

## External Exploration Routes

文化体系、web research、domain skill、human interview、experimentなどは、次roundの材料や問いを得る**外部探索経路**として利用できる。

それぞれが出した仮説やcorrespondenceを、独立した観察事実へ自動昇格させない。

特に `cultural-substrate-weaving` を使う場合、文化体系から得た問い・対応候補は、その由来を保ったまま対象材料へ返す。

## Quality Checklist

- [ ] round数を目的化していない。
- [ ] 前roundを上書きせず、差分として追跡できる。
- [ ] 新材料が触れない部分まで無理由に再構成していない。
- [ ] 使用したsynthesis realizationを追跡できる。
- [ ] gap / conflict / singleton / unresolvedを次の観察事実と混同していない。
- [ ] question shiftを失敗または進捗点数へ単純変換していない。
- [ ] stop理由が外部から説明可能である。
- [ ] private chain-of-thoughtではなく外部成果物を保存している。

## Progressive References

- 標準round記録: `references/ROUND-TEMPLATE.md`
- Layer 1との境界: sibling prototype `../affinity-synthesis/`

## Boundary

このSkillは、何が真実か、どの意思決定を採るべきか、どのactionを実行すべきかを自動決定しない。

役割は、**問いと材料と統合結果の履歴を壊さず、必要なときに次の認知roundへ接続すること**である。
