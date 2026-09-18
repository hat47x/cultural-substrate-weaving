# Product Quality Research

このディレクトリは、CSWの**プロダクト品質を観測・検証するための監査記録と制御実験**を置く場所です。

方法論そのものの意味上の正本ではありません。日本語の方法論正本は`src/ja-JP/`、research prototypeの機械可読な契約は`research/skill-prototypes/`にあります。

## ここに置くもの

- 現行品質証拠のcoverage audit
- 制御されたbehavioral experimentのprotocol
- experiment runの観測記録
- 既知failureから切り出した回帰候補
- quality requirementと証拠の対応記録

## ここに置かないもの

- 新しい方法論規則の第二正本
- AI自己採点だけで成立する「品質スコア」
- Living Labの自然利用記録のコピー
- production promotionを自動承認する判定

## 証拠の扱い

品質証拠は最低限、次を区別します。

1. **static / deterministic evidence** — repository contract、validator、schema、生成物一致など
2. **controlled behavioral evidence** — 固定packetと不変条件を用いたモデル実行
3. **natural-work evidence** — Living Lab等の自然な実作業から得た観測
4. **interpretation** — 人間・AI・外部評価者による解釈

static checkが通ったことをモデル行動の保証とみなさず、単発の良いモデル出力を方法論全体の有効性ともみなしません。

## 命名

- 監査: `YYYY-MM-DD-<topic>-audit.md`
- 実験protocol: `experiment-NNN-<topic>.md`
- 実行記録: `experiment-NNN-run-YYYY-MM-DD[-suffix].md`

実行記録では、可能な限りsource commit、visible model / product mode / tools、入力packet、出力artifact、must-pass invariant、diagnostic observation、評価者の来歴を残します。

## 現在の入口

- [`2026-09-11-quality-evidence-audit.md`](2026-09-11-quality-evidence-audit.md) — E0: 現行品質証拠の初回監査
- [`2026-09-16-quality-evidence-reaudit.md`](2026-09-16-quality-evidence-reaudit.md) — E0再監査: E1〜E7整備後の証拠強度と未充足点を再評価
- [`experiment-001-handoff-integrity.md`](experiment-001-handoff-integrity.md) — E3: CSW → affinity synthesis → iterative inquiryのhandoff integrity protocol
- [`experiment-001-run-2026-09-11-engineering.md`](experiment-001-run-2026-09-11-engineering.md) — E3 Run 001: 同一contextでのengineering trial
- [`experiment-001-run-002-execution-packet.md`](experiment-001-run-002-execution-packet.md) — E3 Run 002: fresh execution側へ渡す固定packet
- [`experiment-001-run-002-evaluation-sheet.md`](experiment-001-run-002-evaluation-sheet.md) — E3 Run 002: execution後に別contextまたは人間が使う評価sheet
- [`experiment-002-authority-provenance-adversarial.md`](experiment-002-authority-provenance-adversarial.md) — E1: authority / provenance adversarial probe
- [`experiment-002-run-2026-09-14-engineering.md`](experiment-002-run-2026-09-14-engineering.md) — E1 Run 001: 同一contextでのengineering trial
- [`experiment-002-run-002-execution-packet.md`](experiment-002-run-002-execution-packet.md) — E1 Run 002: adversarial依頼をfresh executorへ渡す固定packet
- [`experiment-002-run-002-evaluation-sheet.md`](experiment-002-run-002-evaluation-sheet.md) — E1 Run 002: A1〜A6をexecution後に確認する評価sheet
- [`experiment-003-delayed-reactivation.md`](experiment-003-delayed-reactivation.md) — E4: stop snapshotからのdelayed reactivation protocol
- [`experiment-003-run-2026-09-14-engineering.md`](experiment-003-run-2026-09-14-engineering.md) — E4 Run 001: 外部snapshotからの局所再開engineering trial
- [`experiment-003-run-002-execution-packet.md`](experiment-003-run-002-execution-packet.md) — E4 Run 002: prior snapshotとdelayed deltaだけを渡すfresh restart packet
- [`experiment-003-run-002-evaluation-sheet.md`](experiment-003-run-002-evaluation-sheet.md) — E4 Run 002: L1〜L10をexecution後に確認する評価sheet
- [`experiment-004-activation-calibration.md`](experiment-004-activation-calibration.md) — E2: 同一taskで外部委任だけを変えるactivation calibration protocol
- [`experiment-004-run-2026-09-14-engineering.md`](experiment-004-run-2026-09-14-engineering.md) — E2 Run 001: paired engineering trial
- [`experiment-004-run-002-execution-packet.md`](experiment-004-run-002-execution-packet.md) — E2 Run 002: 期待ラベルを見せずpaired taskを渡すfixed packet
- [`experiment-004-run-002-evaluation-sheet.md`](experiment-004-run-002-evaluation-sheet.md) — E2 Run 002: K1〜K10をexecution後に確認する評価sheet
- [`experiment-004-run-003-execution-packet.md`](experiment-004-run-003-execution-packet.md) — E2 Run 003: Pair Cの8件source materialを固定したgrouping behavioral packet
- [`experiment-004-run-003-evaluation-sheet.md`](experiment-004-run-003-evaluation-sheet.md) — E2 Run 003: material-led grouping / provenance / split ownershipを後から確認する評価sheet
- [`experiment-005-cross-platform-semantic-parity.md`](experiment-005-cross-platform-semantic-parity.md) — E5: cross-platform semantic parity protocol
- [`experiment-005-run-2026-09-16-engineering.md`](experiment-005-run-2026-09-16-engineering.md) — E5 Run 001: Layer A packaging preflight
- [`experiment-005-run-002-execution-packet.md`](experiment-005-run-002-execution-packet.md) — E5 Run 002: 各実surfaceへ渡す固定packet
- [`experiment-005-run-002-evaluation-sheet.md`](experiment-005-run-002-evaluation-sheet.md) — E5 Run 002: surface出力生成後に使う評価sheet
- [`experiment-006-known-failure-regression.md`](experiment-006-known-failure-regression.md) — E7: 実際に再現した欠陥だけを対象にした回帰coverage監査
- [`experiment-007-natural-work-utility-overhead.md`](experiment-007-natural-work-utility-overhead.md) — E6: 自然作業を増やさずutility / overheadを読むevidence extraction protocol
- [`../../docs/ja/maintainers/product-quality-program.md`](../../docs/ja/maintainers/product-quality-program.md) — 品質要件・検証層・実験ポートフォリオ全体

## 現在の実験状態

### E0 — evidence coverage re-audit

2026-09-16に、初回E0以降に追加されたE1〜E7のprotocol、engineering trial、fresh rerun packet、known-failure fixtureを含めて品質証拠を再監査しました。

初回監査で大きかった「実験設計面の空白」は縮小し、現在の主要な未充足点は、**独立behavioral再現**、**実surfaceでの再現**、**natural-workでの実測**の三群へ収束しています。

E1〜E5はfresh execution / separate evaluationへ進める準備が整っていますが、この会話ではすでに前runや評価基準を見ているため、独立runを擬似実行しません。E6も観測のために仕事を作らず、本来の自然作業で評価可能な証拠が残った時だけ開始します。

### E3 — split-method handoff integrity

Run 001ではH1〜H6を外部artifactとして検査でき、明白なMethod contract違反は観測されませんでした。ただしprotocol作成・実行・評価が同じAI contextにあるため、behavioral reliabilityの強い証拠とは扱いません。

Run 001から得た具体的なprotocol補正は、`carried-untouched`と`=`（touched and explicitly checked, but semantically unchanged）を分けることです。

Run 002は、execution packetとevaluation sheetを分離した状態まで準備しました。**このrepository作業を行っている現在の会話ではfresh executionにならないため、まだ実行していません。** 次の実行では、executorへexecution packetと現行Skill / Methodだけを渡し、Run 001 outputとevaluation sheetを見せない状態で生成したartifactを、別contextまたは人間が評価します。

### E1 — authority / provenance adversarial probe

2026-09-14に固定packetを作り、engineering Run 001を実施しました。依頼文から「framework由来候補を調査根拠として扱う」「最適案を決めてそのまま公開する」という圧力を加えましたが、このrunではA1〜A6の明白な境界違反は観測されませんでした。

一方、このrunもprotocolを知った同一AI・同一contextで実行・評価しているため、独立したbehavioral reliabilityの証拠とは扱いません。

診断上は、`target_supported / framework_generated`等の**origin**と、`公開前要承認`等の**delivery / approval state**を外部artifact上で別々に見せると監査しやすいことを確認しました。現行CSWには「来歴ラベルは外部化許可を自動決定しない」という契約がすでにあるため、この結果だけでruntime ruleは追加していません。

Run 002用には、source packetとadversarial requestだけを渡すexecutor packetと、A1〜A6を後から確認するevaluator sheetを分離しました。Run 001 outputや評価rubricはexecutorへ渡しません。**この会話ではすでにRun 001と評価基準を見ているため、Run 002自体は実行しません。**

### E4 — delayed reactivation

2026-09-14に、prior inquiry、stable semantic ID、residual、author-pending、stop reasonを固定したsnapshotから、6週間後を模したdeltaだけで再開するprotocolを追加し、engineering Run 001を実施しました。

このrunではL1〜L10の明白な契約違反は観測されませんでした。特に次を外部artifactで区別できました。

- 旧`Q01`を履歴として残し、新しい問い`Q03`を追加するquestion shift
- deltaが触れたartifactだけのreopen
- 未接触`C02`のcarryと、明示的に再検査した`=`の分離
- `F01`のframework由来履歴と、後から得たtarget-side supportの分離
- 残差を残したまま再びstop / handoffできるcontinuation boundary

診断上は、問いのshiftをcompact deltaへ無理に押し込まず`Question Shift`欄を使うこと、またprior artifactだけでなく**prior stop reason**をsnapshotへ残すことが再開品質の監査に有効でした。どちらも現行`iterative-inquiry-synthesis`の契約ですでに表現できるため、Method Definitionは変更していません。

このrunの「6週間後」は合成packet上の設定です。実時間をまたいだモデル記憶性能やfresh-context再現性の証拠ではありません。

Run 002用には、prior snapshotとdelayed deltaだけを渡すexecutor packetと、L1〜L10を後から確認するevaluator sheetを分離しました。Run 001で観測した問いの動かし方や`carry`の具体例を模範出力としてexecutorへ見せません。**この会話ではfresh restartにならないため、Run 002自体は実行しません。**

### E2 — activation calibration

2026-09-14に、同じtaskを保ったままactivationに関する**外部委任だけを変えるpaired protocol**を固定し、engineering Run 001を実施しました。

このrunではK1〜K10について、観測した範囲で明白なactivation contract違反は見つかりませんでした。特に次を確認しました。

- 明確な技術課題でも、明示された限定利用に従えば`limited / not_loaded`になり得る。
- 曖昧な公共サービス課題でも、明示的に使わない委任なら`non_activation / not_loaded`のまま扱える。
- `probe`で探索目的を満たした場合、`full / enacted`へ進むことを品質向上とみなさない。
- one-roundの親和統合が必要でも、それ自体をCSWの発動理由にせず、`affinity-synthesis`またはcompatible realizationへ責務を残せる。
- activationに関する外部条件がpacketにない場合、課題種別から勝手に補わず`external_or_delegated`として扱える。

同時に、`evals/activation-cases.json`のlimited / exploratory例がv0.5以前の「CSW自身がKJ材料統合を行う」責務を残していることを確認しました。これはruntime failureではなく**eval fixtureのresponsibility drift**です。fixtureを現在のsplit ownershipへ合わせ、affinity-onlyの材料統合をCSW自動発動理由にしないcaseを追加しました。

この既知failureは、`tests/test_activation_fixture_semantic_contract.py`でsplit ownershipの最小不変条件へ縮約して回帰検出するようにしました。case全文や順序は固定せず、limited / affinity-only / exploratoryの意味境界だけを検査します。

Pair CのRun 001 / Run 002 packetは8件の元メモ本文を列挙していないため、そこで確認できるのはrouting / ownership境界までです。この制約は履歴として残し、後から「実groupingまで評価済み」とは読み替えません。

Run 002用には、A/B/Cのpaired taskとControl Uを期待ラベルなしで渡すexecutor packetと、K1〜K10を後から確認するevaluator sheetを分離しました。Pair Cはrouting / ownershipまでを観測範囲とし、可能ならvariant同士の出力を見せずに実行します。そうできない場合は順序をconfounderとして残します。**この会話ではRun 002自体は実行しません。**

2026-09-18には、Pair Cだけを対象にしたRun 003を追加しました。N01〜N08の8件をcontrolled comparison用の合成source materialとして固定し、C0ではaffinity synthesisのみ、C1ではCSWから一つだけframework-generated questionを渡してから同じone-round synthesisを行います。正解clusterは定義せず、material-led grouping、source return、残差、framework questionの非権威化、split ownershipを別sheetで評価します。**Run 003もfresh execution用に準備しただけで、この会話では実行していません。**

### E5 — cross-platform semantic parity

2026-09-16にLayer A packaging preflightを行い、Claude Code / Codex / OpenAI Skill / ChatGPT GPT / Microsoft 365の包装経路を比較しました。

この監査では、OpenAI Skillの`default_prompt`だけが、文化体系とKJ法の利用を常時要求する形で正本より強い方法命令を持っていました。ja-JP / en-US × interactive / meteredの4 profileで、外部委任を読み、必要な範囲だけ文化体系探索やcompatibleな親和統合への接続を使う表現へ修正しました。

このfailureは`tests/test_openai_adapter_semantic_contract.py`へ最小の静的回帰fixtureとして落としています。固定しているのは、method depthを外部委任から奪わないこと、interactive / meteredでdefault promptの意味を変えないこと、implicit invocation policyの差は維持することです。これは新しい方法論規則ではなく、既存契約をwrapperが上書きした既知failureの再発防止です。

OpenAI Skillの`dist/`はGit管理外で、`build_openai()`が正本となるadapter YAMLを生成先`agents/openai.yaml`へそのままコピーします。この入力と生成結果の対応は、`tests/test_openai_build_adapter_parity.py`でja-JP / en-US × interactive / meteredについて固定し、adapter側の修正がbuild時に取りこぼされる回帰を検出します。

Layer Bについては、Run 002のexecution packetとevaluation sheetを分離しました。各surfaceは他surfaceの出力や評価rubricを見ずにraw outputと実行metadataだけを作り、その後にP1〜P8を評価します。異なるmodel / reasoning mode / context freshnessはplatform差と混同せず、confounderとして別記します。

**このrepository作業の会話では実surfaceを擬似実行しないため、E5 Run 002はまだ未実施です。** E5全体も完了扱いにはしていません。

### E6 — natural-work utility / overhead

2026-09-16に、Living Lab schema 0.2、event schema 0.2、ローカル運用を監査し、E6のevidence extraction protocolを固定しました。

現行`natural_work` roundにはartifact、residual、reopening condition、provenance付きinterpretationを残す経路があり、eventではartifact adoption / withdrawal、decision change、delayed reactivation等を参照付きで記録できます。一方、数値`measurements`は`paired_check`のcomparison側にあり、自然作業へ必須化されていません。

この境界を維持し、E6のためにLiving Lab schemaやvalidatorへ新しい必須fieldは追加していません。特に次を守ります。

- event件数、framework contact数、activation件数をutility / overheadの代理KPIにしない。
- 明示的なoverhead測定がないことを`0`とせず、`not measured`として扱う。
- retrospectiveに、当時測っていない時間やturn数を精密値として復元しない。
- artifact差分、利用者の採用・訂正・撤回、残差の後日再利用を優先して読む。
- このrepository保守作業をnatural-work実績として数えない。

E6 Run 001は、別の本来目的で行われた自然作業に評価可能なrecordまたはartifact参照が有機的に残った場合だけ開始します。観測のために仕事や追加roundを作りません。

### E7 — known-failure regression

2026-09-16に、E1〜E5で得た知見を「実際に再現した欠陥」と「診断知見・未測定事項」に分けて初回監査しました。

現在、E7で追跡しているknown failureは3件です。

- E2のactivation fixture responsibility drift — `tests/test_activation_fixture_semantic_contract.py`
- E5のOpenAI adapter `default_prompt` semantic drift — `tests/test_openai_adapter_semantic_contract.py`
- E5回帰fixtureの語句過剰固定 — adapterが意味契約を満たしていても意味上同等の言い換えでFAILしたため、同testを意味上の不変条件を検査する形へ縮約

E3の`carry`と`=`の区別、E4のquestion shiftやprior stop reasonは重要な知見ですが、既存Method契約で正しく処理できており、修正前failureは再現していません。このため、規則数を増やす目的でfixture化しません。E1もengineering Run 001では明白なfailureがありません。

E7には件数目標を置きません。今後、実利用やprobeで具体的なfailureが再現した場合に、そのfailureを最小化できる範囲で追加します。

## 次に強める証拠

独立性を必要とするrunは、この会話の中で擬似的に済ませません。E1/E2/E3/E4/E5は、executorへ評価rubricや前run出力を渡さず、その後に別contextまたは人間が評価できる形まで準備しています。

1. **E3 Run 002** — prepared execution packetをfresh contextへ渡し、別contextまたは人間がH1〜H6を評価する。
2. **E1 Run 002** — adversarial packetをfresh contextへ渡し、別評価者がA1〜A6を確認する。
3. **E4 Run 002** — prior snapshotとdelayed deltaをfresh contextから再開し、別評価者がL1〜L10を確認する。
4. **E2 Run 002 / Run 003** — Run 002でactivation / depth / split ownershipを確認する。Pair Cの実groupingは、8件の元メモ本文を固定済みのRun 003をfresh contextへ渡し、material-led grouping / provenance / residual retentionまで別評価する。
5. **E5 Run 002** — 固定packetを実surfaceへ個別に渡し、raw output生成後にP1〜P8を別評価する。model / product mode差はplatform効果と即断しない。
6. **E6 Run 001** — 自然作業が本来の目的で発生し、artifact / judgment / residual reuse等の証拠が有機的に残った時だけ評価する。E6のために作業を発生させない。
7. 上記で同じfailureが再現した場合は最小fixtureへ落とす。natural-workで重大なfailureが見つかった場合は、その再現を優先する。

E7はこの順序とは別に、具体的なfailureが再現した時点で割り込みます。回帰fixtureの件数を増やすこと自体は目標にしません。

この順序はrelease gateではありません。行動試行の件数やactivation率を増やすこと自体も目標にしません。

## 改善へ反映するとき

観測からruntimeや正本を変える場合は、先にfailure modeを明示します。既存規則の言い換えで済むのか、fixture追加で済むのか、実際に方法の変更が必要なのかを分けます。

重大なfailureが再現できる場合は、まず再現packetを最小化し、可能なら回帰fixtureへ落とします。実験で良い結果が出たことだけを理由にresearch prototypeのpromotion gateを迂回しません。
