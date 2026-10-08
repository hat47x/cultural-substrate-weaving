# 記録六種の先行例調査と最小スキーマ案

- 作成日: 2026-10-06
- 位置づけ: [cognitive-foundation-architecture.md](../cognitive-foundation-architecture.md) §5「接続に必要な記録」の形式草案に向けた先行例調査。設計の確定ではなく、作業仮説の置き石である
- 効果は未検証。SUI Sensemaking と SEI Cognition の両文書が自身を「検証未完了」「pre-stable」と明記しているため、本書の対応づけも設計水準にとどまる

## 0. 調査の範囲と確認水準

### 0-1. ローカル文書の読了範囲

| 文書 | 読んだ範囲 |
|---|---|
| `C:\GIT\cultural-substrate-weaving\cognitive-foundation-architecture.md` | 全文 |
| `C:\GIT\cultural-substrate-weaving\csw-2028-2031-positioning.md` | 見出し一覧、§9・§10 全文（200〜381行） |
| `C:\GIT\hat47x\cultural-substrate-weaving\docs\ja\maintainers\sibling-product-semantic-correspondence.md` | 全文 |
| `hat47x\sei-cognition\README.md` | 全文 |
| `sei-cognition\contracts\decision-memory\SEI_DECISION_MEMORY_v1alpha1.md`、`interchange\SEI_SEMANTIC_INTERCHANGE_v1alpha1.md`、`semantic-reference\SEI_SEMANTIC_REFERENCE_v1alpha1.md` | 全文 |
| `sei-cognition\contracts\cognitive-method\SEI_COGNITIVE_METHOD_v1alpha1.md`、`CONTRACT_CATALOG.md` | 見出しと該当節（§5.1〜5.2、Capability Observationの要旨）のみ。全文は未読 |
| `sei-cognition\fixtures\contracts\v1alpha1\boundary\decision-with-unresolved.json` | 全文 |
| `sei-cognition\fixtures\contracts\v1alpha1\negative\decision-authority-field.json`、`contracts\schemas\v1alpha1\decision-memory.schema.json` | 存在の確認のみ。内容は未読（実行環境にPythonが無く、JSON Schemaを展開できなかった） |
| `sei-cognition\evaluation\personal-inquiry-decision\COGNITIVE_RESUMPTION_MODEL.md` | §1〜§4冒頭まで |
| `sei-cognition\product\value\SEI_DECISION_CONTINUITY.md` | 見出しのみ |
| `hat47x\sui-sensemaking\README.md` | 全文 |
| `sui-sensemaking\02_Architecture\sensemaking_artifact_contract_v1alpha1.md` | 全文 |
| `sui-sensemaking\02_Architecture\sensemaking_payload_authority_exchange_v1alpha1.md` | 見出し一覧、§3.1・§3.4・§3.7、§5、§8全体 |
| `sui-sensemaking\02_Architecture\sensemaking_semantic_model.md` | 冒頭〜§3.3 |
| `sui-sensemaking\02_Architecture\schemas.md`（約114KB） | 見出し一覧、§3.2 Card、§9 Island、§14 Hold。ほかは未読 |
| `sui-sensemaking\01_Plans\adr\ADR-0056`、`ADR-0084` | 冒頭〜決定部分まで。ADR-0085〜0088 は未読（親としての参照のみ） |
| `sui-sensemaking\02_Architecture\island_shapes.md` | 冒頭のみ。`llm_escalation_policy.html` は未読 |

### 0-2. 外部出典の確認水準

各出典に次の水準を付ける。記憶だけで書いた書名・条文番号・数値は載せていない。

- **A**: 仕様・原典のページを実際に取得し、本書で使う項目を確認した
- **B**: 検索結果で書誌（著者・年・題名・掲載誌・巻号）と要旨を確認した。本文は精読していない
- **C**: 確認できなかった。本文中で「未確認」と明記する

出典の一覧は §8 にある。本文中の `[W1]` などは §8 の番号に対応する。

## 1. 要点

1. 先行例は記録ごとに厚みが違う。決定記録（ADR、PROV-O、RAPID、IBIS、Toulmin）と、原文への固定参照（Web Annotation、PROV-DM、Memento）は材料が豊富で、そのまま再利用できる部分が多い。逆に、**保留の解除条件と「決めないことのコスト」を一体で持つ台帳**、**停止（範囲外での棄権）の記録**、**誤りの層（事実・予測・枠組み）の判定記録**は、確認できた範囲に直接の標準が無い。
2. 原則(a)（来歴は原文の再読で得る）と原則(b)（LLMの自己申告は根拠にならない）は、そのままでは緊張する。再読して語り直す主体もLLMだからである。解決の筋は、語り直しに**原文からの逐語引用と位置を含めさせ、機械的に照合できる部分を作る**こと、意味の忠実さの判定は別の過程に置くことにある（§4-2、§7）。
3. 六種のうち統合すべきものは無い。**部品（条件トリガ、カード参照、選択子）の共通化**で足りる。分割すべきものは三つある。事前登録（予測・前提・撤回条件で採点方法が異なる）、決定記録（決定と権限）、保留台帳（実体はイベント列、台帳は射影）。
4. 欠けている記録の筆頭は**採点記録**、**権限付与記録**、**誤りの層の判定記録**である。価値・目的は、新しい記録種ではなく「カードの役割」として扱う案を勧める（根拠と反論は §2-3）。
5. SUI/SEIとの最大の衝突は、**「権限（Authority）」の語が三つの意味で使われること**である。SUIでは成果物の採用状態、SEIでは決める権限、本構想ではエージェントへの決定権の委任を指す。加えて、SUIの現行契約は「AIがDecisionを生成しても人間のDecision Authorityを持ったことにはならない」と定めており、原則(d)（承認の有無は運用パラメータ）と直接には整合しない（§5）。
6. 停止記録・権限付与記録には、EU AI Actの条文のうち第12条（ログ）、第14条（人間の監督、停止）、第19条・第26条（ログ保存、デプロイヤの義務）、第73条（重大インシデントの報告）が関係する。ただし条文は非公式閲覧サイト経由の確認であり、適用時期は欧州デジタルオムニバスで変わった可能性がある（§3-6）。

## 2. 記録種別ごとの先行例

### 2-1. カード

材料の原文であり、再読の対象になる最小単位。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| W3C Web Annotation Data Model [W1]（A） | 対象（Target）と選択子（Selector）の分離。TextQuoteSelector（`exact`・`prefix`・`suffix`）、TextPositionSelector（`start`・`end`）、RangeSelector、FragmentSelector。状態（State）として TimeState（`sourceDate`）と HttpRequestState。選択子を `refinedBy` で重ねる構造 | 原文が変わったときの扱いは、位置選択子が「変更に対して非常に脆い」という注意書きと、State の併用の勧めにとどまる。**再読を起動する規則や、不一致時の結果の区分は無い** | 位置だけで固定すると、編集で黙って別の箇所を指す。曖昧一致（fuzzy）で再固定すると、誤った箇所へ静かに移る危険がある（これは本書の推論。Hypothesisの記述 [W2]（B）は「軽微な書き換えには耐え、段落の削除や大きな言い換えには耐えない」とする） |
| W3C PROV-DM [W4]（A） | `wasQuotedFrom`（引用）、`hadPrimarySource`（一次資料）、`wasRevisionOf`（改訂）、`wasInvalidatedBy`（失効）。Bundle（来歴の来歴） | 原文のどの範囲かを示す語彙は持たない（選択子は Web Annotation 側） | 一次資料と二次資料の区別を、ラベルで済ませると、再読で確かめられなくなる |
| REFI-QDA 標準 [W7]（B） | 質的データ分析ソフトの交換標準。ATLAS.ti、Dedoose、MAXQDA、NVivo、QDA Miner、Quirkos、Transana などが策定に参加。コードブック交換とプロジェクト交換の二部構成のXML。**ソース、コード付けされた区間、コードを持ち運べる** | 分析（コード付け）のための標準であり、決定・権限・予測は対象外。区間の固定方法の詳細は、今回の検索では確認できなかった（C） | コード（解釈）が原文と同じ層に混ざると、後で原文だけを再読できない |
| Zettelkasten（Luhmann、Schmidt 2016 [W20]（B）、Ahrens 2017 [W21]（B）） | 原子的なメモ、固有の番号、メモ間のリンク。「考えの相手」としての蓄積 | メモは**自分の言葉で書いた派生物**が中心で、「原文」ではない。版固定も範囲固定も無い | 「カード」を要約で作ると、再読の対象が原文でなくなる。SUIのEvidenceも「AIによる要約は元のEvidenceではなく派生」と定める（`sensemaking_payload_authority_exchange_v1alpha1.md` §3.1） |
| Memento RFC 7089 [W10]（A）、Robust Links [W9]（B） | 元のURI、保存した版のURI、リンクした日時の三点組。TimeGate、TimeMap、`Memento-Datetime` | 外部Webの版管理が対象。カードの版管理や再読の起動は対象外 | 外部URLだけに依存する参照は腐る。Zittrain らの調査 [W8]（B）は、ハーバード・ロー・レビューなどのURLの70%超、連邦最高裁判決のURLの50%が、引用当時の内容を指さなくなっていたと報じる |
| SUI Evidence ペイロード（`sensemaking_payload_authority_exchange_v1alpha1.md` §3.1） | `inline_text`、`source_segment`（`sourceRef`、`locatorRef?`、`sourceVersionDigest?`）、`compound`。ロケータをAIが推測して補うことを禁じる | **ロケータの共通契約は未決**（同 §13、`sensemaking_artifact_contract_v1alpha1.md` §14）。ダイジェストは任意 | `source_segment` だけでは、出典が消えたとき原文を再読できない |

**設計への含意。** カード自体を「逐語の本文を内包し、改訂不能な版を持つ単位」とする。範囲の固定は、(1) カード版の内側の範囲（版が不変なので位置選択子で足りる）と、(2) 元の出典の範囲（引用選択子＋位置選択子＋出典の版ダイジェスト＋可能なら保存した写し）の二層に分ける。Web Annotation の位置選択子の脆さは、固定対象を不変の版にすることで避けられる。

### 2-2. 保留台帳

保留中の問い、解除条件、期限、決めないことのコスト。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| RAID ログ（リスク・前提・課題・依存）[W15]（B、実務解説サイトのみで権威は低い） | 項目ごとの担当者、状態、次の行動。前提が崩れたらリスクや課題へ昇格させる運用 | 解除条件を観測可能な形で持つ規定、**決めないことのコスト**、根拠資料への版固定参照は、確認した説明に見当たらない | 作って更新されない台帳。期限と解除条件の混同 |
| Assumption-Based Planning（Dewar ほか 1993、RAND MR-114-A）[W12]（B） | 計画の**荷重を担う（load-bearing）前提**と、脆弱な前提を特定する発想 | 「signpost（前兆指標）」がこの文書の構成要素かは、今回の確認では取れなかった（C） | すべての前提を列挙すると荷重の見分けが付かない |
| ADR の状態と MADR 4.0.0 [W5]（A）、Nygard 2011 [W6]（A） | 状態（proposed → accepted → deprecated／superseded）。古いADRを消さず「superseded」として後継を指す。MADRの `Confirmation` 節（決定が守られているかの確認方法）、YAML front matter（`status`、`date`、`decision-makers`、`consulted`、`informed`） | 状態は**決定の**状態であり、未決の問いの台帳ではない。解除条件・期限・コストの欄は無い | 状態遷移を人が更新し忘れる |
| IBIS（Kunz & Rittel 1970）[W13]（B） | 未解決の論点（Issue）を一級の節点にする。位置（Position）と論拠（Argument）で囲む | 期限、解除条件、コストを持たない | 論点が増え、閉じる規則が無い |
| SUI `Card.holdState`（`held`・`pending`・`shelved`、`schemas.md` §14.1）／SEI の Unknown・Question・Conflict と再開条件（`SEI_DECISION_MEMORY_v1alpha1.md` §6・§10） | 「未解決を解決済みに変えない」原則（`Unknown != No`、`Decision creation != uncertainty resolution`） | SUIは状態のみで、解除条件・期限・コストの欄が無い。SEIは再開条件・見直しトリガを「明示Artifactまたは参照として残せる」とするが、専用の型は無い | 後述（§5）。「held」の語が複数の意味で既に使われている |

**設計への含意。** 台帳そのものを更新可能な表にせず、**保留の開始・延長・解除・失効のイベント列**を実体とし、台帳は射影（派生ビュー）とする。「決めないことのコスト」は、LLMが推定して書くと自己申告になる。観測値、推定値、不明のいずれかを区別して記録し、不明を0と書かせない（SEIの `Unknown != No` と整合）。

### 2-3. 事前登録

予測・前提・撤回条件、採点の方法と時点。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| 研究の事前登録（Nosek ほか 2018、PNAS 115(11):2600-2606、doi:10.1073/pnas.1708274114）[W3]（B）、OSF Registries [W11]（B） | 「予測（prediction）」と「後付け（postdiction）」の区別。登録は**凍結され、編集も削除もできない**。撤回（withdrawal）は可能だが、タイトル等の最小メタデータと撤回理由が残る。第三者が付ける時刻 | 研究仮説の登録が対象。意思決定の前提や撤回条件の欄は無い | 登録後に黙って書き換える。成果が出てから登録する。**LLMが自分で書いた時刻は、時点の根拠にならない**（原則(b)）。第三者の時刻証明が要る |
| Brier（1950、Monthly Weather Review 78(1):1-3）[W16]（B）、Murphy（1973、J. Appl. Meteor. 12:595-600）[W17]（B） | 二値事象の確率予測の採点規則。Murphy は信頼性（reliability）・分解能（resolution）・不確実性への分解を与える | 二値で、結果が明確に決まる事象に限られる。質的前提、撤回条件には使えない | 採点規則を結果が出てから選ぶ。結果が曖昧で採点不能な予測 |
| Tetlock 系：Mellers ほか 2014（Psychological Science 25(5):1106-1115）[W18]（B）、Tetlock & Gardner 2015『Superforecasting』（Crown）[W19]（B） | 予測を記録し、Brier スコアで累積して採点する運用。確率訓練、チーム、選抜が較正と分解能を上げたとの報告 | 組織の意思決定の「決定」との紐づけは範囲外 | Brierは「後で真偽が明確に決まる問い」にしか使えない（[W19] の書評要約による） |
| ForecastBench（Karger ほか、ICLR 2025、arXiv:2409.19839）[W22]（B） | **LLMの予測を、まだ答えの無い将来の事象で採点**する設計。先読みの偏り（look-ahead）を避ける。人間の専門家との比較 | ベンチマークであり、意思決定の記録形式ではない。検索要約にある数値（GPT-4.5 が 0.101、スーパーフォーキャスターが 0.081）は再確認が要る | 質問集合の選び方が結果を左右する |
| Pre-mortem（Klein 2007、HBR 85(9):18-19）[W14]（B） | 「失敗した」と仮定して理由を挙げる。撤回条件・失敗前提の収集に使える | 結果を記録・採点する仕組みではない | 発散で終わり、登録に至らない |
| Nanopublication（Groth, Gibson & Velterop 2010、Information Services & Use 30(1):51-56、doi:10.3233/ISU-2010-0613）[W23]（B） | 主張（assertion）、来歴（provenance）、公開情報（publication info）を**別のグラフに分けて持つ**構造 | 予測・採点の語彙は無い | 主張と来歴を同じ記録に混ぜると、後から来歴だけ更新できない |
| SUI Hypothesis ペイロード（同 §3.4） | `statement`、`about`、`applicabilityRefs`。**プロバイダが自己申告した確信度をTruthスコアにしない**（原則(b)と一致） | 期日・採点方法・撤回条件の欄は無い | `applicabilityRefs` はAuthority Scopeではない（同 §3.4）。語の取り違えに注意 |

**設計への含意。** ABPの「荷重を担う前提」、Brierの「採点できる予測」、Toulminの「反駁（rebuttal）」に当たる撤回条件は、**採点の仕方が違う**。予測は期日に採点でき、前提は変化の監視で、撤回条件は観測されたら行動する規則である。一つの記録種に `claim_kind` を持たせて同居させるのは妥当だが、**採点は別の記録にする**（§3-3）。登録後の凍結は、OSFと同様に「凍結＋追記による修正」で実現する。

### 2-4. 決定記録

決定、根拠として引いたカードへの参照、権限、予測と撤回条件への参照。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| ADR（Nygard 2011）[W6]（A）、MADR 4.0.0 [W5]（A） | 文脈、決定、帰結、状態。決定の理由の可視化。古い決定を消さず後継を指す | **根拠は文章で、版を固定した参照ではない**。権限（誰の資格で決めたか）の欄は `decision-makers` の名前のみ | 理由が事後の合理化になる。MADRの `Decision Drivers` は価値の記録になりうるが、決定ごとの文章にとどまる |
| RAPID（Rogers & Blenko 2006、HBR）[W24]（B） | **推薦（Recommend）・合意（Agree）・実行（Perform）・助言（Input）・決定（Decide）の役割分離** | 記録の形式ではなく役割モデル。版固定や根拠参照は範囲外。DACI は今回未確認（C） | 役割名が付いていても、実際の決定権の根拠は別に要る |
| OMG DMN [W25]（A） | 決定要求図（DRD）で、決定が依存する入力データ、知識ソース、ビジネス知識モデルを示す。FEELによる決定論理。XMLの交換 | 決定の**論理**を表す。ある時点で誰が引き受けた出来事かは対象外と読める（本書の読み。仕様の「対象外」記述は取得できなかった）。現行版はページ表示で 1.7 beta（2026年9月）で、確定版の番号は未確認 | 決定論理の自動実行と、責任の所在の記録を混同する |
| IBIS／gIBIS（Kunz & Rittel 1970、Conklin & Begeman 1988）[W13]（B）、Toulmin 1958『The Uses of Argument』[W26]（B） | 論点・選択肢・論拠の構造。Toulmin の claim、data、warrant、backing、qualifier、rebuttal。qualifier と rebuttal は**撤回条件の原型** | 版固定、時点、主体、権限は対象外 | 論証の見た目が整っていても、データが原文に戻れない |
| W3C PROV-O [W4]（A） | Entity／Activity／Agent。`wasAttributedTo`、`wasAssociatedWith`、`actedOnBehalfOf`（委任）、Plan、Role、Influence の限定関係 | 「決定」「根拠」「権限」を専用の型としては持たない（汎用の来歴語彙） | 汎用語彙に載せると、決定と実行と権限の区別が消える。**SEIは同じ理由で、Recommendation／Decision／Authority／Executionを一つの `action` へ平坦化しない**（`SEI_SEMANTIC_INTERCHANGE_v1alpha1.md` §9、§14-4） |
| W3C ODRL 2.2 [W27]（A） | Policy（Set／Offer／Agreement）、Permission、Prohibition、Duty、Constraint、assigner／assignee。**権限付与の表現に使える** | 権利表現が出自。決定記録との接続は無い | 制約（Constraint）を機械が解釈できる形にしても、その真偽の判定者が別に要る |
| SEI Decision Memory（`SEI_DECISION_MEMORY_v1alpha1.md`） | 決定の同一性、内容、文脈、`basis`（明示的に考慮した根拠）、Rationale（外在化した説明。私的な思考連鎖ではない）、未解決参照、責任（Responsibility）参照、系譜。**Authorityは外部のAuthority ProviderまたはAuthority evidenceへの参照として別境界**。基底の根拠を現在版へ黙って差し替えない | 予測・撤回条件への参照欄は無い（再開条件・見直しトリガを明示Artifactとして残せる、と §6・§10 にある）。範囲（range）での根拠固定は無い | 同上 |
| SUI Decision ペイロード（同 §3.7）と Authority 遷移（`sensemaking_artifact_contract_v1alpha1.md` §7） | `decisionKind`（adopt／defer／reject／investigate／act／other）、`selectedRefs`、`alternativeRefs`、`basisRefs`（厳密なリビジョン参照）。**Decisionと Authority を別の記録にする** | 範囲固定は無い。`authorizedBy.kind="policy"` は予約で、現行では自動昇格に使わない（§7.3） | §5 の衝突点 |
| EU AI Act 第12条、第19条、第26条 [W28]（B、非公式サイト経由） | 第12条は、高リスクAIシステムに、運用期間にわたる事象の自動記録（ログ）を技術的に可能にすることを求める。第19条はプロバイダの、第26条はデプロイヤの、自動生成ログの保存を、少なくとも6か月とする（他のEU法・国内法で異なる場合を除く） | 記録の**項目**を規定するのは、生体認証システムの最小項目に限る（第12条3項。取得できた範囲）。意思決定の根拠や権限の記録は規定しない | 規制は「ログがある」ことを求めるのであって、「根拠へ戻れる」ことは求めない。後者は本構想の側の要件である |

**何が「決定」「権限」「根拠」を分けるか。** 先行例を総合すると、次の三つに分けるのが筋になる。

- **決定**: ある時点で、ある主体が引き受けた言明（出来事）。RAPID の D、SEI の Decision、SUI の Decision payload に当たる。
- **権限**: その主体がその範囲で決める資格を、誰が、いつからいつまで付与したかを示す別の記録。PROV の `actedOnBehalfOf`、ODRL の Permission、SEI の外部Authority参照に当たる。決定記録に埋め込まず、参照する。
- **根拠**: 決定が引いた入力。版と範囲を固定した参照で持ち、**要約ではなく原文へ戻る**。SEI の `basis`、SUI の `basisRefs` が近いが、範囲固定が無い。

理由（Rationale）は根拠ではない。Turpin ほか（NeurIPS 2023、arXiv:2305.04388）[W29]（B）は、思考連鎖による説明が、モデルの予測の真の理由（入力に入れた偏り）に言及しないことがあると報告する。SEIが「Rationaleに私的思考連鎖を要求しない」と定めるのも、この問題の別の側面と読める。

### 2-5. 再開記録

再開時の前提の有効性の確認結果、更新された問い、失効した前提。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| I-PASS（Starmer ほか 2014、NEJM 371(19):1803-1812）[W30]（B） | 引継ぎの構造化。要素は、重症度（Illness severity）、患者要約（Patient summary）、行動リスト（Action list）、状況認識と不測時の計画（Situation awareness and contingency planning）、**受け手による統合（Synthesis by receiver）**。医療ミスが 24.5 件から 18.8 件/100入院、予防可能な有害事象が 4.7 から 3.3 件/100入院へ減ったと報告 | 効果は研修・口頭・書面・持続の施策の**一括（bundle）**に対するもので、記録形式単独の効果ではない。人から人への対面の引継ぎである。SBAR は今回確認していない（C） | 受け手の語り直しは、本構想の「原文の再読による語り直し」に近いが、元の情報を持たない受け手が自分の理解を述べる点で異なる |
| ランブック／ポストモーテム | 手順と事後検証の運用 | 一次出典を今回確認していない（C） | — |
| バイテンポラル（Fowler [W31]（A）、SQL:2011 の時間機能 Kulkarni & Michels 2012、SIGMOD Record 41(3):34-43 [W32]（B）） | **有効な時点（実際の時間）と記録した時点（記録時間）の分離**。遡及訂正を、実際の履歴を直しつつ記録の履歴は追記で残す。SQL:2011 は system-versioned と application-time の期間表 | データの事実を対象とし、「前提が今も成り立つか」の確認手続きは対象外 | 記録時点だけで管理すると、「いつから失効していたか」が分からない |
| イベントソーシング（Fowler [W33]（A）） | 状態の変更をイベント列として保持し、過去状態を再構成する。遡及訂正は、誤ったイベントを逆転して再生する | **外部システムへの問い合わせは、再生時に異なる値を返しうる**ため、問い合わせ結果を保持する設計が要る | 前提の再確認で外部の現在値を取り直すと、当時の判断の根拠が書き換わる。観測値と観測時点を残す |
| 信念改訂（Alchourrón, Gärdenfors & Makinson 1985、J. Symbolic Logic 50:510-530）[W34]（B） | 理論の縮約（contraction）と改訂（revision）の形式。何を捨てるかの選択問題を明示した | 論理的な理論に対する形式で、実務の記録形式ではない | 形式の厳密さと、記録の運用が混同される |
| Argyris 1991（HBR 1991年5-6月）[W35]（B） | 単一ループ学習（設定した目標に合わせて行動を直す）と二重ループ学習（目標・前提自体を問う）の区別 | 記録形式ではない | 前提の見直しが、行動の微修正で済まされる |
| SEI の Cognitive Resumption Model（`COGNITIVE_RESUMPTION_MODEL.md`） | 持続的な意味の記録（Layer A）と、再開用の射影（Layer B：簡潔、選択的、置換可能、再生成可能）の二層。再開支援は記録を権威的には書き換えない | **評価専用（Evaluation-only）の、研究由来の製品モデル**であり、契約ではない。Layer B のみで、前提の確認結果の記録は扱わない | 要約が Unknown を落とす、Conflict の片側を残す、後の証拠を過去の根拠へ混ぜる（同文書 §2.1） |

**設計への含意。** 再開記録を二つに分ける。(i) **確認結果**（前提ごとの判定、確認方法、照合先、有効だった時点と記録した時点）は持続的な記録とし、(ii) **再開用の要約**は再生成できる射影として別に置く。前提の失効は、成果物の改訂とは別の事象である（世界の側が変わった）ため、SEIの `revises／supersedes／withdraws` では表せず、有効な時点の終わりを持つ関係が要る（§5、衝突点 C8）。

### 2-6. 停止記録

範囲外で止まった理由、回した先、影響範囲と可逆性の評価。

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| サーキットブレーカー（Fowler [W36]（A）、Nygard『Release It!』） | 状態（closed／open／half-open）。**状態変更をログに残す**。人手による開閉。半開で限定的に試行して復帰を判断する | 技術的な失敗の連続が契機。**棄権（能力・権限の外で止まる）**は対象外 | 閾値を自己判定にすると、止まらない |
| EU AI Act [W28]（B、非公式サイト経由） | 第14条4項：監督者が、システムの出力を無視、覆す、**停止または中断**する能力を持てること。第26条5項：デプロイヤは、リスクを認めたとき、提供者・流通業者・市場監視当局へ通知し、使用を停止する。重大インシデントは、まず提供者へ知らせる。第73条：**提供者**による重大インシデントの報告。通常は因果関係の確立後すぐに、遅くとも15日以内。広範な違反などは2日以内、死亡は疑った時点で遅くとも10日以内。不完全な初報と、完全な後報を許す。第72条：市販後監視 | 義務の主体は高リスクAIシステムの提供者・デプロイヤで、対象は**害の出た重大インシデント**。害に至る前に範囲外で止まった記録（ヒヤリハット、棄権）を求める条文は、今回確認した範囲に無い | 記録の規制適合と、自前の安全の記録を同一視する |
| AI Incident Database（McGregor 2021、AAAI 35(17):15458-15463）[W37]（B）、OECD「Towards a common reporting framework for AI incidents」（OECD AI Papers No.34、2025年2月）[W38]（B） | 事後の事例収集。OECDの枠組みは29の基準で、インシデントの説明、最初に知られた発生日、重大度、害の種類などを含む | **害が出た後**の事象の報告形式。自律的な停止の理由・回した先・可逆性評価の項目は、今回確認した範囲で見当たらない | 事故報告の形式をそのまま停止記録に流用すると、予防的な停止が記録されない |
| 安全ケース／GSN（GSN Community Standard Version 3、SCSC-141C、2021年5月）[W39]（B） | 主張（Goal）を、論拠（Strategy）、文脈、前提、証拠（Solution）へ分解する論証の構造 | 規格の要素の一覧は今回取得できなかった（C）。運用中の停止の記録ではなく、**運用前の論証** | 論証が静的な文書に終わり、運用記録と接続されない |
| PROV の委任（`actedOnBehalfOf`）[W4]（A） | 回した先（誰へ回したか）を、委任関係で表す | 停止の語彙は無い | — |
| エスカレーション手順 | — | 標準の一次出典を確認できなかった（C） | — |

**設計への含意。** 停止記録は、(i) 停止の契機となった**境界**（権限付与記録の範囲条項、能力の限界、環境）を、観測可能な形で指す、(ii) 回した先と時点を残す、(iii) 影響範囲と可逆性（不明を許す）を残す、(iv) 解消（再開記録または他主体の決定）へ紐づく、の四点を持つ。**「範囲内」「範囲外」の判定をLLMの自己申告に任せない**ため、境界は権限付与記録の条項参照として機械的に特定できるようにする。

### 2-7. 横断：記録の交換形式

| 先行例 | 再利用できる点 | 不足 | 落とし穴 |
|---|---|---|---|
| JSON-LD 1.1（W3C勧告 2020年7月16日）[W40]（A） | `@context`、`@id`、`@type`、`@graph`、`@included`、`@protected`、`@import`。**素のJSONとして読める記録に、意味の写像を別添えにできる** | 語彙の定義が文脈（context）の取得に依存する。文脈の不変性の保証は `@protected` 以外に明示が無い | 外部の文脈ファイルが変わると意味が変わる。文脈を版固定する |
| W3C PROV-O／PROV-DM [W4]（A） | 来歴の汎用語彙。RDF | 重い。必須にすると必須依存になる | — |
| OpenTelemetry GenAI semantic conventions [W41]（A、安定性は未確認） | スパン、メトリクス、イベント、エージェントを対象とする規約。現在は専用リポジトリ `semantic-conventions-genai` へ移管済み（旧ページの案内による）。安定性の区分は取得できなかった | **実行の痕跡**（trace）であり、意味の記録ではない | 痕跡を意味の記録と取り違える。`runRef`（SUI）のように、痕跡へは参照で結ぶ |
| MCP [W42]（A） | 仕様のページは版 2026-07-28 を指す。サーバ機能は Resources／Prompts／Tools、クライアントの Elicitation。拡張として Tasks、Skills over MCP など | **転送の規約**であり、記録の意味形式ではない。Resources として記録を配ることはできる | 転送の都合で記録の意味を決めない |
| Agent Skills [W43]（A） | `SKILL.md`（`name`、`description` 必須。`license`、`compatibility`、`metadata`（文字列から文字列への写像）、`allowed-tools`（実験的）は任意）。`scripts/`、`references/`、`assets/`。段階的開示 | **手順の配布形式**であり、記録の交換形式ではない。記録を書く・読む手順を配るのに向く | `metadata` が文字列のみで、入れ子の記録を載せるのには向かない |
| DSSE [W44]（A）、RFC 8785 JCS [W45]（A） | 署名の封筒（`payload`、`payloadType`、`signatures`）。JSONの正規化（ハッシュと署名のため）。検証した同一バイトを適用側に渡すことを要求 | 鍵管理・信頼の根は範囲外 | 再解析後の値を検証済みとみなす。SEIはすでに `sei.jcs+sha256/v1alpha1` と `sei.raw-bytes+sha256/v1alpha1` を表現プロファイルとして持つ |

## 3. 六種の過不足

### 3-1. 統合すべきもの

**統合は勧めない。** 次の部品を共通化すれば足りる。

| 共通部品 | 使う記録 |
|---|---|
| 条件トリガ（観測可能な条件、観測方法、観測者、期日） | 保留台帳（解除条件）、事前登録（撤回条件、前提の監視）、停止記録（再開条件） |
| カード参照（§4-2） | 決定、事前登録、再開、保留、停止、採点、誤り判定の全て |
| 状態遷移の発端と時点（有効な時点／記録した時点） | 保留、再開、停止 |

停止記録と再開記録を一つの「状態遷移記録」にまとめる案は、再開が停止後に限らず、中断、担当替え、モデル更新でも起きるため採らない。再開記録が停止記録を任意で参照する（`resumes`）形にする。

### 3-2. 分割すべきもの

| 対象 | 分割 | 根拠 |
|---|---|---|
| 事前登録 | `claim_kind` を `prediction`／`assumption`／`withdrawal_condition` とし、採点は別記録 | 採点の方法と時点が異なる（§2-3）。凍結と、結果の追記を分けるため（OSF、Nanopublication の分離構造） |
| 決定記録 | 決定（出来事）と権限（付与）を別記録にする。決定は権限付与記録を**参照のみ**する | SEI は Decision への Authority 埋め込みを拒否する（`SEI_DECISION_MEMORY_v1alpha1.md` §8、§11-6）。SUI も Decision と Authority 遷移を別記録にする |
| 保留台帳 | 実体は「保留エントリ」とその状態変更イベント。台帳は射影 | 可変の表は、後知恵で書き換えられる。SEI の「過去のbasisを黙って差し替えない」と整合 |
| 再開記録 | 確認結果（持続）と再開用要約（射影）を分ける | SEI の Layer A／B の分離（`COGNITIVE_RESUMPTION_MODEL.md`） |

### 3-3. 欠けている記録の提案

| 提案 | 要否 | 根拠 | 補足と反論 |
|---|---|---|---|
| **採点記録** | 必須（B3の成立条件） | 事前登録は凍結するため、結果と採点は別に持つ。採点者は登録者と別の過程にする（設計草案 §4 B3「別の過程で採点される」）。ForecastBench、Tetlock系の運用が前例 | 採点不能・曖昧な結果を、`unresolvable` として残す欄が要る。採点規則を事前登録時に固定する |
| **権限付与記録** | 必須（原則(d)の成立条件） | 承認の有無を運用パラメータにするには、**誰が、どのエージェントに、どの範囲を、いつからいつまで委ねたか**を、決定記録と別に持つ必要がある。停止記録の「範囲外」の定義もここから来る。前例は PROV の委任、ODRL、RAPID の D | SUIの Authority 遷移は成果物の採用状態で、対象が異なる（§5 C1）。付与の対象を「モデルID・版・構成」のどこまで含めるか（モデル更新で付与は引き継がれるか）は未決 |
| **誤りの層の判定記録** | 必須に近い（B3の「事実・予測・枠組みの三層」） | 食い違いが出たとき、事実の訂正で済ませず、どの層の誤りかを判定し、戻り先（問い、保留、カード）を指す。Argyris の単一／二重ループの区別が示唆する | **三層（事実・予測・枠組み）に直接対応する既存標準は確認できなかった**。作業仮説の分類であり、判定の独立性（誰がどの手続きで判定するか）が要る。争いがあれば `contested` として残す |
| **価値・目的の記録** | 新しい記録種にしない案を勧める | 目的は、権限を持つ主体が原文で書いたものであり、再読で語り直す対象である。したがって**カードの役割（`role: purpose`／`role: tradeoff`）**として持ち、決定記録が `value_refs` で版固定参照する。MADRの `Decision Drivers` も決定ごとの価値の文章化である | 優先順位の入れ替わりを機械的に検出したいなら、構造化した記録が要る。その場合に限り別種へ昇格する。判断は未決 |
| 照合（戻し）の記録 | 新種にしない | 戻し先の種類（一次資料、観測、実験、人・組織への確認、時間）は、観測カードの属性と、根拠関係の `return_kind` で持てる | 自己再読や別LLMの批評を「戻した」に数えない規則（設計草案 §4 A4）は、`return_kind` の語彙で区別する |
| 打ち切り・費用の記録 | 低優先 | 位置づけ文書 §9-8 の条件3（費用の自己申告と打ち切り）に対応する。ラウンドの停止は、範囲外の停止（停止記録）とは別 | 費用の自己申告は、観測値（トークン、時間）と推定を区別する |
| 反例の記録 | 新種にしない | 「体系を使っても差が出なかった事例」は、結果の採点記録と誤り判定記録に含められる | 公開記録への反映は運用の問題 |
| 異議・挑戦の記録 | SUI の `ReviewRecord`（`disposition: objected`）を再利用 | 追加不要 | 照合者の独立性（情報源、手続き、時点、権限）の宣言を、採点・誤り判定記録の項目にする |

### 3-4. 小結

六種を、**核となる九種（六種＋権限付与、採点、誤り判定）**と、共通部品（カード参照、条件トリガ、有効時点／記録時点）に整理する。優先順位は、権限付与記録と採点記録を最初に、誤り判定記録をその次に置く。この順にする理由は、前者がないと、決定記録の「権限」と停止記録の「範囲」が定義できず、採点がないと予測・前提の外部照合（B3）が回らないからである。

### 3-5. 原則との整合

| 原則 | 本案での具体化 |
|---|---|
| (a) 来歴は原文の再読で得る。ラベルは索引・警報 | カード参照が版と範囲を固定し、再読を起動する規則を持つ。ラベルの欄は任意で、判定条件に使わない |
| (b) LLMの自己申告は根拠にならない | 時刻は第三者の証明、採点は登録者と別の過程、境界の判定は条項参照で機械的に特定、確信度はTruthスコアにしない |
| (c) 判断は観測できる行動で定義 | 各記録の必須項目は、観測できる行為（誰が・いつ・何を引き・何を決め・何を照合したか）に限る。内的状態の欄を置かない |
| (d) 人間の承認は運用パラメータ | 権限付与記録の `approval_requirement` に置く。決定記録の構造は承認の有無で変えない |

### 3-6. EU AI Act に関する留意

- 条文番号と趣旨は、非公式の閲覧サイト（artificialintelligenceact.eu）の取得結果による（確認水準B）。公式のEUR-Lex（規則（EU）2024/1689）は、取得した結果から条文の見出しを確認できなかった。
- 高リスク義務の適用時期は、複数の法律事務所の解説によれば、デジタルオムニバスにより Annex III の単独システムが2027年12月2日、Annex I の製品組込みが2028年8月2日へ繰り延べられ、EU理事会が2026年6月29日に最終承認したとされる（B、二次情報）。官報での公布と発効の確認は未実施。
- 第14条・第73条などは高リスクAIシステムが対象で、本構想の対象システムが高リスクに当たるかは別の判断である（設計草案 §8、§10の「許容は別の問い」）。

## 4. 最小項目案

### 4-1. 共通の封筒（全記録）

| 項目 | 必須 | 内容 |
|---|---|---|
| `schema` | 必須 | 記録種別と版（例 `csw.record.decision/v0`）。SUI の `sui.…/v1alpha1`、SEI の `contract_id`＋`version` と同じ流儀 |
| `record_id` | 必須 | 論理ID。保管先の行IDや経路にしない（SEI の `Storage identity != semantic identity`） |
| `recorded_at` | 必須 | 記録した時点。**第三者の時刻証明がある場合は `time_proof` に別置**（自己申告の時刻と区別） |
| `author` | 必須 | `{kind: human|ai|system|import|unknown, ref?: 不透明な文字列}`。**不明は `unknown` とし、推測しない**（SUI 来歴エンベロープ §4.2 と同じ）。SUI MVPの主体メタデータ境界（ADR-0056）は §5 C4 参照 |
| `refs` | 条件付き必須 | 他の記録・カードへの参照（§4-2） |
| `valid_from`／`valid_to` | 任意 | 有効な時点（バイテンポラル）。前提・付与・保留で使う |
| `revises`／`supersedes`／`withdraws` | 任意 | SEI の系譜語彙。内容の識別（版）を両端に持つ（`SEI_SEMANTIC_REFERENCE_v1alpha1.md` §3） |
| `integrity` | 任意（推奨） | `{profile, digest}`。表現プロファイルIDを必ず伴う（SEI §4）。署名は DSSE 封筒で外側に付ける |
| `ext` | 任意 | 名前空間付きの拡張。未知の拡張は保持し、既知として黙って解釈しない（SEI Interchange §5） |

欠落を否定事実に変えない（SEI Interchange §12-最後、`Unknown != No`）。

### 4-2. カード参照（`card_ref`）の持たせ方

```text
card_ref:
  card_id          論理ID（必須）
  revision_id      厳密な版（必須）
  content_digest   カード版の本文（逐語）に対するダイジェスト（必須）
  profile          ダイジェストの表現プロファイルID（必須。SEIの2種、またはSUIのsha256）
  range            （任意）カード版の内側の範囲
    quote:   { exact, prefix, suffix }       引用選択子
    position:{ start, end }                  位置選択子（版が不変なので脆くない）
    range_digest 範囲の本文のダイジェスト
  source           （任意）元の出典の固定
    source_ref, source_version_digest, captured_at
    source_range: { quote, position }        出典内の範囲
    snapshot_ref  保存した写しへの参照（Robust Links／Memento の考え方）
  reread           （任意）再読の規則
    triggers: [on_decision_review, on_resume, on_basis_challenged,
               on_digest_mismatch, on_due]
    retelling_required: true|false
```

設計の要点を挙げる。

1. **カード版が逐語の本文を内包する。** 出典が消えても再読できる。出典側の固定は補助である。
2. **範囲は不変の版に対して取る。** W3C Web Annotation が警告する位置選択子の脆さを避けられる。出典内の範囲は、引用選択子と位置選択子を併記する。
3. **検証結果を三つに区別する。** `verified`／`failed`／`not_verified`（SEIの `Verification Outcome`、`SEI_SEMANTIC_REFERENCE_v1alpha1.md` §5）。検証器や出典を取得できないことを不一致と読み替えない。意図的に取得不能な参照と壊れた参照も区別する（SEI Interchange §7）。
4. **再読は、参照に付くラベルではなく、起動規則と出来事の記録である。** `reread` は「いつ再読が必要か」を示す索引・警報にとどまる。再読を行った事実は、独立の出来事として残す（次項）。
5. 参照先が変わっても黙って現行版へ差し替えない（SEI Decision Memory §4）。

**再読の記録（再読イベント）。** `{card_ref, reader, at, retelling_ref}`。語り直しの本文は派生物として別に保持し、原文からの**逐語引用と位置（オフセット）**を含めさせる。これにより、引用部分が原文と一致するかを**決定論的に検査**できる。意味の忠実さ（言い換えが正しいか）は機械では検査できないため、別の読み手による確認を要する。この区別は、原則(a)と(b)の緊張への、本書の暫定の解である（§7）。

### 4-3. 記録別の項目

凡例: ◎必須、○任意（推奨）、△任意。SEI の Progressive Explicitness（低影響の決定に最大項目を強制しない）に従い、必須の範囲は運用の Profile で段階化する。

| 記録 | 項目 |
|---|---|
| **カード** | ◎`card_id`、`revision_id`、`text`（逐語）、`content_digest`＋`profile`、`captured_at`、`author`。○`source`、`role`（`evidence`／`purpose`／`tradeoff`／`observation_of_outcome` など）、`derived_from`（要約・翻訳の場合は必須。原文カード版へ）。△ラベル（索引。判定に使わない） |
| **保留エントリ**（イベント列） | ◎`hold_id`、`question`（文またはカード参照）、`opened_at`、`opened_by`、`basis_refs`、`release_condition`（条件トリガ）、`due`（日付、または `none` と理由）、`cost_of_not_deciding`（`{description, measure?, kind: observed|estimated|unknown}`）。イベント：`extended`、`released`、`expired`、`converted_to_decision`（それぞれ参照を伴う）。○`owner`、`next_review_at`、`linked_decision` |
| **事前登録** | ◎`prereg_id`、`registrant`、`registered_at`＋`time_proof`、`claims[]`。各 claim：◎`claim_kind`、`statement`、`observation_method`、`check_at`。`prediction` は◎`resolution_criteria`、`resolve_by`、`probability`（または結果空間）、`scoring_rule`。`assumption` は◎`load_bearing_for`（決定への参照）、`signposts`（観測可能な兆候）。`withdrawal_condition` は◎`condition`、`action_on_trigger`（`withdraw`／`escalate`／`reopen_hold`）、`decision_ref`。○`basis_refs`。凍結し、修正は `amends` による新記録 |
| **決定記録** | ◎`decision_id`、`statement`、`decided_at`、`decider`、`basis_refs`（`card_ref`の配列）、`authority_grant_ref`（**参照のみ**）、`unresolved_refs`（保留エントリ、SEI の Unknown・Conflict へ。存在する場合）。○`contrary_refs`（検討した反対の根拠）、`alternatives`、`prereg_refs`（予測・前提・撤回条件。重要・不可逆な決定では実質必須）、`value_refs`、`impact_ref`（影響範囲・可逆性の評価）、`rationale`（外在化した説明）、`supersedes`。`decisionKind=defer` の場合は、対応する保留エントリ参照を必須にする |
| **権限付与記録** | ◎`grant_id`、`grantor`、`grantee`（エージェントの識別：モデルID・版・構成のダイジェスト・配備）、`scope`（決定の種類、金額・影響・不可逆性の上限、領域）、`valid_from`、`valid_to`、`approval_requirement`（`required`／`not_required`／`conditional`＋条件）。○`basis`（方針・法的根拠への参照）、`revoked_by`、`stop_clauses`（停止の条項。停止記録が参照する） |
| **再開記録** | ◎`resume_id`、`resumed_at`、`resumed_by`（担当・モデル・版）、`subjects`（再開する決定・保留・事前登録）、`premise_checks[]`：◎`premise_ref`、`check_method`、`source_kind`（外部照合か自己再読か）、`observed_at`、`verdict`（`still_valid`／`invalid`／`changed`／`not_verified`）、`evidence_refs`。◎`updated_questions`、`invalidated_premises`（◎`invalid_since`＝有効時点、`recorded_at`＝記録時点）。○`resumes`（停止記録への参照）、`reread_refs`、`projection_ref`（再生成可能な要約。権威を持たない） |
| **停止記録** | ◎`stop_id`、`stopped_at`、`stopped_by`、`trigger`（権限付与の条項参照、能力の限界、環境のいずれか。観測可能な形）、`subject`（対象の決定・保留）、`routed_to`（相手と経路）、`routed_at`、`impact_assessment`：◎`scope`、`reversibility`（`reversible`／`partial`／`irreversible`／`unknown`）、`assessed_by`。○`interim_measures`、`resolution_ref`、`status`（`halted`／`awaiting`／`resolved`） |
| **採点記録** | ◎`score_id`、`prereg_ref`（claimの識別を含む）、`resolved_at`、`resolution_source`（外部）、`outcome_ref`（観測カード）、`outcome`（`hit`／`miss`／`value`／`ambiguous`／`unresolvable`）、`scorer`、`independence`（登録者との独立性：情報源・手続き・時点・権限）。○`score`、`scoring_rule` |
| **誤り判定記録** | ◎`finding_id`、`trigger_refs`（事前登録と観測、または反する観測）、`layer`（`fact`／`prediction`／`framework`／`multiple`／`unclassified`）、`return_targets`（問い・保留・カードへの参照）、`determiner`、`independence`。○`evidence_refs`、`status`（`proposed`／`contested`／`accepted`） |

## 5. SUI/SEI の既存形式との対応表と衝突点

### 5-1. 対応表

| 本案の記録 | SUI（既存） | SEI（既存） | 対応の度合い |
|---|---|---|---|
| カード | `Card`（`DocumentV1`、可変。`schemas.md` §3.2）、**Evidence 成果物**（`SemanticArtifactRevision`、`kind=evidence`、`ArtifactRevisionRef`＝`artifactId`＋`revisionId`＋`contentDigest`） | Observation、Exact Artifact Binding（論理参照＋ダイジェスト＋表現プロファイル）、Semantic Lineage | 部分的。SUIの `Card` と Evidence は**自動変換しない**（artifact contract §11.1）。範囲の固定は両者に無い |
| 保留台帳 | `Card.holdState`（`held`／`pending`／`shelved`）、`ArtifactLifecycle=held`、`ReviewDisposition=held`、`Shelf` | Unknown、Question、Conflict、再開条件（任意の明示Artifact） | 状態は有るが、解除条件・期限・コストの欄が無い |
| 事前登録 | `Hypothesis` ペイロード（`statement`、`about`、`applicabilityRefs`） | Hypothesis、Cognitive Method Application（`input_refs`・`output_refs`・`residual_refs`） | 予測・期日・採点・撤回条件が無い。拡張で足す余地は有る（Interchange §4は型の一覧を「閉じたUniversal taxonomyにしない」と定める） |
| 決定記録 | `Decision` ペイロード（`decisionKind`、`statement`、`selectedRefs`、`alternativeRefs`、`basisRefs`、`decisionContextRef`） | `sei.decision-memory`（`ref`、`statement`、`basis_refs`、`unresolved_refs`、`rationale`。フィクスチャ `decision-with-unresolved.json`） | 高い。範囲固定と予測・撤回条件への参照が無い |
| 権限付与記録 | `AuthorityTransitionEvent`（成果物の採用状態の遷移）、`AuthorityScope` | 外部Authority Provider／Authority evidence への参照、Responsibility | **対象が異なる**。エージェントへの決定権の委任は、どちらにも無い（C1） |
| 再開記録 | `RoundSnapshotV1`、`InquiryJourneyV1`（再開の出典になりうる）、`ArtifactLifecycle` | `COGNITIVE_RESUMPTION_MODEL.md`（評価専用）、Semantic Lineage | 確認結果の記録は無い |
| 停止記録 | 無い（`llm_escalation_policy.html` は未読。名称が近いが、LLM呼び出しの段階的な切替の方針と推定され、停止記録とは別と思われる） | 無い（`CONTRACT_CATALOG.md` の「semantic escalation negative fixture」は、意味の格上げ（RecommendationのDecisionへの昇格など）の禁止の検査で、停止ではない）。`SEI_DECISION_CONTINUITY.md` §4.5 に Control continuity（製品価値の概念） | 空白 |
| 採点記録 | 無い | 無い（Business Outcome は Decision と別の概念として挙がるが、採点の型は無い） | 空白 |
| 誤り判定記録 | `ReviewRecord`（`challenge`、`objected`）が近い | Conflict | 層の判定の欄は無い |

### 5-2. 衝突点・整合の注意点

| # | 衝突・注意 | 根拠のファイル | 対処の方向 |
|---|---|---|---|
| C1 | **「Authority」が三つの意味で使われる**。SUI＝成果物の採用状態（`working`／`candidate`／`accepted`／`consensus`）。SEI＝決める権限（`Responsibility != Authorization`）。本構想＝エージェントへの決定権の委任 | `sensemaking_artifact_contract_v1alpha1.md` §7、`SEI_DECISION_MEMORY_v1alpha1.md` §8、`sei-cognition/README.md` §1 | 本案の記録名は「権限付与（Delegation Grant）」とし、「Authority」の語を避ける。SEIの外部Authority参照に、本記録を指す形で接続する |
| C2 | **SUIは、AIが生成したDecisionに人間のDecision Authorityを持たせない**。`authorizedBy.kind="policy"` は予約で、現行では自動昇格に使わない | `sensemaking_payload_authority_exchange_v1alpha1.md` §3.7、`sensemaking_artifact_contract_v1alpha1.md` §7.3 | SUIの契約は「採用（adoption）」の領域であり、委任ではない。本構想の「承認が無い運用」は、SUIの外（権限付与記録）で表し、SUIの契約を変えない。SUIは人間承認を既定とする製品方針（SafeMode、`human_reviewed`）で、衝突ではなく**適用範囲の違い**として明記する |
| C3 | **SEI は、Decision 記録に Authority を埋め込むことを拒否する**（契約 §8・§11-6、負例フィクスチャ `decision-authority-field.json`。後者は存在のみ確認、内容は未読） | `SEI_DECISION_MEMORY_v1alpha1.md`、`fixtures/contracts/v1alpha1/negative/` | 決定記録の権限は `authority_grant_ref` の参照のみ（§4-3）。設計草案 §5 の「決定記録は…権限…を持つ」は、「参照を持つ」と読み替える |
| C4 | **カードの可変性とメタデータ境界**。SUIの `Card.text` は可変なCanvas（`DocumentV1` は変えない）。`Card.meta` は既知キー以外を受け付けず、主体メタデータ（起票者など）をMVPで含めない。外部共有では主体メタデータを既定で含めない | `schemas.md` §3.2、`sensemaking_artifact_contract_v1alpha1.md` §11.1、ADR-0056 決定案 3・4 | カードは SUI の Evidence 成果物として書き出す adapter を前提にする。`card_ref` や `author` を `Card.meta` に載せない。共有時の `author` は、既定で空（`unknown`）にできる設計にする |
| C5 | **ロケータ契約が未決**。Evidence の `source_segment` の `locatorRef` は不透明で、AIが推測して補うことを禁じる。ダイジェストは任意 | `sensemaking_payload_authority_exchange_v1alpha1.md` §3.1、§13 | 本案の `range`・`source` は、SUIの未決事項（ロケータの共通契約）の候補になる。SUI側の判断を待つ。推測で補わない規則はそのまま採る |
| C6 | **「held」の語の重複**。`Card.holdState=held`（判断の保留）、`ArtifactLifecycle=held`（`held != Working`）、`ReviewDisposition=held`、さらに本案の保留台帳 | `schemas.md` §14.1、`sensemaking_artifact_contract_v1alpha1.md` §3.2・§6.1 | 保留台帳は「保留エントリ（hold entry）」とし、`Card.holdState=held` を対応するエントリの開始イベントとして読む規則を作る。`pending`（未処理）は保留ではない。SUIの `decisionKind=defer` は、対応する保留エントリ参照を必須にする |
| C7 | **再開記録と再開用要約の権威の違い**。SEI の再開支援（Layer B）は記録を権威的には書き換えない。ただし、同文書は**評価専用**で契約ではない | `COGNITIVE_RESUMPTION_MODEL.md`（状態表記） | 確認結果は Layer A 側の持続的な記録とし、再開用要約を射影として別に置く。評価専用のモデルを根拠に契約を決めない |
| C8 | **系譜の語彙が足りない**。SEI は `revises`／`supersedes`／`withdraws` の三つ。SUI の `ArtifactLineageRole` は8種（`derived_from`、`grounded_by`、`supports`、`contradicts`、`alternative_to`、`synthesizes`、`basis_for`、`supersedes`）。前提の**失効**（世界が変わり、前提が成り立たなくなった）は、どちらにも無い。`withdraws` は「後継を置かず採用候補から取り下げる」で、意味が異なる。SEI はダイジェストの差から系譜を推定することも禁じる | `SEI_SEMANTIC_REFERENCE_v1alpha1.md` §2.3・§8-4、`sensemaking_artifact_contract_v1alpha1.md` §5 | `invalidated_by`（有効時点の終わりを伴う）を拡張の関係として足す案。PROV-DM の `wasInvalidatedBy` が前例。ダイジェストの不一致から系譜を自動生成しない |
| C9 | **ダイジェストの流儀の違い**。SEI は Exact Binding に表現プロファイルIDを必ず持たせる（`sei.jcs+sha256`、`sei.raw-bytes+sha256`）。SUI の `contentDigest` は `sha256:` 前置の文字列で、プロファイルIDを持たない。SUI は、コンテンツストアや正規JSONの部品を共有するかを別に評価するとする | `SEI_SEMANTIC_REFERENCE_v1alpha1.md` §2.2・§4、`sensemaking_artifact_contract_v1alpha1.md` §2.1・§11.2 | `card_ref` に `profile` を必須で持たせ、同一内容で異なるダイジェストが出る場合を区別する |
| C10 | **SEI に予測・採点の型が無い**。Business Outcome は Decision と別と挙げられるが、型は無い。拡張の余地は有る | `SEI_DECISION_MEMORY_v1alpha1.md` §2、`SEI_SEMANTIC_INTERCHANGE_v1alpha1.md` §4 | 事前登録・採点記録は、Interchange の「domain-specific／optional Profile Artifact」として足す。SEIの契約の改訂は求めない |
| C11 | **共有・公開の境界**。SUIの交換バンドルは `safeModeApplied=true` が必須。取り込んだ Authority と Review は**出典側の主張（assertion）**で、ローカルの記録ではない | `sensemaking_payload_authority_exchange_v1alpha1.md` §8.5〜8.7 | 取り込んだ決定記録の権限付与参照は、受け側で再検証するまで有効としない。「Envelopeに入れられる」と「共有してよい」を区別する（SEI Interchange §13） |
| C12 | **成熟度の差**。SUI の記録契約は「L0 計画中、ランタイム未実装」。SEI の契約は pre-stable の `v1alpha1`。両製品とも検証未完了と明記する | `sensemaking_artifact_contract_v1alpha1.md` 冒頭、`sei-cognition/README.md`、`sui-sensemaking/README.md` | 対応は設計水準。実装可能と主張しない。兄弟製品の正本は各リポジトリ（`sibling-product-semantic-correspondence.md`） |
| C13 | **島（Island）は記録の対象にしない**。`Island` は `id`、`cardIds`、`parentIslandId?` の最小型（`schemas.md` §9）で、島の要約や関係は別の節で扱う（未読）。島は交換する記録に含めず、必要なら Structure／Synthesis 成果物として扱う | `schemas.md` §9 | 記録六種に島は含まれない。カードへの回帰が島の要約経由で失われない運用が要る |

## 6. 必須依存を作らずに結ぶ方法

1. **自己記述する。** 各記録が `schema`（種別と版）を持ち、読み手が未知の種別・拡張を、保持して**未検証**として扱える（SEI Interchange §5。「受理できない」「保持するが意味検証不能」「既知部分のみ処理」を区別）。
2. **素のJSONを正本にする。** JSON-LD の `@context` は、必要な読み手向けの**別添え**にする。文脈ファイルは版固定し、変更で意味が変わらないようにする。PROV-O は、読み手が望むときの写像先にとどめる。
3. **参照は、製品内部のIDに依存しない。** 論理ID＋版＋ダイジェスト＋表現プロファイル＋位置の手掛かりで持つ。保管先の行ID、パス、コミットは意味の同一性にしない（SEI Semantic Reference §2.1）。
4. **変換は製品の外に置く。** 書き出しの担い手を、CSWのランタイムにも、SUI/SEIの核にも置かない（`sibling-product-semantic-correspondence.md` §4 の未決事項と同じ立場）。
5. **署名とダイジェストは外側に付ける。** DSSE と RFC 8785 の考え方で、検証した同一バイトを適用側へ渡す。鍵の管理と信頼の根は範囲外とする。
6. **転送・配布は、既存の規約に任せる。** MCP の Resources、Agent Skills（記録を書く・読む手順の配布）、OpenTelemetry（実行の痕跡。記録からは `runRef` のように参照で結ぶ）は、記録の意味形式の代わりにしない。
7. **最小スキーマの原則**: 読めること（素のJSON、人が読める本文）、原文参照（版・範囲）、時点（有効時点と記録時点）、版（改訂は新しい版で、旧版は不変）、署名（任意、外側）、拡張（名前空間付き、未知は保持）、欠落は否定ではない。

## 7. 未確認事項と、設計上のオープンな問い

### 7-1. 未確認事項

- EU AI Act の条文は、公式のEUR-Lexからではなく非公式の閲覧サイトで確認した。第12条の見出し、第73条の各期限、第14条4項の列挙は、公式原文での再確認が要る。デジタルオムニバスの発効は、二次情報のみ。
- DMN の確定版の番号と、DMNが対象外とする範囲（仕様の記述）。取得できたのは「1.7 beta」の表示まで。
- GSN の要素の一覧（規格本文）、ISO/IEC/IEEE 15026-2（今回は調査していない）、SBAR、ランブック／ポストモーテム、DACI、エスカレーション手順の標準の一次出典。
- REFI-QDA の区間（選択範囲）の表現の詳細。CAQDAS各製品の内部モデル。
- ABP における「signpost」の位置づけ（RAND MR-114-A 本文）。
- OpenTelemetry GenAI の安定性の区分。
- Schmidt 2016 の収録書、Conklin & Begeman 1988 の巻号の細目、Toulmin の版元は、書誌の細目を確認していない。
- ForecastBench の Brier の値は、検索要約のため再確認が要る（位置づけ文書 §10-5 も同様の留意を置く）。
- SUI/SEI 側：SEI の `decision-memory.schema.json` と負例フィクスチャの内容、SUI の ADR-0085〜0088、`schemas_review_attribution.md`、`llm_escalation_policy.html`、`schemas.md` の未読部分。
- 三層（事実・予測・枠組み）の誤りに直接対応する既存標準は、確認できなかった。「仮説から事実への昇格」を定義した文献も、位置づけ文書 §10-5 のとおり確認できていない。

### 7-2. 設計上のオープンな問い

1. **原則(a)と(b)の緊張。** 語り直しの主体がLLMである以上、語り直しは自己申告になりうる。本書の暫定の解は「逐語引用と位置を含め、機械検査できる部分と、別の読み手の確認を要する部分に分ける」である。意味の忠実さの検査を、誰が・どの独立性で行うか。人間を使わない運用で、独立した読み手をどう確保するか。
2. **権限付与の対象。** エージェントの識別を、モデルID・版・構成のどこまでで束ねるか。モデル更新で付与は引き継がれるか、失効するか。
3. **時刻の第三者証明。** 事前登録の「登録した時点」を、誰が・どの仕組みで証明するか。外部の時刻証明サービス、公開レジストリ、署名付きの追記専用ログのいずれを許すか。
4. **採点の独立性。** 採点者と登録者を、どの軸（情報源・手続き・時点・権限）でどこまで分けるか。同一モデルの別インスタンスは独立とみなせるか（別モデルでも誤りが相関するという位置づけ文書 §10-1 の所見に照らして）。
5. **保留の「決めないことのコスト」の測り方。** 観測値、推定値、不明のいずれかを区別して持つ運用が、実際に回るか。推定値を後で採点する仕組みを持たせるか。
6. **価値・目的を、カードの役割とするか、別種とするか。** 優先順位の入れ替わりの検出が要るかで決まる。
7. **三層分類の妥当性。** 事実・予測・枠組みの三層で、判定の合意が取れるか。四層以上、または層の複合が要るか。
8. **「held」と権限の語の整理。** SUI/SEI のリポジトリ側の語彙を変えずに、交換形式の側で名前を分けるか。兄弟製品の正本は各リポジトリにあるため、変更は各側の判断になる。
9. **Profile による段階化。** どの影響・可逆性の水準で、どの項目を必須にするか（SEI の Progressive Explicitness に従う）。停止の閾値を誰が決めるか。
10. **範囲外の停止の記録を、規制の記録義務とどう分けるか。** 害の出る前の棄権の記録は、EU AI Act の重大インシデント報告の対象ではない（今回確認した範囲）。社内の記録として持つ場合の保存期間、開示範囲。

## 8. 出典一覧

確認水準：A＝仕様・原典ページを取得して項目を確認、B＝検索結果で書誌と要旨を確認（本文は未精読）。

| 番号 | 出典 | 水準 |
|---|---|---|
| W1 | W3C, "Web Annotation Data Model", W3C Recommendation, 2017-02-23. https://www.w3.org/TR/annotation-model/ | A |
| W2 | Hypothesis, "Fuzzy Anchoring". https://web.hypothes.is/blog/fuzzy-anchoring/ ／ "Robust Anchoring". https://web.hypothes.is/robust-anchoring/ | B |
| W3 | Nosek, B. A., Ebersole, C. R., DeHaven, A. C., Mellor, D. T. (2018). "The preregistration revolution." PNAS 115(11):2600-2606. doi:10.1073/pnas.1708274114 | B |
| W4 | W3C, "PROV-O: The PROV Ontology", W3C Recommendation, 2013-04-30. https://www.w3.org/TR/prov-o/ ／ "PROV-DM: The PROV Data Model". https://www.w3.org/TR/prov-dm/ | A |
| W5 | MADR 4.0.0（2024-09-17）. https://adr.github.io/madr/ | A |
| W6 | Nygard, M. (2011). "Documenting Architecture Decisions". https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | A |
| W7 | REFI-QDA 標準。https://dans.knaw.nl/en/file-formats/computer-assisted-qualitative-data-analysis-caqdas/refi-qda-qualitative-data-analysis/ ／ 公式 www.qdasoftware.org（本文は未取得） | B |
| W8 | Zittrain, J., Albert, K., Lessig, L. (2014). "Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations." 127 Harvard Law Review Forum 176. https://hls.harvard.edu/bibliography/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations | B |
| W9 | Klein, M., Jones, S. M., Shankar, H., Wincewicz, R., Nelson, M. L., Van de Sompel, H. "Robust Links - Specification". https://mementoweb.org/robustlinks/spec/ | B |
| W10 | RFC 7089 (2013年12月) "HTTP Framework for Time-Based Access to Resource States -- Memento". https://www.rfc-editor.org/rfc/rfc7089 | A |
| W11 | Center for Open Science, OSF Help: Registrations. https://help.osf.io/category/549-registration-and-preregistration-faqs ／ https://help.osf.io/article/152-withdraw-a-registration | B |
| W12 | Dewar, J. A., Builder, C. H., Hix, W. M., Levin, M. H. (1993). "Assumption-Based Planning: A Planning Tool for Very Uncertain Times." RAND MR-114-A. https://apps.dtic.mil/sti/pdfs/ADA282517.pdf（検索結果に表示。本文は未精読） | B |
| W13 | Kunz, W., Rittel, H. (1970). "Issues as elements of information systems." ／ Conklin, J., Begeman, M. L. (1988). "gIBIS: A hypertext tool for exploratory policy discussion." ACM Transactions on Information Systems（検索結果では 6(4)）。解説：https://en.wikipedia.org/wiki/Issue-based_information_system | B |
| W14 | Klein, G. (2007). "Performing a Project Premortem." Harvard Business Review 85(9):18-19. https://hbr.org/2007/09/performing-a-project-premortem | B |
| W15 | RAID ログの解説（実務解説サイト）。https://www.smartsuite.com/what-is/understanding-raid-logs-a-key-to-project-success ほか。権威ある標準の一次出典は未確認 | B（低） |
| W16 | Brier, G. W. (1950). "Verification of forecasts expressed in terms of probability." Monthly Weather Review 78(1):1-3 | B |
| W17 | Murphy, A. H. (1973). "A new vector partition of the probability score." Journal of Applied Meteorology 12:595-600 | B |
| W18 | Mellers, B. ほか (2014). "Psychological Strategies for Winning a Geopolitical Forecasting Tournament." Psychological Science 25(5):1106-1115 | B |
| W19 | Tetlock, P. E., Gardner, D. (2015). Superforecasting: The Art and Science of Prediction. Crown | B |
| W20 | Schmidt, J. (2016). "Niklas Luhmann's card index: Thinking tool, communication partner, publication machine."（収録書の詳細は未確認） | B |
| W21 | Ahrens, S. (2017). How to Take Smart Notes | B |
| W22 | Karger, E. ほか (2025). "ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities." ICLR 2025. arXiv:2409.19839. https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea74e45a229dac70b5b63b28d8934db6-Abstract-Conference.html | B |
| W23 | Groth, P., Gibson, A., Velterop, J. (2010). "The anatomy of a nano-publication." Information Services & Use 30(1):51-56. doi:10.3233/ISU-2010-0613 | B |
| W24 | Rogers, P., Blenko, M. (2006). "Who Has the D? How Clear Decision Roles Enhance Organizational Performance." Harvard Business Review. https://store.hbr.org/product/who-has-the-d-how-clear-decision-roles-enhance-organizational-performance/R0601D | B |
| W25 | OMG, Decision Model and Notation (DMN). https://www.omg.org/spec/DMN | A（版の表示は 1.7 beta） |
| W26 | Toulmin, S. (1958). The Uses of Argument（解説：https://www.ai.rug.nl/~verheij/publications/pdf/toulmin2005.pdf） | B |
| W27 | W3C, "ODRL Information Model 2.2", W3C Recommendation, 2018-02-15. https://www.w3.org/TR/odrl-model/ | A |
| W28 | Regulation (EU) 2024/1689（AI Act）第12条、第14条、第19条、第26条、第73条。閲覧：https://artificialintelligenceact.eu/article/12/ ほか（`/14/`、`/19/`、`/26/`、`/73/`）。非公式サイト。EUR-Lex https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 は見出しの確認に至らず。デジタルオムニバスの解説：https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ ほか（二次情報） | B |
| W29 | Turpin, M., Michael, J., Perez, E., Bowman, S. R. (2023). "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023. arXiv:2305.04388 | B |
| W30 | Starmer, A. J. ほか (2014). "Changes in Medical Errors after Implementation of a Handoff Program." N Engl J Med 371(19):1803-1812. https://psnet.ahrq.gov/issue/changes-medical-errors-after-implementation-handoff-program | B |
| W31 | Fowler, M. "Bitemporal History". https://martinfowler.com/articles/bitemporal-history.html | A |
| W32 | Kulkarni, K., Michels, J.-E. (2012). "Temporal features in SQL:2011." SIGMOD Record 41(3):34-43. https://sigmodrecord.org/2012/09/30/temporal-features-in-sql2011/ | B |
| W33 | Fowler, M. "Event Sourcing". https://martinfowler.com/eaaDev/EventSourcing.html | A |
| W34 | Alchourrón, C. E., Gärdenfors, P., Makinson, D. (1985). "On the logic of theory change: Partial meet contraction and revision functions." Journal of Symbolic Logic 50:510-530. doi:10.2307/2274239 | B |
| W35 | Argyris, C. (1991). "Teaching Smart People How to Learn." Harvard Business Review, May-June 1991 | B |
| W36 | Fowler, M. "Circuit Breaker". https://martinfowler.com/bliki/CircuitBreaker.html（Nygard, Release It! を参照） | A |
| W37 | McGregor, S. (2021). "Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database." AAAI 35(17):15458-15463. https://ojs.aaai.org/index.php/AAAI/article/view/17817 | B |
| W38 | OECD (2025). "Towards a common reporting framework for AI incidents." OECD Artificial Intelligence Papers No. 34. https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html | B |
| W39 | SCSC, "Goal Structuring Notation Community Standard, Version 3", SCSC-141C, 2021年5月. https://scsc.uk/scsc-141c | B |
| W40 | W3C, "JSON-LD 1.1", W3C Recommendation, 2020-07-16. https://www.w3.org/TR/json-ld11/ | A |
| W41 | OpenTelemetry, GenAI semantic conventions（移管先）. https://github.com/open-telemetry/semantic-conventions-genai | A（安定性は未確認） |
| W42 | Model Context Protocol, Specification（版 2026-07-28）. https://modelcontextprotocol.io/specification/latest | A |
| W43 | Agent Skills, Specification. https://agentskills.io/specification | A |
| W44 | Secure Systems Lab, DSSE envelope. https://github.com/secure-systems-lab/dsse/blob/master/envelope.md | A |
| W45 | RFC 8785 (2020) "JSON Canonicalization Scheme (JCS)". https://www.rfc-editor.org/rfc/rfc8785 | A |

RFC 7089 と RFC 8785 は著者名を確認していないため載せていない。題名・番号・URLのみを根拠とする。
