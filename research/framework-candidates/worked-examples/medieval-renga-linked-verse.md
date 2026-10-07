# Medieval renga linked-verse worked example

Status: hypothetical / research-only

## Target

分散計算基盤の初期設計レビューで、複数agentに「クラウド費用を減らしながら信頼できる実行を増やす改善案」を出させている。

通常のmulti-agent discussionでは、最初に出た「cache localityを改善する」という案へ全agentが集まり、後続turnもcache hit率、eviction、prefetchの精緻化に集中している。

cacheは有力な論点だが、探索空間全体が一つの技術へ固定されている。

## Framework contact

このpassでは、各turnに二つだけ要求する。

1. 直前の候補との接続を一文で示す。
2. 直前まで支配していた主題をそのまま延長せず、別の対象次元へ移る。

### Turn A — current material

> Artifact cache localityを高め、Worker間転送を減らす。

この案はそのまま材料として保持する。

### Turn B — local link, first release

接続:

> cache localityが効くのは、どのWorkerへplacementするかを決める前提が安定している場合である。

shift:

> 転送量だけでなく、placement proposalとsecurity authorizationを分け、cache hintがAuthorityへ昇格しない設計を確認する。

target-side question:

- cache hitはScheduler signalに留まり、Data ClassやAssuranceのhard constraintを上書きしていないか。

### Turn C — link to B, release from placement optimization

接続:

> Placementの安全性を独立に確認しても、選ばれたWorkerが途中で資源提供をやめる可能性は残る。

shift:

> 性能最適化からLocal Governorのreclaimへ移り、利用者が中央承認なしで資源提供を停止できる経路を確認する。

target-side question:

- Workerのreclaimがstale Leaseやlate Resultによって後から覆されないか。

### Turn D — link to C, release from Worker lifecycle

接続:

> reclaim後のlate eventを拒否するには、現在の実行権限と古い権限を区別する必要がある。

shift:

> Lease fencingとrestart durabilityへ移り、Control Plane再起動後も古いLeaseが復活しないことを確認する。

target-side question:

- fence epochは永続化され、Lease historyの整理後も単調増加を保つか。

### Turn E — link to D, release from control-plane authority

接続:

> durable fencingで実行権限を制御しても、返ってきた結果が正しいとは限らない。

shift:

> 実行権限からResult Verificationへ移り、Workerの自己申告successとAccepted Resultを分ける。

target-side question:

- Worker exit codeやResultClaimだけでaccepted resultへ昇格していないか。

## Target return

文化固有語を外すと、残る探索系列は次になる。

~~~
cache locality
  -> placement signal / authorization separation
  -> local reclaim
  -> lease fencing / restart durability
  -> result verification
~~~

重要なのは、この鎖を「正しいarchitecture」とみなすことではない。

通常のdiscussionがcache最適化だけへ集中した状態から、直前の論点を捨てずに別のauthority boundaryへ順次移り、次の具体的なreview questionを残せたことが候補価値である。

## Evidence to collect

比較時には少なくとも次を分ける。

- local coherence: 各turnが直前の材料へ説明可能に接続しているか
- target relevance: 対象の実際の要件・設計へ戻れるか
- exploration spread: 同一技術の言い換えではない対象次元が増えたか
- verification yield: 後続test / issue / design questionへ変換されたか
- correction cost: reviewerが無関係な飛躍を除去する負荷
- convergence timing: 何turnで一つの主題へ固定したか

semantic diversityだけを成功指標にしない。
