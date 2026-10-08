# CSW位置づけ更新に伴う内部の変更点調査

- 調査日: 2026-10-06
- 対象: `C:\GIT\hat47x\cultural-substrate-weaving\`（ブランチ `develop/v0.5.0`、HEAD `7972fb9`、VERSION 0.5.0）
- 読んだ根拠文書: `C:\GIT\cultural-substrate-weaving\cognitive-foundation-architecture.md`、`csw-2028-2031-positioning.md` §9・§10
- 兄弟リポジトリ: `C:\GIT\hat47x\sui-sensemaking`（`main` @ `2aea09bd`）、`C:\GIT\hat47x\sei-cognition`（`develop/v0.2.0` @ `0a52e4f`）
- 状態: 調査のみ。リポジトリのファイルは一切変更していない。以下の「案文」は適用していない。

## 0. 調査の範囲と限界

- 本環境にはPythonが無く（`python` は Windows ストアのスタブ）、`scripts/validate.py`、`make check`、`make tokens`、各テストは実行していない。テスト・検証の要求は、スクリプトとテストのソースを読んで判断した。
- `scripts/token_budget.py` は `dist/` へ書き込むため実行していない。語数・バイト数はNodeで読み取り専用に数えた。
- 行番号は `develop/v0.5.0` のHEADの作業ツリーによる。`src/en-US/` は ja-JP と同一構造であることと、ラベル語の出現位置が対応していることだけを確認し、英語本文の全文照合はしていない。
- `plugins/` と `dist/` は生成物なので、変更点は `src/`・`adapters/`・`scripts/` 側で数える。

## 1. 現行CSWと更新方針の対照

更新方針の要点は次の五つである。以下、(P1)〜(P5)で参照する。

- (P1) CSWは認識群のうち「問いを立て、深い洞察を生む部分（A1）」に寄与する。基盤は親和図法の深いラウンドとA型／B型の往復。
- (P2) 来歴ラベルは重視しない。判断の時点のスナップショットであり、カード原文へ立ち戻って語らせることが主眼。ラベルは「索引と警報」。
- (P3) 来歴の区別はSUI（親和図法キャンバス）が主体で、SEI等も担いうる。
- (P4) 領域能力を持たず、閉じた問題には使わない。人間の意図を先回りして抑制する安全関門を置かない。
- (P5) 製品間に必須依存を作らない。

### 1-1. 整合する記述（変更不要、または根拠として引ける）

| 箇所 | 現行の記述 | 対応する方針 |
|---|---|---|
| `src/ja-JP/ROUTER.md:3` | 価値判断・利用範囲・停止・採否の決定権は著者または外部委任に属する | P4（先回り抑制をしない）。決定を担わない点はA1への寄与と整合 |
| `ROUTER.md:21`、`ROUTER.md:56`（来歴 ≠ 行動許可）、`core/principles-and-constraints.md:11,44`、`governance/governance-and-records.md:23` | ラベルは採用・発話・外部化・停止の許可を自動的に決めない | P2。ラベルを関門にしない方向と既に一致。`evals/semantic-retention.json` が両ロケールで要求する |
| `ROUTER.md:19`、`core/discovery-pathway.md:88-110`、`docs/ja/maintainers/core-value-and-embodiment-policy.md:117-165`（§5） | 画一的な関門を置かず、五つの光で照らす。光は判定しない | P4。README.md:109 も同じ |
| `core/principles-and-constraints.md:93-110` | 本スキル固有の抑制規則を置くには、外部文書での説明と十分な統計的検証を要する | P4。新しい抑制規則（例：閉じた問題の非発動）をruntimeへ入れる場合の高い閾値になる（1-2の衝突1を参照） |
| `ROUTER.md:30`、README.md:9、`docs/ja/usage-context.md:5` | 領域固有知識・品質基準は本スキルが定義しない | P4（領域能力を持たない） |
| `core/cognitive-stance.md:60-67,81-94,126-128` | 立てた説明は元材料へ返し、材料の側から修正を受ける。「どこから生じた意味かを失うこと」が問題 | P2の「原文へ立ち戻って語らせる」と同方向。現行は「元材料へ返す」の語で書かれている |
| `core/principles-and-constraints.md:22-31` | 対象側材料／体系側材料／接触から生じたもの／判断の四つの情報面を別々に追えるようにする | ラベルを使わなくても成り立つ分け方。P2の下でも保てる |
| `core/iteration.md:63-79` | 後から支持されても、過去のroundへ遡って「最初から対象事実だった」と書き換えない | P2の「ラベルは時点のスナップショット」と一致 |
| `docs/ja/maintainers/core-value-and-embodiment-policy.md:8-33,83-98`（§1・§4） | 触媒的発見＝通常の連想の外にある構造に触れて問いの見え方を組み替える。仮説として保つ（§7、H1〜H5） | P1。A1（問いの構成）への寄与と実質的に同じ内容。効果未検証の扱いも一致 |
| README.md:11、README.md:129、`docs/ja/usage-context.md:45-53` | 検証段階であり、有効性は確立したと扱わない | 位置づけ文書でも「効果は未検証」を維持する根拠 |
| `AGENTS.md:7-11,34` | KJ・親和図法の内部はCSWが所有しない。Skill間のhard dependencyを作らない。欠けたrealizationは模擬せず明示する | P1（基盤は親和図法側）、P5。`methods/integration.md:113-125` も、compatible realizationが無くてもCSW単独で動くと書く |
| `docs/ja/maintainers/sibling-product-semantic-correspondence.md:14,39,106-108` | 兄弟製品との関係が深くても必須依存を意味しない。兄弟の正本は各リポジトリ。未mergeの提案は採用済みとして扱わない | P5。記述の過大化を防ぐ先行規則 |
| `research/skill-prototypes/affinity-synthesis/SKILL.md:157-169`、`README.md:26` | 図解↔叙述↔元材料の照合（map ↔ narrative ↔ source） | A型／B型の往復に相当する機構は、すでに `affinity-synthesis`（research prototype）側にある |
| `research/skill-prototypes/affinity-synthesis/references/TEMPLATE.md:55`、`iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md:23`、`affinity-map.schema.json:54` | `input_status` は閉じたtaxonomyを要求しない。ラベルは呼出側が持つ語彙の一例 | P2。ラベルを必須の語彙にしていない側の実装がすでにある |

### 1-2. 衝突する、または緊張がある記述

| # | 箇所 | 内容 | 扱いの案 |
|---|---|---|---|
| 1 | `ROUTER.md:32`、`core/activation.md:20`、`docs/ja/usage-context.md:41-47`、`evals/semantic-retention.json`（`forbidden_in_router` に「閉じた問題では通常手法を優先する」、`required_by_file[ROUTER.md]` に「課題種別そのものを、本スキル側の自動的な発動・抑制条件にはしない。」） | 方針P4「閉じた問題には使わない」は、現行のruntimeが明示的に禁じている「課題種別による自動の非発動」と正面から衝突しうる。usage-context.md:36-40 は閉じた問題を「単独で使う理由になりにくい状況」に挙げつつ、41行で「自動的な非発動条件ではありません」と書く | 位置づけ文書では「閉じた問題は主対象ではなく、価値が出にくい」と記述にとどめ、runtimeの発動・抑制規則にしない。runtimeへ入れる場合は principles:93-110 の高い正当化閾値と、semantic-retention の改訂が要る。推奨は前者 |
| 2 | `core/principles-and-constraints.md:33-44` は見出し「来歴ラベル」で四ラベルを正式に定義する節。`governance/governance-and-records.md:22`（帰属欄）、`governance/evaluation.md:14`（確認項目8に「ラベルを必要に応じて分け」）、`methods/integration.md:35-38,86-90`（handoffで区別するよう要求）、`core/iteration.md:69-75`（`origin`／`verification`の例） | 現行はラベルを「状態の語彙」として全層に通している。P2の「索引と警報にとどめる」と比べて前景に出すぎている。ただしいずれも「必要に応じて」で、許可には使わない | 語彙は残し、役割の説明を「索引・警報、原文再読の入口」へ書き換える（§2の順序を参照） |
| 3 | `AGENTS.md:20`（所有境界表で、四ラベルと関連する帰属規則をCSW runtimeの所有物として明記）、`sibling-product-semantic-correspondence.md:13`（ラベルの意味はCSW正本）、同:104 | 「来歴の区別はSUIが主体」（P3）と並べると、CSWが来歴の主体であるように読める | 二層に分けて書く。CSWが持つのは「体系由来の候補に由来の印を付け、対象へ返す」責務。原文へ戻れる経路そのものはSUI等が持つ。AGENTS.md:20 は文言を残し、ラベルは索引・警報であることの注記を足す |
| 4 | `docs/ja/maintainers/core-value-and-embodiment-policy.md:139`（由来の光）「既存の来歴ラベルがこの光を担う」、同:235（§9 変えないもの）「来歴ラベルは行動の許可を決めない」 | 139行は由来の光の担い手をラベルだけに読める。P2では、担い手はカード原文への再読とラベル（索引）の両方 | §10としての追記節で、139行を「ラベルと原文再読」へ読み替える旨を明記する |
| 5 | `src/manifest.json`（ja description）、`adapters/claude-code/locales.json:5`、`plugins/*/.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`、`plugins/*/skills/weave/SKILL.md` の frontmatter（いずれも「文化的体系による構造候補の探索とKJ法による断片統合を組み合わせ」） | 方針P1は「基盤は親和図法側、CSWはA1に寄与」。配布メタデータは、CSWがKJ統合を自前で組み合わせて持つと読める。`src/ja-JP/ROUTER.md` 自体は「二つの能力を組み合わせる」を `check_split_ownership.py` が禁じており、ルーターとメタデータの表現がずれている | 位置づけ確定後に、メタデータの説明文を揃える候補。変更は `src/manifest.json` と `adapters/` を正本として生成物へ伝わる（`make build`）。en-USでは `manifest.json` の description（"keeps its interpretation revisable by the target…"）と plugin.json の description（"Combines cultural-framework exploration with KJ integration…"）が食い違っている点も要確認 |
| 6 | `core/cognitive-stance.md:81-94`（「元材料へ返し」）、`methods/framework-application.md:119`（「独立した対象材料で支えられたものだけを `target_supported` へ移す」） | 位置づけ文書（§10-3、H4）は、原文の再読（来歴の区別）と、対象側の外部材料への戻し（誤りの検出）を別の機構として分ける。現行runtimeは「返す／戻す」の一語で両方を指しうる | 追記が要る（1-3を参照）。語義の切り分けのみで、規則は増やさない |
| 7 | README.md:18（三層図の「framework由来候補の帰属を保つ」）、README.md:5、README.en.md:17-19 | 「帰属を保つ」はラベル運用を連想させる。方針と矛盾はしないが、位置づけ段落を足す際の語の揃えが要る | 軽微。READMEの冒頭段落を足すときに併せて調整 |

### 1-3. 言及がなく、追記が要る箇所

調査した範囲（README.md、README.en.md、AGENTS.md、`src/`、`adapters/`、plugin README、`docs/ja/usage-context.md`、`architecture.md`、`getting-started.md`）で「決定主体」「認知基盤」「A1」「SUI」「SEI」の語はヒットしなかった。兄弟製品への言及は `docs/ja/maintainers/` と `research/skill-prototypes/REFERENCE-CLASSIFICATION.md`（付録A）、`research/human-use-gap-kj/README.md` に限られる。

| 追記が要る事項 | 置き場所の候補 | 備考 |
|---|---|---|
| 決定主体として機能しうる生成AIの認知のうち、CSWは「問いを立て、深い洞察を生む部分」に寄与し、来歴の保証・誤りの検出・決定・停止は担わないこと | README.md冒頭（短く）、`core-value-and-embodiment-policy.md` の追記節（詳細） | runtime（`src/`）には「A1」「決定主体」「SUI」「SEI」の語を入れない（5節）。runtimeには「問いと区別の候補を立てる。決定、来歴の保証、誤りの検出は担わない」といった製品名を含まない言い方で足す余地がある |
| 基盤が親和図法の深いラウンドとA型／B型の往復であること（作業仮説、有効性の比較研究は未確認） | 位置づけ文書（docs/ja/maintainers）、README.mdの短い文 | 実体は `research/skill-prototypes/affinity-synthesis/` にある。README.md:13-36 は三層構造を述べるが、「基盤」という重みづけは述べていない |
| ラベルが「索引と警報」であり、来歴の保証はカード原文へ立ち戻って語らせることにあること | `core/principles-and-constraints.md`（正本）、ROUTER.md:21 | 現行の「来歴ラベル」節（33-44行）は、ラベルの定義だけで、原文再読との関係を述べていない |
| 原文の再読（来歴の区別）と、対象側の外部材料への確認（誤りの検出、所見化の条件）の区別 | `core/principles-and-constraints.md` または `cognitive-stance.md:81-94` に1〜2文 | 1-2の衝突6を解消する。規則は増やさず、語義を分けるだけ |
| 「領域能力を持たず、答えが列挙し尽くせる閉じた問題には向きにくいが、自動の非発動条件ではない」 | 既に `docs/ja/usage-context.md:36-47` と ROUTER.md:30,32 にある | 追記は不要。位置づけ文書から参照する |
| 兄弟製品との関係（必須依存なし、各リポジトリの現行文書が述べる範囲） | 位置づけ文書。`sibling-product-semantic-correspondence.md` の追記または参照 | 既存の同文書は2026-09-27時点。2026-10-06のSUI ADR-0091等は反映していない（4節） |
| CHANGELOG | `CHANGELOG.md` の `## Unreleased`（現在は空） | runtimeを変える場合は、著者の方針に基づく変更であることを記録する（AGENTS.md:53「単一の事例から `src/` を変えない」への対応） |

## 2. 来歴ラベルの現在の役割

### 2-1. 定義と手順上の依存

**定義の正本**は `src/ja-JP/core/principles-and-constraints.md:33-44`（英語は `src/en-US/core/principles-and-constraints.md:37-42` 付近）。四ラベルは次の意味を持つ。

- `target_supported`：対象側の資料・観察・反証で独立に支えられた。
- `framework_generated`：文化体系から生じた問い・仮説・対比・対応候補・構成資源。
- `cross_field_emergent`：対象と体系の接触から、どちらにも還元できない区別・問い・関係として生じた第三構造。
- `unresolved`：有用性・帰属・確度の判断がまだ置かれていない残差。

ラベルが担うのは二つの別の仕事である。実質的な規則は2番目で、ラベルはその器にすぎない。

1. 由来の記録（どこから生じたか）。`origin` と `verification` を別に保つ（`core/iteration.md:69-75`、`methods/integration.md:86-92`）。
2. **昇格の条件**。`framework_generated` を `target_supported` へ移すには、体系から独立した対象側の支持が要る（`governance/governance-and-records.md:32`、`methods/framework-application.md:106,111,119`、`methods/system-selection.md:88,145`、`methods/transformation.md:79`）。この規則の本体は、README.md:115 の中核原則（外部体系から得た構造は対象へ返して確かめる）にある。ラベルを下げても、この原則は下げない。

**ラベル語を含む runtime 本文（ja-JP、計34出現、12ファイル）**

| ファイル（`src/ja-JP/`） | 行 | 用途 |
|---|---|---|
| `ROUTER.md` | 21, 48, 56 | 由来を区別して追跡、提示物に来歴を含める、来歴 ≠ 行動許可 |
| `core/principles-and-constraints.md` | 11, 33-44 | 定義と、許可を決めない旨 |
| `core/cognitive-stance.md` | 47 | 第三構造は `cross_field_emergent` として保つ |
| `core/discovery-pathway.md` | 45, 56, 86 | 押し返しの第三構造、target-return後の変形履歴、走らせた結果は `framework_generated` |
| `core/iteration.md` | 69-79 | round間で `origin` と `verification` を別に保つ |
| `methods/framework-application.md` | 7, 27, 80, 100, 106, 111, 119, 123, 127 | 探索出力の既定の扱い、昇格の条件、出口（調査・診断／生成・構成） |
| `methods/system-selection.md` | 88, 145 | 探索利用と帰属利用の分離 |
| `methods/transformation.md` | 79 | 第三構造の昇格条件 |
| `methods/integration.md` | 35-38, 48, 69, 88-92, 134 | 親和統合への受け渡しと受け取り |
| `governance/governance-and-records.md` | 22, 23, 32 | 判断の来歴の記録欄、昇格の条件 |
| `governance/evaluation.md` | 13, 14 | 確認項目7・8 |
| `domains/human-and-taiheki.md`、`frameworks/llull-ars.md` | 21、30 | `unresolved`、`framework_generated` の用例 |

### 2-2. ラベルの存在や語を要求するテスト・検証

runtimeの本文がラベルを持つこと自体を要求する検査は、次のとおり限られる。`scripts/validate.py` は、ラベル語をコードに直書きせず、`evals/semantic-retention.json` を読んで必須句の有無を調べる。

| 検査 | 要求している内容 | ラベル降格との関係 |
|---|---|---|
| `evals/semantic-retention.json`（ja・en 両方）を読む `scripts/validate.py:187-197`、`tests/test_semantic_retention.py` | `core/principles-and-constraints.md` に「来歴ラベルは、採用・発話・外部化・停止の許可を自動的に決めない。」（英語は "Provenance labels do not automatically decide permission to adopt, state, externalize, or stop."）。`methods/framework-application.md` に「対象側で独立に支えられるまで`framework_generated`」。`ROUTER.md` に「来歴 ≠ 行動許可」 | 降格方針と同方向。**書き換えるときも、これらの句は残す** |
| `scripts/validate_research_tension_emergence.py:30,60,109` と `tests/test_research_tension_emergence.py`、`research/skill-prototypes/check_split_ownership.py:55,127` | 両ロケールの `core/cognitive-stance.md` に `cross_field_emergent` の語。`principles-and-constraints.md` に「適合よりも不一致・抵抗・相互修正から生じたものを含む」「対立を自動的に「解決済み」にするラベルではない」。`research/skill-prototypes/evals/CSW-HANDOFF-CASES.md` にも `cross_field_emergent` | 語を消すと `make research-skill-check` と該当テストが失敗する。**削除せず、役割の説明だけを変える**のが安全 |
| `scripts/validate_m365_profile.py:18,27` | Microsoft 365版 `instructions.txt` に `target_supported` の語（ja・en） | 同上。`adapters/microsoft-copilot/ja-JP/instructions.md:64-67` の §6 を消さない |
| `tests/test_affinity_board.py`（33出現）、`tests/test_research_affinity_map_validation.py`（10）、`tests/test_framework_selection_workspace.py`（5） | `input_status` の文字列値（`framework_generated`、`cross_field_emergent`、`target_supported`、`unresolved`）を前提にした操作とその検証 | 研究用ツール側の結合。下記 |

研究用ツールの結合（`research/skill-prototypes/affinity-synthesis/scripts/`）:

- `affinity_board.py:266-268`（`audit-return` は `input_status=framework_generated` を要求）、`:304-306`（`trace-cross-field` は `cross_field_emergent` を要求）、`:1081-1166,1320-1369`（`status` の警報：未trace、yield未分類、return audit欠落、cross-field未trace）、`:1457`。
- `validate_map.py:183-186,229-238,261-263,294-324`。
- `research/framework-candidates/scripts/framework_selection_workspace.py:589`。
- スキーマは `affinity-map.schema.json:54` で `input_status` を単なる文字列とし、列挙にしていない。

したがって、研究用ツールはすでに「索引（入力状態の集計）と警報（`status` の警告リスト）」として動いており、P2の役割と整合する。変更は不要で、変えると出現約50箇所のテストに影響する。

ラベル語を要求しないもの：`scripts/validate.py` の本体、`evals/living-lab-round.schema.json` 等のLiving Lab検査（`unresolved` は通常の英単語としてのみ出現）、READMEとusage-contextを調べる `tests/test_platform_guidance_contract.py`（ラベルは対象外）。

### 2-3. 降格した場合の影響範囲

| 層 | 影響 | 備考 |
|---|---|---|
| runtime ja-JP（`src/ja-JP/`） | 役割の説明の書き換え（2-1の表のうち、principles:33-44、ROUTER:21、governance:21-32、integration:29-45 と 86-95、iteration:63-79、evaluation:13-14）。語彙そのものは残す | 昇格の条件（framework-application、system-selection、transformation）は降格の対象外。原則を弱めない |
| 翻訳（`src/en-US/`、`i18n/translation-manifest.json`） | jaを変えたファイルはすべて、英訳の更新と `scripts/update_translation_hashes.py` による記録更新が要る。更新しないと `validate.py:180-185` が「Translation is stale」で失敗する（AGENTS.md:97） | 英訳と、ハッシュ更新の対が必要 |
| テスト・検証 | 上の必須句は残す。句を変える場合は `evals/semantic-retention.json` と、`validate_research_tension_emergence.py`、`check_split_ownership.py`、`validate_m365_profile.py` を同じコミットで改訂する | 語の削除は避ける |
| 配布物 | `plugins/*/skills/weave/references/*`（ja・en 計21ファイルがラベルを含む）、`SKILL.md`、`dist/` の各アダプターは `make build` で再生成され、生成物のgit差分を含めて提出する。`make check` は生成物の古さを失敗にする（AGENTS.md:62,101） | 手で編集しない |
| アダプター | `adapters/microsoft-copilot/{ja-JP,en-US}/instructions.md`（§6）。`validate_m365_profile.py` の必須語を維持。M365版の上限は `m365_instructions_max_chars` 8000 | runtimeとは別のテキストで、runtimeに連動して自動更新されない |
| 保守文書 | `docs/ja/maintainers/sibling-product-semantic-correspondence.md:47-50`（SEIの対応表）と同:13,104（「来歴ラベルの意味の変更を行わない」）、`csw-tension-emergence-and-aufhebung-contract.md`（9出現）、`csw-thin-synthesis-connection-contract.md`（4）、`skill-improvement-direction.md:57`、`core-value-and-embodiment-policy.md:139` | 日本語の保守文書は自然な日本語の鮮度管理の対象。変更すると manifest の記録更新が要る（5節） |
| 研究用ツール | 変更不要 | 変える利点が小さく、テストのコストが大きい |

### 2-4. 順序とリスク

推奨順序（上から。前の段階が決まるまで次へ進まない）:

1. **著者の確認と、位置づけ文書の確定**（docsのみ、runtime不変）。方針の文言（P1〜P5）と、閉じた問題の扱い（衝突1）を決める。リスク：位置づけの文言が過大になり、README.md:11 の「有効性は確立していない」と食い違う。
2. **docs側の改訂**。`core-value-and-embodiment-policy.md` に追記節、`sibling-product-semantic-correspondence.md` に注記、`AGENTS.md:20` に注記、README冒頭。リスク：natural-Japanese review manifest の更新漏れ（5節）。
3. **ja-JP runtimeの文言**。principles の「来歴ラベル」節、ROUTER:21、governance §10、integration、iteration、evaluation。ラベル語と必須句は残す。昇格の条件は動かさない。リスク：(a) 必須句の取りこぼし（semantic-retentionの失敗）。(b) 「ラベルを下げた」ことが、独立した対象側支持の要件まで下げたと読まれる。(c) `ROUTER.md` はバイト予算に近い（3節）。
4. **en-US翻訳とハッシュ更新**。jaの変更と同じブランチで。翻訳だけ先送りすると検証が失敗する。
5. **アダプター・メタデータ**。M365の `instructions.md` §6、plugin説明文（衝突5）。`make build` と `make check` で生成物を揃える。
6. **CHANGELOG と token-budgets の履歴行**。`evals/token-budgets.json` は「増減は `_history` に理由を書く」運用（同ファイルの `_note`）。
7. **研究用ツールとテスト**は、最後まで触らない。触る場合は、`affinity_board.py` の文言（警報の説明）だけにとどめる。

全体のリスク：

- 一回の事例や評価から `src/` を変えない（AGENTS.md:53）。今回は著者の方針に基づく変更である旨を、CHANGELOGと位置づけ文書に残す。
- ラベル語を消してしまうと、少なくとも3種の検査と、M365アダプター、研究用ツールが同時に壊れる。「語を残して役割を書き換える」が、影響の小さい経路である。
- 降格の結果として、`ROUTER.md` と `principles` が「原文を読み直せ」と命じる形に寄ると、新しい義務（記入欄）になる恐れがある。`discovery-pathway.md:102` の「照らす動きを、すべての候補に毎回課す記入欄にはしない」と同じ書き方にする。

## 3. トークン量の観点

### 3-1. 現状の語数・概算

`scripts/token_budget.py` の式（ja：文字数/1.2〜/0.75、en：文字数/4.5〜/3.0）をNodeで再現した値。式の幅が広いため、範囲として読む。

| ロケール | `*.md` 数 | 文字数 | バイト | 概算トークン（低〜高） |
|---|---|---|---|---|
| ja-JP（`src/ja-JP/`） | 34 | 79,128 | 181,191 | 65,940〜105,504 |
| en-US（`src/en-US/`） | 34 | 167,889 | 168,324 | 37,309〜55,963 |

ja-JPのうち `frameworks/` は31,162文字（約39%）、63,783バイト。大きいファイル（ja、文字数／バイト）は次のとおり。

| ファイル | 文字数 | バイト |
|---|---|---|
| `core/discovery-pathway.md` | 5,296 | 13,024 |
| `methods/system-selection.md` | 5,106 | 12,886 |
| `ROUTER.md` | 4,988 | 11,112 |
| `methods/framework-application.md` | 4,696 | 12,408 |
| `core/principles-and-constraints.md` | 4,190 | 11,654 |
| `frameworks/portfolio.md` | 4,114 | 8,716 |
| `methods/integration.md` | 3,870 | 7,158 |
| `core/cognitive-stance.md` | 3,826 | 10,434 |
| `governance/evaluation.md` | 3,172 | 8,418 |
| `core/iteration.md` | 3,001 | — |
| `governance/governance-and-records.md` | 2,468 | 5,830 |

配布側の実測：`plugins/cultural-substrate-weaving-ja/skills/weave/SKILL.md` 11,565バイト、`plugins/…-en/skills/weave/SKILL.md` 12,001バイト、M365 `instructions.md`（adapters）ja 9,849バイト・en 7,989バイト。

**予算ファイルとの乖離（要確認）**：`evals/token-budgets.json` の上限は、`router_max_bytes` ja 10,000／en 12,000、`claude_skill_md_max_bytes` ja 11,000／en 13,000、`corpus_max_bytes` ja 101,357／en 101,009、`reference_max_bytes` ja 14,857／en 14,566。最終更新は `d1d25eb`（2026-09-27）。その後に `ROUTER.md`（`9d4e805`、`5864ce6`）とframeworks群が増え、実測は ja の ROUTER 11,112バイト、同 corpus 181,191バイト、Claude SKILL.md 11,565バイト、en の corpus 168,324バイトと、記録上の上限を超えている。`validate.py` の `check_budgets` は同じ尺度でこれらを検査するため、現HEADで `make check` の予算検査が通っているかは未確認である（Pythonが無く実行できていない）。位置づけ変更の前提として、予算の現状確認と `_history` の更新が要る。

### 3-2. 短縮できる箇所

ラベルの降格で削れるのは、ラベルまわりの重複であり、量は小さい。ラベル関連の直接の記述は、principles:33-44（538文字）、governance:21-32（513）、integration:29-45（434）と同:73-95（883、うち第三構造の追跡は検証が要求する句を含み残す）、iteration:63-79（約404）、evaluation:13-14（195）、ROUTER:21（166）で、合計約2,200文字（コーパスの約2.8%）にとどまる。

| 候補 | 内容 | 見込み（ja文字数） | 制約 |
|---|---|---|---|
| 重複の統合 | 「ラベルは行動の許可を決めない」が ROUTER:3,21,56、principles:11,44、governance:23 に並ぶ。正本をprinciples:11に置き、ほかは「来歴 ≠ 行動許可」の短い参照にする | 200〜350 | `ROUTER.md` の「来歴 ≠ 行動許可」と principles の必須句は残す |
| 四ラベルの列挙の重複 | principles:35-40、governance:22、integration:35-38、evaluation:14、iteration:71-72 に同じ列挙 | 150〜250 | 定義はprinciplesの1か所とし、他は「来歴ラベル（索引）」への参照にする。ただし `cross_field_emergent` の説明は検証が句を要求する |
| 確認項目の統合 | evaluation:13（除去検査）と14（ラベルを分ける）は framework-application:111 と内容が重なる | 60〜100 | 14「対象についての所見には、独立した対象側の支持を確認した」は昇格の条件に当たるので残す |
| round間の帰属 | iteration:63-79 の `origin`／`verification` の例示 | 100〜150 | `origin` を不変、`verification` を可変とする点は残す |
| 受け取り側の列挙 | integration:73-95 の「統合結果を受け取る」と「meaning / origin / verification」は2回に分けて書いている | 100〜200 | 固定schemaではない旨の1文は残す |

**見込み合計：ja 600〜1,050文字（コーパスの約0.8〜1.3%、バイトで約1,300〜2,300）**。ラベルを降格しても、runtimeの規模は実質的に変わらない。トークン削減を目的とするなら、`frameworks/`（31,162文字）や discovery-pathway・system-selection（各5,000文字超）が支配的であり、今回の変更の範囲外である。

### 3-3. 増やすべき箇所

| 追記 | 内容 | 見込み（ja文字数） | 置き場所 |
|---|---|---|---|
| 来歴の保証は原文再読にあるという1段落 | ラベル節を「索引・警報」へ書き換える際に同時に入れる。置き換えが主で、純増は小さい | +150〜250 | `core/principles-and-constraints.md` |
| 原文の再読と、対象側の外部材料への確認の区別 | 「返す／戻す」の語義を1〜2文で切り分ける | +100〜150 | `core/cognitive-stance.md:81-94` の近く |
| CSWの寄与と担わないことの1文 | 問いと区別の候補を立てる。決定、来歴の保証、誤りの検出は担わない（製品名を含めない） | +80〜150 | `ROUTER.md:21` の置き換えに含める。ROUTERはバイトに余裕が無い（3-1）ため、増分を抑える |

**見込み合計：+330〜550文字。短縮と合わせると、ja全体で −700〜0 文字程度の正味**。`ROUTER.md` には純増を入れず、principles と cognitive-stance に寄せるのが安全である。en-USの増減はjaに対応し、バイトではjaの約0.5倍の増減になる。

README・docs・保守文書の追記はruntimeのトークンに影響しない（`corpus_max_bytes` の検査対象は `src/<locale>/*.md` のみ）。

## 4. 兄弟リポジトリとの記述上の整合

調査したのは、SUI `main` と SEI `develop/v0.2.0` の現行文書である。両リポジトリには、2026-09-27付の `docs/family-apex-backflow-20260927` ブランチがあり、SUI側（`002b88f6`、1コミット）とSEI側（`143875b`〜`624d56e`、4コミット）はいずれも本流へ未mergeの提案（Proposed）である。これらは「現行文書」に数えていない。

### 4-1. SUI Sensemaking が現行文書で述べている範囲

根拠：`README.md`、`AGENTS.md`、`01_Plans/adr/ADR-0084,0085,0086,0089,0091`、`02_Architecture/schemas.md`。

- **検証状況**：`README.md:3-5` に「生成AIを用いた開発中であり、人的レビューは不完全。実装・文書・安全性・利用手順の検証は完了していない。生成物を重要な判断に使用しない。外部利用者による検証も未実施」。README:35 にも「実在の機微な資料の本番分析や、重要な判断への利用は避けてください」。
- **来歴に当たるもの**：README:29 は出力に「元のカードへ戻る経路」を挙げる。README:139-142 は、AIの生成物を「来歴や権限の境界を越えて人間が承認した意味として扱わない」とする。ADR-0091 §3 の差別化軸2は「権限つきの来歴：『AIが考えた』『人が確認した』『承認済みとして共有された』を区別し、あとから辿れる」。実装側は `reviewState` が `unreviewed | human_reviewed` で、昇格は人手のみ（`02_Architecture/schemas.md:96-97,271,284`）。
- **意味成果物の区別**：ADR-0085 は Evidence／Observation／Relation／Hypothesis／Structure／Synthesis／Review／Decision を別の意味成果物として扱うことを決めている。ADR-0086 には「Runtime impact: この変更では影響なし」とあり、設計の決定である。これが実装済みかは、今回確認していない。
- **価値の検証**：ADR-0089 §5 で、一次利用仕事（後から根拠へ戻れること）の仮説H1は T3（生成AIが演じる参加者）による `provisional` の「narrow」。ADR-0091 も、位置づけを強く打ち出すほど実証が追いつかないリスクがあり、H1が検証中であることを公開文書に併記するとしている。
- **KJ法の位置づけ**：README:13-23 は、現在の中核インターフェースを親和図法／KJ法に着想を得たキャンバスと述べる。同時に、KJ法のキャンバスだけを唯一の手段として固定しないことも述べる（README:143）。
- **CSWへの言及**：`main` のREADME、ADR、AGENTSには、CSW・cultural-substrate-weaving の記述が見つからなかった。CSWとの比較実験の記録は、CSW側の `docs/ja/maintainers/sui-sensemaking-cognitive-coevolution.md` にあり、A〜Dの実行記録は未取得（同:173）。

**CSW側が注意すべき点**：SUIの「来歴」は、現行文書では **権限と作成主体の来歴（AI提案か人間確認か）と、元のカードへ戻る経路** を指す。CSWの来歴（対象由来／体系由来／接触由来）とは軸が異なる。SUIが「体系由来か対象由来か」を区別する機構を持つと読める記述は、今回の調査では確認できなかった。

### 4-2. SEI Cognition が現行文書で述べている範囲

根拠：`README.md`、`product/vision/SEI_PRODUCT_VISION.md`、`product/definition/SEI_PRODUCT_SHAPE.md`、`product/principles/SEI_PRODUCT_PRINCIPLES.md`、`release/v0.2.0/RELEASE_NOTES.md`、`product/definition/SEI_REALIZATION_PROVIDER_EXCHANGE.md`。

- **意味境界**：README:12-44 は Observation ≠ Interpretation／Hypothesis ≠ Recommendation ≠ Decision ≠ Authority ≠ Action Intent ≠ Execution ≠ Business Outcome を守る境界とする。Unknown ≠ No、Conflict ≠ latest-wins などの非同一性も並ぶ。Product access permission と semantic Responsibility／Authority も分ける。
- **権限・決定の扱い**：`SEI_PRODUCT_VISION.md:128`「AIへの委任範囲は広がって構いません。ただし…意味差を…無自覚に潰しません」、同:182「Policyにより一定範囲のDecisionをAIへ委任する」は、委任を**記録できる**構造の記述であり、AIが決定主体として機能しうることの実証ではない。
- **検証状況**：README:4 は v0.2.0 Local Reference Product Baseline。README:135 は「運用の継続性や、実利用で価値が届いたことを示すEvidenceはまだありません」。`RELEASE_NOTES.md` は「production完成版ではない」とし、Operational Evidence、Adoption／Outcome Evidence、external Cognitive Methodのlive実行を主張しない。`SEI_PRODUCT_SHAPE.md:387` は、Product Accessと Responsibility／Authority の分離に Design baseline がある一方、実利用品質には別のEvidenceが要るとする。
- **依存**：`SEI_PRODUCT_VISION.md:230` は「SEIはSUI／TEI／EKIを使わなくても成立し」、関連製品であることだけで優先度・信頼・Authorityを与えないと述べる。
- **CSWへの言及**：`SEI_REALIZATION_PROVIDER_EXCHANGE.md:156-158` は、CSWの日本語版 `weave` Skillを固定revisionで取得し、source identityとbytesを検証してMethod Realizationに結び付けたとし、「SkillをLLM上で実行してMethod Applicationを得たことまでは示しません」と書く。CSW側の `REFERENCE-CLASSIFICATION.md` 付録Aは、固定されたblobが現在の `weave` と異なることを記録している。ADR-0002 は、KJ統合やCSWの中間生成物をMethod固有Artifactとして保持し、Universal Interpretationへ変換することを要求しない。
- **注意**：位置づけ文書 §9-7 は「SUIとSEIのどちらも『重要な判断には使わない』…と明記している」と述べるが、「重要な判断には使わない」の趣旨の明記は、SUIのREADMEにはあり、SEIのREADME・リリース文書・ADR・製品文書には確認できなかった。SEIの留保は、「production readinessではない」「Operational／Adoption Evidenceが無い」「Not Yet Verified を残す」という形である。また、SEIの release 文書は旧称 SOZA を使っている（`REFERENCE-CLASSIFICATION.md:163` が旧称と注記）。

### 4-3. CSW側の言い回しの案（過大な主張を避ける）

| 避ける言い方 | 理由 | 代わりの言い方（案） |
|---|---|---|
| 「来歴の区別はSUIが担う」「SUIが来歴を保証する」 | SUIの来歴は権限・作成主体と元カードへの経路。体系由来か対象由来かの区別をSUIが持つ記述は確認できない。SUIは検証未完了で、重要な判断への利用を避けるよう求めている | 「SUIは、カードの原文へ戻る経路と、AI提案と人間確認の区別を保持する設計をとる。体系由来か対象由来かの区別をそこでどう持つかは、SUI側の設計を確かめてから決める。SUIは検証未完了と明記している」 |
| 「SEIが権限・決定の区別を担う」「SEIがあれば決定主体の権限が成立する」 | SEIは意味境界とその記録契約、限定的な実行検証を持つが、運用・採用のEvidenceは無い。AIへの委任は「記録できる」範囲の記述 | 「SEIは、観測・解釈・推奨・決定・権限を同一視しない意味境界と、それを記録する契約を持つ（v0.2.0のローカル参照基盤。運用・採用の証拠は無いと明記している）」 |
| 「CSWはSUI／SEIと組み合わせて決定主体の認知基盤になる」 | 位置づけ文書 §10-3(5)「CSW系だけで成立するとは主張しない」と、両者の検証状況に反する。未merge提案を採用済みのように読ませる | 「CSWは、そうした基盤を構成しうる要素のうち、問いの構成に寄与する部分を担う想定である。他の部分を担う製品との連携は構想であり、必須の依存ではない。効果は未検証」 |
| 「SEIがCSWを組み込んでいる」 | 固定されたのは旧版 `weave` のSkill artifactで、LLM上で実行していない | 「SEIは、CSWの日本語版Skillを固定revisionで取得・検証した（実行はしていない）」 |
| 兄弟側の未merge提案（family apex、SEI_FAMILY_SEMANTIC_MAP 等）を現行の分担として書く | 両リポジトリで未merge | 現行の分担は、各リポジトリのmain／developにある文書だけを根拠にする。未mergeは「提案」として別に書く（既存の `sibling-product-semantic-correspondence.md:32,61` の扱いを踏襲） |

共通の書式の案：兄弟製品に触れる文には、(a) どのリポジトリのどの文書か、(b) その文書が述べる範囲、(c) 検証状況の1句、を添える。例：「（`hat47x/sui-sensemaking` README の記述による。同リポジトリは検証未完了と明記）」。

## 5. 位置づけ文書の置き場所と所有境界

### 5-1. 置き場所の判断

結論：**`docs/ja/maintainers/` に新規の保守者向けノートを置き、`core-value-and-embodiment-policy.md` に追記節（§10）を足し、README冒頭に短い段落を足す**。この三点セットが現行の文書構成に最も合う。

- `docs/ja/maintainers/` は、根幹価値（`core-value-and-embodiment-policy.md`）、兄弟製品との対応（`sibling-product-semantic-correspondence.md`、`sui-sensemaking-*.md`）、方向づけ（`skill-improvement-direction.md`）が既にある場所である。新規ノートの書式は `sibling-product-semantic-correspondence.md:1-17` に倣える（Status: Maintainer note / informative only / no runtime change、Date、Related）。
- `docs/ja/` 直下は利用者向けガイド（`getting-started.md`、`usage-context.md`、`architecture.md`）であり、研究上の位置づけは置かない。`usage-context.md` には、閉じた問題の扱い（既存の36-47行）があるので、重複して書かない。
- 位置づけの追記は、方法論の第二正本にならないようにする（`docs/README.md` の「文書の役割」表：`docs/ja/` は説明・運用文書で、方法論の正本ではない）。
- 位置づけ文書の元の2文書（`C:\GIT\cultural-substrate-weaving\*.md`）はリポジトリの外にある。リポジトリ内の文書からそれらへリンクすると、`tests/test_repository_doc_links.py` の対象となり得るため、リンクではなく、必要な要点を本文へ書き写して根拠を示す形が安全である。

### 5-2. 追加時の付随作業（ja文書）

- 新規の `docs/ja/maintainers/*.md` は `scripts/check_natural_japanese_review.py` の範囲（`review_scope()` が `docs/ja/maintainers/*.md` を glob）に入る。`docs/ja/maintainers/natural-japanese-review-manifest.json` に記録を足す必要があり、無いと「missing natural-Japanese review record」で失敗する。
- `tests/test_japanese_development_docs_contract.py` は、`docs/ja/maintainers/*.md`、README.md、`docs/ja/usage-context.md`、`architecture.md` のパスが `natural-japanese-review.md` に記録されていることを要求する。追記・新規のいずれの場合も、同ファイルへの記録が要る。
- README.md、`docs/ja/usage-context.md`、`architecture.md`、`docs/README.md` は、変更すると鮮度（blob hash）が古くなり、再レビューの記録更新が要る。
- AGENTS.md の「日本語文書の作成」の規則により、内容確定後に独立した自然な日本語の推敲工程を通す。
- `docs/README.md` のQuick navigationに、新規ノートへの行を足す。

### 5-3. 変更の分類（AGENTS.md の所有境界に照らして）

| 変更 | 置き場所 | 所有区分 | 理由 |
|---|---|---|---|
| ラベルの役割を「索引・警報、原文再読の入口」と書き換える | `src/ja-JP/` → `src/en-US/` → 生成物 | CSW runtime | AGENTS.md:20 が、ラベルと帰属規則をCSW runtimeの所有とする |
| 原文再読と外部確認の語義の切り分け | `src/ja-JP/core/` | CSW runtime | 帰属の境界の記述 |
| 「CSWは問いと区別の候補を立て、決定・来歴の保証・誤りの検出を担わない」（製品名なし） | `src/ja-JP/ROUTER.md`（置き換え）または principles | CSW runtime | 既存の決定権の記述（ROUTER:3）の延長 |
| 「A1」「決定主体」「認知基盤」「SUI」「SEI」の語、認知基盤の十項目、他製品の責務 | **`src/` に入れない**。`docs/ja/maintainers/` と README | 文書（runtime外） | runtimeに製品間の分担を入れると、他製品への依存を暗黙に作り（P5）、AGENTS.md:34 の趣旨に反する。runtimeの語はCSW単独で意味が通ること |
| 親和図法の深いラウンド、A型／B型の往復が基盤であるという位置づけ | `docs/ja/maintainers/`、README。実体の記述は `research/skill-prototypes/affinity-synthesis/` | research sibling | AGENTS.md:11,95。内部アルゴリズムを `src/` へ戻さない。A型／B型の語は現行の `src/` に存在しない |
| 閉じた問題の扱い | 既存の `usage-context.md`、ROUTER:30,32 を維持 | CSW runtime／呼ぶ側 | 新しい自動の非発動規則は、高い正当化閾値（principles:93-110）に当たる |
| 兄弟製品の現行記述との対応表の更新 | `docs/ja/maintainers/sibling-product-semantic-correspondence.md` | 保守文書 | 既に同種の対応を置いている。「src/を変えない」という既存の宣言（同:59,104）に注記を足す |
| 位置づけの検証（A1への寄与、ラベルの索引・警報としての有効性） | `research/`（Living Labの記録、または新しい研究ノート） | research | AGENTS.md:39-54。一事例や自己評価で `src/` を変えない |
| 配布メタデータの説明文（KJ統合との組み合わせの表現） | `src/manifest.json`、`adapters/` → 生成物 | adapters／生成 | 位置づけ確定後。runtimeの意味ではなく配布説明 |
| CHANGELOG、`evals/token-budgets.json` の `_history` | リポジトリ直下／`evals/` | 保守 | 運用上の記録 |

## 6. 改訂案（案文。適用していない）

### 6-1. README冒頭の位置づけ段落（案）

README.md の2行目の言語切替の直後、現行の冒頭段落（5行目）の前または後に置く想定である。

> **位置づけ。** 生成AIが決定主体として働くには、問いを立てる、判断を保留する、根拠を区別する、対象へ戻して確かめる、といった認知が要ります。cultural-substrate-weaving（CSW）が寄与するのは、そのうち「問いを立て、深い洞察を生む部分」です。時の試練を経た文化的体系を一時的な認知場として開き、普段の連想の外にある問い・関係・遷移の候補を立て、対象側の材料へ戻して確かめます。
>
> 根拠の区別と作業の土台は、カードの原文へ立ち戻る親和図法（KJ法に学んだ方法）の深いラウンドと、図解と文章化の往復にあると考えています（作業仮説であり、有効性を比べた研究はまだ確認できていません）。CSWの来歴ラベルは、ある時点の判断を記したものにすぎず、読み直しの入口と警報として使います。判断の根拠になるのは、ラベルではなく、カードや資料の原文です。
>
> CSWは、領域の専門能力を持ちません。答えを列挙し尽くせる閉じた問題では、価値が出にくいと考えています（ただし自動の非発動条件にはしません）。誤りの検出、責任の所在、決定、停止の判断も担いません。人間の意図を先回りして抑える安全関門も置きません。ほかの製品への必須の依存はありません。効果は検証中です。

（英語版 README.en.md には、意味を揃えた訳を同時に置く。上記のうち「親和図法（KJ法に学んだ方法）」は、README.md:121 の商標注記と矛盾しない表現にしている。）

### 6-2. `core-value-and-embodiment-policy.md` の追記節の見出し案

現行の §9「変えないもの」の後に、番号を振り直さず §10 として足す案。

```text
## 10. 認知基盤のなかでの位置づけ — 問いと洞察への寄与（2026-10-06の整理）
- 状態: 著者の方針にもとづく位置づけの記述。runtimeの変更ではなく、効果は未検証。
### 10.1 何に寄与し、何を担わないか
    （問いの構成・深い洞察への寄与。決定、来歴の保証、誤りの検出、停止は担わない。領域能力を持たない）
### 10.2 基盤となる親和図法の深いラウンドとA型／B型の往復
    （作業仮説。実体は affinity-synthesis / iterative-inquiry-synthesis。有効性の比較研究は未確認）
### 10.3 来歴ラベルの位置づけ — スナップショット、索引、警報
    （来歴の保証は原文再読。ラベルは入口。§5.2「由来の光」の読み替え。独立した対象側の支持の要件は維持）
### 10.4 原文の再読と、対象側への確認を分ける
    （来歴の区別は再読、誤りの検出と所見化は外部材料への確認。自己再読を「対象へ戻した」に数えない）
### 10.5 閉じた問題と先回りの抑制
    （閉じた問題は主対象でないが、自動の非発動条件にしない。安全関門を置かない既存方針を維持）
### 10.6 兄弟製品との関係
    （必須依存なし。SUI、SEIの現行文書が述べる範囲と検証状況。未mergeの提案は採用済みとして扱わない）
### 10.7 変えないものと未確認
```

あわせて、§5.2 の139行「既存の来歴ラベルがこの光を担う」を「カードや資料の原文への立ち戻りと、来歴ラベル（索引）がこの光を担う」と読み替える、§8「今回の反映範囲」へ1行足す、§9 に「来歴の保証はラベルに置かない」を足す、をセットにする。

### 6-3. ランタイムでのラベルの扱い（日本語の案文）

`src/ja-JP/core/principles-and-constraints.md` の「## 来歴ラベル」節（現行33-44行）の置き換え案。必須句（`cross_field_emergent` の説明と、許可を決めない旨）は現行の文言のまま残す。

> ## 来歴ラベル：索引と警報
>
> 来歴は、根拠にしたカードや資料の原文へ立ち戻り、その原文に語らせて確かめる。次のラベルは、そのときの判断を記したスナップショットであり、根拠そのものではない。使い道は二つに限る。
>
> - **索引**：どの候補を、どの原文から読み直すかを見つける入口。
> - **警報**：由来の印が落ちた候補、体系語が外れて由来が見えなくなった候補、`framework_generated` のまま対象所見のように語られかけた候補を、原文へ戻す合図。
>
> ラベルと原文が食い違うときは、原文を優先し、ラベルを付け替える。付け替えは履歴として残し、過去の記録は書き換えない。
>
> - `target_supported`：対象側の資料・観察・反証によって独立に支えられた。
> - `framework_generated`：文化体系から生じた問い、仮説、対比、対応候補、構成資源。
> - `cross_field_emergent`：（現行の定義文を、そのまま維持する）
> - `unresolved`：有用性、帰属、確度について判断がまだ置かれていない残差。
>
> `cross_field_emergent` は、対立を自動的に「解決済み」にするラベルではない。（現行の42行をそのまま維持する）
>
> 原文の再読は、来歴を区別するための作業である。対象側の独立した材料への確認は、別の作業であり、自己の再読や別の生成AIによる批評で代えない。これらのラベルは来歴・証拠状態を保持するためのものであり、採用・公開・停止を自動決定するラベルではない。ラベル間の移動も、採用、発話、外部化、公開の許可を自動的には意味しない。

`ROUTER.md:21` の置き換え案（現行の「来歴ラベルは…導かない」を残しつつ、役割を書き換える）:

> 文化体系、対象材料、その接触から生じた構造は、由来を区別して追跡できる。区別は、根拠にしたカードや資料の原文へ戻って確かめる。`target_supported / framework_generated / cross_field_emergent / unresolved` などのラベルは、その時点の判断を記録して原文へ読み直す入口と警報であり、それ自体から採用、発話、外部化、停止の可否を導かない。

`core/cognitive-stance.md` の「立てた説明を、対象へ返す」節（現行81行付近）に足す1〜2文の案:

> 元材料へ返して読み直すことは、来歴を区別し、自分の読みを直すための作業である。誤りを見つけるには、対象側の独立した資料・観察・反証へ確かめる必要があり、自分の再読で代えない。

`governance/evaluation.md` の確認項目8（現行14行）の置き換え案:

> 8. 来歴を、ラベルだけでなく根拠にしたカードや資料の原文へ戻って確かめた。ラベルは読み直しの入口として使い、対象についての所見には、文化体系とは独立した対象側の支持を確認した。

### 6-4. 併せて決めておく事項

1. 衝突1（閉じた問題）を、runtimeに入れない、で確定してよいか。
2. 配布メタデータの「KJ法による断片統合を組み合わせ」の表現を、位置づけ確定後に改めるか（衝突5）。
3. 位置づけ文書で A1／B1 といった項目記号を使うか。使う場合も、`src/` と README には出さず、保守者向けノートに限る。
4. `evals/token-budgets.json` の現状との乖離（3-1）を、位置づけ変更の前に解消するか。

## 7. 確認できなかった点（まとめ）

- `make check`、`scripts/validate.py`、各テストの実行結果（Python不在）。予算検査が現HEADで通るかは不明。
- `src/en-US/` の本文全文の照合、`docs/en/` の対応文書の全文。
- SUIの意味成果物（ADR-0085）の実装状況、SUIが体系由来と対象由来を区別する機構の有無（現行文書では確認できなかった、というにとどまる）。
- 兄弟リポジトリの `docs/family-apex-backflow-20260927` ブランチ本体の内容（未mergeの提案であることだけを確認し、中身は精読していない）。
- 位置づけ文書の元の2文書がリポジトリ外にあること以外の、ネットワーク上の公開状態。
