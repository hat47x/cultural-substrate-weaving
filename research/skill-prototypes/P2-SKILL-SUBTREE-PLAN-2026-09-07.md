# Research Skill Suite — P2 Skill Subtree Plan 2026-09-07

Status: read-only source-to-target path planning; no package generation performed

## Purpose

P2ではここまでに三つを分離した。

1. skill / locale realizationが存在するか。
2. そのrealizationを構成するpackage source boundaryは何か。
3. 各distributionで何というtarget Skill名へ置くか。

次に必要なのは、この情報から**予定Skill subtree**を具体的なsource→target pathとして計算し、production builderへ入る前に衝突や構造欠落を見えるようにすることである。

`plan_skill_subtrees.py` はfilesystemへ書き込まない。

出すのは、

```text
source repository path
  -> distribution-relative Skill subtree path
```

の対応だけである。

## Scope

このplannerが扱うもの:

- `explicit_files` の相対path保存。
- `canonical_manifest` のrouter / module target写像。
- distribution別target Skill名。
- standalone / locale bundleのSkill subtree root。
- target file collision。
- blocked bundleでも現在利用可能な部分subtree。

扱わないもの:

- 実file copy/write。
- OpenAI interactive / metered profile root。
- Claude/Codex marketplace manifest。
- host-specific frontmatter mutation。
- adapter instructions。
- ChatGPT GPT / Microsoft Copilot internal knowledge composition。
- ZIP / release asset生成。
- release readiness。

## `explicit_files` mapping

Affinity / Iterativeでは、package source rootからの相対pathをtarget Skill rootの下でも変えない。

たとえばAffinity OpenAI standalone:

```text
research/skill-prototypes/affinity-synthesis/SKILL.md
  -> affinity-synthesis/SKILL.md

research/skill-prototypes/affinity-synthesis/references/METHOD.md
  -> affinity-synthesis/references/METHOD.md

research/skill-prototypes/affinity-synthesis/evals/CASES.md
  -> affinity-synthesis/evals/CASES.md
```

この写像により、source package root内で成立する相対参照をtarget treeでも同じ形に保てる。

これはMarkdown reference内容を全面解析して「完全にリンク検証した」という意味ではない。**path structureを変えないことで、同梱対象間の相対参照を壊さない前提を作る**段階である。

## `canonical_manifest` mapping

現行CSWは別の生成構造を持つ。

`src/manifest.json` は、

- `router`
- `modules[].source`
- `modules[].skill_reference`

を持っている。

production `build.py` はこの情報からOpenAI/ClaudeのSkill subtreeを作る。

research plannerも同じsource contractを読むが、内容変換までは行わない。

### Runtime entry

```text
src/<locale>/ROUTER.md
  -> <target-root>/SKILL.md
operation: render_runtime_entry
```

`render_runtime_entry` はraw copyではないことを明示するmarkerである。

実productionではdistributionごとにfrontmatterやrouter link rewrite等が入る。research plannerはその内容を再実装しない。

### Modules

たとえばja-JP:

```text
src/ja-JP/core/iteration.md
  -> <target-root>/references/00-iteration.md

src/ja-JP/methods/integration.md
  -> <target-root>/references/10-integration.md
```

現在のmanifestは12 modulesを持つため、runtime entryと合わせてCSW Skill subtreeのmappingは13件になる。

## Distribution roots

### OpenAI `standalone_per_skill`

plannerはprofile等より内側のSkill rootだけを見る。

```text
<skill_name>/...
```

current ja-JP:

```text
cultural-substrate-weaving/
affinity-synthesis/
iterative-inquiry-synthesis/
```

### Claude / Codex `locale_bundle`

既存plugin treeに合わせ、

```text
skills/<skill_name>/...
```

を予定rootとする。

current ja-JP:

```text
skills/weave/
skills/affinity-synthesis/
skills/iterative-inquiry-synthesis/
```

CSW `weave` は既存adapter同期済みtarget nameであり、新しいrenameではない。

## Blocked English bundle

現在のen-USは、

- CSW: existing
- Affinity: planned
- Iterative: planned

である。

そのためClaude/Codex三Skill bundle全体はblockedのままである。

ただしplannerは「何も計画できない」とはせず、現在存在するCSW subtreeだけをpartial treeとして出す。

```text
skills/weave/  # CSW only
missing:
  affinity-synthesis
  iterative-inquiry-synthesis
```

これにより、bundle readinessと既存CSW package surfaceを混同しない。

## Collision detection

package target validatorはSkill root名の衝突を先にfail-closedにする。

subtree planner自身もpure functionとしてtarget file pathを集計し、重複を`collisions`へ出す。

これはvalidatorを迂回したsynthetic caseや、将来一つのSkill内で異なるsourceが同じtarget filenameへ射影される場合も観察できるようにするためである。

collisionがあれば`subtree_state`を`collision`とし、planned成功にはしない。

## Composite surfaces

ChatGPT GPT / Microsoft Copilotについては、現段階でcompanion Skill subtreeを作るtarget contractを持たない。

そのためsubtree plannerは、layout plannerのprimary CSW availabilityを残しつつ、

```text
subtree_state: not-applicable
subtrees: []
```

とする。

三Skill分離後の内部Method compositionを、この段階でdirectory treeとして捏造しない。

## Important unresolved adapter boundary

source→target pathが計算できても、まだactual package生成へ直行しない。

特にClaudeでは、現行CSW `build_claude()` がhost-specific frontmatterとして明示呼び出し用設定を付与している。

一方、companion prototype `SKILL.md` は現在のresearch realization本文を直接sourceとしている。

したがって、

> **companion SKILL.mdをClaude bundleへraw copyするのか、host adapter layerでfrontmatterを補うのか**

はまだ設計していない。

subtree plannerはこの差を隠さない。

- companion explicit files: `copy`
- CSW runtime entry: `render_runtime_entry`

とoperationを分けて残す。

次のP2工程では、host adapter transformをsource methodから分離して記述する必要がある。

## Tests

`tests/test_research_skill_subtree_plan.py` は次を固定する。

- Affinity explicit package filesの相対構造保存。
- Iterative standaloneにsibling Affinity treeを埋め込まない。
- CSW Claude targetが`skills/weave`。
- CSW routerが`SKILL.md`へrender mappingされる。
- CSW 12 modulesがmanifestの`skill_reference`へ写る。
- en-US blocked bundleでもCSW partial subtreeを保持する。
- synthetic target collisionを`collision`として見える化する。
- GPT/Copilotで未設計sibling Skill subtreeを発明しない。

これは実build testではない。

## Decision

**P2 can now calculate a concrete, read-only Skill-subtree path plan from declared source and target contracts without changing production build code.**

次に確認すべき境界はhost adapter transformである。

その境界を明示してから、research builderでtemporary output treeを生成・検査するか、production `scripts/build.py` generalizationへ進むかを判断する。

canonical `src/` のKJ分離と公開asset変更はまだ開始しない。
