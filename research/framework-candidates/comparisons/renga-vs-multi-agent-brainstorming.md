# Medieval renga linked verse vs ordinary multi-agent brainstorming

Status: research differentiation / no runtime promotion

## Purpose

複数の生成AIを同じ課題へ参加させても、探索が自動的に広がるとは限らない。

2026年の研究では、multi-agent LLMの密な相互作用が早い収束とsemantic diversityの低下へ結び付く結果が報告されている。別の研究では、discussion structureとmodel choiceが創造性へ別々に影響しうることが示されている。また、LLMの類推生成では、類推先のdomainが偏りやすく、多様性を増やすほど品質が下がるtrade-offも報告されている。

References:

- Chen et al., “Diversity Collapse in Multi-Agent LLM Systems: Structural Coupling and Collective Failure in Open-Ended Idea Generation,” Findings of ACL 2026
  - https://aclanthology.org/2026.findings-acl.13/
- Hu et al., “Multi-agent AI systems outperform human teams in creativity”
  - https://arxiv.org/abs/2605.17885
- Shen et al., “On the Diversity of Analogy Making in Large Language Models”
  - https://arxiv.org/abs/2608.03233

これらの研究はrengaの有効性を示すEvidenceではない。CSWで比較すべきfailure modeを具体化するために参照する。

## Core distinction

| Method | Interaction unit | Diversity mechanism | Main failure mode |
|---|---|---|---|
| independent parallel brainstorm | targetだけを見る独立出力 | 相互影響を減らす | 出力同士が接続せず、統合負荷が高い |
| ordinary round-robin | 前の会話全体を踏まえて順番に応答 | 明示的な制約なし | 早い案や高status agentへ収束しやすい |
| persona-diversified agents | 異なるroleやpersonaから応答 | actor identityの差 | 表現だけ違い、内容が同じになる可能性がある |
| medieval-renga candidate | 直前への接続と長期的な主題固定の解放 | interaction topologyと系列制約 | shiftを強制しすぎると関連性と収束能力を失う |

## What renga may add

候補価値は「多人数」でも「日本的な創造性」でもない。

検証対象は次の構造である。

~~~
previous contribution
  -> explicit local interpretation
  -> next contribution keeps one local link
  -> repeated theme is released
  -> another target dimension opens
~~~

この構造はpersona diversityとは独立している。同じmodel、同じpersonaでもinteraction ruleだけを変えて比較できる。

## Strong counter-hypothesis

ordinary facilitationで十分な可能性がある。

たとえば、

- 前案との接点を一つ書く
- 同じカテゴリの連続を避ける
- 別の観点を出す

という一般的なbrainstorm ruleで同等以上の結果が出るなら、文化体系としてrengaをruntimeへ載せる理由は弱い。

また、historical rengaの厚い文脈を読み込むことで、探索より詩的語彙や文化説明が増えるなら逆効果である。

## First comparison

同じSIer設計challengeで最低限次を比較する。

A. independent parallel ideas  
B. ordinary round-robin discussion  
C. persona-diversified discussion  
D. generic local-link + topic-release rule  
E. renga profile contact + de-binding

EがDを上回らなければ、文化固有frameworkとしての採用を支持しない。

## Measurements

一つの総合scoreにはしない。

- local semantic coherence
- global semantic spread
- unique target dimensions opened
- later target-supported question / test yield
- unsupported leap rate
- reviewer correction cost
- time / turns to premature convergence
- non-activation correctness
- framework-specific language residue after de-binding

global spreadが上がっても、unsupported leapとcorrection costが増える場合は成功としない。

## Product-value interpretation

SIerで価値が出るのは、単に案が増えた場合ではない。

たとえば設計レビューで、最初に出たcache最適化の周辺だけを精緻化していた状態から、placement authority、利用者によるreclaim、lease fencing、result verificationのような別の設計責務へ移り、それぞれがreview questionやtest obligationへ戻った場合に探索増分がある。

一方、無関係な論点を増やしただけなら、探索多様性が高くてもproduct valueとはみなさない。

## Research novelty candidate

CSW-R2候補:

> source-bounded cultural interaction grammarをLLM multi-agent systemのcommunication topologyとして一時的に適用すると、persona diversityや独立samplingとは異なる形で、local coherenceを保ちながらcollective diversity collapseを遅らせられるか。

新規性は、rengaが創造的だという主張には置かない。

- historical source boundaryを保持する
- interaction grammarだけを抽出する
- target authorityへ文化的意味を移さない
- generic rule baselineと直接比較する
- diversityとquality / correction costを分離評価する

という研究設計に置く。

## Runtime decision

この比較を実行する前にruntimeへ昇格させない。

generic local-link + topic-release ruleが同等なら、renga固有のruntime frameworkは追加しない。その場合も、source-bounded interaction grammarを比較した研究結果はRegistryのnegative evidenceとして残す。
