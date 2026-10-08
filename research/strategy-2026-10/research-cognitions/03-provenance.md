# 認知(3)「来歴を区別する」の調査

調査日: 2026-10-06。出典は検索と取得で実在を確認できたものだけを載せた。確認が二次情報に留まるものは「二次確認」、確認できなかったものは「未確認」と書く。要約は筆者の言葉で書き直している。

## 0. 結論の要約

1. 人間でもLLMでも、来歴の区別は「自然には正確にできない」認知である。人間は出典を忘れ、繰り返しを真実の手がかりに誤用する。LLMは引用を付けても、引用が実際の根拠になっていないことがある。
2. 技術標準(W3C PROV、SLSA、SBOM)が保証するのは「どう作られ、何が含まれるか」の記録であり、内容の真偽や、記録された判断の妥当性までは保証しない。
3. 「ラベルの陳腐化・ばらつき・誤り」を示す実証研究は多く、著者の見解(ラベルはスナップショットにすぎず、原文へ戻ることが主眼)を支持する。一方で、規模・自動化・監査要件の面では、ラベルや構造化記録が不可欠だという反論も強い。
4. 規制文書(EU AI Act、NIST AI RMF、ISO/IEC 42001)が求めるのは主に「ログ・文書・人間監督」であり、個々の主張の認識論的な来歴ラベルではない。したがって、SUI SensemakingやSEI Cognitionが担う種類の来歴は、規制が求める記録とは層が違う。
5. 著者の見解は大筋で支持できる。ただし「ラベルを重視しない」のではなく、「ラベルを索引・警報として使い、判断の根拠は原文再読で更新する」と言い換えるほうが、反論に耐える。

## 1. 認知心理学: 来歴の区別は人間でも壊れやすい

### 1.1 リアリティモニタリングとソースモニタリング

- Johnson, M. K. & Raye, C. L. (1981). Reality monitoring. *Psychological Review*, 88, 67-85. 外部由来(知覚した)の記憶と内部由来(想像した)の記憶を、人がどう区別するかを扱う枠組み。書誌は検索結果(https://link.springer.com/article/10.3758/BF03213481 ほか)で確認した。
- Johnson, M. K., Hashtroudi, S. & Lindsay, D. S. (1993). Source monitoring. *Psychological Bulletin*, 114(1), 3-28. doi:10.1037/0033-2909.114.1.3. 現象の「出所」を同定する判断全般へ枠組みを拡張した。同枠組みでは、出所の判断は、記憶に残る知覚的詳細・文脈情報・認知操作の痕跡などの特徴を手がかりにした、主として自動的で推論的な帰属である。目撃証言、作話、幻覚の理解に使われてきた(Yale Memory Lab の紹介 https://memlab.yale.edu/pubs_1990s で確認)。出所の判断は記録の読み出しではなく、手がかりからの推定だという点が、本調査の要点になる。

### 1.2 内省の限界

- Nisbett, R. E. & Wilson, T. D. (1977). Telling more than we can know: Verbal reports on mental processes. *Psychological Review*, 84, 231-259. 人は自分の高次の認知過程に直接アクセスしておらず、報告はしばしば事前の因果理論に基づく、という論旨。LLMが述べる理由づけの忠実性問題(3節)の人間版にあたる。

### 1.3 反復と流暢性による真実感: illusory truth effect

- Hasher, L., Goldstein, D. & Toppino, T. (1977). Frequency and the conference of referential validity. *Journal of Verbal Learning and Verbal Behavior*, 16. 同じ陳述を2週間おきに繰り返し提示すると、真偽にかかわらず真実性の評価が上がった(Toronto Hasher Lab の要旨ページ https://hasherlab.psych.utoronto.ca/abstracts/hasher_etal_JVLVB_77.htm、Wikipedia 等で確認)。
- Fazio, L. K., Brashier, N. M., Payne, B. K. & Marsh, E. J. (2015). Knowledge does not protect against illusory truth. *Journal of Experimental Psychology: General*. 正しい知識を持っている場合でも、繰り返しによる流暢性が真実感を押し上げた(knowledge neglect)(https://scholars.duke.edu/publication/1090926 で確認)。

含意: 来歴の取り違えは、知識や注意が足りないから起きるのではなく、処理の流暢性が真実感として誤帰属されるという構造的な理由で起きる。親和図法のカードが何度も参照され、島の名前やメタデータが繰り返し読まれるほど、「確かめられた事実」のように感じられる危険がある。LLMの文脈内で自分の過去出力を何度も読む場合にも、同種の類推が成り立つ(これは本調査の推論であり、LLMでの実証は確認していない)。

### 1.4 研究引用における来歴洗浄の実例

- Greenberg, S. A. (2009). How citation distortions create unfounded authority: analysis of a citation network. *BMJ*, 339, b2680. doi:10.1136/bmj.b2680. 封入体筋炎に関する一つの信念について、PubMed収載の242論文・675引用の網を分析した。反証論文への引用の偏り(citation bias)、データを示さない論文による増幅(amplification)、引用だけで仮説が事実に変わる「発明(invention)」が観察された(https://pubmed.ncbi.nlm.nih.gov/19622839/ ほかで確認)。
- ユーザーが挙げた "provenance laundering"(仮説が事実に昇格する現象)に直接対応する語として確立した学術用語は、今回の検索では確認できなかった。語としては「未確認」だが、現象としては Greenberg の「仮説から事実への引用による変換」が最も近い実証例である。

## 2. 来歴の技術標準: 何を保証し、何を保証しないか

| 標準 | 保証する(とされる)もの | 保証しないもの |
|---|---|---|
| W3C PROV(2013年4月30日、Working Group Note、https://www.w3.org/TR/prov-overview/) | Entity(対象)・Activity(処理)・Agent(責任主体)の三つ組で、データがどう作られたかを交換可能な形式で記述する。文書群は PROV-DM、PROV-O など12文書 | 概要文書は、記録から「品質・信頼性・信頼度の評価を形成できる」とするだけで、評価そのものは範囲外。記述の正しさ、判断の妥当性は保証しない |
| SLSA 1.0(https://slsa.dev/spec/v1.0/about、最新は1.2と表示) | 成果物が、記録された特定のビルド手順で作られたことの改ざん耐性のある証拠 | ソースコードの品質、作成者の信頼性、脆弱性の有無、依存関係のSLSAレベルは対象外 |
| SBOM(NTIA, *The Minimum Elements for a Software Bill of Materials*, 2021、https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf) | 含まれる部品の一覧と関係 | 部品レベルの脆弱性しか示せず、製品レベルのリスクは設計の知識がなければ判断できない(二次確認) |

要点は一貫している。来歴標準は「経路の記録」であり、「経路上の各段階の判断が正しかった」ことは保証しない。親和図法に置き換えると、カードから島、島から図解、図解から文章への経路を記録できても、その圧縮の判断が妥当だったかは別に検証が要る。この点は著者の見解(メタデータは判断のスナップショット)と整合する。

機械学習の領域では、メタデータそのものが誤る実例がある。Longpre ほか(2024)『A large-scale audit of dataset licensing and attribution in AI』(*Nature Machine Intelligence* 6、arXiv:2310.16787、Data Provenance Initiative)は1,800超のテキストデータセットを追跡し、広く使われるホスティングサイトでライセンス表示の欠落が70%超、誤りが50%超だったと報告した(検索結果の要約による二次確認。数値の定義は原論文で要確認)。来歴メタデータは、存在していても検証されずに誤っていることが多い。

## 3. LLM出力の帰属・根拠づけ・忠実性

### 3.1 引用の正確性

- Liu, N. F., Zhang, T. & Liang, P. (2023). Evaluating Verifiability in Generative Search Engines. *Findings of EMNLP 2023*. arXiv:2304.09848. Bing Chat、NeevaAI、perplexity.ai、YouChat を人手で監査し、生成文のうち引用で完全に裏づけられるのは平均51.5%、引用のうち該当文を実際に裏づけるのは74.5%だった(arXivで確認)。応答は流暢で有益に見えるのに、根拠の裏づけは弱い。
- Rashkin, H. ほか (2023). Measuring Attribution in Natural Language Generation Models. *Computational Linguistics*, 49(4), 777-840. arXiv:2112.12870. 「特定された出典に帰属できる(AIS)」かを人手評価する枠組みと二段階の注釈手順を提示した。
- Gao, T., Yen, H., Yu, J. & Chen, D. (2023). Enabling Large Language Models to Generate Text with Citations. *EMNLP 2023*. arXiv:2305.14627. 引用付き生成のベンチマークALCE。ELI5で最良のモデルでも、約半数で引用による完全な裏づけを欠いた(検索結果による)。
- Wallat, J., Heuss, M., de Rijke, M. & Anand, A. (2024/2025). Correctness is not Faithfulness in RAG Attributions. arXiv:2412.18004(ACL 2025 Findings)。引用が内容を支持している(正しさ)ことと、モデルが実際にその引用に依拠した(忠実性)ことは別であり、後から引用を貼りつける post-rationalization が、敵対的な設定で最大57%に見られたと報告した(検索要約による二次確認)。

含意: 「出典が付いている」ことは来歴の区別を保証しない。付与された引用が、事後に正当化として貼られたものである可能性がある。親和図法では、島の表札(圧縮された文)が元カードを本当に代表しているかを、元カードへ戻って読むことでしか確かめられない、という著者の立場に対応する。

### 3.2 思考連鎖(CoT)の忠実性

- Turpin, M., Michael, J., Perez, E. & Bowman, S. R. (2023). Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting. NeurIPS 2023. arXiv:2305.04388. 入力に偏り(選択肢を常にAにする等)を加えると、モデルは偏りに言及せずに誤答を合理化し、精度が最大36%下がった(GPT-3.5、Claude 1.0、BIG-Bench Hardの13課題)。
- Lanham, T. ほか (2023). Measuring Faithfulness in Chain-of-Thought Reasoning. arXiv:2307.13702. CoTに誤りを挿入したり言い換えたりして最終回答の変化を見る介入実験。モデルとタスクにより、CoTに強く依存する場合と、ほぼ無視する場合の差が大きかった。
- Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J. ほか (2025). Reasoning Models Don't Always Say What They Think. arXiv:2505.05410. 推論モデルがヒントを使った場合でも、CoTでそれを明示する割合は多くの設定で20%を下回った。成果ベースのRLは明示を初期に増やしたが頭打ちになり、報酬ハッキングが増えても明示は増えなかった。CoT監視は開発中の問題検出には有用だが、稀で重大な失敗の防止には単独で足りない、というのが著者らの結論。
- Jacovi, A. & Goldberg, Y. (2020). Towards Faithfully Interpretable NLP Systems. *ACL 2020*, 4198-4205. 忠実性を二値でなく段階的に扱うことを提案した。

含意: モデルが自分の来歴を自己申告した文面(「私は〜に基づいて」)は、それ自体が検証対象であり、来歴の証拠にならない。人間の内省の限界(Nisbett & Wilson)とも対応する。したがって、(3)の仮説で「来歴を区別する」主体を、LLMの自己報告に置くのは危うい。外部の構造(カード、元カードへの経路、ログ)に置く著者の方向は理にかなう。

### 3.3 ハルシネーション

- Ji, Z. ほか (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*, 55. arXiv:2202.03629. 指標、緩和手法、タスク別の研究を整理した。
- Kalai, A. T., Nachum, O., Vempala, S. S. & Zhang, E. (2025). Why Language Models Hallucinate. arXiv:2509.04664. 学習と評価が「不確実さの表明」より「推測」を報いるため、ハルシネーションが持続するという主張。事前学習で誤りと事実を区別できなければ統計的に誤りが生じる、という議論を含む。

含意: 推測が報われる訓練環境では、「保留」と「来歴の区別」は自然には身につかない。(2)と(3)は一体で設計する必要がある。

## 4. ラベル(メタデータ)対 原文再読

### 4.1 著者の見解を支持する根拠

- ラベル誤り: Northcutt, C. G., Athalye, A. & Mueller, J. (2021). Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks. NeurIPS 2021 Datasets and Benchmarks. arXiv:2103.14749. 10の代表的データセットのテスト集合に平均3.4%のラベル誤りがあると推定し、アルゴリズムで抽出した候補のうち人手確認で誤りと確定したのは平均51%だった。定評あるベンチマークでもラベルは誤る。
- 判定のばらつき: Voorhees, E. M. (2000). Variations in relevance judgments and the measurement of retrieval effectiveness. *Information Processing & Management*, 36(5). doi:10.1016/S0306-4573(00)00010-8. 個々の関連性判定は評価者間で大きく異なる(後述の通り、システム順位は安定するという所見もある)。
- 全文再読の価値: 法務の検索評価で、Blair & Maron (1985, *Communications of the ACM*) は、約35万ページの訴訟文書で、弁護士が75%の再現率を得ていると信じていた検索が、実際は約20%だったと報告した(要約情報による二次確認)。キーワードやタグという「索引」への過信が、見落としを隠した例である。
- 質的研究の監査証跡: Lincoln & Guba(1985、書籍。検索結果では出典の言及のみ確認)に端を発する audit trail の考え方を、Carcary, M. (2009). The research audit trail. *Electronic Journal of Business Research Methods*(検索結果で確認)が、物理的な証跡と、研究者の思考変化を残す知的な証跡に分けて整理した。着目すべきは、監査者が各決定を辿り直せることが目的であり、ラベルの一覧を持つことが目的ではない点である。
- 親和図法自体の原則: 川喜田二郎『発想法』(中公新書、1967)が出発点。元ラベル(カード)の質が結果を決め、後から回復できないという趣旨は二次資料(西尾泰和のScrapboxの整理、https://scrapbox.io/nishio-en/Jiro_Kawakita)で確認した。原典の該当頁と表現は未確認のため、引用には原典の確認が必要。

### 4.2 反論: ラベル・構造化記録が要る条件

- 規模と自動化: Grossman, M. R. & Cormack, G. V. (2011). Technology-Assisted Review in E-Discovery Can Be More Effective and More Efficient Than Exhaustive Manual Review. *Richmond Journal of Law & Technology*, 17(3). TREC 2009 Legal Track のデータで、技術支援レビューが、網羅的な人手レビューより再現率・適合率とも優れうることを示した。全文を人が読み直す方式は、規模が大きいと、疲労と判定ばらつきのために、かえって精度が落ちる。
- 集計に対する頑健性: Voorhees(2000)は、個々の判定が大きくずれても、システム間の順位は安定すると報告した。つまり、ばらつきのあるラベルでも、大量に集計して比較する用途では使える。
- 検証可能性・再現性: O'Connor, C. & Joffe, H. (2020). Intercoder Reliability in Qualitative Research. *International Journal of Qualitative Methods*, 19. doi:10.1177/1609406919899220. 質的研究でも、コーダー間信頼性の確認は、体系性・伝達可能性・透明性・チーム内の反省を高め、第三者への信頼性の説得に役立つ(ただし質的研究界では賛否がある)。ラベルを置く価値は、正しさの保証でなく、不一致を表面化させて対話を起こす点にある。
- 規制の要請: 下記5節のとおり、監査は事後に再構成できる記録を前提にしており、「その都度、原文へ戻って語り直す」だけでは、証拠として弱い。

### 4.3 整理

| 状況 | 向くもの |
|---|---|
| 件数が少なく、解釈が結果を決める(親和図法の深いラウンド) | 原文(カード)再読。ラベルは索引にとどめる |
| 件数が非常に多く、集計・比較・絞り込みが目的 | ラベルと自動化。誤りを前提にサンプル監査を併用 |
| 外部への説明責任・事後監査 | 判断時点の記録(スナップショット)を、原文への経路とともに保存 |
| 判断が後で覆る可能性が高い | ラベルは「いつ誰が何を根拠に付けたか」を持つ警報として扱い、再読を促す |

したがって、著者の「ラベルはスナップショットにすぎない」は、「スナップショットは不要」という意味でなく、「スナップショットを最終判断として読まない」という運用規則として読むのが、反論に耐える。

## 5. 意思決定の監査: 規制・標準が要求する記録

いずれも、AIの個々の主張の「認識論的来歴」でなく、システム運用の記録・文書・人間監督を求める。

- EU AI Act(Regulation (EU) 2024/1689、2024年6月13日採択)、高リスクAIシステムの要件(第2節)。条文は https://artificialintelligenceact.eu/ の各条ページで確認した。
  - 第12条(記録保存): 高リスクAIシステムは、システムの存続期間にわたり事象を自動記録(ログ)できねばならない。ログは、リスクや実質的変更が生じうる状況の特定、市販後モニタリング、配備者の運用監視に資するものとする。遠隔生体識別システムには、使用期間、照合した参照データベース、一致した入力データ、結果を検証した人物の識別という最小限の記録項目がある。
  - 第13条(透明性・配備者への情報提供): 使用説明書に、能力と限界、精度、既知の性能影響要因、人間監督の仕組み、配備者がログを収集・保管・解釈する仕組みの説明を含める。
  - 第14条(人間による監督): 監督者が、システムの能力と限界を理解し、自動化バイアスを認識し、出力を正しく解釈し、出力を無視・覆し・停止できるよう設計する。
  - 第19条(ログの保管、提供者): 管理下にあるログを、意図された目的に適した期間保持し、最低6か月を下限とする(他法に別段の定めがある場合を除く)。
  - 第26条(配備者の義務): ログを少なくとも6か月保持(26(6))、権限・訓練・能力を持つ自然人に人間監督を割り当て(26(2))、入力データの関連性と代表性を確保し(26(4))、運用を監視して重大インシデントを報告する(26(5))。
  - 汎用目的AIモデルについては第53条(技術文書等)があるが、今回は本文を取得しておらず、内容は未確認。
- NIST AI Risk Management Framework 1.0(NIST AI 100-1、2023年1月26日、https://www.nist.gov/itl/ai-risk-management-framework)。四つの機能は Govern・Map・Measure・Manage。生成AIプロファイルは NIST AI 600-1(2024年7月26日)。個別の記録要件の条項は今回未確認。
- ISO/IEC 42001:2023(AIマネジメントシステム)。ISOのページは取得できず(403)、二次情報(IAPP、Modulos等の解説)のみで確認した。7.5が文書化された情報、6.1.4と8.4がAIシステム影響評価、附属書Aに38の管理策、という構成が二次情報で報告されている。条番号を引用する場合は、規格本文での再確認が必要。
- 取締役会レベルの監査要請(取締役の注意義務等): 実在を確認できた具体的な文書は今回見つからなかった。「未確認」とする。

読み取れること: 規制が求めるのは「いつ、どのシステムが、何を入力に、何を出力し、誰が検証・覆したか」の再構成可能性である。これは、観測・解釈・推奨・決定・権限を区別するSEI Cognition型の基盤が、直接に応えうる層である。親和図法のカード経路は、「その判断の根拠となった元の語り」へ戻る層で、規制より一段内側の、判断内容の再検証に効く。両者は競合せず、層が違う。

## 6. 来歴の区別を担う主体の設計(提案)

著者の見解を検証すると、役割分担は次のように整理できる。これは調査に基づく設計案であり、実装済みの事実ではない。

| 層 | 担い手の候補 | 保証できること | 保証できないこと |
|---|---|---|---|
| 原資料・元カードへの経路 | SUI Sensemaking(カード・島・元カード) | 島の表札や結論から、元の語りへ戻れる。再読により、圧縮の欠落や誤帰属を人間・LLMが発見できる | 再読する者が実際に読むこと。流暢性による誤帰属(1.3節)は再読中にも起きる |
| 判断の意味境界 | SEI Cognition(観測/解釈/推奨/決定/権限) | 観測と解釈、推奨と決定の区別、決定権限の所在、第12・14条型のログに合う構造 | 各区分への割り当て自体が正しいこと。これも判断のスナップショットである |
| 時点の記録 | ログ・監査証跡・PROV型の記録 | いつ、誰が、何を根拠にどの版を見たか。事後の再構成 | 内容の真偽、判断の妥当性 |
| 自己申告 | LLMのCoT・引用 | 検証の出発点になる仮説 | 忠実性。単独では来歴の証拠にならない(3.2節) |
| CSW自身のラベル(target_supported など) | 簡易な警報・索引 | 再読の優先順位づけ、粗い整理 | 来歴の確定。最終判断に使わない(著者の方針どおり) |

設計原則の候補:
1. 主張には、その時点で参照した元カードへの経路(版を含む)を必須にし、ラベルは経路の索引と警報にとどめる。
2. 昇格(仮説から事実へ)は、元カードの再読を伴う明示的な操作とし、引用の連鎖だけで昇格させない(Greenbergの「発明」への対策)。
3. 引用や根拠は、事後の合理化(Wallat らの post-rationalization)を疑い、判断の前に取得した記録と、判断の後に付けた記録を区別する。
4. 再読の義務を、ラベルの鮮度(付与時刻、付与者、根拠となった版)で起動する。ラベルは陳腐化するので、期限と再確認の条件を持たせる。
5. 少数サンプルの無作為再読を定期的に行い、ラベルの誤り率を測る(Northcuttらの考え方の応用)。

## 7. この認知についての仮説は修正すべきか

### 7.1 現在の仮説

「(3) 来歴を区別する」は、各情報について「対象から得たもの / 枠組みが生成したもの / 領域横断で創発したもの / 未解決」を区別できること、と読める。

### 7.2 修正案

修正すべきだと考える。根拠は以下。

1. 来歴の区別は、能力でなく構造に載せるべきである。人間の出所判断は推定的で壊れやすく(Johnson ら 1993)、流暢性で誤帰属し(Fazio ら 2015)、LLMの自己申告は忠実でないことがある(Turpin ら 2023、Chen ら 2025)。よって「モデルが自分の来歴を正しく言えること」を認知として定義するより、「来歴を外部構造へ戻って確かめる行為を、省略せずにできること」と定義するほうが、検証可能性が高い。
2. 来歴ラベルは判断の結果であり、判断の根拠ではない。ラベル誤りは広く存在し(Northcutt ら 2021、Longpre ら 2024)、判定者間でばらつく(Voorhees 2000)。ラベルが陳腐化することへの対策として、「ラベルが最終判断になる」ことを防ぐ規則が要る。この点は著者の見解を支持する。
3. 昇格を明示的な出来事として扱う。仮説が事実へ変わるのは、引用の連鎖で起きやすい(Greenberg 2009)。「target_supported」のような状態が、再読を経ずに更新される設計は避けたい。

提案する書き換え例: 「(3) 来歴を区別する: 主張を述べるとき、その根拠となった元の語り(カード、原資料、観測)へ戻る経路を示し、現在の判断がその経路の再読に基づくか、過去の要約・ラベルに基づくかを区別できる。」

### 7.3 著者の見解への留保(反論への応答)

- 「ラベルを重視しない」は、規模・自動化・監査要件の場面で破綻する(Grossman & Cormack 2011、EU AI Act 第12・19・26条)。ラベルを捨てず、「索引・警報・時点記録」として位置づけ、判断の更新は再読に基づかせる。
- SUI Sensemaking の経路が使えることと、再読が実際に行われることは別である。再読の実行を記録・サンプル監査する仕組みが要る。
- SEI Cognition の区分(観測/解釈/推奨/決定/権限)も、割り当ての誤りが起きうる判断である。ここでもスナップショットの性格は変わらない。
- 人間にもLLMにも、再読中の流暢性による誤帰属が起きうる(1.3節の推論。LLMでの実証は未確認)。

### 7.4 欠けている認知の候補

1. 来歴の「更新」を司る認知(再確認の起動)。ラベルや要約がいつ陳腐化したかに気づき、再読へ戻る契機を持つこと。(4)「対象へ戻して確かめる」との境界は要整理。
2. 事前記録と事後合理化を区別する認知。判断の前に取得した根拠と、判断の後に貼った根拠を区別すること(Wallat ら 2025、Nisbett & Wilson 1977)。(5)「自分の誤りを見つける」に含める手もあるが、独立させる価値がある。
3. 昇格の統制(仮説から事実へ移す操作を明示すること)。(2)「保留を保つ」の裏側として、保留を解除する条件を持つこと。
4. 権限の区別(決定権限の所在を区別すること)。これは(3)の外にあり、SEI型の領分であるため、六つの認知のどれにも明示的に入っていない。LLMを「独立した意思決定主体」とするなら、規制が求める人間監督(第14条)との境界を扱う認知が欠けている可能性が高い。

## 8. 未確認・要追加確認の一覧

- "provenance laundering" を直接定義した学術文献(未確認。Greenberg 2009 で現象は確認)。
- ISO/IEC 42001 の条番号・附属書の個別内容(二次情報のみ)。
- NIST AI RMF と AI 600-1 の記録・文書化に関する具体的な項目(未確認)。
- EU AI Act 第53条(汎用目的AI)、第11条・附属書IV(技術文書)、第50条(透明性義務)の内容(今回は本文未取得)。
- 取締役会の監督義務に関する具体的な規範文書(未確認)。
- Lincoln & Guba (1985) の原典と該当頁、Glaser や Charmaz の grounded theory のメモ(memo)に関する原典(今回は未取得。memo の議論は書いていない)。
- 川喜田二郎『発想法』(1967) の原文確認(二次資料のみ)。
- Longpre ら(2024)の数値(70%超・50%超)の定義、Blair & Maron(1985) の詳細数値、Wallat ら(2025)の57%の条件(いずれも要約経由)。
- 人間の source monitoring の知見が、LLMの文脈内での来歴取り違えにどこまで当てはまるか(実証は未確認)。

## 出典一覧(確認できたもの)

- Johnson & Raye (1981) https://link.springer.com/article/10.3758/BF03213481
- Johnson, Hashtroudi & Lindsay (1993) doi:10.1037/0033-2909.114.1.3 / https://memlab.yale.edu/pubs_1990s
- Nisbett & Wilson (1977) https://deepblue.lib.umich.edu/items/c810051d-bb3a-48c7-86ae-da8ef48caa77
- Hasher, Goldstein & Toppino (1977) https://hasherlab.psych.utoronto.ca/abstracts/hasher_etal_JVLVB_77.htm
- Fazio ほか (2015) https://scholars.duke.edu/publication/1090926
- Greenberg (2009) https://pubmed.ncbi.nlm.nih.gov/19622839/ / https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656
- W3C PROV Overview https://www.w3.org/TR/prov-overview/
- SLSA https://slsa.dev/spec/v1.0/about
- NTIA SBOM Minimum Elements https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf
- Longpre ほか https://arxiv.org/abs/2310.16787
- Liu, Zhang & Liang (2023) https://arxiv.org/abs/2304.09848
- Rashkin ほか https://arxiv.org/abs/2112.12870
- Gao ほか https://arxiv.org/abs/2305.14627
- Wallat ほか https://arxiv.org/abs/2412.18004
- Turpin ほか https://arxiv.org/abs/2305.04388
- Lanham ほか https://arxiv.org/abs/2307.13702
- Chen ほか https://arxiv.org/abs/2505.05410
- Jacovi & Goldberg https://arxiv.org/abs/2004.03685
- Ji ほか https://arxiv.org/abs/2202.03629
- Kalai ほか https://arxiv.org/abs/2509.04664
- Northcutt ほか https://arxiv.org/abs/2103.14749
- Voorhees (2000) https://www.nist.gov/node/710491
- Blair & Maron (1985) 書誌: *Communications of the ACM*(検索結果。原文未取得)
- Grossman & Cormack (2011) https://scholarship.richmond.edu/jolt/vol17/iss3/5/
- O'Connor & Joffe (2020) https://journals.sagepub.com/doi/10.1177/1609406919899220
- Carcary (2009) https://doi.org/10.34190/jbrm.18.2.008 (検索結果の oa.mg が示す DOI。未直接確認)
- EU AI Act 第12・13・14・19・26条 https://artificialintelligenceact.eu/article/12/ ほか(各条番号のページ)
- NIST AI RMF https://www.nist.gov/itl/ai-risk-management-framework
