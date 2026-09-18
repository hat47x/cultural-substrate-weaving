# E7 known-failure regression — coverage audit

- experiment id: `PQ-E7-006`
- program: E7 — known-failure regression
- initial audit date: 2026-09-16
- last follow-up: 2026-09-18
- source baseline: `develop/v0.5.0@34234c8bf4a502c812c09cb6b81520c9571f6b47`
- primary requirements: PQ-12、関連してPQ-01〜PQ-08、PQ-11
- status: maintained regression coverage audit

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
| E7 follow-up (2026-09-17) | `tests/test_openai_adapter_semantic_contract.py`が英語promptの意味境界ではなく`as needed` / `compatible affinity synthesis`という特定語句へ固定され、意味上は同等のcanonical promptを誤ってFAILにした | regression fixture over-specification | 条件付き適用・外部委任・compatibleなaffinity-synthesisへの接続という意味上の不変条件だけを検査し、同義表現を許容する | **covered in 2026-09-18 follow-up** — 同testをsemantic predicateへ縮約 |
| E7 follow-up (2026-09-18) | production metadataの一部がsplit ownership前の「CSW自身がKJ統合を行う」説明を保持している | production metadata responsibility drift | canonical input・build hard-code・generated artifactの修正範囲を監査済み。正規build可能環境で一括修正する | **open / not fixtureized** — `2026-09-18-production-metadata-split-ownership-audit.md` |

### E2 failureの最小不変条件

E2の修正を回帰fixtureへ落とす際、文面全体は固定しない。少なくとも次だけを守る。

- 明示的なlimited caseでは、文化体系を開かない限定利用が成立する。
- one-round affinity synthesisが必要な場合、CSW内部のKJ統合責務として記述せず、`affinity-synthesis`またはcompatible realizationへ委ねる。
- affinity synthesisだけを依頼し、CSWを使わない明示指定では`no_activation`を維持する。
- exploratory caseでも、親和統合が必要ならsplit ownershipを維持する。
- ja-JP / en-USで同型の責務境界を持つ。

activation caseの文章そのものやcase順序は契約にしない。

### E5回帰fixture自体のfailureと最小不変条件

2026-09-17の隔離実行では、OpenAI adapter本体が現行契約を満たしているにもかかわらず、回帰test側が英語promptの特定語句へ固定されていたためFAILした。これはadapter semantic driftの再発ではなく、**回帰fixtureの過剰指定**である。

修正後のtestでは、次の意味境界だけを固定する。

- 方法の深度を「必要な範囲」「必要に応じて」など依頼に応じた条件付きで扱い、常時深く適用する命令にしない。
- compatibleな`affinity-synthesis`への接続可能性を保ち、CSW自身へone-round synthesisを戻さない。
- 方法の深度と採否・価値判断が外部の委任に結び付いている。
- 旧promptの「文化体系とKJを常に使う」命令へ戻らない。
- interactive / metered間ではdefault promptの意味を変えず、implicit invocation policyだけを分ける。

英語では`where needed`と`as needed`、`needed`と`necessary`といった意味上同等の言い換えをfailureとしない。日本語側も同様に、一つの定型句ではなく、条件付き適用・委任・split ownershipを検査する。

## open known failure — production metadata split ownership drift

2026-09-18の追加監査で、CSW単体を説明するproduction metadataの一部に、split ownership前の「文化体系探索とKJ統合をCSW自身が組み合わせる」という責務表現が残っていることを確認した。

影響範囲には、少なくとも次が含まれる。

- `src/manifest.json`のja-JP / en-US description
- `adapters/claude-code/locales.json`のdescription
- OpenAI Skillのja-JP / en-US short_description
- ChatGPT GPTのja-JP / en-US instructions prefix
- `scripts/build.py`のroot Claude marketplace description
- そこから生成されるtracked plugin / marketplace metadata

Microsoft 365 limited compositeは、surface制約のため最小compatible material-synthesis fallbackを明示的に埋め込み、CSW本体の所有責務ではないことも説明しているため、同じfailureへ自動的に含めない。

詳細な影響範囲、修正対象、生成先、完了条件は`2026-09-18-production-metadata-split-ownership-audit.md`へ固定した。

**判定:** failure自体は実在するが未修正。canonical inputを変えるとtracked generated artifactも正規buildする必要があるため、build不能な現在の環境ではrepairを開始しない。修正完了前にpassing regression fixtureだけを追加することもしない。

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
