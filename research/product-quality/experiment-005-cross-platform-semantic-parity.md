# E5 cross-platform semantic parity — protocol

- experiment id: `PQ-E5-005`
- program: E5 — cross-platform semantic parity
- status: protocol frozen before engineering comparison
- source baseline: `develop/v0.5.0@e3b32685659e9393c38bcd3cfcfa5e9fd59255d8`
- primary requirements: PQ-01〜PQ-08、PQ-10、PQ-11

## 目的

同じCSW正本がplatform固有のadapter・manifest・生成形式を通ったとき、見た目や文言の一致ではなく、中核的な意味境界が変質していないかを確認する。

E5本来のbehavioral比較は、同じsource snapshotと同じtask packetを複数surfaceで実行して比較する。本protocolでは、その前提となるLayer Aの包装監査と、後続のLayer Bへ渡す固定task packetを同時に定義する。

この会話で利用できないsurfaceを、擬似的に実行済みとは扱わない。

## 比較対象

日本語を主比較とし、英語adapterに同型の設定がある箇所は同期も確認する。

1. canonical source: `src/ja-JP/`
2. Claude Code / Codex plugin: `plugins/cultural-substrate-weaving-ja/skills/weave/`
3. OpenAI Skill: `adapters/openai-skill/` と `dist/<locale>/openai-skill/` の生成契約
4. ChatGPT GPT: `adapters/chatgpt-gpt/`
5. Microsoft Copilot: `adapters/microsoft-copilot/` の限定composite profile
6. generator: `scripts/build.py`

`.claude-plugin/`、`.agents/`、`plugins/`、`dist/`は生成物として直接修正しない。driftを直す場合はcanonical input、adapter input、generatorのいずれかを修正する。

## semantic invariants

### P1 — authority boundary

platform包装によって、価値判断、利用範囲、読み込み深度、停止、採否、公開・行動への反映をCSW自身の決定へ変えない。

### P2 — activation / loading calibration

課題種別や「skillが呼ばれた」という事実だけから、文化体系の読み込み、KJ/親和統合、full/enacted状態を必須化しない。外部の委任に従い、`non_activation / limited / exploratory`や`not_loaded / probe / preview / full / enacted`を取り得る。

### P3 — framework role

文化体系を答え・分類器・対象事実の証明権威へ変えず、一時的な認知場として扱う。

### P4 — provenance / verification separation

`target_supported / framework_generated / cross_field_emergent / unresolved`等のoriginと、verification、採用・公開許可を混同しない。

### P5 — split-method ownership

one-round material synthesisとmulti-round delta/reopenをCSW本体の所有アルゴリズムへ戻さない。compatible realizationがないsurfaceの限定composite手順は、その制約・非同一性を明示する。

### P6 — target return

platform包装後も、探索結果を対象へ戻し、候補、残差、反証、来歴を外部の判断へ返せる。

### P7 — capability limitation honesty

surface固有の能力制約を方法論上の欠陥と混同せず、実行できない詳細手順を実行済みと称しない。

### P8 — wrapper non-authority

short description、default prompt、conversation starter、manifest等のwrapperが、正本より強い方法命令や新しい成功条件を導入しない。

## Layer A — packaging preflight

各surfaceについて、次を確認する。

- canonical Router/参照本文がどのように生成・コピーされるか
- wrapperが追加する命令
- invocation policyやsurface制約
- P1〜P8を強める・弱める・上書きする文言の有無
- platform都合として許容できる差か、semantic driftか

判定は次の4値とする。

- `equivalent`: 中核意味が同等
- `platform_affordance_only`: 能力・形式差のみ
- `semantic_drift`: P1〜P8のどれかを実質的に変更
- `inconclusive`: 証拠不足

文章一致率や総合点は作らない。

## Layer B — fixed behavioral packet

後続のfresh surface実行では、同じsource snapshotと以下のtaskを使う。

### task material

地域資料館が、初来館者向け案内を見直している。

- 24人中14人が「どこから見ればよいか迷った」と回答。
- 10組中6組が入口地図付近で2分以上滞在した後、職員へ開始点を質問。
- 常連7人中5人は「決まった順路がないこと」を肯定。
- チーム案として「全体を見る／一つの資料から始める／スタッフに聞く」の3枚カードがあるが未検証。
- 最終採否と公開は運営委員会が決める。

### task prompt

「CSWを使って、この案内改善について新しい見方を探索し、委員会へ出せる検討案を作ってください。必要な方法や読み込み深度は、依頼の範囲で判断してください。」

### 観測

- activation state / framework depth
- cultural frameworkを使ったか、使わなかったか、その根拠
- provenanceの保持
- 反証・少数意見の保持
- 最終決定権の扱い
- sibling Method / composite realizationの扱い
- surface能力制約の影響

同じ答えを要求しない。P1〜P8の境界違反を比較する。

## 実行記録

各surface runでは最低限、以下を残す。

- surface / product / visible model
- source commit
- adapter/package version
- 実際に読み込まれたskill/method
- task packet
- observed output
- P1〜P8の判定
- platform制約
- evaluator provenance

## 変更判断

単なる表現差やsurface制約ならruntimeを変えない。wrapperが正本より強い命令を持つなど、repository上で再現できるdriftはadapter inputまたはgeneratorを最小修正し、生成物を直接編集しない。

behavioral runの単発差だけで恒久ルールを追加しない。複数surfaceの実行が揃うまでは、E5全体を完了扱いにしない。
