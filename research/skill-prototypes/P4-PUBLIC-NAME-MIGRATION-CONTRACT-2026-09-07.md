# P4 Public Name Migration Contract — 2026-09-07

Status: design-only; research IDs remain canonical inside the research suite

## 目的

Layer 1 の research ID `affinity-synthesis` と、production installable name 候補 `material-led-synthesis` を同一視せず、production promotion 時にどの参照を変更し、どの参照を保持するかを固定する。

この contract は rename を実行しない。complete-checkout research gate、public-name recheck、English independent review が通過するまで `src/skills/` を作らない。

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

Layer 1 だけが意図的に research/public 名を分ける。

## 変更するもの

production promotion 時には、少なくとも次を proposed installable name へ合わせる。

### Skill identity

- production `SKILL.md` frontmatter `name:`
- OpenAI standalone Skill directory name
- Claude/Codex sibling Skill subtree name
- production package target name
- production OpenAI companion metadata path
- explicit runtime handoff で installable Skill を名前指定する箇所

Layer 1 の例:

```text
name: material-led-synthesis
```

Layer 2 から明示的に sibling Skill 名を挙げる場合も、production runtime では `material-led-synthesis` を使う。

## 保持するもの

次は機械的に rename しない。

### Research history

- research directory `research/skill-prototypes/affinity-synthesis/`
- research suite `research_id`
- 過去 eval / paired-run / migration record
- research commit history
- research artifact の stable ID

これらは再現性と履歴追跡のため `affinity-synthesis` を保持する。

### Display / explanatory terms

- `Affinity Synthesis`
- `親和統合`
- `material-led synthesis` という方法説明
- KJ法 / 親和図法 / qualitative integration 等の lineage 記述

表示名は installable identifier ではない。

公開時の display は別 gate で最終確認する。

## Runtime handoff policy

production runtime で sibling Skill を指す場合、優先順位は次とする。

1. role / capability を自然言語で記述する。
2. installable name を必要な場合だけ明示する。
3. filesystem sibling path を前提にしない。
4. unavailable の場合は compatible realization へ fallback できる表現を残す。

望ましい例:

```text
Use `material-led-synthesis` when installed, or another compatible
one-round material-synthesis realization satisfying the same Method Definition.
```

避ける例:

```text
../affinity-synthesis/
research/skill-prototypes/affinity-synthesis/
```

production runtime は research filesystem layout を知らない。

## Layer 2 への影響

研究版 `iterative-inquiry-synthesis` は現在 `affinity-synthesis` を research companion 名として明示している。

これは research branch では変更しない。

production canonical source を作る際に、次を別途確認する。

- ja-JP runtime の explicit sibling name
- en-US runtime の explicit sibling name
- Progressive References 内の sibling filesystem wording
- Method Definition 内の realization 名
- OpenAI default prompt / bundle description に旧 research ID が混入していないか

Layer 2 の意味論は変えない。名前だけを production projection に合わせる。

## CSW への影響

CSW は原則として installable name を強く結び付けず、compatible realization への delegation を表す。

したがって production promotion で必要なのは、

- thin ownership の維持
- `affinity-synthesis` を公開Skill名として前提にする表現があれば除去
- `material-led-synthesis` を必須 hard dependency にしない

ことである。

## Adapter metadata policy

research prototype metadata は research ID を含む directory に置いてよい。

production promotion 時は production path へコピー・再記述し、production builder が research metadata を直接読まない。

Layer 1 の production candidate:

```text
adapters/openai-skill/{locale}/material-led-synthesis/openai.interactive.yaml
adapters/openai-skill/{locale}/material-led-synthesis/openai.metered.yaml
```

bundle metadata の `contains` / description も production name を使う。

## Package / release policy

production package 内には `affinity-synthesis` と `material-led-synthesis` を同時に入れない。

公開時の Layer 1 installable tree は一つだけとする。

```text
material-led-synthesis/
```

research ID を compatibility alias directory として追加しない。alias が必要になる明確な ecosystem 事情が出た場合は別 design decision とする。

## Lineage policy

公開名変更は KJ法との系譜を隠すためではない。

Method Definition / evidence では、

- KJ法®を公式再現・認定Skillと称しない
- 親和図法との近接と差を説明する
- generated-AI-specific safeguards を明示する

という既存方針を維持する。

## Validation candidates

production canonical source を作った後、validator に最低限次を追加する。

1. sibling production `SKILL.md` frontmatter name = production target name。
2. production package tree に research-only `affinity-synthesis` directory が存在しない。
3. production runtime / adapter metadata に `research/skill-prototypes/` path がない。
4. Layer 2 production runtime に sibling filesystem path がない。
5. explicit Layer 1 installable-name reference は `material-led-synthesis` に統一される。
6. research suite / eval / migration record は research ID を保持する。
7. display / lineage textを identifier rename と誤認して変更しない。

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
identity / handoff referencesだけpublic nameへ投影
        ↓
production build / validator generalization
        ↓
generated-artifact diff review
        ↓
release internal-composition validation
```

## 現時点の判断

- research ID `affinity-synthesis` は維持する。
- production candidate は `material-led-synthesis`。
- rename は production projection でのみ行う。
- display `Affinity Synthesis / 親和統合` は installable name と独立に扱う。
- runtime handoff は role-first、name-second、filesystem-independent とする。
- research history を public-name rename で書き換えない。
