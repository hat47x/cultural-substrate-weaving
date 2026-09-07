# Research Skill Suite — P2 Skill Subtree Plan 2026-09-07

Status: read-only source-to-target path planning; production build unchanged

## Purpose

P2で分離した次の契約から、distribution内の予定Skill subtreeを具体的なsource→target pathとして計算する。

1. locale realization availability
2. `package_source` — 何を持っていくか
3. `package_targets` — distribution上で何というSkill名に置くか

`plan_skill_subtrees.py` はfilesystemへ書き込まない。

```text
source repository path
  -> distribution-relative target path
  + operation: copy | render_runtime_entry
```

## Why this is separate from layout

`plan_suite_layout.py` の `buildable` は、realization・package source・target nameが揃うことしか意味しない。

subtree planはその次に、実際のdirectory/path topologyを外部化する。

## explicit_files

Affinity Synthesis / Iterative Inquiry Synthesisでは、package source rootからの相対構造を基本的に維持する。

```text
references/METHOD.md
  -> <target-root>/references/METHOD.md
```

ただしlocale source上のruntime entry filenameは配布面のcanonical entryへ射影する。

```text
ja-JP: SKILL.md    -> <target-root>/SKILL.md
en-US: SKILL.en.md -> <target-root>/SKILL.md
```

source identityは失わない。mappingの `source` は `SKILL.en.md` のまま保持する。

operationは `copy` とする。host固有frontmatter処理は後段へ渡す。

## canonical_manifest

CSWは既存 `src/manifest.json` を正本として再利用する。

```text
src/<locale>/ROUTER.md
  -> <target-root>/SKILL.md
  operation = render_runtime_entry

src/<locale>/<module source>
  -> <target-root>/references/<skill_reference>
  operation = copy
```

routerはraw copyではない。現行production builderがfrontmatter付与とrouter link rewriteを行うため、research plannerは `render_runtime_entry` として境界だけ残す。

## Distribution roots

OpenAI standalone:

```text
<skill_name>/...
```

Claude / Codex locale bundle:

```text
skills/<skill_name>/...
```

現在の日英両localeで、Claude/Codexの予定rootは同じである。

```text
skills/weave/
skills/affinity-synthesis/
skills/iterative-inquiry-synthesis/
```

英語sibling realizationは `translated-draft` であり、treeを計画できることはpromotion readinessを意味しない。

## Collision

同一distribution内で同じtarget fileへ複数mappingが入れば `collision` とする。

package target validatorはSkill root名の衝突を先に防ぐが、subtree planner側でもtarget file pathを再集計する。これによりsynthetic caseや一Skill内部の投影衝突も観察できる。

## Composite surfaces

ChatGPT GPT / Microsoft Copilotは現段階でsibling Skill subtreeをmaterializeする契約を持たない。

```text
subtree_state = not-applicable
subtrees = []
```

composite内部構成をdirectory treeとして捏造しない。

## Tests

`tests/test_research_skill_subtree_plan.py` は少なくとも次を固定する。

- ja-JP explicit filesの相対構造保持
- en-US `SKILL.en.md -> SKILL.md`
- 日英Claude/Codexで三Skill subtreeが揃う
- Iterative standaloneがAffinity treeをhard dependencyとして埋め込まない
- CSW router/moduleが既存shapeへ写る
- target collisionがfail-closedに見える
- composite surfaceがsibling treeを発明しない

## Boundary

このplannerは次を行わない。

- file write/copy
- frontmatter mutation
- OpenAI agent metadata
- Claude/Codex plugin metadata
- marketplace catalog
- archive/release generation
- host routing validation

これらのうちSkill entry frontmatterだけを、次の `plan_skill_entry_transforms.py` で独立して扱う。

## Decision

**P2はsource boundary・target name・target pathを別契約として保持し、runtime entryのcopy/render差も明示する。**

production `scripts/build.py` の一般化前に、このread-only tree contractを安定させる。
