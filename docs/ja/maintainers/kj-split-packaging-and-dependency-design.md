# KJ系技能分離 — パッケージングと依存設計

作成日: 2026-09-06

Status: research design; runtime build not yet changed

## 1. 問題

KJ法由来の技能を次の三層へ分ける設計が固まりつつある。

1. `affinity-synthesis` — 一回の材料主導統合。
2. `iterative-inquiry-synthesis` — 複数roundの差分・再開・停止管理。
3. `cultural-substrate-weaving` — 文化体系を認知場として投入し、帰属を保って対象へ返す専門Skill。

しかし、公開Agent Skillの一般仕様には、別Skillを依存先として自動インストールする標準的な `dependencies` 契約がない。

そのため、CSWからKJ実装を完全に削除し、外部の `affinity-synthesis` が必ず存在すると仮定すると、利用環境によってはCSWだけがインストールされ、統合処理を呼び出せない。

一方、三Skillへ同じ手順をコピーすると、方法正本が三つに分裂する。

必要なのは、**方法定義を一つに保ちながら、配布単位だけを環境に合わせて変えられる構造**である。

## 2. 現行リポジトリの制約

現行 `src/manifest.json` は単一Skill前提である。

```text
name: cultural-substrate-weaving
router: ROUTER.md
modules: [...]
knowledge_groups: {...}
```

`build.py` も `config["name"]` を一つだけ読み、OpenAI Skill、Claude Plugin、Codex Plugin、ChatGPT GPT、Microsoft Copilotを一組生成する。

Claude/Codexについては、plugin manifestが `skills/` ディレクトリを参照するため、一つのplugin内へ複数Skillを置く技術的余地がある。

一方、OpenAI Skillのstandalone生成は一つのSkill directoryを前提としている。ChatGPT GPTとMicrosoft Copilotはさらに一段上の「agent realization」であり、Agent Skillの複数directoryをそのまま公開するモデルではない。

validatorも単一Skillの名前・byte budget・marketplace entryを固定前提としている。

したがって、`src/manifest.json` を即座に複数Skillへ変えるのではなく、まず配布モデルを決めてからbuild/validation contractを一度に更新する。

## 3. 方法定義と配布単位を分ける

```text
Method Definition
      ↓ realized as
Agent Skill A / Agent Skill B / embedded agent procedure
      ↓ packaged as
standalone skill / multi-skill plugin / composite GPT
```

方法の意味境界は配布形式に従属させない。

`affinity-synthesis` のMethod Definitionは一つだけ持つ。Claude向け、OpenAI向け、CSW内fallback向けに別々の方法文章を正本化しない。

## 4. 比較した配布案

### 案A — 三Skillを完全に別リポジトリへ分ける

長所:

- 所有範囲が明確。
- release cycleを独立できる。
- `affinity-synthesis` をCSWと無関係に発見・導入しやすい。

短所:

- Agent Skills仕様にdependency resolverがないため、CSWだけ導入された場合の保証がない。
- 初期段階では三repoのCI、translation、release、issue管理が増える。
- 方法がまだ評価中の段階で物理repo境界を固定しすぎる。

判定: **将来候補。初回分離には早い。**

### 案B — 一つのCSW Skillの内部moduleとしてだけ分離する

長所:

- 現行buildをほぼ維持できる。
- dependency問題がない。

短所:

- `affinity-synthesis` を単独で利用できない。
- KJ系統合のrelease cycleがCSWへ縛られる。
- Method DefinitionとCSWの専門探索責務の分離が公開上見えない。

判定: **不採用。今回の分離目的を満たさない。**

### 案C — 同一repo・同一plugin bundleに三つの独立Skillを同梱する

例:

```text
plugin/<locale>/skills/
  cultural-substrate-weaving/SKILL.md
  affinity-synthesis/SKILL.md
  iterative-inquiry-synthesis/SKILL.md
```

長所:

- CSWとcompanion skillsを一度にインストールできる。
- 標準dependency fieldがなくても、同じplugin package内に必要なSkillが存在する。
- 各Skillは独立したdescription / activation boundaryを持てる。
- sourceは一つに保ち、build時に複数Skillへ生成できる。

短所:

- `cultural-substrate-weaving` というplugin名で一般的な親和統合Skillまで入るため、bundle名と内容の射程がずれる。
- host側がsibling Skillを必ず自動選択・連携するとは限らない。
- OpenAI standalone Skill等ではbundleという概念が同じ形で使えない。

判定: **初回分離の最有力。**

### 案D — 同一repoから三つを独立packageとしてのみ出す

長所:

- repoは一つ、公開Skill名は独立。
- standalone利用が明確。

短所:

- CSW利用者がcompanion skillを別途導入しない可能性がある。
- dependency問題が残る。

判定: **案Cと併用する。**

## 5. 推奨する移行形

初回公開では、**同一repoをmethod suiteのsource repositoryとして使い、配布面ではbundleとstandaloneの両方を生成する**。

### Source

```text
src/
  manifest.json                  # suite-level manifestへ発展
  skills/
    cultural-substrate-weaving/
      ja-JP/...
      en-US/...
    affinity-synthesis/
      ja-JP/...
      en-US/...
    iterative-inquiry-synthesis/
      ja-JP/...
      en-US/...
```

これは将来案であり、現行 `src/<locale>/` を直ちに移動しない。

### Claude / Codex

一つのlocale pluginへ三Skillを同梱する。

```text
skills/
  weave/SKILL.md
  affinity-synthesis/SKILL.md
  iterative-inquiry-synthesis/SKILL.md
```

`weave` がLayer 1/2の全文を再実装しない。

### OpenAI Agent Skill

各Skillをstandalone directoryとして生成する。

```text
dist/<locale>/openai-skill/<profile>/
  cultural-substrate-weaving/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

必要なら三SkillをまとめたZIPも別に作れるが、Skill directoryそのものは独立させる。

### ChatGPT GPT / Microsoft Copilot

これらはAgent Skill directoryのbundleではなくagent realizationなので、当面は **CSW composite realization** を維持する。

ただし内部知識・手順の正本は分離後のMethod Definitionからbuildする。つまり、UI上は一つのGPT/agentでも、内部ではLayer 1 / Layer 2 / Layer 3の境界を保つ。

将来、各methodを別GPT/agentとして公開する価値が出た場合にのみ増やす。

## 6. Hard dependencyを置かない

CSWのruntime文には、次のような断定を置かない。

> 必ず `affinity-synthesis` Skillを呼び出せ。

hostによってSkill routing機構が異なるためである。

代わりに、責務境界を次のように持つ。

```text
if a compatible affinity-synthesis realization is available:
    delegate one-round material integration to it
else:
    preserve the minimal handoff contract and avoid pretending the missing method ran
```

ただし、このfallbackがLayer 1全文の複製になってはいけない。

## 7. Minimal fallback contract

CSW側に残せるfallbackは、方法手順ではなく**安全な接続境界**だけとする。

例えば:

- framework-generated candidateをtarget-supported findingへ自動昇格させない。
- target materialの意味を文化体系へ合わせて分類しない。
- 統合Skillが利用できない場合、カード化・表札・A/B統合を「実行済み」と称さない。
- frameworkから得た問い・仮説・残差を、その由来を保ったままcallerへ返す。

これなら、Layer 1が無い環境でもCSWは嘘のKJ実行をせず、文化体系探索だけを安全に完了できる。

## 8. Sibling Skill routingはoptimizationとして扱う

三Skillを同じpluginへ同梱しても、hostが常に自動でsibling Skillを呼ぶ保証をMethod Definitionに入れない。

同梱は次を改善する**realization-level optimization**である。

- discovery
- install completeness
- likely routing availability
- consistent version pairing

方法の正しさはsibling auto-callへ依存させない。

## 9. Versioning

初期段階ではsuite全体に一つのrepository release versionを持つ案が扱いやすい。

各Skillには別途method/realization versionを持てるようにする。

```text
repository release: 0.5.0

skills:
  cultural-substrate-weaving realization: 0.5.x
  affinity-synthesis realization: 0.1.x
  iterative-inquiry-synthesis realization: 0.1.x
```

repository release versionとcognitive method versionを同一視しない。

十分に成熟しrelease cycleが乖離した時点で、別repoへの抽出を再検討する。

## 10. Naming and bundle identity

短期的には既存repo名 `cultural-substrate-weaving` を維持してよい。

ただし三Skillを恒久的に同梱するなら、将来はrepository / marketplace bundleの表示名を中立化する余地がある。

候補例:

- `material-led-inquiry-skills`
- `emergent-synthesis-skills`
- `affinity-inquiry-skills`

現段階でrenameは行わない。方法名がまだresearch candidateであり、repo renameが別の大きなmigrationを発生させるためである。

## 11. Build migration plan

現行releaseを壊さず、次の順で進める。

### Phase P0 — research prototypes

現在地。

- `research/skill-prototypes/affinity-synthesis/`
- `research/skill-prototypes/iterative-inquiry-synthesis/`
- paired eval / large-set retrospective
- external-skill assimilation

### Phase P1 — suite manifest prototype

runtime `src/manifest.json`とは別に、research用の複数Skill manifestを作る。

検証項目:

- skill id/name collision
- locale parity
- source reference ownership
- per-skill byte budget
- sibling bundle layout
- standalone layout

### Phase P2 — build/validator generalization

`manifest()` を単一Skill configではなくsuite configへ拡張する。

重要:

- `build_openai`: skillごとにstandalone directory生成
- `build_claude`: 一plugin内へ複数skills生成
- `build_codex_plugin`: skills rootはそのまま利用可能
- `validate`: skillごとのfrontmatter、references、byte budget、locale parityを検査
- `package`: standalone Skill packagesとbundle packageを区別

### Phase P3 — canonical source migration

prototypeとcurrent CSWのpaired evaluationを通過後、

- Layer 1をcanonical skill sourceへ昇格
- Layer 2をcanonical skill sourceへ昇格
- CSW `integration.md` / `iteration.md` を接続契約へ縮小

### Phase P4 — public naming / release

- trademark presentation再確認
- repository / bundle identity再評価
- README / marketplace / docs更新
- release gate全通過

## 12. 推奨決定

現時点では次を採る。

> **同一repoに三つの独立Method/Skill sourceを置き、Claude/Codexでは一つのpluginに同梱し、standalone Skillを必要とする環境では個別に生成する。**

> **CSWはhard dependencyを宣言せず、sibling Skillが利用可能なら委譲し、不在時には文化体系探索と帰属保持までで安全に停止できる。**

> **ChatGPT GPT / Microsoft Copilotのようなagent realizationは、当面一つのCSW compositeを維持してよい。Method Definitionまで一体化しない限り、公開面の粒度が異なることは問題ではない。**

この形は、Method Definition ≠ Realization ≠ Packageという既存の設計原則とも整合する。
