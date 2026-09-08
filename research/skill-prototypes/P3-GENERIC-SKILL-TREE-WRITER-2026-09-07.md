# P3 Generic Skill-tree writer — 2026-09-07

## 目的

research suiteでは、三Skillのruntime/package topologyをproduction変更の外側で段階的に確認してきた。

一方、現行`production scripts/build.py`は、OpenAIとClaudeのSkill tree生成をそれぞれのhost関数内で直接行っている。

具体的には両方で、

1. frontmatterを作る。
2. router linkを書き換える。
3. `SKILL.md`を書く。
4. canonical moduleを`references/`へコピーする。

という同じ責務を別々に持つ。

三Skill化の段階でこのままhost関数へcompanion Skillの処理を追加すると、hostごとに類似rendererが育つ危険がある。

そこで、**production出力を一切増減させないまま、すでに解決・render済みのSkill entry bodyとreferencesからSkill treeを書く最小処理だけをhost非依存関数へ切り出す。**

## 変更

`scripts/build.py`へ次を置く。

### `canonical_reference_files(locale, config)`

現行CSW canonical manifestから、

```text
(source path, target reference name)
```

の列を作る。

これはCSW固有source resolverである。

### `write_skill_tree(...)`

すでに解決済みの次の入力だけを受け取る。

- target path
- Skill name
- description
- **YAML frontmatterを含まない、render済みentry body**
- reference source / target name pairs
- explicit invocation flag

そして、

```text
SKILL.md
references/*
```

だけを書く。

この関数は次を知らない。

- Cultural Substrate WeavingというSkill名
- `src/manifest.json`
- locale
- OpenAI / Claude / Codexというhost名
- profile
- plugin manifest
- marketplace
- `agents/openai.yaml`
- research suite
- source kindそのもの

つまり、**source resolution / entry transformと、最終Skill tree renderingを分離する。**

## Source-kind境界

この関数を「どのcanonical Skill sourceでもそのまま受け取れるwriter」とは扱わない。

現行CSWは、

```text
ROUTER.md
  -> link rewrite済みのfrontmatter-free body
  -> write_skill_tree()
```

という経路である。

一方、別レーンのP4 promotion designでは、将来のsibling Skill source候補として、すでに`SKILL.md`を持つlocale treeが検討されている。

```text
src/skills/<public-name>/<locale>/SKILL.md
src/skills/<public-name>/<locale>/references/...
```

このようなsourceをproductionへ昇格させる場合、canonical `SKILL.md`全体を`body`として`write_skill_tree()`へ渡してはならない。そうするとfrontmatterを二重に生成する可能性がある。

multi-Skill wiring時には、source kindごとに次の境界を明示する。

```text
canonical_manifest
  -> CSW source resolver / router transform
  -> frontmatter-free body + references
  -> write_skill_tree()

locale_tree / explicit Skill source
  -> source-kind固有 entry transform / copy contract
  -> host向けentry + references
  -> 必要な最終tree writer
```

そのsource adapterを本PRで先取りして作らない。

`write_skill_tree()`の「host非依存」は、**source format非依存という意味ではなく、解決済みrender inputをhost package外周から分離したという意味**である。

## 現行productionでの利用

### OpenAI

`build_openai()`はこれまでと同じCSW一つだけを生成する。

変更後は、

1. CSW router bodyを一度解決する。
2. canonical reference pairを一度解決する。
3. interactive / meteredそれぞれで同じ`write_skill_tree()`を呼ぶ。
4. profile固有の`agents/openai.yaml`は従来どおりhost関数がコピーする。

profile差をSkill method treeへ入れない境界が明確になる。

### Claude

`build_claude()`も、これまでと同じ`weave`一つだけを生成する。

Skill treeは`write_skill_tree()`へ渡し、

```text
explicit_invocation=True
```

だけhost policyとして指定する。

plugin manifest、README、standalone marketplaceは従来どおり`build_claude()`が所有する。

## 出力不変条件

このPRでは次を変更しない。

- OpenAI Skill数
- Claude/Codex plugin内Skill数
- target path
- Skill名
- description
- frontmatter形式
- router link rewrite
- reference file集合
- reference file byte内容
- OpenAI profile metadata
- Claude/Codex plugin metadata
- README
- marketplace
- GPT / M365 / canonical docs

`make check`の`generated-artifacts-check`は、build後の`.claude-plugin`、`.agents`、`plugins`にGit差分が残れば失敗する。

`dist/`についても既存`test_build.py`、`validate.py`等が現在のCSW出力を検査する。

したがってこのrefactorは、**現在のCSW rendererをhost外周から分離する内部境界を作るだけで、現在の公開artifactを変更しない**ことを前提とする。

## Tests

`tests/test_skill_tree_writer.py`で、generic writer自体について次を確認する。

1. 解決済みname / description / bodyをそのまま使う。
2. 指定されたreferenceだけを指定target nameへコピーする。
3. explicit invocationはfrontmatter policyとして一度だけ入る。
4. CSW固有Skill名を要求しない。
5. canonical reference resolverは現行manifest順序とtarget名を保持する。
6. ja-JP / en-USの現在のCSWについて、旧renderer式で組み立てた`SKILL.md` byte列と新writer出力が一致する。
7. OpenAI側ではreference集合と各reference byte列も旧式と一致する。

既存`test_build.py`はまだ単一Skill production contractを維持する。

このPRで`test_generated_plugin_reference_sets_match_manifest`の「Skill数=1」を外さない。

それを外すのは、companion runtimeをproductionへ実際に追加する別段階である。

## Research materializerとの関係

research側の`materialize_skill_tree.py`は、CSW entryについてproduction `skill_frontmatter()`を再利用している。

今回も`skill_frontmatter()`の意味とsignatureは変えない。

したがってPR #294のCSW parity gateが前提としているproduction frontmatter boundaryを壊さない。

将来、research materializerとproduction builderでgeneric writerそのものを共有するかは別判断とする。

現段階でresearch prototype sourceをproduction build dependencyへしない。

## 次のproduction refactor

Skill tree writerの抽出後、次に一般化すべきなのはvalidator側である。

現行validator / build testsには、

- OpenAI targetが`config["name"]`一つである。
- Claude plugin内Skill数が1である。
- byte budget対象がCSW Skill一つである。

という前提が残る。

そのため次は、**検査対象artifactへ適用できるvalidator helperへ切り出しつつ、現在はCSW一つだけを渡す出力不変refactor**を行う。

builderとvalidatorのmechanicsを公開集合判断から分けた後で、production source contractとsource-kind adapterを明示して初めてcompanion wiringへ進む。

## canonical migrationとの順序

```text
P2 research package topology
        ↓
P3 current-CSW production Skill-tree writer extraction   ← 本変更
        ↓
P3 generic production Skill validator
        ↓
production inclusion / source contract
        ↓
source-kind adapter + intentional multi-Skill wiring
        ↓
companion promotion decision
        ↓
canonical CSWからKJ / iteration責務を移す
```

canonical sourceの意味変更を、build mechanicsの変更と同じPRで行わない。

## 結論

**production builderをmulti-Skill対応可能な形へ進める最初の変更は、Skillを増やすことではなく、現行CSW一つの生成結果を保ったまま、render済みSkill-tree入力をhost依存処理から分離することである。**

このwriterは将来の全source kindを吸収する万能rendererではない。P4で検討される`locale_tree`等のcanonical sourceは、そのsource contractをproduction側で確定した後、別のsource-kind adapterを通して接続する。
