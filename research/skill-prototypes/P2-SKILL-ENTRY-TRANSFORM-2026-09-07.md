# Research Skill Suite — P2 Skill Entry Transform Audit 2026-09-07

Status: research adapter-transform contract; production build remains unchanged

## Purpose

P2ではここまでに、次の三つを分離した。

1. locale realizationが存在するか。
2. runtime packageを構成するsource boundaryが分かっているか。
3. distribution内でどのSkill名へ置くか。

さらにSkill subtree plannerによって、source→target pathも計算できるようになった。

しかし `SKILL.md` は、単純なbyte copyだけではhostごとの差を吸収できない。

現行production builderは、OpenAI SkillとClaude/Codex共有Skill treeでfrontmatterを変えている。

```python
skill_frontmatter(name, description, claude_explicit=False)
```

OpenAIでは、

```yaml
---
name: cultural-substrate-weaving
description: ...
---
```

Claude/Codex共有treeでは、

```yaml
---
name: weave
description: ...
disable-model-invocation: true
---
```

となる。

一方、companion prototypesの `SKILL.md` は既に `name` / `description` frontmatterを持つ。

したがってmulti-Skill化では、CSWのようにrouterからSkill entryを生成するケースと、既にSkill entryであるcompanionを正規化するケースを分ける必要がある。

## Current transform boundary

### Canonical CSW

CSWについては新しいrendererを作らない。

Skill-subtree planではruntime entry mappingを、

```text
operation = render_runtime_entry
```

として残している。

entry-transform planではこれを、

```text
transform_mode = existing_canonical_builder_render
```

として扱う。

つまり `scripts/build.py` が現在持つ、

- locale descriptionの採用
- distribution target nameの採用
- router link rewrite
- Claude明示呼び出しflag

をresearch prototype側で再実装しない。

この境界は、production移行前に二つのrendererが同じCSW entryを別々に生成する状態を避けるためである。

### Explicit companion Skill entries

Affinity / Iterativeはsourceそのものが `SKILL.md` である。

この場合は `normalize_explicit_skill_frontmatter` を使う。

責務は限定する。

- source `description` を保持する。
- `name` はsourceの値を盲信せず、distribution target contractの `skill_name` へ揃える。
- OpenAI Skillでは `disable-model-invocation` を付けない。
- Claude/Codex共有Skill treeでは `disable-model-invocation: true` を一度だけ付ける。
- 既に古いflagがあっても二重化しない。
- bodyは意味変更しない。

このtransformは方法論、routing、Skill activation判断を所有しない。

## Why a deliberately small frontmatter parser

research helperはprototype entryで現在使われている一行scalar frontmatterだけを扱う。

現時点でYAML parser一般化を行わない。

複雑なnested YAML、multiline scalar、anchor等へ自動対応すると、「production parserを選ぶ」という別の設計判断をresearch helperが先取りするためである。

対応外frontmatterはfail-closedにする。

production migrationへ進む段階では、host仕様と依存関係を確認して正式なparser/rendererを決める。

## Distribution policies

### OpenAI Skill

```text
entry_policy = openai_skill
disable_model_invocation = false
```

sourceがexplicit Skill entryならfrontmatterを正規化する。

CSWはexisting builder renderのまま。

この段階では `agents/openai.yaml` を生成しない。

OpenAIのinteractive / metered profile差もentry transformの責務ではない。

### Claude plugin

```text
entry_policy = claude_codex_shared_skill_tree
disable_model_invocation = true
```

明示呼び出し専用という現行CSW pluginの境界をcompanionへも適用する。

これは「companionが常に自動呼び出し禁止であるべき」という一般方法論ではない。

現行suite distribution prototypeが、CSWと同じ明示呼び出し型plugin内へ三Skillを置く設計だからである。

### Codex plugin

現行production structureではClaudeとCodexが同じplugin directoryの `skills/<name>/SKILL.md` を共有する。

そのためresearch planでも同じentry policyを使う。

これは将来不変とは限らない。

Codex側のSkill entry仕様がClaudeと分岐する場合、`codex_plugin` policyを独立させる。

「同じ今のtreeを共有している」ことと「両hostの仕様が永久に同じ」であることを混同しない。

## What the plan now exposes

各planned entryについて少なくとも次を外部化する。

```text
skill_id
target_name
source
target
input_operation
transform_mode
entry_policy
disable_model_invocation
```

これにより、たとえばAffinity ja-JPは、

```text
OpenAI:
  source = research/skill-prototypes/affinity-synthesis/SKILL.md
  target = affinity-synthesis/SKILL.md
  transform = normalize_explicit_skill_frontmatter
  explicit flag = false

Claude/Codex:
  source = same
  target = skills/affinity-synthesis/SKILL.md
  transform = normalize_explicit_skill_frontmatter
  explicit flag = true
```

と区別できる。

## Boundaries still unresolved

この段階では次を扱わない。

### OpenAI agent metadata

現行OpenAI packageはSkill subtreeに加えて、

```text
agents/openai.yaml
```

をprofile別adapterから持つ。

companion Skillで、

- 同じadapter templateを使うか
- Skillごとのdescriptionをどう反映するか
- interactive / meteredの差をどう持たせるか

は未設計である。

### Plugin metadata

Claude/Codex bundleでは、Skill entryだけでなく、

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- locale README
- marketplace entry

が必要である。

三Skill bundleへ拡張したときのplugin description / keywords / catalog wordingは未設計である。

### Relative references after rendering

companion Skill bodyのrelative referenceは、explicit-files subtreeで現在の構造を保つため、path自体は保存できる。

しかしhost側がentry bodyを追加変換する場合、relative linksの再検証は別途必要である。

### Actual artifact rendering

このresearch helperはpure transformを提供するが、repositoryのgenerated artifactを書き換えない。

`plugins/`、`.agents/`、`dist/`をmulti-Skillへ変更していない。

## Decision

P2 packaging contract now distinguishes four layers:

1. realization availability
2. package source boundary
3. distribution target name and subtree path
4. Skill-entry frontmatter transform

この四層が揃ったことで、次に検討できるのはhost adapter metadataのplannerである。

ただしproduction `scripts/build.py` のgeneralizationはまだ行わない。

先にOpenAI agent metadataとClaude/Codex plugin metadataについて、**既存CSW adapterを正本として何をbundle-levelへ引き上げ、何をSkill-levelに残すか**を切り分ける。

complete checkoutで実 `make check` を通すrelease gateも未通過のままである。
