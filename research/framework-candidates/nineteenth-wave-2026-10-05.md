# Framework corpus nineteenth wave — 2026-10-05

Status: candidate-quality expansion / no runtime adoption

## Decision

上座部アビダンマの Paṭṭhāna（『発趣論』）に見られる条件関係の分析を、profile-readyの研究候補として追加する。

今回の目的は、二十四縁をITや組織へそのまま移植することではない。

CSWで取り出す構造核は、**「条件する側」「条件される側」「どのような仕方で条件となるのか」を分け、一つの結果に複数の異質な条件が収束する場合でも、一種類の矢印へ潰さずに保持する**ことである。

Pali Text SocietyはPaṭṭhānaをAbhidhamma-piṭakaの最終書とし、conditionalityを非常に詳細に分析する技術的な文献として説明している。Springerの研究項目も、Paṭṭhānaをdependent originationの比較的コンパクトな連鎖とは区別されるconditional-relationsの体系として位置づけている。

## Why this fills a real corpus gap

現行の `dependent-origination` はすでに強い候補であり、

- condition-chain;
- upstream-condition;
- cessation-counterfactual;
- dependency-reframing;

を提供している。

したがって、Paṭṭhānaを「もっと詳しい縁起」として追加しても価値はない。

今回埋めるgapはcoverage mapに残っていた **branching conditional networks** である。

具体的には、

- 一つの結果に複数条件が収束する;
- 一つの条件が複数結果へ広がる;
- 条件関係に同時・継起・相互・持続等の違いがある;
- 依存そのものは観測できてもrelation modeは未確定である;

といった状況を、一つのroot causeや一種類のdependency edgeへ早く畳まないための認知操作を候補化する。

## Product-value hypothesis

SIerの設計・障害分析では、「原因はXだった」という総括が早すぎると、再発条件が残る。

例えば認証エラーの背後に、

- credential validity;
- stale capability cache;
- heartbeat freshness;
- authoritative revision;
- queue redelivery;

が重なっている場合、それぞれは同じ種類の条件ではない。

Paṭṭhāna由来のcontactが有効なら、単に原因候補を増やすのではなく、**異なるcondition modeごとに別のテスト義務・監視点・authority boundaryを作れる**はずである。

worked exampleでは、rolling deployment後の分散job-control障害を題材に、この違いをtarget-side設計質問へ戻す。

## Strong counter-hypothesis

最大の比較対象は ordinary typed dependency graph / fault tree / causal map である。

de-binding後に残るものが、

1. nodeを置く;
2. edgeに種類を書く;
3. incoming edgeを複数残す;
4. evidenceを確認する;

だけなら、文化体系をruntimeへ持ち込む理由は弱い。

したがってprofile-ready化は採用判定ではない。

**普通の工学的dependency分析と比較できる程度に、source basis、固有の認知操作、stop condition、non-activationを明示できた**という段階である。

## Historical / doctrinal boundary

- PaṭṭhānaはTheravāda Abhidhammaに固有の文脈を持ち、「仏教一般の因果論」として扱わない。
- 二十四縁をtarget側の固定taxonomyにしない。
- dhamma、kamma、rebirth、解脱論等を対象領域へ移さない。
- 伝統的な成立・著者帰属の主張を、構造候補の正当化に必要な事実として扱わない。
- canonical statusをtarget-side evidenceの権威へ変換しない。
- relation mapが精緻であることを、因果関係が実証されたことと同一視しない。

## Target-return value

positive exampleでは、障害を一つのlinear root causeへ閉じず、

- prerequisite/presence;
- persistence from an earlier observation;
- concurrent state constraint;
- co-present eligibility;
- sequential opportunity;

というtarget-sideの異なる関係として分ける。

重要なのは、この英語ラベル自体でもない。

最終的に残すべきものは、

- cache invalidation test;
- heartbeatとcredentialのずれを再現するtest;
- stale deliveryがauthoritative revisionを上書きしないtest;
- scheduling eligibilityとexecution authenticationの分離;

といった対象側の検証項目である。

negative exampleでは、単純な三段階exportの最初でI/O errorが起きているだけの状況にmulti-condition networkを持ち込まず、non-activationとする。

## Runtime decision

runtimeへは採用しない。

次に比較する:

- current dependent-origination;
- ordinary typed dependency graph;
- fault-tree analysis;
- sequential / co-present / shared / reciprocal relationsが混ざった実務fixture;
- simple chainでnon-activationが正解となるfixture.

Paṭṭhāna由来のcontactが、普通のdependency分析では見落とすtarget-supportedなrelation-mode差分を安定して増やす場合にのみ、runtime候補として再検討する。

広範なefficacy benchmarkはまだ開始しない。
