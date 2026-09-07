# P2 CSW subtree parity gate — 2026-09-07

## 目的

三Skill化のresearch lineでは、`suite-manifest.json`、package source descriptor、target naming、entry transform、adapter metadata、Skill-tree materializerまでを段階的に外部化した。

次にproduction builderをmulti-Skill化すると、既存のCultural Substrate Weavingまで新しい生成経路へ巻き込まれる可能性がある。その前に、research側のcanonical renderが、現在Git管理されているproduction生成物と同じCSW Skill subtreeを再現できることを回帰条件として固定する。

この検査は、companion Skillをproductionへ昇格させる承認ではない。また、canonical `src/`からKJ法由来部分を削る判断でもない。

## 比較対象

現時点でGit管理されているja-JP production pluginのCSW subtreeを基準にする。

```text
plugins/cultural-substrate-weaving-ja/skills/weave/
  SKILL.md
  references/...
```

research materializerからは、ja-JPについて次の二つを一時領域へ生成する。

```text
claude_plugin
codex_plugin
```

両distributionは現在、同じ `skills/` treeを共有する設計である。そのため、それぞれの

```text
skills/weave/
```

について、相対file pathの集合と各fileのbyte列をtracked production subtreeと比較する。

## なぜOpenAIをこのgateへ含めないか

OpenAI Skillのproduction出力は`dist/`配下であり、Git管理するcanonical comparison targetではない。

また、OpenAIはprofileごとに`agents/openai.yaml`を持ち、Skill subtree外のadapter metadataもpackage contractへ入る。このgateの目的はhost package全体のparityではなく、**既存CSW Skill subtreeの生成意味を新しいresearch経路が変えていないこと**を固定することである。

OpenAIのhost package parityは、production builder generalizationへ進む際に別の比較として扱う。

## 回帰テスト

`tests/test_research_csw_subtree_parity.py` を追加する。

テストはrepository外のtemporary directoryへresearch materializerを実行し、次を確認する。

1. ja-JP Claude materializationがpartialではない。
2. `skills/weave/` が生成される。
3. materialized subtreeとtracked production subtreeでfile path集合が一致する。
4. 対応する全fileのbyte列が一致する。
5. ja-JP Codexについても、共有Skill treeとして同じ比較が成立する。

比較は文意の近さではなくbyte parityとする。既存CSWの生成結果を意図せず変えた場合、差分を「ほぼ同じ」として通さないためである。

## このgateが保証すること

テストが通る場合、現在のresearch packaging contractについて次を言える。

- `canonical_manifest`からCSW runtime entryとreferencesを読む境界が、tracked production subtreeと一致する。
- research materializerが再利用する`skill_frontmatter()`と`replace_router_links()`の組み合わせが、現在のja-JP Claude/Codex CSW subtreeを再現する。
- companion Skillを同じbundleへ加える前段で、既存CSW subtreeを変えない基準線を機械的に持てる。

## このgateが保証しないこと

次は判定しない。

- Claude Code / Codex上の実routing挙動。
- companion Skillの方法上の正しさ、有効性、公開準備。
- ja-JP三Skill bundle全体のhost package完成度。
- en-US companion realizationのparity。
- OpenAI `agents/openai.yaml`、plugin manifest、marketplace、README、ZIP、release assetのparity。
- ChatGPT GPT / Microsoft Copilot composite realizationの内部composition。
- canonical CSWからKJ統合責務を外してよいか。

したがって、このgate通過をproduction migrationやrelease readinessの代替にしない。

## Production generalizationへの境界

production `scripts/build.py`をmulti-Skill化する場合、少なくとも次の順序を守る。

1. 現行CSW subtree parityを維持する。
2. companion Skill subtreeを追加する。
3. Skill-level source/renderとbundle-level metadata生成を分ける。
4. OpenAIのper-Skill metadataとClaude/Codexのbundle metadataを混同しない。
5. generated artifact checkを新しい期待treeへ更新する前に、旧CSW基準線との差を明示する。
6. canonical `src/`の責務分離は、package生成経路が安定してから別変更として行う。

この順序により、方法論の分離、package topologyの変更、既存CSW生成物の変更を一つの大きな差分へまとめない。

## 実行状態

この変更では、production builder、canonical `src/`、generated plugin、release artifactを変更しない。

追加するのはparity regression testと、その検査境界を記録する本書だけである。

GitHub Actionsは現在意図的に無効化されているため、CI成功をこの文書から主張しない。完全なcheckoutで`make check`を実行できる環境では、この新テストも既存`unittest discover`の一部として実行される。

## 判断

**research Skill-tree materializerからproduction multi-Skill builderへ進む前に、既存ja-JP CSW subtreeのbyte parityを必須の回帰基準として置く。**

この基準を保持したまま、次の段階ではhost package全体の差分を切り分け、production generalizationに必要な最小共通関数を検討する。
