# CSW改善 cross-lane integration sequence — 2026-09-07

## 目的

CSW改善では、方法論の責務分離、research prototype、package topology、production builder/validator、production inclusion、Living Lab評価が複数レーンで並行して進んでいます。

各レーンで先へ進めることと、productionへ昇格してよいことは同義ではありません。本書は、他レーンの未完了判断をproduction都合で先取りしないために、**耐久的な統合順序、停止条件、レーン責務、promotion開始条件**だけを共有します。

## この文書が正本とするもの／しないもの

本書が正本として持つのは次です。

- A → B → Cという統合の考え方
- 各グループの停止条件
- レーンごとの責務
- production promotionを始めるための条件

一方、次のような変化の速い状態は本書の正本にしません。

- 各PRのopen/closed/mergeable等のlifecycle
- 各Skillのlocale realizationの現在状態
- adapter metadataの現在のmaturity
- active research branchでの最新prototype状態

これらは次を参照します。

```text
PR current state
  -> 各PR

research realization current state
  -> suite manifest / owning research branch

host materialization implementation
  -> owning package-research branch
```

本文で時点依存の状態に触れる場合も、参考snapshotとしてのみ扱います。

## 方法論側の共通前提

次は、production側が先回りしないための耐久的な前提です。

- KJ系技能をCSW本体から分離する方向は有力です。
- 一回の材料統合と、複数roundの探索継続は別責務として検討します。
- `affinity-synthesis` / `iterative-inquiry-synthesis` はworking nameであり、公開最終名とは限りません。
- CSWは文化的体系による探索、体系由来候補の帰属、対象側への戻しを中心責務として残す方向です。
- CSW → Iterative → Affinityのhandoffでは、framework由来候補のprovenance / epistemic statusを保持し、target-side supportへ無言で昇格させません。
- compatible one-round synthesisが必要なのに利用できない場合、未実行の処理を実行済みと扱いません。
- canonical `integration.md` / `iteration.md` は、分離後のhandoffと評価が十分になるまで縮小しません。
- package、translation、adapter metadata等のprototypeが存在することは、production readyを意味しません。

## 統合グループA — research parity / host-package contract

### 目的

production buildへ入る前に、research側で予定package形と既存CSWの不変条件を観測します。

### 重要な収束方針

hostごとの検査観点は複数あっても、**host package materializerの恒久実行経路は一つにします。**

OpenAI専用、Claude/Codex専用のprobeから得た強いinvariantは、単一の汎用host materialization contractへ吸収します。専用scriptを第二正本として恒久維持しません。

残す価値が高いinvariantは、例えば次です。

```text
OpenAI
  - interactive / meteredで agents/openai.yaml を除くSkill treeがbyte-identical
  - packaged agents/openai.yaml がdeclared metadata sourceとbyte-identical

Claude / Codex
  - 同localeで skills/ subtreeがbyte-identical
  - bundle metadata wordingとrepository VERSION由来manifestがdriftしない

共通
  - repository外にのみmaterializeする
  - failure時にpartial outputを残さない
  - prototypeをproduction reviewedとして扱わない
```

### 統合条件

- 既存CSW subtreeのbyte parityが実測で確認できること。
- host package生成がstaging等を使い、途中失敗時にpartial final outputを残さないこと。
- 専用probeで得たoracleを汎用materializer/testへ核融合できていること。
- 古くなったlocale readiness前提を固定testとして残さないこと。
- complete checkoutで関連unit testを実行できること。

## 統合グループB — production mechanical refactor

### 目的

公開Skill集合を変えずに、production内部のmechanicsだけを複数Skillへ拡張可能な形へ整えます。

対象は、Skill tree writerやartifact validation等のmechanicalな責務です。

### 統合条件

- production Skill数を増やさないこと。
- canonical method contentを変更しないこと。
- host metadataの意味を変えないこと。
- `generated-artifacts-check`で既存生成物に意図しない差分が出ないこと。
- validation report schemaや既存token budget semanticsを変えないこと。
- complete checkout上で`make check`を実行すること。

## 統合グループC — production inclusion boundary

### 目的

「researchで作れるSkill」と「productionに含めるSkill」を明示的に分けます。

production descriptorは、方法論側の候補を自動発見しません。他レーンで明示的な昇格判断が終わったSkillだけを受け入れます。

### 依存関係

production inclusionは、少なくとも次の順序で進めます。

```text
research inclusion decision
  -> minimal production Skill-set
  -> read-only resolver / current-build parity
  -> intentional multi-Skill wiring
```

multi-Skill wiring前にexact-one legacy gate等を置く場合、そのgateは恒久制約ではなく、公開集合の変更とbuild wiringを同じ意図的変更にするためのmigration guardとして扱います。

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
3. inclusion判断を外在化する

という順にすると、意味上の原因を追いやすくなります。

## A〜Cを終えても止める境界

A〜Cをすべて整えても、次は別のpromotion phaseです。

- production descriptorへのcompanion追加
- multi-Skill build outputの有効化
- marketplace / release ZIPへのcompanion追加
- canonical KJ/iteration責務の削減
- locale/hostごとのcompanion公開

## 方法論レーンから必要なpromotion input

production multi-Skill wiringへ進む前に、少なくとも次を他レーンと照合します。

### 名称

- working nameを公開名として採用するか。
- 「KJ法」という一般名を過度に代表する名称になっていないか。
- 既存のAffinity Mapping系Skill等との役割差が利用者に説明可能か。

### 責務

- one-round material synthesisとmulti-round orchestrationの境界が安定しているか。
- CSW固有のframework exploration / attributionがcompanion側へ漏れていないか。
- Iterative側へgrouping algorithmを複製していないか。
- Affinity側へ文化体系由来の意味づけを埋め込んでいないか。

### Handoff

- framework由来statusがhandoff後も保存されるか。
- target-supported findingとの二重計上を防げるか。
- compatible synthesis不在時を実行済みと誤認しないか。
- delayed reactivation / residual / untouched regionを保持できるか。

### 評価

- same-authoring-session fixtureだけでなく、独立性の高い実タスク評価があるか。
- one-round synthesisが実際に必要になるroundを含むか。
- 長期session handoffを含むか。
- useful nonuse / stoppingを観測できるか。
- Living Labの観察を単発scoreへ還元していないか。

### Locale / host

- locale単位の段階公開を認めるか。
- host metadataがproduction review済みか。
- README / marketplace等のpackage外周文面が新しい構成に追随しているか。
- 実hostでinvocation / routing behaviorを確認したか。

## Production Skill-set source contract

production wiringを始める前に、**production Skill-set source contractを確定**します。

現在の単一CSWを`id + source_manifest`で表すcontractが妥当でも、将来のcompanion canonical sourceがlocale treeになる場合、そのまま二件目へ追加できるとは限りません。

promotion時には、少なくとも次のどちらかをproduction側で明示的に決めます。

1. companionにも薄いproduction manifestを持たせ、既存`source_manifest`型へ揃える。
2. production Skill-set schemaをversion-upし、`manifest` / `locale_tree`等のsource kindを区別して表現・検査する。

research `suite-manifest.json`やpromotion planning descriptorをproduction builderが直接読む第三経路は作りません。

## Production wiring開始条件

次の全体像が揃って初めて、production descriptorへ二つ目以降のSkillを追加する変更を検討します。

```text
method boundary stable enough
        +
handoff/fallback evidence acceptable
        +
public naming decision
        +
production Skill-set source contract resolved
        +
production metadata review
        +
generic writer/validator integrated
        +
current CSW parity verified
        +
host materialization contract consolidated
        +
package/release validators prepared
        +
full checkout make check available
```

## レーン間の責務

- 方法論レーン: 何を別Skillとして成立させるかを決めます。
- 評価/Living Labレーン: 分離が実タスクで何を保ち、何を失うかを観察します。
- package researchレーン: hostごとの予定形をproduction外で検証し、実行経路を一つに保ちます。
- production mechanicsレーン: 公開集合を変えずにwriter/validatorを一般化します。
- production inclusionレーン: 方法論側の判断を先取りせず、公開集合とsource contractの境界を明示します。

**production inclusionレーンは、他レーンで確定していない意味上の判断を代行しません。方法論レーンは、production mechanicsの都合だけでcanonical分離を急ぎません。**
