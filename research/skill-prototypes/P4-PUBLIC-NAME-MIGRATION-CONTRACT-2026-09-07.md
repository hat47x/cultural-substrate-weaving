# P4 Public Name Migration Contract — 2026-09-07

Status: design-only; research IDs remain canonical inside the research suite

## 目的

Layer 1のresearch ID `affinity-synthesis` と、production installable name候補 `material-led-synthesis` を同一視せず、production promotion時にどの参照を変更し、どの参照を保持するかを固定する。

このcontractはrenameを実行しない。complete-checkout research gate、public-name recheck、English independent reviewが通過するまで `src/skills/` を作らない。

## 基本原則

```text
research identity
  != public installable name
  != display name
  != method lineage term
  != filesystem path
```

一括文字列置換は禁止する。

## 現在の写像

```text
research id                  production installable candidate
----------------------------------------------------------------
cultural-substrate-weaving   cultural-substrate-weaving
affinity-synthesis           material-led-synthesis
iterative-inquiry-synthesis  iterative-inquiry-synthesis
```

Layer 1だけが意図的にresearch/public名を分ける。

## 変更するもの

production promotion時には、少なくとも次をproposed installable nameへ合わせる。

### Skill identity

- production `SKILL.md` frontmatter `name:`
- OpenAI standalone Skill directory name
- Claude/Codex sibling Skill subtree name
- production package target name
- production OpenAI companion metadata path
- explicit runtime handoffでinstallable Skillを名前指定する箇所
- production packageへ選択されたsupport copy中のexplicit installable identifier
- productionへそのまま出るhost-visible adapter prose中のinstallable identifier

Layer 1 の例:

```text
name: material-led-synthesis
```

Layer 2から明示的にsibling Skill名を挙げる場合も、production runtimeでは `material-led-synthesis` を使う。

## 保持するもの

次は機械的にrenameしない。

### Research history

- research directory `research/skill-prototypes/affinity-synthesis/`
- research suite `research_id`
- 過去eval / paired-run / migration record
- research commit history
- research artifactのstable ID

これらは再現性と履歴追跡のため `affinity-synthesis` を保持する。

ここでいう「保持」は **research原本を変更しない** という意味である。現在のruntimeがpackage-local progressive supportとして直接参照し、production locale treeへcopyするeval / evidence等は、production-facing copy内のexplicit installable identifierだけをpublic nameへ投影できる。research側の元file、research path、commit historyは書き換えない。

したがって、たとえば日本語Layer 1の `evals/CASES.md` / `evidence/dossier.md` はresearch原本では `affinity-synthesis` を保持してよいが、production packageへ投影したcopyではinstallable identifierとして `material-led-synthesis` を使う。表示名 `Affinity Synthesis / 親和統合` や方法系譜の語は別である。

### Display / explanatory terms

- `Affinity Synthesis`
- `親和統合`
- `material-led synthesis` という方法説明
- KJ法 / 親和図法 / qualitative integration等のlineage記述

表示名はinstallable identifierではない。

公開時のdisplayは別gateで最終確認する。

## Runtime handoff policy

production runtimeでsibling Skillを指す場合、優先順位は次とする。

1. role / capabilityを自然言語で記述する。
2. installable nameを必要な場合だけ明示する。
3. filesystem sibling pathを前提にしない。
4. unavailableの場合はcompatible realizationへfallbackできる表現を残す。

望ましい例は次のとおりです。

```text
Use `material-led-synthesis` when installed, or another compatible
one-round material-synthesis realization satisfying the same Method Definition.
```

避ける例は次のとおりです。

```text
../affinity-synthesis/
research/skill-prototypes/affinity-synthesis/
```

production runtimeはresearch filesystem layoutを知らない。

## Layer 2 への影響

研究版 `iterative-inquiry-synthesis` は現在 `affinity-synthesis` をresearch companion名として明示している。

これはresearch branchでは変更しない。

production canonical sourceを作る際に、次を別途確認する。

- ja-JP runtimeのexplicit sibling name
- en-US runtimeのexplicit sibling name
- Progressive References内のsibling filesystem wording
- Method Definition内のrealization名
- OpenAI default prompt / bundle descriptionに旧research IDが混入していないか

Layer 2の意味論は変えない。名前だけをproduction projectionに合わせる。

## CSW への影響

CSWは原則としてinstallable nameを強く結び付けず、compatible realizationへのdelegationを表す。

したがってproduction promotionで必要なのは、

- thin ownershipの維持
- `affinity-synthesis` を公開Skill名として前提にする表現があれば除去
- `material-led-synthesis` を必須hard dependencyにしない

ことである。

## Adapter metadata policy

research prototype metadataはresearch IDを含むdirectoryに置いてよい。

production promotion時はproduction pathへコピー・再記述し、production builderがresearch metadataを直接読まない。

Layer 1のproduction candidate:

```text
adapters/openai-skill/{locale}/material-led-synthesis/openai.interactive.yaml
adapters/openai-skill/{locale}/material-led-synthesis/openai.metered.yaml
```

OpenAI sibling prototypeは現在byte-identical promotionを予定している。そのためhost-visible YAML本文にhyphenated research ID `affinity-synthesis` が入った時点で、byte-identical copyは安全ではなくなる。research pathやdisplay term `Affinity Synthesis / 親和統合` は許容するが、production host UIへ識別子として露出する研究IDは許容しない。

Claude/Codex bundle prototypeでは `contains` はresearch側の構成監査情報としてresearch IDを保持してよい。production host catalogへ未知fieldとして持ち込まずdropする。productionへ昇格するhost-visible fieldはsplit-aware `description` だけであり、その本文にはhyphenated research IDを残さない。

production suiteの三Skill構成そのものはproduction suite descriptorがpublic installable identityで保持する。

この境界は `scripts/validate_research_adapter_public_identity.py` で独立に検査する。

## Package / release policy

production package内には `affinity-synthesis` と `material-led-synthesis` を同時に入れない。

公開時のLayer 1 installable treeは一つだけとする。

```text
material-led-synthesis/
```

research IDをcompatibility alias directoryとして追加しない。aliasが必要になる明確なecosystem事情が出た場合は別design decisionとする。

## Lineage policy

公開名変更はKJ法との系譜を隠すためではない。

Method Definition / evidenceでは、

- KJ法®を公式再現・認定Skillと称しない
- 親和図法との近接と差を説明する
- generated-AI-specific safeguardsを明示する

という既存方針を維持する。

## Validation candidates

production canonical sourceを作った後、validatorに最低限次を追加する。

1. sibling production `SKILL.md` frontmatter name = production target name。
2. production package treeにresearch-only `affinity-synthesis` directoryが存在しない。
3. production runtime / adapter metadataに `research/skill-prototypes/` pathがない。
4. Layer 2 production runtimeにsibling filesystem pathがない。
5. explicit Layer 1 installable-name referenceは `material-led-synthesis` に統一される。
6. research suite / eval / migration recordの原本はresearch IDを保持する。
7. production packageへ選択されたsupport copyは、installable identifierとして旧 `affinity-synthesis` を残さない。
8. display / lineage textをidentifier renameと誤認して変更しない。
9. productionへそのまま出るOpenAI metadata本文とClaude/Codex bundle descriptionに、rename対象のhyphenated research IDが残らない。
10. research-only `contains` やresearch filesystem pathにresearch IDが残ること自体は誤検知しない。

## Promotion sequence

```text
complete-checkout research gate PASS
        ↓
public-name collision recheck
        ↓
independent English review
        ↓
production canonical sourceを別pathへ作成
        ↓
identity / handoff / packaged-support referencesだけpublic nameへ投影
        ↓
production build / validator generalization
        ↓
generated-artifact diff review
        ↓
release internal-composition validation
```

## 現時点の判断

- research ID `affinity-synthesis` は維持する。
- production candidateは `material-led-synthesis`。
- renameはproduction projectionでのみ行う。
- research原本の履歴ID保持と、production-facing support copyのpublic-name投影を両立させる。
- display `Affinity Synthesis / 親和統合` はinstallable nameと独立に扱う。
- runtime handoffはrole-first、name-second、filesystem-independentとする。
- host-visible adapter proseもpublic identity境界に含めるが、research-only `contains` / pathは履歴・監査情報として保持できる。
- research historyをpublic-name renameで書き換えない。
