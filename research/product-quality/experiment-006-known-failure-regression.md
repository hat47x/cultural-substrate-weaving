# E7 known-failure regression — coverage audit

- experiment id: `PQ-E7-006`
- program: E7 — known-failure regression
- audit date: 2026-09-16
- source baseline: `develop/v0.5.0@34234c8bf4a502c812c09cb6b81520c9571f6b47`
- primary requirements: PQ-12、関連してPQ-01〜PQ-08、PQ-11
- status: initial regression coverage audit

## 目的

Product Quality Programで実施したE1〜E5のengineering trialと包装監査について、**実際に再現した欠陥**と、単なる診断知見・未測定事項を分ける。

E7では、見つかった知見をすべてtestへ昇格させない。修正前にrepositoryまたは実行artifact上で存在したfailure modeだけを対象にし、既存契約の言い換えや「念のため」の規則増加を避ける。

この監査の対象は、2026-09-16時点の`research/product-quality/`で記録しているE1〜E5である。リポジトリの全履歴に存在したすべてのbugを網羅する台帳ではない。

## E7の回帰対象にする条件

既知failureとして扱うには、少なくとも次を満たす。

1. 修正前の具体的な入力・設定・artifactを特定できる。
2. 何が期待契約に反したかをfailure modeとして説明できる。
3. 修正箇所を特定できる。
4. 同じfailure modeを、過度に実装詳細へ固定せず再検出できる。
5. behavioralな非決定性を静的testへ偽装しない。

満たさない診断知見はprotocolやrun記録に残しても、回帰fixtureへは昇格させない。

## 現在のknown-failure inventory

| source | observed failure | failure class | repair | regression status |
|---|---|---|---|---|
| E2 Run 001 | `evals/activation-cases.json`のlimited / exploratory例が、v0.5以前の「CSW自身がKJ材料統合を行う」責務を残していた | eval fixture responsibility drift | affinity synthesisを`affinity-synthesis`またはcompatible realizationへ戻し、affinity-onlyでCSWを発動しないcaseを追加 | **covered in this change** — 監査開始時はgap。`tests/test_activation_fixture_semantic_contract.py`を追加 |
| E5 Run 001 | OpenAI Skillの`default_prompt`が、外部委任にかかわらず文化体系とKJの利用を常時要求していた | adapter semantic drift | ja/en × interactive/meteredのpromptを外部委任・必要範囲・compatible realizationに整合 | **covered** — `tests/test_openai_adapter_semantic_contract.py` |

### E2 failureの最小不変条件

E2の修正を回帰fixtureへ落とす際、文面全体は固定しない。少なくとも次だけを守る。

- 明示的なlimited caseでは、文化体系を開かない限定利用が成立する。
- one-round affinity synthesisが必要な場合、CSW内部のKJ統合責務として記述せず、`affinity-synthesis`またはcompatible realizationへ委ねる。
- affinity synthesisだけを依頼し、CSWを使わない明示指定では`no_activation`を維持する。
- exploratory caseでも、親和統合が必要ならsplit ownershipを維持する。
- ja-JP / en-USで同型の責務境界を持つ。

activation caseの文章そのものやcase順序は契約にしない。

## fixtureへ上げない診断知見

### E1 — authority / provenance adversarial probe

engineering Run 001ではA1〜A6の明白な違反は観測されていない。originとdelivery / approval stateを外部artifact上で分けると監査しやすいという診断は得たが、修正前の欠陥ではない。

**判定:** E7 fixtureなし。fresh independent rerunを優先する。

### E3 — split-method handoff integrity

`carried-untouched`と`=`を区別する必要性が明確になったが、現行`iterative-inquiry-synthesis`はもともと`=`を「touched and explicitly checked, but semantically unchanged」と定義していた。Run 001も未接触artifactを`=`へ誤分類していない。

**判定:** product/runtime failureではなくprotocol表現の明確化。新しい回帰規則は追加しない。

### E4 — delayed reactivation

question shiftをcompact deltaの`~`へ押し込まず別欄で扱うこと、prior stop reasonをsnapshotへ残すことが有効だった。しかしengineering Run 001では既存Method契約で正しく処理できており、修正前failureは再現していない。

**判定:** E7 fixtureなし。fresh Run 002を優先する。

### E5 — Layer B behavioral comparison

Run 002は未実施である。未実施surfaceやmodel/context差をfailureへ数えない。

**判定:** 新しいbehavioral failureが実surfaceで再現した場合にのみE7へ追加する。

## 今回の変更判断

E2 responsibility driftは、修正前の具体的fixtureと修正後の状態を特定でき、静的に再検出できる。そのため、`tests/test_activation_fixture_semantic_contract.py`へ最小のunit testを追加した。

一方、E1/E3/E4の診断知見を「重要そうだから」という理由でtestへ昇格させない。これによりPQ-12を、規則数の増加ではなく**実際に起きた欠陥の再発防止**として運用する。

## 今後の追記単位

新しいknown failureが生じた場合は、この文書へ少なくとも次を追記する。

```text
source:
source_commit_or_run:
failure_mode:
pre_fix_reproduction:
repair:
regression_fixture:
fixture_layer: static / behavioral
known_limits:
```

behavioral failureは、一度のモデル出力をそのままdeterministic release gateへ変えない。安定した局所不変条件へ縮約できる場合だけ静的fixture化する。
