# E5 Run 001 — cross-platform packaging preflight

- experiment id: `PQ-E5-005-R001`
- date: 2026-09-16
- source baseline: `develop/v0.5.0@e3b32685659e9393c38bcd3cfcfa5e9fd59255d8`
- protocol commit: `550a34af5ae9fbcb6d68c4d2c1ffc193e930f6be`
- evidence layer: Layer A / repository packaging preflight
- executor / evaluator: GPT-5.6 Sol、同一conversation context
- repository access: GitHub connector
- behavioral surface execution: **未実施**

## 1. 今回確認したもの

E5本試験の前段として、正本から各surfaceへ意味が渡る経路を読み、wrapperが中核契約を上書きしていないかを確認した。

確認対象:

- `src/ja-JP/ROUTER.md`
- `scripts/build.py`
- Claude Code / Codex共用plugin tree
- `adapters/openai-skill/ja-JP/` と `en-US/`
- `adapters/chatgpt-gpt/ja-JP/instructions-prefix.md`
- `adapters/microsoft-copilot/ja-JP/instructions.md`

比較軸はprotocolのP1〜P8とした。

## 2. packaging経路

### Claude Code / Codex

`build.py`は同じ`plugins/<locale>/skills/<skill>/SKILL.md`をClaude CodeとCodexで共有する。本文はcanonical Routerへlink置換を施したものから生成される。

Claude側では`disable-model-invocation: true`をfrontmatterへ追加する。これはinvocation affordanceの差であり、Router本文のauthority、provenance、split ownershipを書き換えない。

判定: `platform_affordance_only`

### ChatGPT GPT

canonical Routerの前に`instructions-prefix.md`を付加する。prefixは利用範囲・読み込み深度・採否・停止・価値判断を著者または外部委任へ返し、課題種別だけで利用を自動拡大・抑制しないことを明示している。

「KJ統合」という短い表現は残るが、同じ生成物にはRouter本体も続き、compatible realizationへの分離契約が読める。今回の静的比較だけではP5を上書きする独立命令とは判定しなかった。

判定: `equivalent`（P5の表現は今後のbehavioral runで要観察）

### Microsoft Copilot

限定Instructionsは、兄弟Skillを常時呼べないsurface制約を明示し、親和統合コアの「最小互換手順」をcomposite realizationとして埋め込む。一方で、それをCSW本体の所有アルゴリズムとは扱わず、`affinity-synthesis`完全実装や`iterative-inquiry-synthesis`完全実装を称しない。

したがって能力差そのものをsemantic failureとは扱わない。

判定: `platform_affordance_only`

### OpenAI Skill

interactive / meteredの両profileで、Skill本文自体はcanonical Routerから生成される。しかしadapterの`default_prompt`が追加で次を命令していた。

> 文化的体系とKJ法を使って

英語版も`use cultural frameworks and KJ`と同型だった。

これは、明示利用でも文化体系の`not_loaded / probe / preview / full / enacted`を委任に応じて選び、親和統合を必要時にcompatible realizationへ接続する正本契約より強い。とくに「skillが呼ばれた」ことから文化体系とKJの双方を必須化し得るため、P2 activation/loading calibrationとP8 wrapper non-authorityのdriftと判定した。

判定: `semantic_drift`

## 3. 最小修正

OpenAI adapterの`default_prompt`だけを修正する。interactive / meteredのinvocation policy差はそのまま保持する。

日本語:

- 旧: 文化的体系とKJ法を使うことを無条件に指示
- 新: **必要な範囲で**文化的体系による探索やcompatibleな親和統合への接続を使う

英語も同じ意味境界へ合わせる。

`short_description`は能力の説明であり実行命令ではないため、今回のfailureを直すためには変更しない。

生成物である`plugins/`、`.claude-plugin/`、`.agents/`、`dist/`は直接編集しない。

## 4. P1〜P8判定

| invariant | pre-fix | after adapter fix | 備考 |
|---|---|---|---|
| P1 authority | PASS | PASS | OpenAI promptも採否・価値判断を外部委任へ返していた |
| P2 activation/loading | **FAIL** | PASS（static） | OpenAI wrapperが文化体系+KJを常時命令 |
| P3 framework role | PASS | PASS | 答え・分類器への昇格は観測せず |
| P4 provenance/verification | PASS | PASS | Router/prefix/limited profileで境界保持 |
| P5 split ownership | PASS | PASS | M365 compositeは非同一性を明示。OpenAI修正後はcompatible affinityへの接続を明示 |
| P6 target return | PASS | PASS | canonical contractを各主要経路で保持 |
| P7 limitation honesty | PASS | PASS | M365が能力制約を明示 |
| P8 wrapper non-authority | **FAIL** | PASS（static） | OpenAI default promptを最小修正 |

ここでのPASSはrepository上の文面・生成契約に対する静的判定であり、モデル行動のPASSではない。

## 5. behavioral E5は未実施

protocolに固定した地域資料館packetを、Claude Code、Codex/OpenAI Skill、ChatGPT GPT、Microsoft Copilot等の実surfaceでまだ実行していない。

この会話から利用できないsurfaceを模倣して「cross-platform behaviorが同等だった」とは扱わない。E5全体の状態は**Layer A preflight completed / Layer B pending**とする。

## 6. 検証上の限界

- GitHub connectorからrepository内容を読み比べた静的監査である。
- `make build`、`make generated-artifacts-check`、`make check`は実行していない。
- GitHub Actionsによるcheck結果もない。
- generated artifactを直接編集していない。
- evaluatorはprotocol作成者と同じAIであり、独立評価ではない。

## 7. 判断

- runtime / Method Definition: **変更しない**
- adapter input: **OpenAI default promptのみ修正**
- generated artifact: **直接変更しない**
- promotion state: **変更しない**
- E5 behavioral completion: **未達**

次は、このprotocolのfixed behavioral packetを各実surfaceへそのまま渡し、P1〜P8を別々に比較する。surface固有の能力差は記録するが、それ自体をfailureへ数えない。
