# P4 Public Name Recheck — 2026-09-07

Status: current collision recheck; does not authorize production promotion

## 目的

production canonical sourceを作る前の名称gateについて、2026-09-07時点の公開GitHub / Web検索を再確認した。

research IDは変更しない。

```text
research id: affinity-synthesis
production installable candidate: material-led-synthesis

research id: iterative-inquiry-synthesis
production installable candidate: iterative-inquiry-synthesis
```

## 再確認結果

### `material-led-synthesis`

GitHub code searchでexact stringを検索したが、今回の再確認では一致を確認できなかった。

一般Web検索でも、同名の公開Agent Skillを示す結果は確認できなかった。

したがって現時点では、Layer 1のproduction installable name第一候補を `material-led-synthesis` のまま維持する。

ただし検索結果ゼロは、すべてのSkill registryや非index repositoryでの未使用を証明しない。canonical promotion直前にも再検索する。

### `iterative-inquiry-synthesis`

GitHub code searchでexact stringを検索したが、今回の再確認では一致を確認できなかった。

一般Web検索でも、同名の公開Agent Skillを示す結果は確認できなかった。

現時点ではproduction installable name候補を維持する。

### `Affinity Synthesis`

表示語としては一般語の検索noiseが多く、installable identifierの一意性を示す用途には向かない。

このため、

```text
display name: Affinity Synthesis
installable name: material-led-synthesis
```

の分離を維持する。

日本語表示名 `親和統合` も、特定の公式技法を独占する名称ではなく、このresearch Methodの表示語として用いる。

## KJ法との境界

`KJ法®` は系譜・参照元として保持し、public installable nameには用いない。

production runtime descriptionでも、公式KJ法の認定Skill・完全再現・標準実装であるとは称しない。

## 判定

名称gateのうち、**現時点の公開衝突再確認**は次の状態とする。

```text
material-led-synthesis       -> rechecked; no current exact collision found
iterative-inquiry-synthesis  -> rechecked; no current exact collision found
Affinity Synthesis           -> display-only; not used as installable identity
KJ Method / KJ法             -> lineage-only; not used as public Skill name
```

これはproduction promotionの承認ではない。

未通過のgateは引き続き残る。

- complete checkout上の `make research-skill-check`
- English sibling realizationsの独立査読
- production source / adapter metadata / builder generalization後のgenerated diff review
- release package内部composition validation

## 次の再確認点

canonical promotion直前に、少なくともGitHub code searchと利用可能なSkill registryを再確認する。

その時点で衝突が見つかった場合もresearch IDはrenameせず、production name projectionだけを変更する。
