# Twentieth framework wave — 2026-10-07

Status: research-only / no runtime promotion

## Purpose

Registryの件数を増やすのではなく、coverage mapで独立して扱われていなかった **sequential collaborative linking / controlled thematic release** を候補化する。

今回の候補は`medieval-renga-linked-verse`である。

## Why this operation now

現行corpusには、状態遷移、条件network、role-conditioned perspective、argument / objection structure、pacing、reception、provenance、route / spatial structure等がかなり揃っている。

一方、複数の生成者が一つの系列を作る際に、

- 直前の材料との接続を保つ
- 一つの主題の連続支配を弱める
- 系列を別方向へ開く
- 完全なrandom restartにはしない

というinteraction topologyそのものは独立operationとして薄い。

2026年のLLM研究では、multi-agent ideationでも密な相互作用が多様性を自動的に保証せず、早い収束を起こしうることが報告されている。類推生成についても、多様性と品質を別に見る必要が示されている。これらをCSWの効能Evidenceにはせず、比較すべきproduct failureとして使う。

## Candidate

- id: `medieval-renga-linked-verse`
- readiness: `profile-ready`
- runtime: no
- source basis: 3件
- positive fixture: 1件
- non-activation fixture: 1件
- comparison: ordinary / persona-diverse multi-agent brainstormingとの比較を追加

## Structural core

~~~
preceding material
  -> interpret local connection
  -> add one linked contribution
  -> release repeated theme/category
  -> open another target dimension
  -> return to target questions
~~~

この構造を中世連歌そのものと同一視しない。中世連歌からCSWが抽出した研究用の表現として扱う。

## Product-value hypothesis

SIerの設計探索では、生成AIを増やしても最初に出た技術案の周辺を精緻化するだけになることがある。

renga由来のcontactに価値があるなら、単に案数を増やすのではなく、

- cacheからplacement authorityへ
- placementからreclaimへ
- reclaimからfencingへ
- fencingからverificationへ

のように、直前との接続を説明できる状態で別の設計次元を開き、最終的にreview questionやtest obligationへ戻せるはずである。

## Counter-hypothesis

genericなfacilitation ruleで十分な可能性が高い。

したがって、runtime promotion前に必ず、

- independent brainstorm
- ordinary round-robin
- persona-diversified agents
- generic local-link + topic-release
- renga contact

を比較する。

文化名を外したgeneric ruleと差が残らなければ、rengaはresearch profileのまま維持する。

## Academic novelty

CSW-R2の論文化候補として、文化体系の内容ではなく**source-bounded interaction grammar**をmulti-agent communication topologyとして用いる。

2026年研究が示すdiversity collapse / diversity-quality trade-offを背景に、

- local coherence
- global diversity
- target-supported yield
- unsupported leap
- correction cost

を分けて評価する。

CSW-R1が「何の構造で見るか」を扱うのに対し、R2は「複数生成者がどの接続規則で探索を受け渡すか」を扱う。

## Current decision

runtimeへは採用しない。

まずprofile、正例、non-activation例、ordinary baseline比較をRegistryへ揃える。その後も、generic ruleとの差が残るまではruntime promotionを支持しない。
