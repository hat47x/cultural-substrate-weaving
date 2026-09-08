# Research Skill Suite — P2 Package Target Naming Audit 2026-09-07

Status: research packaging contract; production build remains unchanged

## Purpose

`package_source` が「何を持っていくか」を表すのに対し、`package_targets` は **そのSkillを各distributionのどこへ、何という名前で置くか** を表す。

Method Definition、Skill identity、source boundary、host上のtarget nameを同一視しない。

## Current target names

現在は日英とも三Skillのruntime artifactが存在する。英語siblingは `translated-draft` でありpromotion readyではないが、package topologyを検証するためのtarget nameは明示できる。

### Affinity Synthesis — ja-JP / en-US

```text
openai_skill   -> affinity-synthesis
claude_plugin  -> affinity-synthesis
codex_plugin   -> affinity-synthesis
```

### Iterative Inquiry Synthesis — ja-JP / en-US

```text
openai_skill   -> iterative-inquiry-synthesis
claude_plugin  -> iterative-inquiry-synthesis
codex_plugin   -> iterative-inquiry-synthesis
```

### Cultural Substrate Weaving — ja-JP / en-US

```text
openai_skill   -> cultural-substrate-weaving
claude_plugin  -> weave
codex_plugin   -> weave
```

CSWの `weave` は新規命名ではなく、既存 `adapters/claude-code/locales.json` のcontractを明示したもの。Codexも現在はClaude pluginの `skills/` treeを共有するため同じtarget名を使う。

## Why target name belongs to realization packaging metadata

同じMethod・同じruntimeでもhostによってdirectory名や公開名が異なり得る。したがって `package_targets` はMethod Definitionではなくlocale realizationのpackaging metadataとして持つ。

`installable_name` は安定したSkill candidate identityだが、それだけから全host targetを推測しない。

## Scope

`package_targets` を要求するのはSkill subtreeをmaterializeするdistributionだけ。

- `standalone_per_skill`
- `locale_bundle`

現在は `openai_skill`, `claude_plugin`, `codex_plugin` が対象。`chatgpt_gpt` と `microsoft_copilot` はcomposite realizationなので、sibling Skill subtree名をこの段階では要求しない。

## Validator

`scripts/validate_research_package_targets.py` はbase suite validatorと分ける。

base validator:
- runtime / Method Definition
- `package_source`
- source-root boundary
- research metadata

package-target validator:
- realized localeが必要targetを過不足なく持つ
- planned localeにstale targetを残さない
- target `skill_name` が単一の安全なpath componentである
- 同一locale / distribution namespace内でtarget nameが衝突しない

拒否例:

```text
""
" affinity-synthesis"
"."
".."
"../other"
"a/b"
"a\\b"
```

## Adapter synchronization

CSWのClaude/Codex targetは既存adapterの `skill_name` と一致させる。OpenAIについては現在、全realized Skillで `skill_name == installable_name` を回帰testとして固定する。

## Planner consequence

Skill-tree distributionで `buildable` とするには次が必要。

1. status != planned
2. runtime entry
3. package source
4. 当該distributionのpackage target

したがってClaude targetだけ欠ければ、OpenAI/CodexはbuildableのままClaudeだけblockedにできる。

composite realizationはprimary CSWのruntime/package-source availabilityだけを見る。target subtree名やinternal Method parityはassertしない。

## Current planned bundle topology

日英ともClaude/CodexのSkill subtree候補は次になる。

```text
skills/
  weave/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

これは**source/target metadata上でtreeを計画できる**という意味であり、production builderが実生成できること、host routingが確認済みであること、英語版が査読済みであることを意味しない。

## Decision

**P2は、Skill identity・package source boundary・distribution-specific target nameを別契約として保持する。**

次はP3でsourceとtargetの双方から予定package treeを作り、relative structure・collision・link topologyをresearch-onlyに検査する。
