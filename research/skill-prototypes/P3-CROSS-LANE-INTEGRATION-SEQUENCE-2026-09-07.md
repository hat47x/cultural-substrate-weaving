# CSW改善 cross-lane integration sequence — 2026-09-07

> 2026-09-08 source-contract refresh: A→B→Cという統合原則は維持しつつ、P4で収束したproduction source contractを反映した。
>
> 2026-09-08 package-closed refinement: sibling `locale_tree`自体をruntime package境界とし、builder側のresearch-only除外filterへ責務を逃がさないこと、research→production source mappingはread-only planとして先に観測することを追補した。

## 目的

CSW改善では、方法論の責務分離、research prototype、package topology、production builder/validator、production inclusion、Living Lab評価が複数レーンで並行して進んでいます。

各レーンで先へ進めることと、productionへ昇格してよいことは同義ではありません。本書は、他レーンの未完了判断をproduction都合で先取りしないために、**耐久的な統合順序、停止条件、レーン責務、promotion開始条件**だけを共有します。

## この文書が正本とするもの／しないもの

本書が正本として持つのは次です。

- A → B → Cという統合の考え方
- 各グループの停止条件
- レーンごとの責務
- production source contractの耐久的な境界
- production promotionを始めるための条件

一方、次のような変化の速い状態は本書の正本にしません。

- 各PRのopen/closed/mergeable等のlifecycle
- 各Skillのlocale realizationの現在状態
- adapter metadataの現在のmaturity
- public/installable name候補の最新値
- active research branchでの最新prototype状態
- complete-checkout commandの現在のPASS/FAIL

これらはそれぞれのowning authorityを参照します。

```text
PR current state
  -> 各PR

research realization / naming / review current state
  -> suite manifest / P4 descriptor / owning research branch

host materialization implementation
  -> owning package-research branch

complete-checkout execution state
  -> dedicated execution-status record
```

本文で時点依存の状態に触れる場合も、参考例としてのみ扱います。

## 方法論側の共通前提

次は、production側が先回りしないための耐久的な前提です。

- KJ系技能をCSW本体から分離する方向は有力です。
- 一回の材料統合と、複数roundの探索継続は別責務として扱います。
- research内部のSkill identityとpublic/installable nameは同一概念ではありません。
- `affinity-synthesis`はone-round material synthesisのresearch identityであり、公開名称をその文字列へ固定するものではありません。
- `iterative-inquiry-synthesis`はmulti-round inquiry orchestrationのresearch identityとして扱います。
- CSWは文化的体系による探索、体系由来候補の帰属、対象側への戻しを中心責務として残す方向です。
- CSW → Iterative → one-round synthesisのhandoffでは、framework由来候補のprovenance / epistemic statusを保持し、target-side supportへ無言で昇格させません。
- compatible one-round synthesisが必要なのに利用できない場合、未実行の処理を実行済みと扱いません。
- research branch上のthin canonical ownership experimentは進めてよいが、その結果をhandoff・評価・promotion gateなしにdevelop / production baselineへ昇格しません。
- package、translation、adapter metadata等のprototypeが存在することは、production readyを意味しません。

## 統合グループA — research parity / host-package contract

### 目的

production buildへ入る前に、research側で予定package形と既存CSWの不変条件を観測します。

### 二層のmaterialization境界

host package materializerの恒久実行経路は一つにしますが、低位のSkill-tree materializerとhost package外周は別責務として保ちます。

```text
low-level Skill-tree materializer
  -> canonical/package sourceからskills/* subtreeをmaterialize

host-package materializer
  -> low-level treeを再利用
  -> OpenAI / Claude / Codex固有metadataを外側へ付加
  -> staging / failure atomicityを所有
```

したがって、既存CSW `skills/weave/` のbyte parityを低位materializerに対して固定するoracleと、host package全体のcross-surface oracleは競合しません。

残す価値が高いinvariantは次です。

```text
CSW subtree
  - ja-JP / en-USのtracked production weave subtreeとbyte parity
  - Claude / Codexでshared Skill tree semanticsを維持

OpenAI
  - interactive / meteredで agents/openai.yaml を除くSkill treeがbyte-identical
  - packaged agents/openai.yaml がdeclared metadata sourceとbyte-identical

Claude / Codex
  - 同localeで skills/ subtreeがbyte-identical
  - bundle metadata wordingとrepository VERSION由来manifestがdriftしない

共通
  - repository外にのみmaterializeする
  - failure時にpartial final outputを残さない
  - prototypeをproduction reviewedとして扱わない
  - packageとして宣言したMarkdown内部の参照閉包をruntime entry一段だけに限定しない
```

### 統合条件

- 既存CSW subtreeのbyte parityが実測で確認できること。
- host package生成がstaging等を使い、途中失敗時にpartial final outputを残さないこと。
- host-specific probeで得たoracleを汎用host materializer/testへ核融合できていること。
- packageに宣言されたMarkdownの多段参照がpackage root外やundeclared fileへ漏れないこと。
- 古くなったlocale readiness前提を固定testとして残さないこと。
- complete checkoutで関連unit testを実行できること。

## 統合グループB — production mechanical refactor

### 目的

公開Skill集合を変えずに、production内部のmechanicsだけを複数Skillへ拡張可能な形へ整えます。

対象は、Skill tree writerやartifact validation等のmechanicalな責務です。

### Writer境界

production writerは、source-formatの意味判断と最終tree書き込みを分離します。

```text
canonical_manifest source resolver
  -> frontmatter-free rendered body + references
  -> low-level writer

locale_tree source adapter
  -> package-closed canonical Skill tree
  -> 明示されたentry/content transform
  -> relative pathを保ったtarget tree copy
```

低位writerを「全source kindをそのまま飲み込む万能renderer」にしません。特に、frontmatterを持つcanonical `SKILL.md`をfrontmatter-free bodyとして誤投入し、二重frontmatterを生成しないようにします。

`locale_tree`では、runtimeに含めないresearch-only fileをbuilderが後から除外する設計を採りません。production source root自体をpackage-closedにし、builderはその境界を信頼してcopyします。rename、frontmatter name、明示installable-name等の必要なcontent transformはpromotion/source-adapter contractへ明示し、暗黙の文字列置換へしません。

### Validator境界

validator側も、production対象Skillを選ぶ責務と、解決済みsource/artifactを検査する責務を分けます。

```text
production authority / source resolver
  -> locale_tree source package purity
  -> source / generated subtree parity
  -> generated artifact paths
  -> runtime-entry budget
  -> installed package-local reference closure
```

writerだけが複数Skill対応し、validatorが単一Skill前提のまま残る状態を許しません。また、generated treeが正しいだけでは不十分で、`locale_tree` source自身にruntime外fileを混在させてbuilder filterへ責務を逃がしていないことも検査対象とします。

### 統合条件

- production Skill数を増やさないこと。
- canonical method contentを変更しないこと。
- host metadataの意味を変えないこと。
- current CSW path / name / frontmatter / reference bytesを変えないこと。
- `generated-artifacts-check`で既存生成物に意図しない差分が出ないこと。
- validation report schemaや既存token budget semanticsを変えないこと。
- future `locale_tree`検査がsource purity / generated parity / installed closureを別々に観測できる設計であること。
- complete checkout上で`make check`を実行すること。

## 統合グループC — production inclusion boundary

### 目的

「researchで作れるSkill」と「productionに含めるSkill」を明示的に分けます。

production descriptorは、方法論側の候補を自動発見しません。他レーンで明示的な昇格判断が終わったSkillだけを受け入れます。

### 依存関係

P4でsource-mode設計が収束したため、production inclusionの耐久的な順序は次とします。

```text
research inclusion decision
  -> production source contract
  -> read-only research-to-production source promotion plan
  -> promotion mapping / exclusion / transform inspection
  -> thin production suite descriptor
  -> source-kind resolver / adapter
  -> current-build parity guardの意図的置換
  -> intentional multi-Skill wiring
```

read-only promotion planは、research側でpackage対象として既に選ばれたfileをfuture production sourceへどう対応させるか、何をresearch-onlyとして残すか、どのrename/content transformが必要かを観測するためのものです。production `src/skills`を作るmutationでも、promotion authorizationでもありません。

旧い`id + source_manifest`一種類のprojectionをfuture multi-Skill schemaとして暗黙拡張しません。

current one-Skill buildとdescriptorのずれを防ぐexact-one gate等をmigration期間に置く場合、そのgateは恒久制約ではなく、**二つ目のSkill追加とsource-kind wiringを同じ意図的変更にするためのfail-closed guard**として扱います。

## グループ間の推奨順

production出力を変えない範囲では、次を推奨します。

```text
A: research parity / host-package contract
        ↓
B: production mechanical refactor
        ↓
C: production inclusion boundary
```

厳密なコード依存では一部を並行できますが、レビュー上は、

1. research側で予定形と不変条件を観測する
2. production mechanicsを出力不変で一般化する
3. production source / inclusion authorityを明示する
4. read-only source promotion planでmapping・除外・transformを点検する
5. その後にだけmulti-Skill wiringを行う

という順にすると、意味上の原因を追いやすくなります。

## A〜Cを終えても止める境界

A〜Cをすべて整えても、次は別のpromotion phaseです。

- production descriptorへのcompanion追加
- multi-Skill build outputの有効化
- marketplace / release ZIPへのcompanion追加
- thin-CSW ownership変更のdevelop / production昇格
- locale/hostごとのcompanion公開

A〜Cは「昇格可能なmechanicsとcontractを整えた」ことを意味しても、「昇格してよい」というauthorizationではありません。

## 方法論レーンから必要なpromotion input

production multi-Skill wiringへ進む前に、少なくとも次を他レーンと照合します。

### 名称

- research identityとは別にpublic/installable nameを採用する判断があるか。
- 「KJ法」という一般名を過度に代表する名称になっていないか。
- 既存のAffinity Mapping系Skill等との役割差が利用者に説明可能か。
- production promotion直前に名称衝突を再確認したか。

### 責務

- one-round material synthesisとmulti-round orchestrationの境界が安定しているか。
- CSW固有のframework exploration / attributionがcompanion側へ漏れていないか。
- Iterative側へgrouping algorithmを複製していないか。
- one-round側へ文化体系由来の意味づけを埋め込んでいないか。
- CSW固有のtension / sublation ownershipをgeneric layerへ移していないか。

### Handoff

- framework由来statusがhandoff後も保存されるか。
- target-supported findingとの二重計上を防げるか。
- compatible synthesis不在時を実行済みと誤認しないか。
- carry-forward stateをreopen / continuation authorityと混同しないか。
- delayed reactivation / residual / untouched regionを保持できるか。

### 評価

- same-authoring-session fixtureだけでなく、独立性の高い実タスク評価があるか。
- one-round synthesisが実際に必要になるroundを含むか。
- 長期session handoffを含むか。
- useful nonuse / stoppingを観測できるか。
- Living Labの観察を単発scoreへ還元していないか。

### Locale / host

- translation source-hash refreshと独立English reviewを混同していないか。
- locale単位の段階公開を認めるか。
- host metadataがproduction review済みか。
- README / marketplace等のpackage外周文面が新しい構成に追随しているか。
- 実hostでinvocation / routing behaviorを確認したか。

## Production source contract — resolved design boundary

production wiringを始める前に確定すべきsource contractについて、P4では次の二つのmodeを別物として扱う設計へ収束しています。

### `canonical_manifest`

既存CSWのsource contractです。

```text
production source
  -> src/manifest.json
  -> locale router + canonical modules
  -> runtime entry render + manifest-declared references
```

`src/manifest.json`はCSW一Skillのruntime manifestとして維持し、generic suite manifestへ変形しません。

### `locale_tree`

sibling Skillのproduction canonical source候補です。

```text
src/skills/<installable-name>/<locale>/
  SKILL.md
  references/...
  [runtime packageに含めるfileだけ]
```

このlocale tree自体を **package-closed production source boundary** とします。builderはrelative pathを保ってtreeをcopyし、research-only fileを除外するfilterを持ちません。

したがって、maintainer-only migration record、未参照のresearch evidence、review packet、promotion rationale等をproduction locale treeへ置いて「build時に落とす」設計にしません。runtimeからprogressive referenceされるeval/evidence等はpackage contentとして入れられますが、存在するresearch materialを自動的にproductionへ昇格させることはしません。

locale treeはcanonical `SKILL.md`を持つため、CSWのrouter-render pathへ無理に正規化しません。relative pathを保ったcopy / source-kind固有entry transformとして扱います。

英語incubation sourceの`.en.md`等をproduction canonical filenameへ正規化する必要がある場合も、renameとpackage-local reference/content transformをpromotion planへ明示し、source filenameの偶然やresearch IDから暗黙推測しません。

### Research → production source promotion planning

research sourceからproduction `locale_tree`へ進む前に、read-only planで少なくとも次を可視化します。

```text
research package_source.files
  -> promotion candidate mappings

research metadata not selected by package_source
  -> excluded / research-only

research identity / incubation filename
  -> explicit production target / rename

content-level public-name or realization rewrite
  -> explicit transform declaration
```

このplanの存在やvalidator通過はproduction mutationではありません。実際のproduction source作成、builder wiring、artifact generation、release validation、promotion authorizationを別段階として残します。

### Production suite descriptor

二つのsource modeを束ねる薄いproduction descriptorを、既存CSW manifestとは別責務として扱います。working pathはP4設計上 `src/skill-suite.json` です。

そのdescriptorが所有するのは、概ね次です。

```text
suite identity / locale set
production-included Skill identities
production source mode / source path
distribution target names
production adapter metadata source
bundle composition
```

含めないもの:

```text
research eval history
migration discussion
paired-run evidence
unresolved naming debate
promotion rationale
research-only maturity state
```

research `suite-manifest.json`、research P4 descriptor、research adapter prototypeをproduction builderが直接読む第三経路は作りません。

## Identity境界

次の三つを分離します。

```text
research identity
public/installable name
distribution target name
```

P4のある時点では、one-round layerについて、

```text
research identity: affinity-synthesis
public/installable candidate: material-led-synthesis
```

という関係が使われていますが、最新のpublic-name authorityはowning P4 descriptor / naming gate側に置きます。

同様にCSWは、同じSkillでもdistribution targetが、

```text
OpenAI: cultural-substrate-weaving
Claude/Codex: weave
```

となり得ます。

したがってbuilderはresearch IDからhost target名を推測しません。

## Production wiring開始条件

次の全体像が揃って初めて、production descriptorへ二つ目以降のSkillを追加する変更を検討します。

```text
method boundary stable enough
        +
handoff / fallback evidence acceptable
        +
CSW-specific tension / sublation ownership preserved
        +
translation source tracking synchronized
        +
independent English review acceptable
        +
public naming decision + immediate recheck
        +
production source contract resolved
        +
read-only source promotion mapping / exclusion / transform plan internally consistent
        +
production metadata review
        +
generic writer / validator integrated
        +
current CSW parity verified
        +
generic host materialization contract consolidated
        +
package / release validators prepared
        +
real-host invocation / routing evidence
        +
complete-checkout execution evidence
```

これらを単一`ready=true`へ潰しません。異なる由来・強さのevidenceを互いの代用品として扱わず、promotion authorizationは別判断とします。

## レーン間の責務

- 方法論レーン: 何を別Skillとして成立させるかを決めます。
- 評価/Living Labレーン: 分離が実タスクで何を保ち、何を失うかを観察します。
- package researchレーン: hostごとの予定形をproduction外で検証し、host package実行経路を一つに保ちます。
- production mechanicsレーン: 公開集合を変えずにwriter/validatorを一般化します。
- production inclusionレーン: 方法論側の判断を先取りせず、公開集合・source mode・distribution target・source promotion mappingの境界を明示します。

**production inclusionレーンは、他レーンで確定していない意味上の判断を代行しません。方法論レーンは、production mechanicsの都合だけでcanonical分離を急ぎません。**

## 結論

production側で先に固定するのは「どの候補を公開するか」ではなく、**既存CSWを壊さず、異なるsource kindとidentityを混同せず、package-closed sourceから生成と検査を対称に拡張できる境界**です。

そのうえで、research evidence、naming、locale review、host behavior、complete-checkout executionが揃った段階に限り、intentional multi-Skill wiringへ進みます。
