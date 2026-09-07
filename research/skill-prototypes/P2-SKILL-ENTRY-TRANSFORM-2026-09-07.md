# Research Skill Suite — P2 Skill Entry Transform Audit 2026-09-07

Status: research host-entry contract; production build unchanged

## Purpose

Skill subtreeのsource→target pathが決まっても、`SKILL.md` はhostごとに同じbyte列を置けばよいとは限らない。

現行production buildではOpenAIとClaude/Codexでfrontmatter policyが異なるため、path planningとentry renderingを分離する。

```text
realization
  -> package source
  -> package target
  -> Skill subtree mapping
  -> Skill entry transform
```

Method DefinitionやSkill本文の意味をhost adapter policyへ吸収しない。

## Canonical CSW

CSWのruntime entryは `render_runtime_entry` であり、research側に第二のrendererを作らない。

```text
transform_mode = existing_canonical_builder_render
```

現行 `scripts/build.py` が持つ次の責務を維持する。

- locale description
- target Skill name
- router link rewrite
- Claude explicit-invocation flag

research plannerは、この既存rendererを使うべきことだけを外部化する。

## Explicit sibling Skill

Affinity / Iterativeはsource自体がfrontmatter付きSkill entryであるため、次の限定transformを使う。

```text
transform_mode = normalize_explicit_skill_frontmatter
```

責務:

- source `description` を保持
- `name` をdistribution target `skill_name` に正規化
- bodyを意味変更しない
- 古い `disable-model-invocation` を二重化しない

### OpenAI

```text
entry_policy = openai_skill
disable_model_invocation = false
```

### Claude / Codex shared tree

```text
entry_policy = claude_codex_shared_skill_tree
disable_model_invocation = true
```

これは一般方法論ではなく、現在のlocale pluginが明示呼び出し型であることに由来するhost packaging policyである。

## Bilingual source boundary

英語siblingのsource entryは `SKILL.en.md` だが、subtree plannerがtarget-relative entryを `SKILL.md` に正規化する。

したがってentry transformは日英とも同じtarget contractを扱える。

```text
affinity-synthesis/SKILL.en.md
  -> affinity-synthesis/SKILL.md

iterative-inquiry-synthesis/SKILL.en.md
  -> iterative-inquiry-synthesis/SKILL.md
```

元source filenameとlocaleはplan上に残る。

## Frontmatter parser boundary

research helperは現在のprototypeが使う一行scalar frontmatterだけを扱う。

複雑なYAMLを推測して処理せず、対応外はfail-closedとする。production一般化時にはhost仕様と依存関係を確認して正式parser/rendererを選ぶ。

## Composite surfaces

ChatGPT GPT / Microsoft Copilotは現在Skill subtreeをmaterializeする契約を持たないため、entry transformも作らない。

```text
state = not-applicable
entries = []
```

## Tests

`tests/test_research_skill_entry_transforms.py` は日英について次を固定する。

- OpenAI explicit siblingにClaude flagを入れない
- Claude/Codex siblingにflagを一度だけ入れる
- target nameはsource frontmatterではなくpackage target contractから取る
- English sourceは `SKILL.en.md` のまま追跡し、targetは `SKILL.md`
- CSWは日英ともexisting builder render boundaryを保つ
- bodyを保つ
- duplicate key / missing descriptionはfail-closed
- composite surfaceでentry transformを捏造しない

## Still out of scope

- `agents/openai.yaml`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- marketplace metadata
- plugin-level description / keywords
- actual artifact write
- host routing behavior
- release readiness

これらはSkill entryより一段外側のadapter metadataである。

## Decision

**P2 packaging contractは、realization availability / source boundary / target name+path / Skill-entry transformを別々に保持する。**

次はhost adapter metadataを同じ考え方で分離するかを検討できるが、実行環境でresearch gateを通すまではproduction build一般化を急がない。
