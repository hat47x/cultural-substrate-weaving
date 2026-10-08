# 認知(6)「連続して存在する」に関する調査

調査日: 2026-10-06。方法: Web検索で書誌情報と要旨を確認できたものだけを「確認済み」として載せた。確認できなかった点は「未確認」と書いた。要約はすべて自分の言葉で書いており、本文の転載はしていない。数値は検索結果に出ていたものに限る。

## 0. 要約

1. 連続性の失敗は、記録がないことよりも、記録はあるが再開に必要な形をしていないことで起きる。引継ぎ研究(Arora 2005)が示した失敗の中心は、内容の欠落(薬、未解決の問題、保留中の検査)と、対面のやりとりがない運用だった。
2. 引継ぎを構造化すると誤りが減るという実証がある。I-PASS(Starmer 2014)は、医療ミスの率を24.5から18.8件/100入院に、予防可能な有害事象を4.7から3.3件/100入院に下げた。
3. LLMエージェントの長期実行では三つの限界が確認できる。第一に、長い文脈で性能が不均一に落ちる(Liu 2023、Chroma 2025)。第二に、セッション間の記憶がない(Anthropic 2025)。第三に、記憶を足すこと自体が誤りを増幅する(Xiong 2025)。
4. 時間付き知識グラフ(Zep)や bitemporal(Fowler)は、「いつ事実だったか」と「いつ知ったか」を分けて持つ設計として使える。「後勝ち(latest-wins)で上書きする」方式の代替になる。
5. AIの「同一性」は、モデル(重み)・担当(役割)・記録(系譜)の三つに分解して扱うのが妥当だと考える。責任は法人格ではなく、記録を持つ人間または組織に帰属させる議論が優勢である(Bryson 2017、Chesterman 2020)。
6. 仮説(6)は「連続して存在する」から「再開できる形で、判断の系譜を保つ」へ書き換えるのがよい。欠けている認知の候補は「引き継がれた前提を疑う(前提の失効検知)」と「権限・責任の境界を知る」である(第7節)。

## 1. 組織記憶と知識の継承

### 確認済みの出典

- Walsh, J. P., & Ungson, G. R. (1991). Organizational Memory. Academy of Management Review, 16(1), 57-91. 組織記憶に関する最初の統合的な枠組みとされる(Waikato大学のリポジトリなどで書誌確認)。記憶の「保管庫」を複数に分けて論じた論文として広く引用される。保管庫の具体的な内訳(個人、文化、変換、構造、生態、外部文書)は私の記憶によるもので、今回の検索では内訳までは確認できなかった。内訳の使用前に原文で確認すること。
- Argote, L., Beckman, S. L., & Epple, D. (1990). The Persistence and Transfer of Learning in Industrial Settings. Management Science, 36(2)(検索結果に頁140-154とあるが、リンク先DOIの頁表記が食い違うため頁は要再確認)。製造現場で、生産から得た知識が急速に目減りすることを示した。累積生産量という従来の学習指標は、学習の持続を過大に見積もる、という結論である。担当や時間が変わると、蓄積した知識は自動では残らないことの実証的な根拠になる。
- Argote, L., & Ingram, P. (2000). Knowledge Transfer: A Basis for Competitive Advantage in Firms. Organizational Behavior and Human Decision Processes, 82(1), 150-169. 知識移転を促す要因と妨げる要因を整理した。
- Argote, L., & Miron-Spektor, E. (2011). Organizational Learning: From Experience to Knowledge. Organization Science, 22(5), 1123-1137. 経験が文脈と相互作用して知識になるという枠組み。知識の生成、保持、移転を分けて扱う。
- Argote, L., & Ren, Y. (2012). Transactive Memory Systems: A Microfoundation of Dynamic Capabilities. Journal of Management Studies, 49(8), 1375-1382. 誰が何を知っているかを集団で符号化、保管、検索する仕組みとして transactive memory を位置づける。
- Wegner, D. M., Giuliano, T., & Hertel, P. (1985). Cognitive interdependence in close relationships. In W. Ickes (Ed.), Compatible and Incompatible Relationships (pp. 253-276). Springer. transactive memory の原典。また Wegner, D. M. (1986). Transactive memory: A contemporary analysis of the group mind. In Mullen & Goethals (Eds.), Theories of Group Behavior (pp. 185-208). Springer。
- Lewis, K. (2003). Measuring transactive memory systems in the field. Journal of Applied Psychology, 88(4), 587-604. doi:10.1037/0021-9010.88.4.587. 専門分化、信頼性、調整の3次元15項目の尺度。
- Nonaka, I. (1994). A Dynamic Theory of Organizational Knowledge Creation. Organization Science, 5(1), 14-37. 暗黙知と形式知の対話で組織の知識が生まれるとする。SECI(共同化、表出化、連結化、内面化)は、この論文を土台に Nonaka と Takeuchi が展開した(検索結果の記述による)。

### 本調査への含意(私の解釈)

- Walsh & Ungson の観点では、記憶は文書だけにあるのではなく、人、手順、構造にも宿る。担当が替わると、文書に出ていない部分(誰に聞けばよいか、何が暗黙の前提か)が落ちる。CSWの「系譜」は、文書側の保管庫しか担わない。人に宿っていた部分をどこまで外に出せるかが限界になる。
- Wegner と Argote の transactive memory は、「誰が何を知っているか」のメタ知識が記憶の中核だと言う。SEIの「担当・権限」の区別は、このメタ知識の外部化に相当し得る。LLMの担当やモデルが替わるときは、「前の担当は何を知っていた(知らなかった)か」の記録が要る。
- SECI の表出化(暗黙知から形式知へ)は、親和図法の深いラウンド(A型図解、B型文章化の往復)と対応づけやすい。ただし、SECI が「内面化」を循環の必須段階に置く点は注意が要る。LLMには人と同じ意味の内面化がないため、次回の再開時に毎回「読み直す」コストを払う設計になる。これは設計上の前提であり、既存研究で確かめられた事実ではない。
- 暗黙知の継承失敗については、製造業の学習の目減り(Argote 1990)以外に、今回の調査で直接の実証を追加確認できていない。Nonakaの理論は概念枠であり、失敗率を測った研究ではない。

## 2. 決定記録(ADR、決定ログ、議事録)

### 確認済み

- Nygard, M. (2011-11-15). Documenting Architecture Decisions. Cognitect blog. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions 。ADRの出発点。書式は、題、背景(Context)、決定(Decision)、状態(Status: 提案、承認、廃止、置換)、帰結(Consequences)。
- Fowler, M. Architecture Decision Record (bliki). https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html (検索で存在確認。内容の詳細は未取得)。
- 「知識の蒸発(knowledge vaporization)」は Jansen と Bosch が提唱した概念で、設計判断の理由が失われ、保守費用の増加と設計の劣化につながるとされる(検索結果の記述。原著の書誌は未確認)。
- ADRの実践に関する実証は少ない。アクションリサーチで、文化と組織、暗黙知、文書化の手順、ツールに課題があると報告された研究があるとの検索結果を得たが、書誌(著者、年、題名)は今回確認できなかったため未確認とする。また arXiv 2604.27333 に、ADRテンプレート間の理解しやすさ、使いやすさ、導入のしやすさを比べた研究があることを確認した(題名は検索結果で確認。内容の精査はしていない)。

### 含意

- ADRで効くのは「状態」と「帰結」の欄である。決定を後から「置換」とマークする運用は、上書きせず系譜を残す設計の最小例になる。SEIの「決定」と「系譜」は ADR を一般化したものと位置づけられる。
- ADRが記録するのは決定であり、却下した代替案や、その時点で保留にしたことは書式の必須項目にない。CSWの「保留」は、ADRにない欄を補う。
- 議事録の効果については、今回の調査で実証研究を確認できていない。未確認。

## 3. 長期の思考の連続性: ノート、Zettelkasten、commonplace book

### 確認済み

- Schmidt, J. F. K. (2016). Niklas Luhmann's card index: Thinking tool, communication partner, publication machine. 検索で題名と著者を確認(掲載書の詳細は未確認)。Luhmannの索引カード箱が、思考の道具であり、対話相手でもあり、出版の装置でもあったという論考。
- Ahrens, S. How to Take Smart Notes. 検索で存在と内容(文献メモと自分の考えのメモを分け、番号で相互に結ぶ。主題索引を持つ)を確認した。出版年は検索結果から確認できなかった。
- Blair, A. M. (2010). Too Much to Know: Managing Scholarly Information before the Modern Age. Yale University Press. 抜粋、要約、整理、保管という近世の情報管理が、現代の技術の源にあると論じる。florilegium と commonplace book を扱う(Harvard Gazette などの紹介記事で確認)。

### 未確認

- 実験室ノートの機能に関する実証研究は、今回は確認できていない。未確認。

### 含意(私の解釈)

- 上記の例に共通するのは、(a) 文献由来のメモと自分の考えを分ける、(b) 項目に固定の識別子を付けて相互参照する、(c) 検索用の索引を別に持つ、の三点である。これは SUI の「カード・島」と、SEIの「観測と解釈の区別」に似た構造である。来歴の区別が、長期のノートの標準的な作りと重なることは、根拠として使える。
- 再開時に必要な情報の実証データは見つからなかった。ここでは、Luhmann型の運用の記述から「入口となる索引」と「相互参照」が再開を支えると推測するにとどまる。推測であり、検証されていない。

## 4. LLMエージェントの長期実行の現状と限界

### 4.1 文脈の劣化

- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023/2024). Lost in the Middle: How Language Models Use Long Contexts. arXiv:2307.03172; Transactions of the ACL に採録。複数文書QAとキー値検索で、関連情報が文脈の先頭や末尾にあると性能が高く、中央にあると大きく落ちる、U字の曲線を報告した。確認済み。
- Chroma Research (2025). Context Rot: How Increasing Input Tokens Impacts LLM Performance. https://research.trychroma.com/context-rot 。18のLLMで、入力が長くなるほど、単純な課題でも性能が不均一に不安定になると報告。検索結果は、10kから100k超のトークンで検索課題の精度が20から50%落ちるという二次的な記述を含むが、一次資料で数値を確認していないため、この数値は未確認とする。ベンダー(ベクトルDB企業)の技術報告であり、査読論文ではない点に注意。

### 4.2 長時間タスクの能力

- Kwa, T. ほか(METR) (2025). Measuring AI Ability to Complete Long Tasks(後の版の題は Measuring AI Ability to Complete Long Software Tasks). arXiv:2503.14499. 「50%タスク完了時間幅(time horizon)」、すなわち、AIが50%の成功率でこなせる課題が、人間の専門家で何分かかるかという尺度を提案した。論文公表時点でo3は約110分。時間幅は2019年以降およそ7か月で倍増し、2024年以降は加速した可能性があるとする。向上の要因は、信頼性、誤りへの適応、論理推論、道具の使用が主とされる。確認済み(検索結果の要旨)。
- METR の公開ページ(https://metr.org/time-horizons/、2026-05-08更新)に、Claude Mythos Preview(初期版)、GPT-5.4、Gemini 3.1 Pro、Claude Opus 4.6 が測定対象として載っていることを確認した。同ページに「16時間を超える測定は、現行のタスク群では信頼できない」と明記されている。タスクは主にソフトウェア、機械学習、サイバーセキュリティで、他領域への一般化には限界がある。
- 二次的な報道(X上のMETR投稿の引用や記事)によれば、Mythos Preview の50%時間幅は少なくとも16時間(95%信頼区間 8.5から55時間)、タスク群228件中16時間以上のものは5件のみである。一次資料(METR自身の報告書)は直接読めていないため、数値は参考扱いとする。
- 解釈上の注意(私見): この時間幅は「一つの課題を、成功率50%で終えられる長さ」であり、数日から数週にわたる意思決定の連続性や、前提が変わる環境での一貫性を測っていない。連続性そのものの能力として読んではならない。

### 4.3 セッションをまたぐ記憶の欠落と、引継ぎの人工物

- Young, J. (2025-11-26). Effective harnesses for long-running agents. Anthropic Engineering. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents 。エージェントは離散的なセッションで動き、新しいセッションは前の記憶なしに始まる。この記事は次の失敗を挙げる: 早すぎる完了宣言、一度に多くを試みて文脈を使い切ること、十分に検証しないまま完了とすること、環境が壊れた状態で次に渡すこと。対策として、機能リスト(JSON、合否付き)、進捗ファイル(claude-progress.txt)、初期化スクリプト、小さなコミット履歴を挙げる。「交代制で働く技術者」に似せて、引継ぎ文書を作る考え方である。確認済み。企業の実践報告であり、定量的な効果検証ではない点に注意。

### 4.4 永続記憶システムの設計と評価

- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as Operating Systems. arXiv:2310.08560. OSの階層記憶に倣い、文脈内(主記憶)と文脈外(外部記憶)をページングで行き来する「仮想文脈管理」を提案。文書分析と会話エージェントで既存手法を上回ったと報告。
- Letta のドキュメント(https://docs.letta.com/guides/agents/memory)。MemGPTの実装系。常時文脈にある記憶ブロック(ラベル、説明、値、文字数上限)と、文脈外の保管(archival)を持ち、エージェントがツールでブロックを編集する。確認済み(ドキュメントの記述による)。
- Chhikara, P., Khant, D., Aryan, S., Singh, T., & Yadav, D. (2025). Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. arXiv:2504.19413. 会話から重要情報を抽出、統合、検索する記憶中心の構成と、グラフ記憶の変種。要旨は、p95遅延が91%低く、トークン費用を90%超削減したとする。精度の比較値は今回確認していない。著者は製品の開発元であり、自己評価である点に注意。
- Rasmussen, P. ほか (2025). Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv:2501.13956. 時間認識つき知識グラフ Graphiti を用いる。二つの時間軸(事象の時系列と、データ取り込みの順序)を持つ「bi-temporal」モデル。DMRで94.8%対93.4%(MemGPT比)、LongMemEval で最大18.5%の精度向上、遅延90%減と報告。これも製品開発元の自己評価。
- Wu, D. ほか (2024/2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv:2410.10813 (ICLR 2025)。情報抽出、複数セッション推論、時間推論、知識更新、棄権(答えられないと言う力)の5能力を、500問で測る。商用チャット助手と長文脈LLMで、持続的な対話にわたる記憶の精度が約30%落ちたと報告。確認済み。知識更新と時間推論が評価軸に入っている点が、本調査の関心に直結する。
- Maharana, A., Lee, D.-H., Tulyakov, S., Bansal, M., Barbieri, F., & Fang, Y. (2024). Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo). ACL 2024 (Long Papers), arXiv:2402.17753. 平均600ターン、約16kトークン、最大32セッションの会話。長文脈LLMやRAGは改善をもたらすが、人間には大きく及ばない、特に長期の時間的、因果的な関係の理解が難しいと報告。

### 4.5 記憶が引き起こす誤り

- Xiong, Z., Lin, Y., Xie, W., He, P., Liu, Z., Tang, J., Lakkaraju, H., & Xiang, Z. (2025). How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior. arXiv:2505.16067。エージェントは、入力が似た過去の記録を検索すると、似た出力を返す「経験追従」を示す。このため (1) 誤った過去の実行が保存されると、それが再利用されて誤りが伝播、増幅する。(2) 入力が似ていても出力の質が低い記録(誤整合な経験の再生)が残る。選択的な追加と、複合的な削除の方針で平均10%(絶対値)の改善が出たと報告。確認済み。「誤った記憶の増幅」の直接的な根拠として使える。
- 「古い前提の固着」について、今回、LLMエージェントを対象に直接測った一次研究は確認できなかった。ただし LongMemEval の「知識更新」の課題設定は、この問題を評価対象に含めている点で近い。固着を主張する際は「評価軸としては存在するが、現象の大きさを測った決定的な研究は未確認」と書くこと。

### 4.6 モデル交代時の挙動変化

- Chen, L., Zaharia, M., & Zou, J. (2023). How Is ChatGPT's Behavior Changing over Time? arXiv:2307.09009. GPT-3.5とGPT-4の2023年3月版と6月版を7課題で比較。素数判定の精度は、GPT-4で84%から51%に下がり、センシティブな質問への回答率や、コード生成の書式の誤りも変化した。同名のサービスでも、更新で挙動が変わることの実証。確認済み。
- Anthropic (2025). Commitments on model deprecation and preservation. https://www.anthropic.com/news/deprecation-commitments 。公開モデルの重みを少なくとも同社が存続する限り保存する、廃止時にモデルへのインタビューと事後報告を作成して重みとともに保存する、とする。2026年1月5日に Claude Opus 3 が最初の廃止事例になった(検索結果の記述)。これは、モデル(重み)の連続性についての事業者側の方針で、利用者側のエージェントの意思決定の連続性を保証するものではない。
- 私見: 担当モデルが替わると、同じ記録を読んでも解釈や判断の傾向が変わり得る。したがって、記録は「結論」だけでなく、観測、解釈、根拠を分けて残さないと、新しいモデルが前任の結論を再検証できない。SEIの「観測、解釈、推奨、決定、権限、系譜」の分離は、この意味で設計上の正当性がある。ただし、分離すれば再現性が上がるという実証は今回確認していない。

## 5. 連続性とバージョン管理

### 確認済み

- Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). On the logic of theory change: partial meet contraction and revision functions. Journal of Symbolic Logic, 50(2), 510-530. 信念改訂(AGM)理論の出発点。信念集合を、新しい情報で縮約、改訂するときの合理性の公準を与える。要点は、矛盾が生じたとき、何を残し何を捨てるかに、順序や優先度といった追加の基準が要ること。「新しいものが勝つ」は、その基準の一つにすぎない。
- Fowler, M. Bitemporal History. https://www.martinfowler.com/articles/bitemporal-history.html 。「実際の履歴」と「記録上の履歴(いつそれを知ったか)」を分けて持つ。給与の昇給通知が、給与計算の後に届く例を使う。確認済み。
- Fowler, M. Event Sourcing (2005年に記述したとされる)。状態の変化を、出来事の列として追記して保存する。検索結果は二次的な記述のみで、Fowler の原文は直接確認できていない。この項は「原典は未確認」とする。

### 解釈(私の整理)

- 「Conflict ≠ latest-wins」を支持する根拠は、次の三つに整理できる。(a) AGM: 衝突時の選択に、時刻以外の基準(信頼度、出所、権限)が要る。(b) bitemporal: 「いつ事実だったか」と「いつ知ったか」が別なので、新しく届いた情報が、新しい事実とは限らない(遅れて届いた古い事実がある)。(c) 来歴: 同時に二つの情報源が食い違うとき、片方を消すと、後で誤りに気づけない。これは設計原則としての提案で、「latest-wins が誤りを増やす」ことを直接測った研究は今回確認していない。
- 追記のみの履歴(append-only)は、訂正を別の出来事として積むので、誤りの履歴も残る。これは、後述の責任の連続(記録保持)とも整合する。コストは、読み取り時に現在状態を再構成する負荷である。

## 6. 引継ぎの実証研究

### 医療

- Arora, V., Johnson, J., Lovinger, D., Humphrey, H. J., & Meltzer, D. O. (2005). Communication failures in patient sign-out and suggestions for improvement: a critical incident analysis. Quality & Safety in Health Care, 14(6), 401-407. 研修医26人が担当した82人の患者について、サインアウト(引継ぎ)の不備によるインシデント25件を面接で聞き取った。失敗の主因は、内容の欠落(薬、活動中の問題、保留中の検査)と、対面の議論の不在といった、失敗しやすい手順だった。ほぼ全例で、その後の判断に不確実性が生じた。研修医は、対面で、予想される問題を確認する口頭の引継ぎと、読みやすく更新された書面を望んだ。確認済み。
- Starmer, A. J. ほか (2014). Changes in Medical Errors after Implementation of a Handoff Program. New England Journal of Medicine, 371, 1803-1812. 小児科研修プログラム9施設で、I-PASS(Illness severity, Patient summary, Action list, Situation awareness and contingency plans, Synthesis by receiver)を中心とした引継ぎ一式を導入。10,740入院で、医療ミスは24.5から18.8件/100入院(23%減)、予防可能な有害事象は4.7から3.3件/100入院(30%減)に低下した(AHRQ PSNet などの二次資料で数値を確認)。確認済み。「受け手による要約(Synthesis by receiver)」が型に含まれる点は、LLMの引継ぎ設計に直接参照できる。
- Haig, K. M., Sutton, S., & Whittington, J. (2006). SBAR: a shared mental model for improving communication between clinicians. Joint Commission Journal on Quality and Patient Safety, 32(3), 167-175. SBAR(Situation, Background, Assessment, Recommendation)の導入例。有害事象と薬剤関連事象が減ったと報告されている(検索結果の記述。数値は未取得)。
- Patterson, E. S. (2004). Handoff strategies in settings with high consequences for failure: lessons for health care operations. International Journal for Quality in Health Care, 16(2), 125-132. doi:10.1093/intqhc/mzh026. スペースシャトル管制、原子力発電、鉄道運行指令、救急搬送の指令で、21の引継ぎ戦略を観察と面接から分類した。筆頭著者は Patterson と確認できたが、共著者の構成は検索で確認できていない(他のリストでは共著者が付く表記もあるため、共著者名は書かない)。他産業の引継ぎ手法を調べた、横断的な観察研究。

### 航空

- 航空のブリーフィングについては、今回の調査で書誌を確認できた一次文献がない。CRM(クルー・リソース・マネジメント)など、航空の乗員間コミュニケーション訓練の文献は存在すると考えられるが、本調査では未確認とする。

### ソフトウェア運用

- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.) (2016). Site Reliability Engineering. O'Reilly. 第15章 Postmortem Culture: Learning from Failure。https://sre.google/sre-book/postmortem-culture/ 。ポストモーテムは、インシデント、その影響、対応、根本原因、再発防止策の書面記録。「責めない(blameless)」運用では、関係者が持っていた情報のもとで善意で最善を尽くしたと仮定し、個人の責任追及を目的にしない。この文化は、医療と航空に由来すると同章が述べる。確認済み。runbook については、今回確認できた一次文献がない。未確認。

### 何が引継ぎに必須か(上記から導ける範囲)

- 現在の状態と重症度(何が急ぎか)、未解決で保留中のもの、次に取る行動とその条件、予想される事態への備え、受け手による復唱または要約。Starmer と Arora の内容を合成した整理で、一次研究の一つが全項目を同時に検証したわけではない。
- 構造化は有効だが、構造化が引継ぎの質のすべてを決めるわけではない。Patterson の研究は、引継ぎの目的が複数あり、状況ごとに戦略が異なることを示唆する(要約の限り)。

## 7. AIを独立した決定主体にする際の「同一性」と「責任の連続」

### 確認済み

- 欧州議会 (2017-02-16). Civil Law Rules on Robotics(決議)。第59項(f)で、最も洗練された自律ロボットに「電子的な人格(electronic person)」という特別な法的地位を設ける可能性を、委員会に分析するよう求めた。これに対し2018年に、Nevejans らが欧州委員会に宛てた公開書簡で、電子的な法人格を作らないよう求めた(検索結果の記述)。
- Bryson, J. J., Diamantis, M. E., & Grant, T. D. (2017). Of, for, and by the people: the legal lacuna of synthetic persons. Artificial Intelligence and Law, 25, 273-291. 純粋に人工の存在に法人格を与えることは、道徳的に不要で、法的にも厄介だと論じる。「電子的な人」が他者の権利を侵害したときに責任を負わせることの難しさが、保護すべき道徳的な利益を上回る、というのが結論。
- Chesterman, S. (2020). Artificial intelligence and the limits of legal personality. International and Comparative Law Quarterly, 69(4), 819-844. 多くの法体系は新しい法人格の類型を作れるが、そうすべきだという論拠は十分でないと論じる。法人との類比は、道具的な議論にとどまる。
- EU AI規則(Regulation (EU) 2024/1689)。第12条(記録保存)は、高リスクAIシステムが、システムの存続期間にわたり事象の記録(ログ)を自動で残せることを求める。第26条は、利用者(deployer)に、自動生成されたログを少なくとも6か月保持し、人による監督を割り当てることを求める(Mishcon、欧州委員会のAI Act Service Desk などの解説で確認)。第14条は人による監督を要求する。なお、高リスク規定の適用時期が2027年12月に延期されるとの二次情報があるが、確定は未確認であり、時期の記述は2028-2031年の前提に使う前に公式文書で確認すること。

### 解釈(私の整理)

- 「同一性」は少なくとも三層に分けられる。(a) モデルの同一性(重みと版)。(b) 役割の同一性(担当、権限)。(c) 判断の系譜の同一性(何を観測し、何を前提に、誰の権限で決めたか)。法的責任は、(b)と(c)に結びつけるのが実務的で、(a)は監査の補助情報になる。Chen 2023 が示すように、同名のモデルでも版で挙動が変わるため、(a)を「同じAI」の根拠にするのは弱い。
- 法人格をAIに与える案は、上記の三つの文献で否定的に扱われている。記録保持の要件(EU AI規則)は、責任主体を人間または組織に置き、AIの挙動の事後検証を可能にする方向を採っている。したがって CSW/SEI の系譜は、法人格の代わりに、責任を人や組織へ辿り直せるための基盤として位置づけるのが、現行の議論に整合的である。
- 事業者側のモデル保存の方針(Anthropic 2025)は、モデルの連続性に関する取り組みだが、利用者側の判断の責任の連続とは別の層である。混同しないこと。

## 8. この認知についての仮説は修正すべきか。欠けている認知はないか

### 8.1 仮説(6)の修正案

現行の「連続して存在する」は、次の理由で言い換えるべきだと考える。

1. 根拠: 連続性の失敗は、存在の断絶ではなく、再開時に必要な情報の欠落で起きる(Arora 2005)。LLMでも、セッション間の記憶欠落が主因で、引継ぎ人工物で緩和される(Anthropic 2025)。
2. 根拠: 連続性は、あるほど良いとは限らない。記憶は誤りを増幅し(Xiong 2025)、古い前提を固着させ得る。文脈が長くなるほど性能が不均一になる(Liu 2023、Chroma 2025)。「たくさん覚えている」ことは目標にならない。
3. 根拠: モデルが替われば挙動が変わる(Chen 2023)。連続しているのは主体の内的状態ではなく、記録と手続きである。

提案する書き換え: 「判断の系譜を、担当やモデルが替わっても再開できる形で保ち、再開のたびに前提の有効性を確かめる」。「存在」という語を避け、「再開可能性」と「前提の再検証」を入れる。

さらに、次の設計上の区別を仮説に含めるとよい。(i) 記録する(追記のみ)ことと、現在の信念を決める(改訂)ことを分ける。(ii) 記録には、観測、解釈、推奨、決定、権限を別項目で残し、受け手が復唱(要約)して確認する(I-PASS の「受け手による要約」に倣う)。(iii) 衝突は新しさで解かず、出所、権限、時間の二軸(実際にいつ有効か、いつ知ったか)で扱う。(iv)いつ・誰が・どのモデルで書いたかを記録に残す。

ただし、上記(ii)から(iv)の効果について、LLMエージェントを対象に検証した研究は今回確認していない。医療の引継ぎの効果(Starmer 2014)をLLMにそのまま移せるかは未検証である。

### 8.2 欠けている認知の候補

1. 前提の失効を検知する認知。仮説(2)保留、(4)確かめる、(5)誤りを見つける、のいずれにも、「過去に有効だった前提が、今は無効になっていないか」を再開時に問う動作が明示されていない。Xiong 2025 の誤りの増幅、LongMemEval の知識更新、bitemporal の議論から、独立した認知として置く価値があると考える。ただし(4)(5)の一部として吸収する設計も可能で、その方が六つの枠を保てる。判断は設計者に委ねる。
2. 権限と責任の境界を知る認知。「何を自分で決めてよく、何を人間に返すか」の区別。EU AI規則の人による監督(第14条)、Bryson 2017 の責任帰属の議論は、独立した決定主体として振る舞うAIが、責任をどこまで担えるかを問題にする。六つの認知のどれにも、この境界の自覚が明示されていない。SEIの「権限」はデータ項目として持つが、それを使って自分の判断を止める認知は仮説に出てこない。
3. 他の担当を想定して書く認知(受け手を意識した外部化)。引継ぎ研究(Arora 2005、Starmer 2014)で効くのは、送り手が自分の覚えている前提に頼らず、受け手が使える形に書くこと。(3)来歴を区別する、(6)連続して存在する、の接点にあたる。独立した認知とするほどの根拠は今回の調査では得られていないため、「候補」にとどめる。

### 8.3 注意点(根拠の強さ)

- 強い根拠: Lost in the Middle、METR の時間幅の定義、LongMemEval の設計、Xiong 2025、Chen 2023、Starmer 2014、Arora 2005。いずれも書誌と要旨を確認した。
- 弱い根拠: Chroma の数値(ベンダー報告で、数値は二次情報)、Mem0 と Zep の性能(開発元の自己評価)、METR の最新モデルの数値(二次情報で、METR自身が信頼性に限界を述べている)。
- 未確認: 航空ブリーフィングの実証、runbook の実証、議事録の効果、ADRの実践研究の書誌、実験室ノートの機能研究、Event Sourcing の原典、Walsh & Ungson の保管庫の内訳、EU AI規則の高リスク規定の適用時期の最新の扱い。
- この調査は、LLMを「独立した決定主体」として長期に運用した実証研究を見つけていない。本稿の設計提案は、他分野の研究からの類推であり、2028-2031年の想定に対する検証は、別途の実験が必要である。

## 付録: 出典URL一覧(確認できたもの)

- https://arxiv.org/abs/2307.03172 (Lost in the Middle)
- https://arxiv.org/abs/2503.14499 (METR time horizon)
- https://metr.org/time-horizons/
- https://arxiv.org/abs/2310.08560 (MemGPT)
- https://docs.letta.com/guides/agents/memory
- https://arxiv.org/abs/2504.19413 (Mem0)
- https://arxiv.org/abs/2501.13956 (Zep)
- https://arxiv.org/abs/2410.10813 (LongMemEval)
- https://arxiv.org/abs/2402.17753 (LoCoMo)
- https://arxiv.org/abs/2505.16067 (experience-following)
- https://arxiv.org/abs/2307.09009 (ChatGPT behavior)
- https://research.trychroma.com/context-rot
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/news/deprecation-commitments
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://www.martinfowler.com/articles/bitemporal-history.html
- https://qualitysafety.bmj.com/content/14/6/401 (Arora 2005)
- https://sre.google/sre-book/postmortem-culture/
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12
- 書誌のみ確認(URLは検索結果の二次サイト): Walsh & Ungson 1991、Argote ほか各論文、Nonaka 1994(https://ideas.repec.org/a/inm/ororsc/v5y1994i1p14-37.html)、Lewis 2003、Starmer 2014(https://psnet.ahrq.gov/resources/resource/28485)、Haig 2006、Patterson 2004、AGM 1985、Bryson 2017、Chesterman 2020
