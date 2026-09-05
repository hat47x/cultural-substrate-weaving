# 外部化閾値に残る決定権の監査

## 目的

`methods/scope-and-facts.md` には、収集段階と外部化段階の閾値を分ける重要な原則とともに、次の文が残っている。

> 外部化するときに別の責任検査を通す。

英語では `Apply a separate responsibility check before publication or execution.` である。

収集段階で弱い信号を消さないことと、公開・実行の閾値をSkill自身が決めることを分離する。

## 導入履歴

### 10205bb3 — collection threshold ≠ publishing threshold

この原則は、生成AI側の抑制が入口へ移り、後から意味を持つ弱い信号を捨てる問題への対抗として導入された。

コミット説明は次を明示する。

- collecting threshold is not the publishing threshold
- checks applied at the door discard weak signals that only pay off later
- five additions in this commit loosen rather than restrain

当時の英語本文は、弱い材料を来歴・不確実性付きで収集側に残し、外へ出す途中で `pass a separate check on the way out` としていた。

この導入目的は、**外部化のための抑制を収集段階へ逆流させないこと**である。普遍的な「責任検査」の内容や、その判断主体をSkillへ与えることは実測・定義されていない。

## PR #193以降の決定権境界

PR #193では、次の決定権をSkill静的規則から外した。

- 利用範囲
- 読み込み深度
- 停止
- 採用
- 公開
- 関連する価値判断

決定権の出所は、依頼者・著者、上位利用条件、または実行AIへ明示的に委任された裁量である。

この境界から見ると、「別の責任検査を通す」は二つの読みを許してしまう。

1. 外部化には領域・利用条件に応じた別の閾値がある、という正しい区別。
2. CSW自身が未定義の責任検査を必須ゲートとして課す、という過剰な読み。

後者を避ける必要がある。

## 守るもの

1. 収集段階と外部化段階の閾値を同一にしない。
2. 低確度の証言、理由の言えない違和感、複数成り立つ説明を、来歴・留保付きで研究/KJ材料として保持できる。
3. 収集したこと自体を、公開・実行してよいという判断へ変換しない。
4. 公開・実行側では、その領域に必要な正確性・責任・品質基準を適用できる。

## 再配置するもの

外部化の閾値と責任をCSW固有の未定義検査として持たせない。

代わりに、

- 領域固有の基準
- 依頼者・著者や上位の外部利用条件
- 実行AIへ明示的に委任された裁量

へ返す。

これにより、`collection threshold ≠ externalization threshold` の原意を保ちながら、公開・実行の決定権をSkillへ逆輸入しない。

## runtime改定方針

現在の

> 外部化するときに別の責任検査を通す。

を、

> 外部化の閾値と責任は、領域基準・外部条件・委任裁量に従う。

相当へ変更する。

英語も `Publication or execution thresholds follow domain criteria, external conditions, or delegated discretion.` 相当へ揃える。

新しい固定ゲート、責任観、公開基準は追加しない。

## 結論

残すべきなのは**閾値を二層に分ける構造**であり、CSW自身が外部化を許可・拒否することではない。

この修正は、10205bb3の抑制緩和の意図と、PR #193の決定権境界を両立させる。

## 参照

- commit `10205bb3cef0f31cc092d246355bdf2bdf8fba6b` — collecting threshold vs publishing threshold
- PR #193 — `runtime: 著者決定権を外部利用条件へ再配置する`
