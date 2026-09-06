# Research Skill Suite — P2 Package Target Naming Audit 2026-09-07

Status: research packaging contract; production build remains unchanged

## Purpose

`package_source` によって「何をpackageへ持っていくか」は記述できるようになった。

しかし、source boundaryだけでは「そのSkillをdistribution内のどこへ、何という名前で置くか」は決まらない。

この差は現行Cultural Substrate Weavingですでに具体的に存在する。

- OpenAI Skillではsource manifestのinstallable name `cultural-substrate-weaving` を使う。
- Claude/Codexのlocale pluginでは既存adapterがSkill名を `weave` としている。

したがって `installable_name` を全distributionのdirectory / Skill名へ機械的に流用すると、現行package contractと不一致になる。

P2では、locale realizationごとにdistribution別 `package_targets` を持たせる。

## Current target names

### Affinity Synthesis / ja-JP

```text
openai_skill   -> affinity-synthesis
claude_plugin  -> affinity-synthesis
codex_plugin   -> affinity-synthesis
```

### Iterative Inquiry Synthesis / ja-JP

```text
openai_skill   -> iterative-inquiry-synthesis
claude_plugin  -> iterative-inquiry-synthesis
codex_plugin   -> iterative-inquiry-synthesis
```

### Cultural Substrate Weaving / ja-JP and en-US

```text
openai_skill   -> cultural-substrate-weaving
claude_plugin  -> weave
codex_plugin   -> weave
```

CSWのClaude target `weave` は新しく命名したものではない。既存 `adapters/claude-code/locales.json` の `skill_name` をresearch suite側へ明示したものである。

Codexも現行production buildではClaude plugin directoryの `skills/` treeを共有するため、同じtarget名を使う。

## Why target name is realization metadata

package target nameはMethod Definitionの性質ではない。

同じ方法・同じruntime entryでも、hostやdistributionによって公開名・directory名が異なり得る。

したがってskill top-levelの恒久的identityではなく、locale realizationのpackaging metadataとして持つ。

`installable_name` はskill candidateの安定した公開候補名として維持するが、それだけからすべてのhost targetを推測しない。

## Scope of package targets

現在 `package_targets` を要求するのは、Skill subtreeをmaterializeするdistributionだけである。

- `standalone_per_skill`
- `locale_bundle`

現在のmanifestでは次の三つに対応する。

- `openai_skill`
- `claude_plugin`
- `codex_plugin`

`chatgpt_gpt` と `microsoft_copilot` は現段階ではcomposite agent realizationであり、sibling Skill directoryを作る設計をまだ確定していない。

そのためP2でtarget Skill名を捏造しない。composite plannerはprimary CSW source availabilityだけを限定的に扱う。

## Validator

`validate_research_package_targets.py` はbase suite validationとは別にpackage topology固有の契約を検査する。

### Realized vs planned

- realized locale: 対象となるSkill-tree distributionの `package_targets` を過不足なく持つ。
- planned locale: staleな `package_targets` を持たない。

English companion Skillはまだplannedなので、英語target nameを先に予約・捏造しない。

### Path-component safety

`skill_name` は単一のpackage path componentとして扱えることを要求する。

少なくとも次を拒否する。

- empty / surrounding whitespace
- `.` / `..`
- `/`
- `\\`
- NUL

ホスト名の文字種を閉じたASCII enumへ固定しない。ここで守るのはpath traversal / accidental nestingを起こさない境界である。

### Collision

同じlocale・同じdistribution namespace内で、複数のrealized Skillが同じtarget `skill_name` を持つ場合はfail-closedにする。

たとえばClaude ja-JP bundleでAffinityとIterativeが両方 `affinity-synthesis` を名乗れば、同じ `skills/affinity-synthesis/` subtreeへ衝突するため許可しない。

異なるdistribution間で同じ名前を使うこと自体は衝突ではない。

## Existing adapter synchronization

CSWだけは既存production adapterがすでにtarget名を所有している。

回帰testは `adapters/claude-code/locales.json` を読み、ja-JP / en-USそれぞれについて

```text
suite CSW claude_plugin skill_name == adapter skill_name
suite CSW codex_plugin  skill_name == adapter skill_name
```

を確認する。

これによりresearch manifest側の `weave` が将来単独で漂流しないようにする。

OpenAIについては現行の全realized Skillで、research target nameとskill `installable_name` が一致することを現在状態の回帰として固定する。

## Planner consequence

`plan_suite_layout.py` はsource readinessとdistribution target readinessを分ける。

### Skill-tree distribution

OpenAI standalone、Claude/Codex bundleでは、次がそろったときだけそのSkillをそのdistributionでbuildableとする。

1. statusがplannedではない。
2. runtime entryがある。
3. package sourceがある。
4. そのdistributionのpackage targetがある。

したがってsourceが完全でもClaude targetだけ欠けていれば、OpenAI/Codexはbuildableのまま、Claudeだけblockedにできる。

### Composite realization

GPT/Copilotはtarget Skill subtree名をまだ要求しない。

primary CSWのruntime/package source availabilityのみを見て、scopeに

> no sibling Skill-tree target name is required here

と残す。

これはcomposite Method parityや将来の三Skill内部構成を保証しない。

## Current layout implication

ja-JP Claude/Codex bundleのtarget Skill名は次になる。

```text
skills/
  weave/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

この段階では予定treeであり、実packageを生成した証拠ではない。

en-USはcompanion realizationsがplannedなので、現時点で配置可能なのはCSW `weave` だけであり、三Skill bundle全体はblockedのままである。

## Next P2 step

source descriptorとtarget namingの両方が明示されたため、次はread-only package subtree plannerで具体的なtarget pathsを計算できる。

次段階で確認するもの:

1. `explicit_files` の相対構造がtarget subtreeへ保存されるか。
2. `canonical_manifest` のrouterがtarget `SKILL.md`、modulesが`references/<skill_reference>`へ写る既存OpenAI/Claude shapeを表現できるか。
3. 同一target path collisionがないか。
4. source fileからの相対Markdown referenceがplanned tree内で切れないか。
5. Claude/Codexで共用するSkill subtreeが二重に別規約へ分岐していないか。

ここが安定するまでproduction `scripts/build.py` は変更しない。

## Decision

**P2 now distinguishes skill identity, package source boundary, and distribution-specific target name.**

これにより「sourceがあるからどこかへ置けるはず」「installable nameを全hostへそのまま使えばよい」という暗黙前提を外し、既存CSW `weave` contractを保ったままcompanion Skillの配置を計画できる。
