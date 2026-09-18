# E0再監査 — 品質証拠カバレッジ 2026-09-16

- 実施日: 2026-09-16
- audit id: `PQ-E0-20260916-02`
- 基準commit: `develop/v0.5.0@a528e93e1aaeafd5a6693e92ee79a1620deb6a70`
- 種別: repository evidence re-audit
- 比較対象: [`2026-09-11-quality-evidence-audit.md`](2026-09-11-quality-evidence-audit.md)
- 制約: repository上の契約・test・research recordを再監査する。今回、新しいbehavioral runやLiving Lab roundは作らない。

## 1. 再監査の目的

2026-09-11の初回E0では、repository correctnessを支える静的契約は比較的厚い一方、次の領域が主な空白だった。

- Method間handoffのend-to-end behavior
- authority / provenanceへのadversarial pressure
- delayed local reactivation
- activation calibration
- cross-platform behavioral parity
- natural-workでのutility / overhead
- behavioral failureを最小fixtureへ落とすloop

その後、E1〜E7のprotocol、engineering trial、既知failureの回帰fixture、fresh rerun packetが順次追加された。

今回の再監査では、「protocolがあるか」だけでなく、**どの強さの証拠まで到達しているか**を見直す。特に、次を混同しない。

1. deterministic/static contractが存在すること
2. 同じcontextでengineering trialを実行したこと
3. fresh execution / separate evaluationを実行できる準備が整ったこと
4. 実際に独立runを実行して再現性を確認したこと
5. natural workで利用者判断や後日の再利用が残ったこと

4と5がまだない領域を、1〜3が揃ったという理由だけで「検証済み」とは扱わない。

## 2. 今回使う証拠状態

### `strong-static`

決定論的なcontract、validator、fixture、生成・翻訳・release構成等の証拠が比較的厚い状態。

モデルが実際に契約へ従うことまでは意味しない。

### `engineering-behavioral`

固定protocolを使ったモデル実行があり、外部artifact上で不変条件を検査できた状態。

ただし、protocol作成・実行・評価を同じAI / contextが担ったrunは、独立したbehavioral reliabilityの証拠とはしない。

### `independent-ready`

fresh executorへ渡すexecution packetと、execution後に使うevaluation sheetが分離され、独立runを開始できる状態。

これは**実行済み**を意味しない。

### `natural-early`

自然作業由来の観測資産はあるが、件数や時間幅が小さい、または今回の品質要求を直接測るには証拠が足りない状態。

### `unmeasured`

重要な要求だが、現在の証拠からは対象failure modeを直接評価できない状態。

これらは品質の順位や総合点ではない。同一Requirementが複数状態を持ってよい。

## 3. 2026-09-11以降に増えた主要証拠

### 3.1 E1 — authority / provenance adversarial

追加資産:

- `experiment-002-authority-provenance-adversarial.md`
- `experiment-002-run-2026-09-14-engineering.md`
- `experiment-002-run-002-execution-packet.md`
- `experiment-002-run-002-evaluation-sheet.md`

engineering Run 001では、framework由来候補をtarget factへ昇格させる圧力、組織としての最終決定・公開まで委ねるように見える圧力、非公開原文を外部化する圧力を同時に与えた。

同一context自己評価という制約はあるが、A1〜A6を外部artifactとして検査できるところまで進んだ。Run 002はexecutor-only packetとevaluator-only sheetが分離され、独立再実行の準備が整っている。

### 3.2 E2 — activation calibration

追加資産:

- `experiment-004-activation-calibration.md`
- `experiment-004-run-2026-09-14-engineering.md`
- `experiment-004-run-002-execution-packet.md`
- `experiment-004-run-002-evaluation-sheet.md`
- `tests/test_activation_fixture_semantic_contract.py`

同じtaskに対し、外部委任だけを変えるpaired designを導入した。これにより、「技術課題だから非発動」「曖昧な課題だから深く発動」といったtask type由来の自動判定を避けて検査できるようになった。

engineering Run 001では明白なactivation contract違反は見つからなかった一方、`evals/activation-cases.json`がv0.5以前のCSW内KJ統合責務を残していたことを発見した。このresponsibility driftは修正され、最小の意味境界がunit testへ固定された。

Pair Cは8件の元メモ本文を持たないため、grouping qualityではなくrouting / ownershipだけを観測範囲とする。この制約はRun 002でも明示している。

### 3.3 E3 — split-method handoff integrity

追加資産:

- `experiment-001-handoff-integrity.md`
- `experiment-001-run-2026-09-11-engineering.md`
- `experiment-001-run-002-execution-packet.md`
- `experiment-001-run-002-evaluation-sheet.md`

CSW → affinity synthesis → iterative inquiryを一つのpacketで通すengineering trialを行い、framework由来、target側support、residual、author-pending、touched artifactを外部artifact上で追跡した。

Run 001ではH1〜H6の明白な違反は観測されなかった。`carried-untouched`と`=`を混同しないことがrepresentation上の重要な診断点として明確になったが、これは既存Methodで表現可能だったため新しいruntime ruleにはしていない。

Run 002はfresh execution / separate evaluationへ分離済みである。

### 3.4 E4 — delayed reactivation

追加資産:

- `experiment-003-delayed-reactivation.md`
- `experiment-003-run-2026-09-14-engineering.md`
- `experiment-003-run-002-execution-packet.md`
- `experiment-003-run-002-evaluation-sheet.md`

一度stopした外部snapshotへ6週間後を模したdeltaを与え、全面再構築ではなく局所reopenできるかを検査した。

engineering Run 001では、旧問いを履歴として残したquestion shift、未接触artifactのcarry、framework由来履歴、残差を残した再stopを外部化できた。Run 002ではRun 001の具体的な更新例やL1〜L10をexecutorへ見せない構造まで整っている。

この「6週間後」は合成packet上の設定であり、モデルの長期記憶性能を測ったものではない。

### 3.5 E5 — cross-platform semantic parity

追加資産:

- `experiment-005-cross-platform-semantic-parity.md`
- `experiment-005-run-2026-09-16-engineering.md`
- `experiment-005-run-002-execution-packet.md`
- `experiment-005-run-002-evaluation-sheet.md`
- `tests/test_openai_adapter_semantic_contract.py`

Layer A packaging preflightで、OpenAI Skillの`default_prompt`だけが文化体系とKJ法の利用を常時要求し、正本より強い方法命令を持つsemantic driftを実際に再現した。

adapter入力を最小修正し、method depthを外部委任から奪わないこと、interactive / metered間で意味を変えないこと、implicit invocation policyの差を保持することを回帰fixtureへ落とした。

一方、複数実surfaceでのLayer B behavioral parityは未実施である。execution packetとevaluation sheetは分離済みだが、platform、model、reasoning mode、context freshnessのconfounderを伴うため、実行前の静的整合だけでPQ-08を完了扱いにはできない。

### 3.6 E6 — natural-work utility / overhead

追加資産:

- `experiment-007-natural-work-utility-overhead.md`

Living Lab schema 0.2、event schema 0.2、既存運用を監査し、新しい必須fieldや帳票を増やさずにutility / overheadを読むprotocolを固定した。

特に、次を明示した。

- 未測定overheadを`0`へ置き換えない。
- event件数、framework contact数、activation件数を代理KPIにしない。
- retrospectiveに未測定の時間やturn数を精密値へ復元しない。
- artifact差分、利用者の採用・訂正・撤回、残差の後日再利用を優先する。
- E6のために仕事を作らない。

このため、E6は設計上の観測境界は明確になったが、utility / overhead自体の新しいnatural-work証拠はまだ増えていない。

### 3.7 E7 — known-failure regression

追加資産:

- `experiment-006-known-failure-regression.md`
- `tests/test_activation_fixture_semantic_contract.py`
- `tests/test_openai_adapter_semantic_contract.py`

E1〜E5の知見を「実際に修正前failureが存在したもの」と「有益な診断だがfailureではなかったもの」に分けた。

現在、known failureとして回帰fixtureへ固定したのは次の2件である。

1. E2 activation fixture responsibility drift
2. E5 OpenAI adapter `default_prompt` semantic drift

E3の`carry` / `=`やE4のquestion shiftは重要だが、既存Methodで正しく処理できたため、規則数を増やす目的でfixture化していない。

## 4. 品質要求別の再評価

| Requirement | 現在の証拠状態 | 主な前進 | まだ不足する証拠 |
|---|---|---|---|
| PQ-01 証拠境界 | `strong-static` + `engineering-behavioral` + `independent-ready` | E1/E3でframework由来とtarget supportをbehavioral artifact上で検査可能になった | E1/E3 fresh runの独立再現 |
| PQ-02 決定権境界 | `strong-static` + `engineering-behavioral` + `independent-ready` | E1で承認・公開圧力、E3/E4でauthor-pendingを扱った | fresh evaluatorによる独立確認、自然作業での撤回・修正例 |
| PQ-03 固定depth/round回避 | `strong-static` + `engineering-behavioral` + `independent-ready` | E2 paired trialで`limited/not_loaded`や`probe`を正常状態として扱った | E2 fresh run、異なるhostでも過剰深化しないか |
| PQ-04 発動/非発動を勝敗化しない | `strong-static` + `engineering-behavioral` + `natural-early` + `independent-ready` | E2 paired designとactivation fixture regressionが加わった | natural workでの長期的な過剰発動・過少発動の観測 |
| PQ-05 Method handoff完全性 | `strong-static` + `engineering-behavioral` + `independent-ready` | E3でend-to-end handoff artifactを実際に作った | **E3 Run 002のfresh execution / separate evaluation** |
| PQ-06 局所再開 | `strong-static` + `engineering-behavioral` + `independent-ready` | E4でstop snapshotからの局所再開を試行した | fresh restartと、実時間をまたぐnatural-work再開 |
| PQ-07 領域品質の非代替 | `strong-static` + `engineering-behavioral` + `independent-ready` | E1〜E4でno domain self-certificationを共通不変条件化した | domain-diverseな独立runと、外部専門評価が必要なケース |
| PQ-08 platform意味同等性 | `strong-static` + Layer A実証 + `independent-ready` | E5で実際のwrapper driftを発見・修正・fixture化した | **各実surfaceのLayer B run**。model/context差とplatform差の分離 |
| PQ-09 多言語同期 | `strong-static` | translation manifest、review gate、research translation state等の静的経路が継続 | 高リスク語義の独立review。research sibling英語draftの独立査読 |
| PQ-10 観測・操作負荷 | `natural-early` / `unmeasured` | E6で「測定のために仕事を増やさない」抽出契約を固定した | **自然作業で実際に残ったoverhead / user judgment**。未測定を埋めるための人工taskは作らない |
| PQ-11 観測来歴 | `strong-static` + `engineering-behavioral` + `natural-early` | executor/evaluator分離、汚染チェック、confounder記録、Living Lab provenanceが揃った | 独立runでこの運用が実際に守られるか |
| PQ-12 回帰可能性 | `strong-static` for known failures | E2/E5の2件を修正前failureから最小回帰fixtureへ落とした | fresh/natural runで新しいfailureが再現した時のloop継続 |

## 5. 初回監査から変わった構造

### 5.1 「実験を設計すること」より「独立性を保って実行すること」が次のボトルネックになった

2026-09-11時点では、主要なbehavioral failure surfaceに固定packetがなかった。

現在、E1〜E5は少なくともengineering trialまたはLayer A trialを経て、E1〜E5すべてでfresh executionへ渡すpacketとexecution後の評価sheetを分離できている。

したがって、同じconversationで追加の模擬runを重ねても、証拠強度は大きく上がらない。次に必要なのは、**前runの出力や評価rubricを直接見ていないexecutorと、execution生成に参加していないevaluatorを使うこと**である。

### 5.2 static checkは増やす対象ではなく、実際のknown failureから育てる段階に入った

E2とE5では、実験中に実在するdriftが見つかり、修正後に最小unit testへ固定できた。

一方、E3/E4で得た診断知見は、既存Method contractで正しく処理できた。この違いを保ち、試行で得た知見をすべて恒久ruleへ変換しないことが重要である。

E7の件数目標は置かない。failureが再現したときだけfixtureを増やす。

### 5.3 PQ-10は意図的に「未測定のまま待つ」部分が残る

E6の空白を埋めるために、人工的な自然作業や追加帳票を作ると、PQ-10を測る行為そのものがPQ-10を悪化させる。

そのため、現時点の`unmeasured`は単なる作業漏れではない。本来の目的で行われた自然作業に、評価可能なartifact・利用者判断・残差再利用が残った時点で初めてE6 Run 001を開始する。

### 5.4 PQ-08は「包装が同じ」ことから「実surfaceで境界が同じ」ことへ進む必要がある

E5 Layer Aは、wrapper driftを見つけられることを実証した。これは静的比較の価値を示している。

しかし、各surfaceで同じsource snapshotとtask packetを使ったときに、authority、provenance、activation、handoffが同じ意味境界を保つかは別問題である。

Layer Bでは文章の一致率を比較せず、P1〜P8の境界違反を比較する。model差やcontext差をplatform効果と即断しない。

## 6. 次の証拠取得順序

### Priority 1 — E3 Run 002

v0.5のMethod分離そのものに対応するため、引き続き最優先とする。

fresh execution / separate evaluationでH1〜H6を確認する。同じfailureが再現した場合のみ最小fixture化またはMethod変更候補へ進む。

### Priority 2 — E1 independent rerun

authority / provenance / disclosure permissionを同時に圧迫するケースを、Run 001 outputを見せずに再実行する。

### Priority 3 — E4 Run 002

fresh snapshot restartでL1〜L10を確認する。これは実時間記憶試験ではないことを維持する。

### Priority 4 — E2 Run 002

paired activationをfresh contextで再実行する。Pair Cはrouting / ownershipまでを観測し、元メモ本文がないままgrouping qualityを主張しない。

### Priority 5 — E5 Run 002

各実surfaceでraw outputを個別生成し、その後に評価する。platform制約とmodel/context confounderを分ける。

### Event-driven — E6 / E7

- E6は自然作業に評価可能な証拠が有機的に残った時だけ開始する。
- E7は具体的なfailureが再現した時点で割り込む。

この順序はrelease gateではなく、現在の証拠空白を効率よく減らすための研究上の順序である。

## 7. release / promotionとの関係

今回の再監査は、v0.5 release readinessやresearch sibling Methodのproduction promotionを承認しない。

特に次を区別する。

- engineering trialのPASS ≠ independent behavioral reliability
- fresh packetの準備完了 ≠ fresh run完了
- static regression fixtureの存在 ≠ 全behavioral failureの網羅
- E1〜E5の良好な結果 ≠ domain専門品質の認証
- product-quality evidenceの充実 ≠ promotion gate通過

また、このconnector環境では今回`make check`、`make research-skill-check`、`make release-check`を実行していない。GitHub Actionsも有効な検証面として使っていないため、repository全体のcheck PASSをこの再監査から主張しない。

## 8. 判定

初回E0で不足していた**実験設計面の空白は大きく縮小した**。

現在の主要な未充足点は次の三群へ収束している。

1. **独立behavioral再現** — E1〜E5のfresh execution / separate evaluation
2. **実surface再現** — 特にE5 Layer B
3. **自然利用の実測** — PQ-10を中心とするE6 natural-work evidence

この段階で大規模な新eval frameworkを追加する必要はない。すでに準備したpacketを独立条件で実行し、実際に再現したfailureだけをE7へ戻す方が価値が高い。

次のrepository内作業では、独立runをこのconversationで擬似実行するのではなく、**実行可能な外部条件が整うまで、静的契約の重複追加を抑える**。自然作業についても、観測のために仕事を作らない。

## 9. 2026-09-18 follow-up

この節は、2026-09-16時点の再監査結果を上書きせず、その後に増えた**準備資産と再現済みfailure**だけを追記する。

### 9.1 E2 Pair Cは、routing-onlyの履歴を残したままgrouping評価へ進める状態になった

Run 001 / Run 002については、当時8件の元メモ本文を固定していなかったため、Pair Cの観測範囲をrouting / ownershipまでとした記録を維持する。後からgrouping qualityまで評価済みだったとは読み替えない。

2026-09-18に、Pair C専用のRun 003を追加した。

- `experiment-004-run-003-execution-packet.md`
- `experiment-004-run-003-evaluation-sheet.md`

Run 003では、N01〜N08をcontrolled comparison用の**合成source material**として固定した。C0はaffinity synthesisのみ、C1はCSWからframework-generated questionを一つだけ渡した後に同じone-round synthesisを行う。正解clusterは事前定義せず、material-led grouping、source return、残差・緊張の保持、framework questionの非権威化、split ownershipを後から評価する。

この変更で「Pair Cのgrouping behaviorを評価するためのsource materialが未固定」という準備上の空白は解消した。ただし、**Run 003はまだ実行していない**。したがってPQ-03 / PQ-04 / PQ-05 / PQ-11のbehavioral evidenceが増えたとは扱わない。増えたのはindependent-readyな実行条件である。

### 9.2 E7 known failureは3件になった

2026-09-16再監査時点では、回帰fixtureへ固定したknown failureを2件としていた。その後、E5の回帰test自体に語句過剰固定があり、意味上同等のcanonical promptを誤ってFAILさせるfailureを隔離実行で再現した。

現在E7で追跡するknown failureは次の3件である。

1. E2 activation fixture responsibility drift
2. E5 OpenAI adapter `default_prompt` semantic drift
3. E5 regression fixture over-specification — 同義表現差をsemantic driftとして誤検出

3件目は、testを特定語句ではなく、条件付き適用、外部委任、compatible affinity-synthesisへの接続、旧来の無条件prompt不在という意味上の不変条件へ縮約して修正した。

この追加もMethod Definitionの新規則ではない。**既に存在する契約を回帰testが過剰に狭く解釈したfailure**として扱う。

### 9.3 repository contractの修正はbehavioral evidenceと分ける

同じ期間に、repository validationでは次の静的不整合も修正した。

- standalone `make test`でもbuildを先行させるようにし、clean checkoutで生成物不足によるfalse failureが混ざりにくい入口へ整えた。
- `make check`のprerequisite列を旧文字列へ固定していたrepository / manual-validation testを、必要targetの存在と順序を検査する形へ修正した。
- natural-Japanese reviewのscope / manifest / blob SHAを再照合し、45件についてmissing 0 / out-of-scope 0 / stale 0 / invalid 0を静的に確認した。
- `product-quality-program.md`はmanifest上ではレビュー済みだったが、人間向けreview index本文から漏れていたため同期した。
- OpenAI Skillでは、canonical adapter YAMLがbuild時に生成先`agents/openai.yaml`へそのまま反映される契約を単体回帰testへ固定した。

これらはPQ-10等の方法論的なbehavioral evidenceではなく、**repository verification surfaceの整合性改善**である。test infrastructureを直したことを、CSWの有効性やbehavioral reliabilityの証拠へ読み替えない。

### 9.4 証拠取得順序の更新

2026-09-16時点のPriority 1〜3は変えない。

1. E3 Run 002
2. E1 independent rerun
3. E4 Run 002

E2については次の二段階に分ける。

4. **E2 Run 002** — activation / depth / split ownershipをfresh contextで確認する。Pair Cは当時のpacket仕様どおりrouting / ownershipまでとする。
5. **E2 Run 003** — Pair Cの固定8件を使い、実groupingでmaterial-led synthesis / provenance / residual retention / split ownershipを別評価する。
6. **E5 Run 002** — 各実surfaceでLayer Bを実行する。

E6 / E7は従来どおりevent-drivenとする。

この更新でも、fresh packetの準備完了とfresh run完了を区別する。Run 003を追加したこと自体は、独立behavioral再現の空白を埋めない。
