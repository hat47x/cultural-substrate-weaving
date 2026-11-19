# CSW × YI Constellation：開発実践からの認知方法改善とDSH適用研究

- 状態：**横断研究計画／CSW×YICの独立比較は未実施／製品要件・現行Skillへの採用なし**（2026-11-08策定、2026-11-19比較条件を再照合）。
- 目的：YI Constellation（以下YIC）の開発課題を、CSWが対象を捉え直す力を磨く実践的研究の場として使う。YIC側への貢献とCSW自体の改善を**別の成果**として観測する。
- 所有境界：CSWは認知方法と文化体系の読解、各YIC Productは仕様・意味・実装・検証、TAIは横断価値とHarness接続、OS/Hostは実効権限を担う。新しい共通Agent Loop、正本Store、Registry、権限機構を設けない。
- 適用範囲：本資料は**実験者向けの任意の計画**である。公開済みの執筆向け3 Skill、著者による採否、R-D固定4入力、通常の執筆フローは変更しない。CSWをYICの必須開発Gateや第七製品にしない。
- 主な接続先：[CSW研究マップ](CSW_MAGI_ASSUMPTION_CONTEXT_AND_EVIDENCE_MAP_20261029.md)、[Reframe研究](CSW_COGNITIVE_REFRAMING_RESEARCH_NOTE_20261101.md)、[縦断研究](CSW_MAGI_LONGITUDINAL_INSIGHT_AND_DELIBERATION_PROTOCOL_20261029.md)、[CSW #593](https://github.com/hat47x/cultural-substrate-weaving/issues/593)、[TAI #422](https://github.com/hat47x/tai-pleroma/issues/422)、[TAI #168](https://github.com/hat47x/tai-pleroma/issues/168)、[TEI #2509](https://github.com/hat47x/tei-platform/issues/2509)、[TEI #2899](https://github.com/hat47x/tei-platform/issues/2899)。

## 1. 双方向の改善。ただし自動的な相互昇格はしない

```text
YICの具体的な開発課題 ────────────────────────┐
       │                                    │
       ├── 通常の工学的検討 ────────────────┤
       │                                    │
       └── CSWの自由な生成的探索            │
                │                           │
         新しい区別・問い・関係・代案         │
                │                           │
                └────→ 独立した工学的照合 ←──┘
                            │
                 各Product Ownerの採否
                            │
                   実装・結果の観測
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
      YICでの改善                        CSWへの学び
    設計/実装/検証                    方法/技法/適用境界
          │                                   │
          └──── 次の実問題で限定的に再検証 ───┘
```

この図は作業内容の関係を表し、全案件へ強制する順序ではない。CSWを使わず通常の設計で解決できる案件は、そのまま進める。文化的体系は事実を保証する外部Authorityではなく、固有の意味・分節・関係を仮に動かすための認知資源である。

**三つの区別を残す。**

1. **CSWで着想を得たこと**と、**その着想に独立の設計上の価値があること**。
2. **YICが改善されたこと**と、**その改善がCSW固有の働きで生じたこと**。
3. **DSHでSkillをロードできたこと**と、**CSWの効果・三者協調・長期記憶が成立したこと**。

文化体系がなくても通常の一般的発想支援で同じ案に到達した場合、CSW固有の効果は未識別である。ただし、同じ結論へより少ない負荷で到達したり、重要な問いを早く発見したりする経路上の価値は、別に観測してよい。現行Skillの定型化や汎用化を先行させない。

## 2. YICでの導入先とOwner境界

| 領域 | CSWによる探索の具体例 | 正しさ・採否の所在 | 優先 |
| --- | --- | --- | --- |
| **TEI** | 共通Application Operation／Plugin Lifecycle図の欠けた経路、状態・時機・中間条件・複数関係を別の見方から発見 | TEIの型付き契約、独立Expected、実Provider/Host、Owner | 最初の合成read-only対象 |
| **SHO** | 原典・原稿・図面の関係、表現形式と理解の差、設計文書を変える問いを発見 | 文書内出典・Reader・保存再開、執筆者の判断 | 第二の移転検証候補 |
| **SUI** | 孤立した観察や異論、分類前の素材が見せる別のまとまりを探る | SUI自身の候補・提示・根拠復帰 | 観測できる差が生じた場合 |
| **SEI** | 問い自体を変え、競合仮説を分け得る次の観測を考案 | SEIのMethod、TEI等の実Source・Oracle・権限は各Owner | 認知的転用の比較候補 |
| **EKI** | 継続・中断・分岐・回復を異なる時間と関係から見直す | EKIの実行・Effect・回復・Receipt | 後続の安全な合成Case |
| **TAI** | 一つの手段への固定を外し、利用者が実際に選べる価値の構造を見直す | 価値研究と各ProductのOwner | 横断評価に接続 |

CSWにProductの仕様・認可・実行を肩代わりさせない。TEIの共通Application APIや既存Plugin Compositionの第二実装、SUI/SEIのMethod Engineの複製を要求しない。「YICで使えた」という説明を、現行3 Skillの執筆能力の実証へ転用しない。

## 3. 最初の実践課題：TEI read-onlyの構造的Reframe

**対象の固定**：TEIの既存Source・Application API・Plugin/Interaction Lifecycleのうち、秘密を含まない**公開の合成Fixture一つ**を選ぶ。初回は読取・設計検討だけとし、実DB変更、実業務Effect、Pluginの活性化、PRマージを対象にしない。TEI #3262のDesign Context Queryは設計・実装差を確認し、実在しないCommandやToolの成功を前提にしない。

**製品の現在地に合わせる**：[TEIの優先計画](https://github.com/hat47x/tei-platform/blob/main/plan/NOW.md)では「受注の一変更」を最優先とし、初回の操作は既存Ruleの修正でなく`unit_price_positive`の**新規追加**である。[TAI merged #779](https://github.com/hat47x/tai-pleroma/pull/779)は同じTaskをTool-onlyのB0として固定した。実PostgreSQL・実Chromeによる自動試験は進んでいるが、初回利用者による独力完走やOwnerの意味受理は未検収。CSWのCX比較はこの実User Jobから問いを選んでもよいが、最初は公開・合成Sourceに戻れるread-only設計課題に限定し、TEIの製品受入やTAIのB0試験を代行しない。

**事前に独立して準備するもの**：対象Revision、何を変えてよいか、何を変えてはならないか、既知の反例、独立のExpected、設計の判別に必要な最小入力、採否権限。最終採点語・手製の正負例は生成側へ前置きしない。探索用の広い問題文と、検証者側のOracleを分ける。

**生成側に許すこと**：文化体系の固有な区別や意味を探索へ大胆に使う。元のモデルにない経路や状態を仮説として生成する。途中で生じた別の問いや、既存の図に置けない残差も扱う。説明のための比喩を使ってよいが、その比喩からTEIの実装済み機能や権限を推認しない。

**検証側が見ること**：新しい問いが実際の図・API・テストに存在する未説明条件を発見したか。対応する負例は独立の材料で検証可能か。既知の不変条件を破ったか。単なる一般語や記号対応だけを増やしたか。次の検証可能な一手が生まれたか。

### 最初に実行する一件：製品Studioの未審査候補（CX-P1、未実施）

最初のCX比較は、抽象的なPlugin全体ではなく、**すでに製品画面で操作できた一つの候補を、実際の変更として保存するには何が必要か**に絞る。TEI [merged #5669](https://github.com/hat47x/tei-platform/pull/5669)では、生成したWindows Wailsの実WebView2で、`studio.inspection_response.snapshot_fingerprint` の必須指定について、Host Catalogからの選択→Inspect→候補ボタンの実クリック→型付きJSONの表示→Workspace切替後の候補失効を一つの試行で確認した。一方、CodeMirrorはread-onlyで、Source byteは不変、製品内のAccept／Save UIはない。これは**候補を操作できたという実証**であって、製品Studioからの書込やセルフビルドの完了ではない。

**実行前に固定する材料**：TEIのその時点の対象コミット、`cmd/tei-studio/test/desktop_webview_smoke.py`の該当箇所、[製品の優先計画](https://github.com/hat47x/tei-platform/blob/main/plan/NOW.md)のStudio段落、対象と二つの公開・合成Workspaceの版。TEIの既存試験が何を確かめたかは、生成者にも全条件共通で渡す。一方、評価者が事前に選んだ独立Expected・未公表の負例・他条件の回答は渡さない。実行時に新しいmainを使う場合は、対象と証拠を改めて固定し、古いCIの成功を新しい版の成功に読み替えない。

**三条件に共通する問い**：「この未審査候補を、利用者が正式に保存した変更として扱えるようにするには、現状の実装と試験に照らして何を確かめる必要があるか。今ある説明の言い換えではなく、次に実行すると区別がつく問いや試験を提案してください。今回はソースコードを変更しません。」

- **CX0**：通常の工学的な設計検討。**CX1**：同じ材料と予算で、文化体系を使わない一般的な発想支援。**CX2**：現行CSW本文を実際に読ませ、文化体系を使うかどうかも含めて自由に探索する。文化体系名・象徴・「三者会議」を生成時の必須項目にしない。
- **観測**：三条件それぞれの実際の入力、読めたSource／Skillの本文、出力全文、未解決の問い、かかった時間・費用、回答に含まれる誤認を残す。DSHを使う場合も、同じrootからforkした別Sessionを独立反復に数えない。現行の実隔離資格がなければ、公開・合成資料を用いる同一環境内の比較に限定し、DSHのH2/H3有効性を主張しない。
- **生成後に独立して読む**：TEI #5669で既に確認済みの性質を言い直しただけか、それまで未検証の境界を**既存のSource／Operation／テストで確かめられる問い**へ変えたか。正規のReview／Accept／Source保存・再読込と、単なるPreview／旧候補の失効を混同していないか。新しいWriter・Host・Registryの追加を当然視していないか。良い問いでも、Ownerにとっての採用価値と実装結果は後で別に確認する。

**出口**：CX2に追加価値が見えなければ、その結果を残し、Skill改訂を行わない。発見があれば、TEIの既存[#4583](https://github.com/hat47x/tei-platform/issues/4583)のOwnerに**一つの検証可能な問い**として返す。CSW側は、その問いが文化体系のどの意味・関係・操作から生じたかを遡れる場合に限り、[#593](https://github.com/hat47x/cultural-substrate-weaving/issues/593)で執筆への移転可能性を検討する。実際の三条件生成、独立評価、Owner採否はまだ行っていない。TEIの「受注の一変更」初回利用者検収やStudioの製品保存を、この研究で止めない。

### 初期の判別カード（合成・未実行）

| Case | 二つの説明／反例 | 正しい研究上の扱い |
| --- | --- | --- |
| CY-01 経路差 | 最終状態が同じでも、途中の不可逆Effect／Grant／再読込有無が異なる | 同じ終状態を同じ実行保証としない。文化体系の「経路」の見方が新たな検証対象を発見したか調べる |
| CY-02 欠けたノード | 図にない状態が本当に未実装か、表示・取込・Scopeだけで欠けているか | 欠落を即時に不存在と断定しない。有限なRequired集合の検証はTEIで行う |
| CY-03 偽の新規性 | CSWの専門用語を除くと、CX1の通常批評と同じ問い・修正しか残らない | 「固有増分なし／まだ識別できない」も有効な結果とする |
| CY-04 過剰な類推 | 易の遷移などの構造から、元Sourceにない認可や業務意味を断定する | 生成仮説と契約判断を分離し、独立Expectedで反証する |
| CY-05 問いの転換 | 元の「どのPluginを選ぶか」から「選択が変更されたとき実際に何が再資格化されるか」へ移る | 問いが変わった事実と、その変化が設計に役立ったかを別に記録する |
| CY-06 何も使わない | CX0の既存設計で反例が解決し、CSWを起動しないほうが余計な作業が少ない | 不使用をCSWの失敗とも成功とも自動判定せず、適用条件を学ぶ |

## 4. 方法の効果とHarnessの効果を別の軸で比較する

**CSWの認知方法の軸（CX）**を先に比較する。`CX0/CX1/CX2`はこの研究計画内だけの条件名であり、TAIのSkill選択や外部Harnessの条件名とは異なる。可能な範囲で同じモデル、生成予算、公開Fixture、Tool能力、時間・権限条件を固定する。

- **CX0：通常の設計・レビュー**。一般の生成AIと既存工学手法。
- **CX1：一般的な発想支援・独立批評**。CSW原典・技法を使わず、検討時間と追加レビューの効果を対照する。
- **CX2：現行CSW Skillを用いた探索**。まず文化的体系Skillを必要な部分だけ使用し、親和図法とwriting-flowは用途に応じて任意利用。どの本文・参照節を実際に渡したかを観測する。

比較するのは**認知方法の追加価値**である。CX0/CX1にはCSW本文・評価者だけが持つ採点基準・他条件の生成結果を事前に見せない。製品Tool、Source、入力版、実行予算、許可された情報範囲は揃え、違いが残る場合は明示する。全Skillを常時読み込むことや、複数の認知方法を同時に変更することは避ける。

CX0/CX1/CX2で**実際の問題解決・反例の発見・設計の具体性・採否・誤判断・作業費**を分ける。単に候補数が多いこと、文章が魅力的なこと、別AIが高評価したことを成果の代用にしない。少数試行は探索的であり、一般的な因果効果・有意差を主張しない。できればモデル実行と盲検評価を異なる文脈・担当に分け、順序・再試行・設定を記録する。

**TAIのB0/B1/B2と混同しない（11月19日再照合）**：[TAIのSkill構成計画§59](https://github.com/hat47x/tai-pleroma/blob/main/docs/yi-constellation/harness-skill-plugin-plan-2026-11-02.md)では、`B0`はTool-only（Skillなし）、`B1`はProduct Skill追加、`B2`は必要な場合の横断Skill利用を比較する。一方、本計画の従来のB0/B1/B2は通常設計・一般的発想支援・CSWによる探索という**認知方法の比較**だった。同じ記号でも目的と試験条件が違うため、今回から後者をCX0/CX1/CX2と呼ぶ。CX2をTAIのB2として集計したり、TAIの採点器へCX群の結果をそのまま入力したりしない。[TAI merged #775](https://github.com/hat47x/tai-pleroma/pull/775)では`B0/B1/B2`以外（`b0`やHarnessの`H2`など）を理由付き未採点にする合成回帰が統合されている。別研究間の対応付けは、同一Task・実Tool・Skill配信と独立Expectedが確認された場合に限る。

**独立試行と開示の確認**：[TAI merged #778](https://github.com/hat47x/tai-pleroma/pull/778)は同一`caseId`・`arm`の重複記録を未採点にする合成検査であり、独立Attemptを実証したものではない。CXでも同じ結果の再掲を反復試験に数えず、入力版・実Attempt・露出条件と生成全文を照合する。[TAI merged #776](https://github.com/hat47x/tai-pleroma/pull/776)・[#777](https://github.com/hat47x/tai-pleroma/pull/777)は評価レポートに秘密を再掲しないための限定修正である。元Trial、Tool Reply、実Network送出は別の機密境界なので、私的な原稿や秘匿Expectedを公開研究記録へ転記しない。

**既知の負例から引き継ぐ判定の境界（CSW旧v39／DG研究との接続）**：[CSW交差研究 §20](CSW_MAGI_CROSSING_RESEARCH_DESIGN.md)の旧アブレーションでは、**文化体系ではなく直接関係文法（DG）を渡しただけでも主要な発見の多くが得られた**。また[同§21](CSW_MAGI_CROSSING_RESEARCH_DESIGN.md)の旧v39では、対象に適合しない体系の**native operationを強制**した条件が、事前登録評価で不支持だった。したがって、YICの**CX2がCX1より良い**場合でも、まず「既存の工学的区別を言い換えたのか」「一般的な関係文法や追加の資料・推敲だけで十分か」を確認する。CX0/CX1/CX2が識別するのは初めは**CSWを含む支援方式全体の増分候補**であり、**文化体系固有の因果寄与そのものではない**。本当に必要になった場合だけ、同じ情報量・実行条件の限定的なDG対照を**別世代の研究**として検討する。逆にCX2が不利でも、強制された体系操作・読込量・対象不適合を区別し、「文化的な着想を任意に開くことまで有害」と一般化しない。固定R-D、通常の執筆Skill、既存のCX0/CX1/CX2初回条件は変更しない。

**Harnessの軸（H）**は別に扱う。H2（外部Toolのみ）とH3（同じTool＋Skill実Load）を同じ問題で比較するが、CX2の探索方法の効果とDSHのTool transport／Skill deliveryの効果を一つの「DSHが良い」に畳まない。初回にCX×Hの全面直積実験を課さない。

- **実Skillの読み込み**は「配置した」「検索候補に現れた」「Toolで本文を受領した」「回答で実際に参照した」の観測境界を分ける。最後の段階の内部因果利用は外形から証明しきれない。
- **Toolの事実**は「実Tool起動」「Requested」「Returned」「Harnessが受領」「Consumerへ提示」「回答の根拠に使った」を区別する。56 Call／55 Resultのような欠落を正常完了の一語で隠さない。
- **比較割付**は事前に固定した独立Session・同一Task・同一Source/Tool許可・同一Model条件を確保する。過去の探索Sessionを後から正式対照へ編入しない。**Session IDが別でも入力文脈が独立とは限らない**。[TEI merged #3745](https://github.com/hat47x/tei-platform/pull/3745)で、DSHの親Turn完了後にforkした子Sessionの初回モデル要求へ親の合成Canaryが継承される限定実測がある。各セルを独立rootで開始することを優先し、Nativeのroot／seed／inherited event／実際にモデルへ渡った事前文脈を可能な範囲で照合する。親IDが空でも独立性の証明にはならない。[TAI merged #649](https://github.com/hat47x/tai-pleroma/pull/649)のSK-02合成82ケース成功は判定器の回帰であり、実隔離やCSW試験の成功ではない。
- **実効安全性**は許可Read成功だけでなく、禁止Readの**OS/Process上の拒否**、Network／Log／Telemetry等の送出経路、権限の現行性を観測する。合成・非機密の閉域試行を先行させる。未証明の外部送出安全性を前提に私的原稿・Token・秘密SourceをDSHへ渡さない。

**ローカル保存面の限定実測をCSWへ接続（2026-11-13、CSW側試行はNOT RUN）**：[TEI #2515のH6-E6記録](https://github.com/hat47x/tei-platform/issues/2515#issuecomment-6715885926)・[merged Evidence PR #3309](https://github.com/hat47x/tei-platform/pull/3309)では、DSH 0.2.2-rc.1／Windows／headless／read-onlyの**合成Canaryを実Toolで読んだ1 Session**に限り、headless stdoutとローカル永続`session.v4.jsonl.zstd`の`tool/result`に同じCanaryが残った。Sessionファイルは**連結9 zstd frame**で、最初のframeだけ展開すると内容を見落とす。局所調査した`storages`・`cache`・`attachments`では当該Canaryが見つからなかったが、全Sink・別SessionからのRead・削除／保持期間・暗号化・外部Providerへの実送出は**未確認**である。

この観測を、**実際のTool受領／ローカル永続保存／HTTPやModelへの送出／別Readerへの実効Read可否**を分けて扱う根拠とする。Session Log拡張のHTTP設定を無効化しても、ローカル保存の消失を証明したことにはならない。通常のCSW執筆に新たな検査を義務化せず、外部Harnessへ**非公開原稿・著者の作業記録・秘密Source**を渡す場合だけ、利用するHost・Profileで実効のアクセス範囲と保存面を別途確認する。未確認なら公開・合成材料の探索にとどめ、機密を渡して安全性を試さない。これはCSW×DSHの品質・安全性を新たにPASSとするものではなく、G0/G1等の既存Harness/OS Ownerの確認を再利用する。CSW独自のLog Store、削除機構、Runtime Gateを作らない。

**成果を渡すことと旧Sessionを見せることを分ける（2026-11-14、後続研究案・NOT RUN）**：[TAI #234の複数UI設計](https://github.com/hat47x/tai-pleroma/issues/234#issuecomment-6856979920) と[Draft #648](https://github.com/hat47x/tai-pleroma/pull/648) は、**現在の資料・成果の開示／Activityの限定引継ぎ／同じNative Sessionの過去履歴の閲覧／複数UIからの同時操作**を別資格として扱う。CSWの具体例では、著者がMAGIとの非公開の試行錯誤から選んだ一場面を編集者へ見せてよい場合でも、当該Sessionの**不採用案、元の非公開原稿、旧Tool結果、著者がまだ明示していない判断**まで見せてよいとは限らない。成果本文の引き渡しは、旧Transcriptの全体開示と同じ行為ではない。

**後続CSW×Harnessの扱い**：現時点のRecipient/Scopeで新しい本文を渡せることと、旧Sessionに残るすべての内容をそのRecipientが読めることを区別する。旧履歴の閲覧資格を実Hostで確かめられない場合、Live Sessionの共有を成功と扱わず、**必要な目的・許可された成果・未決事項だけを選択的に新Sessionへ受け渡す**方式を比較候補とする。複数画面から同じSessionを操作するなら、実Native Turnの帰属・直列化・遅着の確認はさらに別であり、編集者の閲覧許可を著者の採否・書換え権限へ拡張しない。これは**CSWの新しい権限正本・Activity Store・二画面機能の実装要求ではない**。既存のProduct/TAI/Host Ownerの証拠へ帰属させ、通常の執筆と固定R-Dには追加Gateを設けない。複数UIの実接続・許可外閲覧拒否・共同操作・CSWの著者受理は **NOT RUN**。

**確認済みのDSH基線（2026-11-07、CSWの実証ではない）**：TEI #2509／TAI #168の4 Session資料により、H3-A/Bでは同一5,482 byteのProduct Skill本文と参照7,710 byteのTool Readが発生した。一方H2-Aは既存h2-08 Sessionの再利用で、4件を事前独立割付した比較ではない。**比較適格0/4、CSWを使ったCX0/CX1/CX2試験はNOT RUN**。この限定実績を「CSW×DSHの効果」へ流用しない。

DSH公式のCordis／Profile／Bundle／patch／headless・sdk-minimal構成は**実験環境の候補**であり、CSWの認知方法の保存先ではない。版、Profile実効構成（例：`--dump-config`）、Skill実byte、許可Tool、Host/OS条件を実行時に固定する。専用Cordis Pluginは、Skillテキストと既存Profile／Toolで不足する**反証可能な具体的能力**（実Skill受領の可観測性、試行分離、必要なTool結果の保全など）が明らかになったときだけ比較する。CSWの恒久的なAgent Loopや専用永続Storeを先に作らない。

**ハーネス選択はベンダー中立とする（2026-11-19補足）**：DSHを技術的に先行させるのは、OSSとしての実装検査のしやすさとTEIのPlugin構想との親和性による。YICの利用者向け契約・Skill・成果の採否は、DSHのProfile／Native Session形式に依存させない。[TAI merged #730](https://github.com/hat47x/tai-pleroma/pull/730)ではCodex非対話JSONLの最小Adapterと合成契約テストが加わったが、実Codex起動・TEI MCP往復・SkillやSession再開の対応は未実証または未対応である。DSHとCodexを同等の**実能力が実証済み**とせず、利用可能なCapabilityと不支持時の縮退を明示して比較する。

## 5. CSW自身へ何を持ち帰るか

製品での成功を自動的にSkill改訂と呼ばず、次の**原因候補を競合させる**。

| 観測 | 見直す先 | 早まってはいけない結論 |
| --- | --- | --- |
| 実用的な新しい関係が見えた | 文化体系のどの原典のどの意味・操作が効いたか、CSW #593の「体系→技法→実作」の単位で読む | その体系全体を常用推奨する |
| 良い問いは出たが採用されなかった | 適用範囲・残差・採否の理由を確認 | 不採用＝無価値 |
| CX1と差がない | 文化固有操作、読む量、生成経路の必要性を検討 | 体系固有の効果が実証された |
| 語が増え、反例や設計が改善しない | 技法の「元対象への還元」と文章中のノイズを減らす | 詳細化すれば自然に良くなる |
| 原典の取り違え／無根拠な権限主張 | 出典と探索仮説の区別、後段の独立検証 | 生成段階全体へ停止Gateを設ける |
| Tool受領漏れ・未読込・Scope差 | Harness・YIC適用層の実配信／実Source／権限を修正 | CSWの認知方法が悪かった |
| 本文変更後だけ改善／悪化 | 実際に渡したSkill版、入力、モデル、評価条件を再照合 | 単一の成功例で現行3 Skillの標準手順を変更 |
| 後日同じ問いが出た | 保持・検索・再提示・再生成を区別するR-C研究へ | 永続記憶が働いた |

改善候補は、**観測した対象差分 → 方法上の競合仮説 → 別条件の反例 → 必要なら技法の小変更 → 独立再試行**として扱う。採用されればSkillの必要箇所へ短く戻し、詳細な作例は参考資料へ置く。変化が観測されない場合は改訂を増やさない。

YIC固有のPlugin/API/Role/OS用語をCSW本体に持ち込む必要があるとは限らない。領域の違いを保ったまま再利用できる操作（例：位置の意味の読解、経路・時機・主体の差、対象にない関係の発見）を取り出せた場合だけ、執筆でも意味のある形で再表現する。逆に、文化体系を離れた一般的なデバッグ手順はYIC適用層へ置く。

## 6. 最小の証拠と再資格化

日常利用の新SOP・全発言ログ・固定記録Schemaは不要。ただし、研究と称して比較する**その試行に限り**、再解釈できる最小の外部観測を残す。

| 観測対象 | 残すもの | 独立して判定するもの |
| --- | --- | --- |
| 入力 | 対象Source/Revision、Task、生成側への実配信本文、権限Scope | DeclaredとActual Deliveredの一致 |
| 実行 | Harness/Model/Profile/Skill/Toolの実版、Session ID、再試行と欠落 | Toolの起動・Reply・実受領・越境拒否 |
| 探索 | 外在化した新しい問い、候補、異論、未決、引用先 | CX0/CX1/CX2の差と独立資料との関係 |
| 結果 | Ownerの採否、設計差分、独立Expected、後続実装・実Effectの有無 | 採用と実証と実行を混同しない |
| 縦断 | 後日の新材料、旧候補の保存／検索／提示／採否 | 旧Sourceの資格・実記憶と偶然の再生成を混同しない |

保存されない候補、検索されない候補、提示されない候補、採用されない候補は異なる。不完全な観測から「異論なし」「有益な候補なし」「忘れた」を導かない。同一Sourceと同一LLMの三役出力を独立Evidenceの三票として加算しない。課題ごとの対象集合・可視性・新旧Revisionが変われば、成立範囲を再照合する。非公開原稿・個人情報・Secret・raw Tool応答はPublic GitHubへ置かず、公開できる抽象化された知見と実記録を分離する。

## 7. 実施順序と小さな受入条件（CSW×YICの新規実験はNOT RUN）

| 段階 | 最小の作業 | 次へ進める条件／不成立時 |
| --- | --- | --- |
| **M0：Source確定** | 現行CSW 3 Skillと必要な参考節、対象TEI合成Revision、既存のOwner/Issueを固定 | どの本文を誰が読んだか区別可能。研究票だけ増やして実課題を失わない |
| **M1：Harness基線** | TAI #168／TEI #2509の適格な独立H2/H3、実OS拒否、送出/Replyの確認を再利用 | 比較適格なSlotがなければHarnessの優越性を主張せず、CSWのB比較は別の同一環境で可能な範囲に限る |
| **M2：TEI一課題** | まず§3のCX-P1一件でCX0/CX1/CX2を比較する。CY-01〜06は採点項目を増やすためではなく反例を読む手掛かりとする | 実際の回答と独立Expectedを照合し、追加価値なし／誤認／有用な問いのいずれも残す。Owner受理なしにTEI仕様化しない |
| **M3：移転試験** | SHOの文書改稿、またはSEIの問いに相対的な次の観測へ、**同じ認知操作**を限定移転 | TEIだけで有効な開発技法と、異領域でも働くCSW操作を区別 |
| **M4：方法改訂** | 効果に寄与した操作・失敗条件を研究ノートとCSW #593に戻し、必要な場合だけSkill本文の小差分をDraft化 | CX0/CX1との再試行と執筆上の妥当性を見ないまま標準昇格しない |
| **M5：縦断** | 後日新しい実材料で問いがどう再活性化されたか、著者／Ownerの採否を別途観測 | 初回セッション内の自己参照を長期学習と呼ばない |

**優先順序**は、既存CSW研究のR-D固定4入力・独立モデル生成の先行を変更しない。YICの探索的M0/M2は、R-Dへの入力や判定条件の混入を避けて別枠で実施できる。R-A（文化体系固有効果）、R-C（後日の問い）、R-B（三者協調）を一回のYIC実験で一括実証しない。YIC向けの三者役割は、将来の任意研究条件であって現行三Skillと一対一には対応しない。

## 8. 採用・不採用の判断条件

- **継続する**：通常経路にない判別的な問い、反例、構造変化が生まれ、少なくとも一つが独立のSourceやOwner判断へ接続した。
- **保留する**：新規性がCX1と区別できない、Tool実配信が不明、対象の独立Expectedが弱い、適用先の実Sourceが欠けている。
- **縮小する**：追加Skill／Cordis Plugin／多Agent運用の負荷が、得られた成果を上回りそうなとき。必要な一部だけを使う。
- **導入しない**：通常の工学的検討で十分であり、CSWによる改善または認知研究上の識別可能な問いがないとき。

どの判断も、探索そのものを禁止する製品規則ではない。一般的なコストや性能の数値は実測まで推定値と明記する。

## 9. 関連する実行環境・計画

- DSH公式：[Architecture](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)（Cordis、Profile、Bundle、可逆登録、構成確認）。実際の使用時に版を固定し、公式の安全上の注意とOS/Host適合を確認する。
- YIC共通Harness： [TAI #168](https://github.com/hat47x/tai-pleroma/issues/168)、[TAI #232](https://github.com/hat47x/tai-pleroma/issues/232)、[TAI #422](https://github.com/hat47x/tai-pleroma/issues/422)、[TAI #488](https://github.com/hat47x/tai-pleroma/issues/488)。CX比較の成果は既存の横断価値レビューへ返す。ただしTAIの`B0/B1/B2`採点器とは別の研究条件とし、第二の横断Owner／評価基盤を作らない。
- TEI： [#2509](https://github.com/hat47x/tei-platform/issues/2509)、[#2515](https://github.com/hat47x/tei-platform/issues/2515)、[#3262](https://github.com/hat47x/tei-platform/issues/3262)、[Draft #3515](https://github.com/hat47x/tei-platform/pull/3515)。H2/H3・Design Context Query・Independent Expectedの既存Ownerに証拠を返す。
- CSW：現行の3 Skillの開放的な探索と執筆を優先する。[R-D初回固定入力](CSW_MAGI_RD_FIRST_RUN_INPUTS_20261102.md)は変更しない。**今回の確定成果は責務境界と反証可能な比較計画の整理まで。CSW×YIC効果、実DSH適用、Ownerによる採用、Skill改善の実証はNOT RUN。**


## 10. 11月19日の横断再照合：実際の対象への往復を中心にする

**研究上の更新であり、CSWの実使用・独立評価・YICの正式受理はNOT RUN。** [TAI merged #648](https://github.com/hat47x/tai-pleroma/pull/648)が整理した、Activityの引継ぎ、Native Sessionの再接続・履歴閲覧、Product Operationの再開は別の仕事である。CSWでも「前の問いを引き継ぐ」「同じ会話を再開する」「元資料を実際に読み直す」「生成案を現行の成果物に適用する」を同じ成功と数えない。TEIのセルフビルドと[TAI #168](https://github.com/hat47x/tai-pleroma/issues/168)の隔離された外部Harness比較は引き続き独立した優先作業であり、CSWはどちらにも新しい必須Gateを追加しない。

### 一つの対象を用いた最小の往復（次の比較候補）

1. **対象へ戻る**：公開・合成TEIの一つのSubjectとそのSource Revisionを固定し、現在のread-only Reader／CLIが本当に読んだものを確認する。画面上の選択文字列や古い会話の記述だけで、実対象が存在し続けると決めない。[TEI #4597](https://github.com/hat47x/tei-platform/pull/4597)のPin負例では、Workspace A→B→Aに戻ってもCatalog・Model Revision・World／Source Index Fingerprintが異なれば再Pinが必要である。これはPinの保守的な局所検査であり、Source意味の完全同一性や現在Grantの証明ではない。
2. **問いを育てる**：既存のCX0／CX1／CX2で、一件の実際の設計上の問いから新たな関係・代案・負例が得られるかを比較する。文化体系の名前や候補数ではなく、元の契約に戻ったとき新しく判別できることを重視する。旧v39／DGの負結果を保持し、文化体系固有の増分を先取りしない。
3. **選択的に届ける**：CSWの候補や未決を別のUI・編集者・Harnessへ渡す場合、対象の現在のScope・開示資格と、渡す成果本文の範囲をその時点で確認する。旧Native Sessionの全Transcript・不採用案・Tool結果の閲覧資格まで拡大しない。受け渡し先が現行Sourceを自分で読み直したことと、引用・要約したPayloadだけを受領したことは別の観測である。
4. **結果から学ぶ**：修正の提案、Ownerの採用、実際のファイル差分、実Providerの結果、執筆者の選択を別々に記録する。著者がAI案を採用しても元案の由来は変わらないが、著者自身による実質的な改稿まで元AIの出力と同一視しない。[CSW merged #600](https://github.com/hat47x/cultural-substrate-weaving/pull/600)のMAGI研究で明確になった区別を用い、新しい帰属SchemaをCSW本体へ課さない。

### SUI Canvasの候補は実装決定ではない

[SUI #3400](https://github.com/hat47x/sui-sensemaking/issues/3400)の価値研究と、[CSW PR #599](https://github.com/hat47x/cultural-substrate-weaving/pull/599)の**未マージで閉じた提案**は、AIが提示する候補と人間の配置・保留・訂正を往復させる構想の参照先である。現時点でCSWの標準経路や既存計画の正式な次工程として扱わない。まずSUI自身のread-only投影・選択の同一性・元材料への復帰が確認できた範囲で、CX0/CX1/CX2（認知方法）とCanvas有無（UI）の**別の差**を探索する。Native Session共有と実書込みはさらに後続の別資格とし、CSWの比較や初回DSH四Slotの前提にしない。

**本節を追加したことによって実証済みになったのは何もない。** 次の情報増分は研究票を増やすことではなく、一つの公開対象での実Source読取、実際の生成と回答全文、独立した比較・採否、または既存G0/G1/G2の実隔離・送出・Replyの結果から得る。実行の記録がない項目はNOT RUNのまま保持する。
