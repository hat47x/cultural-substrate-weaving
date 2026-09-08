# P2 CSW subtree parity gate — refreshed 2026-09-08

Status: research regression contract; does not authorize production promotion

## 目的

current active research lineのSkill-tree materializerが、既存Cultural Substrate Weavingのtracked production Skill subtreeをbyte-for-byte再現できることを固定する。

これはcompanion Skillをproductionへ昇格させる承認でも、canonical CSWからKJ由来責務を外す判断でもない。

## なぜactive research branchを基準にするか

このgateが最初に作られた後、`materialize_skill_tree.py`自体がactive P4で更新された。

したがって古いdevelop branch上のmaterializerへparity testを掛けても、現在promotion designが利用しているmaterializerの回帰保証にはならない。

本gateはcurrent active `research/kj-skill-delegation-v0.5`へ載せ、**現行research materializerとtracked production CSW outputの差**を観測する。

## 比較対象

tracked production baseline:

```text
plugins/cultural-substrate-weaving-ja/skills/weave/
plugins/cultural-substrate-weaving-en/skills/weave/
```

research materializer output:

```text
claude_plugin -> skills/weave/
codex_plugin  -> skills/weave/
```

各locale / distributionについて、

- 相対file path集合
- 各fileのbyte列

を対応するtracked subtreeと完全一致で比較する。

## Locale readinessをこのgateへ固定しない

### ja-JP

通常materializationとして実行する。

### en-US

`allow_partial=True`を指定するが、これはen-USをpartial-readyと宣言するものではない。

このflagは、suite全体のhost readinessが将来変化しても、**既存CSW `weave/` subtreeだけを独立して比較できるようにするprobe許可**として使う。

locale / distribution全体のmaterializabilityはsuite manifest、adapter metadata、host materializer側のauthorityが判断する。

```text
CSW subtree parity
  != locale readiness
  != host readiness
```

## なぜOpenAIをここへ含めないか

OpenAIのproduction Skill treeはtracked plugin subtreeではなく`dist/`側で生成され、profile固有`agents/openai.yaml`も持つ。

本gateは**低位CSW Skill subtree rendererのtracked baseline parity**だけを担当する。

OpenAI interactive/metered parity、host metadata source parity、Claude/Codex bundle外周はcross-surface host-package oracle側で扱う。

## 回帰テスト

`tests/test_research_csw_subtree_parity.py`はrepository外temporary directoryへcurrent research materializerを実行し、次を確認する。

1. ja-JP Claudeの`skills/weave/`がtracked ja subtreeとbyte-identical。
2. ja-JP Codexの`skills/weave/`が同じtracked ja subtreeとbyte-identical。
3. en-US Claudeの`skills/weave/`がtracked en subtreeとbyte-identical。
4. en-US Codexの`skills/weave/`が同じtracked en subtreeとbyte-identical。
5. file集合の増減もbyte差と同じくfailする。

文意の近さではなくbyte parityとする。

## このgateが保証すること

実行PASSが記録された場合に限り、少なくとも次を言える。

- current research materializerのCSW `canonical_manifest` renderがtracked production subtreeを変えていない。
- Claude / Codex向けcurrent CSW Skill tree semanticsが既存baselineと一致する。
- companion subtreeやproduction source-kind wiringを検討する前に、既存CSWを壊していない基準線を持てる。

## このgateが保証しないこと

- complete checkout全体のPASS。
- OpenAI host package parity。
- Claude/Codex plugin manifest / README / marketplace parity。
- companion Skillの方法上の妥当性。
- English independent reviewの完了。
- production adapter metadata promotionの承認。
- real-host invocation / routing behavior。
- production builder / validator generalizationの安全性。
- canonical CSW責務分離の承認。
- production promotion / release readiness。

## Production generalizationへの順序

```text
current active research materializer
  -> existing CSW subtree parity gate
  -> host-package cross-surface oracle
  -> production mechanical writer / validator refactor
  -> production source-kind / inclusion wiring
  -> intentional companion promotion
  -> canonical CSW responsibility migration
```

`locale_tree` sibling sourceはpackage-closed production sourceとして扱い、canonical `SKILL.md`をCSW router rendererへ無理に流し込まない。

既存CSW parity、package topology変更、canonical method ownership変更を一つの差分へまとめない。

## 実行状態

このPRはtest/docだけを追加し、production builder、canonical `src/`、generated plugin、release artifactを変更しない。

GitHub Actionsは無効で、Remote Desktopの完全checkout端末も現在offlineである。したがってtest sourceの存在やGitHub mergeabilityをexecution PASSとは扱わない。

## 判断

**既存CSW subtree parityは、古いdevelop materializerではなくcurrent active research materializerに対して観測する。suite全体のreadinessは別authorityへ残したまま、tracked production baselineのbyte parityだけをこのgateで固定する。**
