# Framework corpus seventeenth wave — 2026-10-05

Status: candidate-quality expansion / no runtime adoption

## Decision

中世スコラ学の disputed question / `quaestio disputata` を、profile-readyの研究候補として追加する。

追加の目的は中世思想の内容を対象へ移すことではない。今回取り込む構造核は、**一つの問いに対して異なる反対論を消さずに保持し、主たる判断を出した後で、それぞれへ個別に応答する**というレビュー構造である。

Stanford Encyclopedia of Philosophyは、13〜14世紀の大学でdisputationが教育・研究の制度的形式として使われ、賛否の論拠を出した後、masterがdeterminationと反対論への応答を行ったことを整理している。Aquinasの項目も、彼の著作における典型的な構造を、arguments → sed contra → main reply → replies to initial argumentsとして説明している。『Summa Theologiae』I, q.2, a.2は、その文学的形式を一次作品上で確認できる。

## Why this fills a real corpus gap

現行portfolioには、近いが異なる操作がすでにある。

- Classical stasis theoryは、争点がfact / definition / evaluation / procedureのどこにあるかを分ける。
- Nyāya five-member inferenceは、thesisからreason・example・applicationを経てconclusionへ至る推論橋を露出させる。
- Mīmāṃsāは規定文の意味・文脈・規範衝突を扱う。

今回の候補が追加するのは、**反対論をstableな個別対象として保存し、最終判断が各反対論へ本当に答えたかを再点検する操作**である。

一般的なpros/cons listとも異なる。列挙後に一つの総括文を書いて終えるのではなく、O1→R1、O2→R2のようにpointwiseな応答関係を残し、答えられない反対論をunresolvedとして持ち越す。

これはSIerの設計review、ADR、障害対策、移行判断で価値がある。議論の最後に「総合的にはこの案」と書いた結果、初期に出た運用・移行・障害時の反対論だけが消える失敗を検出しやすくなる。

## Historical boundary

この候補を「西洋の一般的な論理的思考法」にはしない。

- disputed questionは中世大学の制度的文脈を持つ。
- ordinary disputation、quodlibetal disputation、reportatio、書かれたSummaの形式は同一ではない。
- masterのdeterminationという制度上の非対称を、対象側の権限構造へ移さない。
- sed contraに置かれるauthorityは歴史的形式の一部であり、CSWでは引用自体をtarget Evidenceへ昇格させない。
- Aquinasは資料が豊富な代表例だが、すべてのscholastic practiceを定義する存在として扱わない。

## Target-return value

de-binding後に残すのはラテン語の形式ではなく、次の操作である。

1. 何を決める問いなのかを固定する。
2. 異なる反対論をまとめすぎない。
3. determination candidateを出す。
4. 各反対論に対するreplyを明示する。
5. replyが無ければunresolvedとして残す。
6. authorityではなく対象Evidenceへ戻る。

worked exampleでは、分散計算基盤のstate store判断を使い、4件の異なる反対論のうち1件を意図的にunresolvedとして残した。

negative exampleでは、まだ発散探索中でstableなthesisが無い場面にこの形式を当てると、探索を早く閉じてしまうためnon-activationとした。

## Runtime decision

runtimeへは採用しない。

次に比較すべきなのは、

- ordinary design-review checklist;
- Classical stasis theory;
- Nyāya five-member inference;

である。

比較では「最終判断が良くなったか」だけでなく、

- 初期の異なる反対論が何件残ったか;
- main rationaleで未回答なのに消えた反対論がないか;
- pointwise replyによって新しいEvidence要求が出たか;
- frameworkを外した後もunresolved objectionがtarget-side review itemとして残るか;

を確認する。

広範なefficacy benchmarkはまだ開始しない。
