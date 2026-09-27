# Production metadata split-ownership audit — 2026-09-18

- status: open known failure / repair deferred until canonical build can run
- baseline: `develop/v0.5.0@9225eec53ce571c0bcaf5de3085e306ef46eb58d`
- scope: CSW単体を説明するproduction metadataと、そのtracked / untracked生成先
- related requirements: PQ-01、PQ-05、PQ-08、PQ-10、PQ-12
- repair state: **not repaired**
- regression fixture: **not created**
- production promotion: unchanged

## 1. 目的

thin-CSW / split-method移行後の責務境界と、production metadataの説明が一致しているかを確認する。

現行Routerは、材料のone-round affinity synthesisやmulti-round delta / reopen orchestrationが必要な場合、利用可能なら専用のcompatible realizationへ委ね、CSW自身はそれらの内部アルゴリズムを所有しないと明示している。

一方、production metadataの一部には、移行前の一体型CSWを前提にした「文化体系探索とKJ統合をCSW自身が組み合わせる」という説明が残っている。

この監査では、これを**実在するmetadata responsibility drift**として記録する。ただし、canonical inputを修正するとGit管理対象の生成物も再buildする必要があるため、正規buildを実行できない現在の環境では修正を開始しない。

## 2. 正本側の責務境界

現行の日本語 / 英語Routerはいずれも、少なくとも次を明示している。

- 文化体系は一時的な認知場として使う。
- one-round material synthesisは `affinity-synthesis` またはcompatible realizationへ委ねる。
- multi-round delta / reopenは `iterative-inquiry-synthesis` またはcompatible realizationへ委ねる。
- CSWはそれらの内部アルゴリズムを所有しない。
- compatible realizationが実行されていない場合、親和統合やmulti-round orchestrationを実行済みと称しない。
- KJの認知姿勢や問いの生成はCSW側で参照できても、framework outputはgrouping / labelの権威にならない。

したがって、production metadataが「CSW自身がKJ材料統合を実行するSkill」であるかのように読める場合、現在のsplit ownershipより強い責務をCSWへ戻してしまう。

## 3. 確認したdrift

### 3.1 `src/manifest.json`

ja-JP description:

> 文化的体系による構造候補の探索とKJ法による断片統合を組み合わせ…

en-US description:

> ...opens cultural frameworks as temporary cognitive fields, and combines them with KJ integration...

このdescriptionはOpenAI SkillのfrontmatterやClaude/Codex Skill treeにも流れるため、単なる内部説明ではない。

**判定:** driftあり。

### 3.2 `adapters/claude-code/locales.json`

ja-JP / en-USとも、CSWが文化体系探索とKJ統合を一体で行う説明を保持している。

このdescriptionは `build_claude()` / `build_codex_plugin()` により、少なくとも次へ投影される。

- `plugins/cultural-substrate-weaving-*/.claude-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-*/.codex-plugin/plugin.json`
- root `.claude-plugin/marketplace.json` のplugin description
- locale-specific standalone marketplace package

**判定:** driftあり。

### 3.3 OpenAI Skill `short_description`

ja-JP:

> 文化的体系とKJ法で問い・関係・状態・空白・来歴を探索・統合する

en-US:

> Explore and integrate questions, relations, states, gaps, and provenance with cultural frameworks and KJ

`default_prompt`は既に「必要な範囲で文化体系探索を行い、必要時にcompatibleなaffinity-synthesisへ接続する」契約へ修正済みである。そのため、現在は同じadapter内でshort descriptionとdefault promptの責務表現が揃っていない。

interactive / metered間のshort descriptionは同一なので、profile差の問題ではない。

**判定:** driftあり。

### 3.4 ChatGPT GPT instructions prefix

ja-JP:

> 本スキルが提供する認知操作・文化体系資料・KJ統合・来歴記録の詳細

en-US:

> ...cognitive operations, cultural-framework resources, KJ integration, and provenance recording provided by this skill

prefixだけを読むと、KJ integrationそのものをCSWが提供するように見える。後続のRouterにはsplit ownershipがあるが、wrapper側の説明が正本より強い。

**判定:** driftあり。

### 3.5 root Claude marketplace description

`scripts/build.py` の `write_root_marketplace()` は、root marketplace descriptionを次でhard-codeしている。

> Localized skills for cultural-framework exploration, KJ integration, and provenance-aware structural work.

これは `.claude-plugin/marketplace.json` へそのまま生成されている。

**判定:** driftあり。

## 4. 生成済みtracked artifactで確認した伝播

現行tracked artifactにも、正本入力の旧表現が実際に投影されている。

### 4.1 Skill frontmatter

- `plugins/cultural-substrate-weaving-ja/skills/weave/SKILL.md`
- `plugins/cultural-substrate-weaving-en/skills/weave/SKILL.md`

frontmatter descriptionは `src/manifest.json` のlocale descriptionを使っているため、旧責務表現が残る。

### 4.2 Claude plugin metadata

- `plugins/cultural-substrate-weaving-ja/.claude-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-en/.claude-plugin/plugin.json`

`adapters/claude-code/locales.json` のdescriptionが反映されている。

### 4.3 Codex plugin metadata

- `plugins/cultural-substrate-weaving-ja/.codex-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-en/.codex-plugin/plugin.json`

top-level descriptionと `interface.shortDescription` の双方に旧表現が反映されている。

### 4.4 root Claude marketplace

- `.claude-plugin/marketplace.json`

root descriptionは `scripts/build.py` のhard-coded文字列、各plugin descriptionはClaude locale metadataから生成されるため、両層にdriftがある。

## 5. 同じfailureへ含めないもの

### Microsoft 365 limited composite

Microsoft 365 adapterは、独立sibling Skillを常に呼べないsurface制約のため、最小compatible material-synthesis fallbackをInstructionsへ埋め込む**limited composite realization**として設計されている。

adapter本文 / package READMEは、少なくとも次を明記する。

- CSW本体が材料統合アルゴリズムを所有する意味ではない。
- full `affinity-synthesis`を称しない。
- KJ法の公式実装を称しない。
- full `iterative-inquiry-synthesis` governanceを称しない。

したがって、Microsoft 365の「材料統合を含む」表現を、他surfaceと同じ理由で自動的にdrift判定しない。

必要なら別途、limited compositeの短いagent descriptionがこの制約を十分伝えるかを評価するが、今回のfailureとは分ける。

## 6. 修正時に守る意味上の不変条件

最終文面そのものは、正規build可能な修正branchで決める。少なくとも次を守る。

1. CSWの主要責務は、文化体系を一時的な認知場として開くこと、候補・差分・来歴を保持すること、対象へverification handoffすることとして説明する。
2. one-round material synthesisをCSW自身の所有機能として説明しない。
3. 材料統合へ触れる場合は、必要に応じてcompatible affinity-synthesis realizationへ接続する表現にする。
4. multi-round orchestrationをCSW自身の所有機能として説明しない。
5. KJの認知姿勢を参照できることと、KJ/affinity synthesis algorithmを所有することを区別する。
6. ja-JP / en-USで同型の責務境界を保つ。
7. OpenAI interactive / meteredでshort descriptionの意味を変えない。
8. Microsoft 365 limited compositeのsurface-specific exceptionを消さない。
9. descriptionを弱くしすぎて、CSWの探索・provenance・target return能力まで消さない。
10. metadata修正を、runtime / Method Definitionの新しい責務変更として扱わない。

## 7. 修正対象となるcanonical input

build可能環境で、少なくとも次を同一branchで確認・修正する。

- `src/manifest.json`
  - ja-JP / en-US locale description
- `adapters/claude-code/locales.json`
  - ja-JP / en-US description
- `adapters/openai-skill/ja-JP/openai.interactive.yaml`
- `adapters/openai-skill/ja-JP/openai.metered.yaml`
- `adapters/openai-skill/en-US/openai.interactive.yaml`
- `adapters/openai-skill/en-US/openai.metered.yaml`
  - short_descriptionのみ。現行default_promptはsplit ownershipに整合しているため、不要に書き換えない。
- `adapters/chatgpt-gpt/ja-JP/instructions-prefix.md`
- `adapters/chatgpt-gpt/en-US/instructions-prefix.md`
  - 「CSWがKJ統合を提供する」という説明をsplit ownershipへ整合
- `scripts/build.py`
  - root Claude marketplace descriptionのhard-coded文言

## 8. 修正時に再生成するtracked artifact

canonical inputの修正後は**手編集せず**、`make build`で再生成する。

少なくとも次が差分候補になる。

- `.claude-plugin/marketplace.json`
- `plugins/cultural-substrate-weaving-ja/skills/weave/SKILL.md`
- `plugins/cultural-substrate-weaving-en/skills/weave/SKILL.md`
- `plugins/cultural-substrate-weaving-ja/.claude-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-en/.claude-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-ja/.codex-plugin/plugin.json`
- `plugins/cultural-substrate-weaving-en/.codex-plugin/plugin.json`

`.agents/plugins/marketplace.json`は現行buildではdescriptionを持たないため、今回のmetadata driftから直接変わらない可能性が高い。実際のbuild diffで確認する。

OpenAI / ChatGPT GPT / Microsoft 365の `dist/` はGit管理外であるため、build後に生成結果を検査するがrepositoryへ直接コミットする対象ではない。

## 9. 修正候補文面

実装時の出発点として、意味境界を次のように置ける。

### ja-JP — manifest / Skill frontmatter向け

> 文化的体系を一時的な認知場として開き、問い・関係・状態・空白・来歴を探索し、必要に応じてcompatibleな親和統合や反復統合へ接続する補助AIスキル。利用範囲、採否、価値判断は著者またはスキル外の委任に従う。

### en-US — manifest / Skill frontmatter向け

> A complementary AI skill that opens cultural frameworks as temporary cognitive fields, explores questions, relations, states, gaps, and provenance, and connects to compatible affinity or iterative synthesis realizations when needed. Usage scope, adoption, and value judgments follow the author or delegation outside the skill.

短いhost metadataでは、これを圧縮してよい。ただし「CSW自身がKJ integrationを所有する」表現へ戻さない。

## 10. regression fixtureの扱い

現時点では修正前failureが存在するが、repairが完了していないため、**今すぐpassing regression fixtureを追加しない**。

修正branchでは、過度に具体的な定型文を固定せず、次のsemantic predicateへ縮約できるかを検討する。

- CSW descriptionがcultural-framework explorationを保持する。
- provenance / target returnまたはcompatible handoffを保持する。
- CSW単体がone-round KJ / affinity synthesisを所有すると読める旧表現を含まない。
- ja/enで同型。
- OpenAI short descriptionとdefault promptが責務境界で矛盾しない。
- generated tracked metadataがcanonical inputと一致する。

修正前の単語列だけを禁止するtestにはしない。E7 follow-upで経験したfixture over-specificationを繰り返さない。

## 11. 完了条件

このfailureをclosedへ移すには、同一の修正branchで次を満たす。

1. canonical inputをsplit ownershipへ整合。
2. ja-JP / en-USを同時更新。
3. `make build`を実行。
4. tracked generated artifactの差分をreview。
5. `make generated-artifacts-check`を実行。
6. 関連unit testを実行。
7. 実行可能なら `make check`まで確認。
8. passing regression fixtureを追加する場合は、意味上の不変条件へ縮約。
9. E7 inventoryをopenからcoveredへ更新。
10. repairをproduction promotionの根拠へ読み替えない。

## 12. 今回の判断

- runtime / Method Definition変更: **なし**
- canonical metadata修正: **今回は行わない**
- generated artifact直接編集: **行わない**
- regression fixture追加: **行わない**
- E7 status: **open known failureとして記録**
- 次の実装条件: **canonical buildを実行できる環境**

この監査によってfailureの存在、影響範囲、正本、生成先、例外、完了条件は固定できた。次の作業は、build可能環境でこの一群を一括修正することであり、surfaceごとに別branchへ分割しない。
