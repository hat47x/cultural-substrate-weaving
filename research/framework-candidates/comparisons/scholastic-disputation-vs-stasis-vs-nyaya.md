# Scholastic disputed question vs Classical stasis vs Nyāya inference

Status: research differentiation / no runtime promotion

## Purpose

三つの候補はいずれも「議論を整理する」ように見えるが、同じ操作として扱うとCSWの体系差が消える。

この比較では、文化名や語彙ではなく、de-binding後に対象へ返る認知操作を分ける。

## Core distinction

| Framework | Primary question | Preserved object | Typical target-return |
|---|---|---|---|
| Classical stasis theory | 何について争っているのか | fact / definition / evaluation / procedure等のissue state | 「この証拠は別の争点に答えている」 |
| Nyāya five-member inference | この結論へ至る推論橋は成立しているか | thesis / reason / example / application / conclusion | 「理由と対象事例の間の適用橋が不足している」 |
| Scholastic disputed question | 判断は提示された反対論へ本当に答えたか | question / distinct objections / determination / pointwise replies | 「O3だけ未回答なので残差として残す」 |

## Same target, different operations

Target:

> 初回リリースでembedded relational state storeを採用してよいか。

### Stasis pass

Stasisは、議論が混ざっていないかを見る。

- fact: restart後もTask identityを保持できるか。
- definition: 「durable」と呼ぶ最低条件は何か。
- evaluation: 運用上十分と判断できるか。
- procedure: 誰がproduction profileとして承認するか。

価値は、異なる種類の問いへ同じEvidenceを使わないことにある。

### Nyāya pass

Nyāyaは、たとえば次の主張を展開する。

- thesis: embedded storeでM0を開始できる。
- reason: 必要なtransaction / revision / restart durabilityを満たせる。
- example: 同じ性質を持つ既知のlocal relational deployment。
- application: EKIのM0条件でもその性質が成立する。
- conclusion: M0ではembedded storeが候補になる。

価値は、reasonからtarget caseへ適用する橋を露出させることにある。

### Scholastic disputed-question pass

このpassは、異なる反対論をO1/O2/O3/O4として残す。

main determinationを出した後も、

- O1 restart durabilityへ回答したか;
- O2 multi-instance assumptionへ回答したか;
- O3 operational recoveryへ回答したか;
- O4 replacement lock-inへ回答したか;

を一件ずつ確認する。

価値は、総括判断が一部の反対論を黙って消すことを防ぐ点にある。

## Non-substitutability

### Stasis cannot replace disputed-question structure

issue stateを正しく分類しても、同じissue typeに属する複数の反対論が一つに圧縮される可能性がある。

例:

- backup手順がない;
- corruption recoveryがない;

はどちらも運用評価の問題に分類できるが、片方へ答えても他方へ答えたことにはならない。

### Nyāya cannot replace disputed-question structure

推論橋を十分に説明できても、反対側の独立した懸念がすべて解消されたとは限らない。

強いpositive inferenceと、unanswered operational objectionは同時に存在できる。

### Disputed-question structure cannot replace Stasis or Nyāya

反対論へ一件ずつreplyしても、

- そもそもfactとevaluationを混同している;
- reasonからconclusionへの推論橋が壊れている;

ことは別問題である。

したがってscholastic passを万能な「厳密レビュー」にしない。

## Selection cues

### Prefer stasis when

- participants appear to answer different kinds of questions;
- evidence appropriate to one issue is being used for another;
- factual, definitional, evaluative, and procedural disagreement are entangled.

### Prefer Nyāya when

- a fluent claim hides the bridge from reason to target case;
- examples may be illustrative rather than probative;
- application of a general relation to the concrete case is the weak point.

### Prefer scholastic disputed question when

- a concrete proposal or determination already exists;
- several materially different objections must survive review;
- the final rationale risks answering the thesis without returning to earlier concerns;
- unresolved objections need stable carry-forward.

### Prefer non-activation when

- no stable thesis or decision question exists yet;
- the task is divergent exploration;
- objections would have to be invented to populate a form.

## Authority boundary

None of the three frameworks decides the target.

- issue classification is not truth;
- a five-member inference is not proof merely by form;
- a determination is not authoritative because it occupies the historical master's position.

Target-side Evidence and caller/domain criteria remain authoritative.
