# P2 Claude/Codex plugin core materializer — 2026-09-07

## 目的

Claude CodeとCodexの現行production adapterは、一つのlocale plugin directoryと一つの`skills/` treeを共有している。

三Skill suiteへ移行するときに、

- Claude用Skill tree
- Codex用Skill tree

を別々に生成し始めると、同じmethod realizationがhostごとに静かに分岐する危険がある。

一方、plugin-level metadataはhostごとに別manifestを持つ。

```text
.claude-plugin/plugin.json
.codex-plugin/plugin.json
```

そこでproduction builderをmulti-Skill化する前に、research suiteから

1. Claude / CodexそれぞれのSkill subtree planを実体化する。
2. 両treeがbyte-for-byteで一致することを確認する。
3. 一つの共有`skills/` treeだけをplugin coreへ配置する。
4. ja-JP三Skill用bundle metadata prototypeからhost別manifestを構成する。

という境界を一時領域で確認する。

## Script

`research/skill-prototypes/scripts/materialize_claude_codex_plugin_core.py`

## 出力

ja-JPでは次のcoreをrepository外へ作る。

```text
<output>/
  cultural-substrate-weaving-ja/
    skills/
      weave/
        SKILL.md
        references/...
      affinity-synthesis/
        SKILL.md
        references/...
        evals/...
        evidence/...
      iterative-inquiry-synthesis/
        SKILL.md
        references/...

    .claude-plugin/
      plugin.json

    .codex-plugin/
      plugin.json
```

三Skillのtarget名は既存suite package target contractに従う。

CSWだけは既存互換の`weave`、companion二Skillはそれぞれinstallable nameと同じ名前を使う。

## Shared Skill-tree invariant

`materialize_skill_tree.py`をClaude/Codexそれぞれについて独立に呼び出し、生成された全fileの相対pathとbyte列を比較する。

一致しない場合はplugin coreを作らない。

したがって、このmaterializerは

> 現在同じdirectoryを共有しているから、今後もたぶん同じだろう

とは仮定しない。

**両distribution planが実際に同じtreeを生成することを毎回検査する。**

これは将来Codex側のSkill entry仕様がClaudeと分岐した場合、無理に共有を続けるための規則ではない。その場合は差分をfailさせ、package topology自体を再設計する契機にする。

## Bundle metadata

ja-JPでは現在、

```text
research/skill-prototypes/adapters/claude-codex/ja-JP/bundle-metadata.json
```

をprototype sourceとして使う。

そこには次が明示されている。

- `plugin_name`
- `display`
- `description`
- `contains`
- `invocation_policy = explicit`
- `status = prototype`

Claude / Codex双方のadapter metadata planが同じprototype sourceと同じcatalog entryを指していることを確認し、driftしていればmaterializationを止める。

## Host-specific manifest

### Claude

現行production manifestの構造を維持する。

- name
- description
- version
- author
- homepage
- repository
- license

ただしuser-facing descriptionは単一Skill時代のlocale catalogではなく、三Skill bundle用research prototypeから取る。

### Codex

現行production manifestの構造を維持する。

加えて、

- `skills: ./skills/`
- `interface.displayName`
- `interface.shortDescription`
- developer / category
- current keyword baseline

を持つ。

ClaudeとCodexでdescriptionの意味を別々に再生成しない。

## Invocation boundary

現在のja-JP bundle prototypeは明示呼び出し専用である。

各Skill `SKILL.md`には、既存Skill-tree materializerのentry transformにより

```text
disable-model-invocation: true
```

を一度だけ付ける。

plugin core materializerがこのfrontmatterを追加生成することはしない。

## en-US

en-USではcompanion Skill realizationがまだplannedである。

したがってClaude/Codex locale bundleはruntime上blockedであり、partial bundleを作らない。

OpenAI standalone-per-skillのようなpartial probeをClaude/Codexへ持ち込まない。locale bundleは`contains`全体が揃って初めて一つのbundleとして実体化する。

失敗時には利用者指定output directoryを作成しない。

## まだ生成しないもの

この段階では意図的に次を生成しない。

- locale README
- root Claude marketplace
- standalone Claude marketplace
- root Codex marketplace
- archive / ZIP
- release manifest
- release asset

理由は、現行READMEやmarketplace wordingが単一CSWを前提としており、三Skill bundle向けの説明としてまだreviewされていないためである。

runtime coreが作れることを理由に、未レビューの外側metadataまで既存文面で埋めない。

## Tests

`tests/test_research_claude_codex_plugin_core.py`で次を固定する。

1. ja-JPで一つのplugin rootと三Skill共有treeを作る。
2. Claude/Codex subtree planはmaterialization時にbyte一致を要求する。
3. 三Skillすべてexplicit invocation frontmatterを一度だけ持つ。
4. Claude/Codex manifestは同じbundle prototypeのname / descriptionを使う。
5. Codex display / short descriptionもprototypeと一致する。
6. current `VERSION`をmanifestへ入れる。
7. README / marketplaceをまだ生成しない。
8. en-US blocked bundleはoutputを残さない。
9. repository内outputを拒否する。

## PR #294 / #295との関係

段階は次のようになる。

```text
#294
research Skill renderer → 既存CSW subtree parity

#295
OpenAI standalone host package composition

本変更
Claude/Codex shared plugin core composition
```

それぞれ別の失敗面を持つため、一つの巨大なproduction migrationへまとめない。

## Production generalizationへ渡す不変条件

この段階までが検証できた後、production builder側へ渡すべき条件は次になる。

- CSW rendererの結果を変えない。
- companion Skillはcanonical化されるまではresearch/prototype maturityを失わない。
- OpenAIはSkillごと、Claude/Codexはlocale bundleとしてpackage topologyを分ける。
- Claude/Codexは共有Skill treeを一つだけ持つ。
- host別manifestの違いをSkill method treeへ漏らさない。
- bundle descriptionを各SkillのMethod Definitionへ混ぜない。
- 未レビューREADME / marketplaceはproduction既存文面から自動流用しない。

## 次の段階

次に残る外側のpackage contractは、Claude/CodexのREADME / marketplaceである。

ただし、そこはmethod executionではなく配布・発見・導線の層である。

そのためproduction builder generalizationに必要な最小条件を考える際には、

1. plugin coreまでを先にgeneralizeする。
2. marketplace / READMEは互換性とuser-facing namingを別PRで扱う。

という分割も可能である。

この判断は、plugin core materializerの実checkout検証結果と、既存release/package validatorがどこまで外側artifactを必須としているかを照合して決める。

## 結論

**Claude/Codexについて、三SkillのMethod treeをhostごとに複製せず、一つの共有runtime treeへ束ねながらhost-specific manifestだけを分離する研究境界を実ファイルtreeとして外在化する。**

production multi-Skill化の前に、この共有境界が成立することを検査可能にする。
