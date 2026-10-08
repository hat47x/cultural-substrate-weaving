# 認知(2) 保留を保つ、および親和図法が決定主体の基盤になりうる根拠

調査日: 2026-10-06
対象: CSW(文化的体系を触媒に使う思考基盤)と親和図法(KJ法)の深いラウンドを組み合わせ、LLMが開いた問題空間(2028-2031年)で独立した決定主体として働くための認知基盤。

## 0. 読み方と確認水準

- 出典は WebSearch/WebFetch で実在(書誌情報の一致)を確認したものだけを載せた。確認水準は三段階で示す。
  - [確認A] 検索結果で書誌と要旨が一致し、一次ページ(arXiv、出版社、PubMed 等)に到達できたもの。
  - [確認B] 書誌は複数ページで一致したが、本文は精読していないもの(要旨レベルの把握)。
  - [二次] 解説ページ・個人サイト経由の情報で、一次資料の確認が済んでいないもの。
- 本文の精読まで済ませた出典はない。主張は要旨・検索要約の範囲にとどめた。数値は検索結果に現れたものだけを使い、頁数など確認できなかったものは書かない。
- 末尾「9. 未確認事項」に、確認できなかった点をまとめた。
- 2026年7月・8月投稿の arXiv 論文を2本含む(3.2, 4.4)。査読前で、評価は暫定。

---

## 1. 早すぎる収束(premature closure)の研究

### 1.1 診断推論

- Graber, M. L., Franklin, N., & Gordon, R. (2005). Diagnostic error in internal medicine. Archives of Internal Medicine. PubMed: https://pubmed.ncbi.nlm.nih.gov/16009864/ [確認A]
  - 内科の診断エラー100例(解析できた93例)を調べ、1例あたり約5.9個の要因(計548)を同定した。認知的要因が関与した症例は74%、システム要因は65%。認知要因のうち、最初の診断に到達した後に妥当な代替案の検討をやめること(premature closure)が単独で最多の原因だった、と報告している。
  - 含意: 早すぎる収束は「知識不足」より「初期仮説に到達したあとの探索停止」として現れる。保留とは、仮説を持たないことではなく、仮説を持ったあとも代替案の検討を止めないことである。
- Croskerry, P. (2003). The importance of cognitive errors in diagnosis and strategies to minimize them. Academic Medicine, 78(8), 775-780. https://academic.oup.com/academicmedicine/article-abstract/78/8/775/8355718 [確認A]
  - premature closure を「不完全な情報で診断を確定すること」、anchoring を「矛盾する情報が出ても暫定診断を見直さないこと」として区別している。対策として認知的な脱バイアス(cognitive debiasing)の研究を求めている。両者は別の失敗であり、保留の設計は「確定を急ぐ」失敗と「確定後に動かない」失敗の双方を対象にすべきである。
- Mamede, S. et al. (2010). Effect of availability bias and reflective reasoning on diagnostic accuracy among internal medicine residents. JAMA, 304(11), 1198-1203. https://cris.maastrichtuniversity.nl/en/publications/effect-of-availability-bias-and-reflective-reasoning-on-diagnosti [確認B(著者は第一著者のみ確認)]
  - 直近に経験した症例に引きずられる availability bias が非分析的推論で出て、事例の所見を構造的に再分析する「診断的リフレクション」がそれを弱め、診断精度を上げた(研究室条件、研修医36名)。保留を手続きとして組み込めば効果が出うる、という実験的な根拠になる。

### 1.2 閉鎖欲求(need for cognitive closure)

- Kruglanski, A. W., & Webster, D. M. (1996). Motivated closing of the mind: "Seizing" and "freezing". Psychological Review, 103, 263-283. https://terpconnect.umd.edu/~hannahk/NFC-KW96.html [確認A]
  - 閉鎖欲求を「ある問題について確定した知識を求める欲求」と定義し、結果を二つの傾向に分ける。早く結論に飛びつく urgency(seizing)と、得た結論を長く保持する permanence(freezing)。印象形成、ステレオタイプ、帰属、説得、集団意思決定に効果があるとしている。
  - 含意: 保留を壊す力は「急ぐ」と「固まる」の二方向にある。エージェント設計では、締切や完了報告の圧力が seizing を、一度書いた結論の再利用が freezing を生む対応関係が考えられる(推論であって、同論文の主張ではない)。
- Webster, D. M., & Kruglanski, A. W. (1994). Individual differences in need for cognitive closure. Journal of Personality and Social Psychology, 67, 1049-1062. https://terpconnect.umd.edu/~hannahk/NFC-WK94.html [確認A]
  - 閉鎖欲求を五側面(予測可能性への欲求、秩序・構造の選好、曖昧さへの不快、決断性、閉鎖的思考)で測る尺度を提示した。曖昧さへの不快と決断性が別側面として分かれている点は、後述の「保留から決定への橋」の設計に使える。保留を保つ能力と決定する能力は一つの軸の両端ではなく、別々に鍛えうるという示唆である。

### 1.3 Keats の negative capability

- Keats, J. 1817年12月の兄弟宛書簡(Poetry Foundation の「Selections from Keats's Letters」所収)。https://www.poetryfoundation.org/articles/69384/selections-from-keatss-letters [確認A(書簡の抜粋ページ)]
  - 「事実や理由を苛立たしく追い求めることなく、不確かさ・神秘・疑いの中にいられる」状態を negative capability と呼んだ。文学上の概念であり、認知科学的な実証は伴わない。比喩としては有用だが、設計の根拠にするなら 1.1-1.2 の実証研究のほうが強い。
  - 書簡の日付は検索結果で「1817年12月21-27日ごろ」とされている(BARS の記事)。正確な日は未確認。

### 1.4 コミットメントのエスカレーションとアンカリング

- Staw, B. M. (1976). Knee-deep in the big muddy: A study of escalating commitment to a chosen course of action. Organizational Behavior and Human Performance. [確認B(検索結果の要約は複数ページで一致。巻号頁は未確認)]
  - 事業投資のシミュレーションで、自分が選んだ案件に悪い結果が出たとき、個人責任が高い参加者ほど追加資源を投じた。
- Sleesman, D. J., Conlon, D. E., McNamara, G., & Miles, J. E. (2012). Cleaning up the big muddy: A meta-analytic review of the determinants of escalation of commitment. Academy of Management Journal, 55(3), 541-562. DOI: 10.5465/amj.2010.0696 [確認B]
  - エスカレーションの規定因を理論別に比較したメタ分析。結果の中身(どの理論が強いか)は要旨レベルでも未確認。
  - 含意: 公開した結論や自分が選んだ案は、後から動かしにくくなる。保留の台帳は、結論を書く前の仮説の段階から履歴を残し、撤回を「失敗」ではなく通常の操作にする設計が望ましい。
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. Science. PubMed: https://pubmed.ncbi.nlm.nih.gov/17835457/ [確認A]
- Furnham, A., & Boo, H. C. (2011). A literature review of the anchoring effect. The Journal of Socio-Economics, 40(1), 35-42. https://ideas.repec.org/a/eee/soceco/v40y2011i1p35-42.html [確認A]
  - アンカリングは数値推定に限らず、法的判断、価格交渉、予測にも及ぶ。最初に提示された値が最終判断に不釣り合いな影響を持つ。LLMの文脈では、プロンプトの冒頭に置いた仮説が同じ働きをするかどうかは別に検証が要る(5.2 参照)。

### 1.5 直観の妥当性の条件

- Kahneman, D., & Klein, G. (2009). Conditions for intuitive expertise: A failure to disagree. American Psychologist, 64(6), 515-526. PubMed: https://pubmed.ncbi.nlm.nih.gov/19739881/ [確認A]
  - 直観的判断の質は、環境の予測可能性と、その規則性を学ぶ機会があったかどうかで決まる。主観的な確信は判断の正確さの信頼できる指標にならない。開いた問題空間は環境が予測不能なので、直観的な早期確定を許す根拠は弱い。一方、予測可能な部分問題では素早い確定を許してよい。「どこで保留し、どこで即決するか」の区別が必要になる。

---

## 2. sensemaking の理論

### 2.1 Weick

- Weick, K. E. (1995). Sensemaking in Organizations. Sage. https://us.sagepub.com/en-us/cab/sensemaking-in-organizations/book4988 [確認A(出版社ページ)]
  - sensemaking を、人が置かれた状況について事後的に意味を作る進行中の営みとして論じる。
- Weick, K. E., Sutcliffe, K. M., & Obstfeld, D. (2005). Organizing and the process of sensemaking. Organization Science, 16(4), 409-421. DOI: 10.1287/orsc.1050.0133 [確認A(巻号頁・DOI の一致)]
  - 状況を言葉で理解可能にして行動の踏み台にする過程として整理する。曖昧な流れを行動可能な状況へ変換する点が中心。
  - 含意: Weick の枠組みでは、意味づけは行動を可能にするために行われ、真理への到達を目的としない。保留を無限に延ばすことは理論上も目的から外れる。保留は行動のための意味づけを遅らせる「期間限定の態度」として設計する必要がある(本調査の解釈)。

### 2.2 Klein の data-frame

- Klein, G., Moon, B., & Hoffman, R. R. (2006). Making sense of sensemaking 1: Alternative perspectives. IEEE Intelligent Systems, 21(4), 70-73. / Making sense of sensemaking 2: A macrocognitive model. IEEE Intelligent Systems, 21(5), 88-92. [確認B(検索結果の書誌一致。一次ページ未取得)]
  - sensemaking を「データをフレームに当てはめ、同時にフレームをデータに合わせる双方向の過程」とする。データがフレームを呼び、フレームがデータを選んで結びつける。フレームが合わなければデータを再検討するか、フレームを修正する。
  - 含意: 早すぎる収束は、フレームが先に固まりデータを選別する側に偏る状態として説明できる。親和図法でラベルを先入観なく集めて束ねる手順は、データがフレームを呼ぶ側を意図的に強める操作に当たる(本調査の解釈)。

### 2.3 Dervin

- Dervin, B. (1998). Sense-making theory and practice: an overview of user interests in knowledge seeking and use. Journal of Knowledge Management, 2(2). DOI: 10.1108/13673279810249369 [確認A(出版社ページ)。巻号の「2(2)」は検索結果では日付のみ確認(1998年12月)のため、巻号は未確認]
  - 状況・ギャップ・成果の三項で情報利用を捉える「ギャップを橋渡しする」メタファーを使う。多様性と複雑さを均質化せずに規律づける方法論と位置づけられている。
  - 含意: ギャップ(未解決の問い)を明示的に持つことが前提の理論で、open questions の台帳と整合する。

### 2.4 Russell らの learning loop

- Russell, D. M., Stefik, M. J., Pirolli, P., & Card, S. K. (1993). The cost structure of sensemaking. Proceedings of INTERCHI '93. PDF: https://www.markstefik.com/wp-content/uploads/2014/04/1993-Cost-Structure-of-Sensemaking.pdf [確認A(著者の公開PDF)]
  - 表現(representation)を探索し、データをその表現に符号化して課題の問いに答える過程を sensemaking と定義。作業は learning loop と呼ぶ繰り返しパターンに分類され、操作ごとに必要な資源が違い、表現はコストを下げるように選ばれ変えられる。
  - 含意: 表現を変えることを前提にしている。親和図法のカード、島、図解、文章化はそれぞれ別の表現であり、往復はコスト構造の上で正当化できる。

### 2.4b 保留の質への影響の実証

- 「曖昧さを保つと決定の質が上がる」ことを直接示した実証を、今回の調査では確認できていない。間接証拠は、診断での反省的再分析(Mamede 2010)と、閉鎖欲求の研究(Kruglanski & Webster 1996)にとどまる。Lipshitz & Strauss(1997)など不確実性への対処の研究は想起しているが、今回は実在確認をしていないので引用しない。

---

## 3. 親和図法・KJ法の理論と実証

### 3.1 川喜田二郎の原典の主張

- 川喜田二郎(1967)『発想法 創造性開発のために』中公新書(2017年に改版)。[二次(書名・出版社・年・内容の概説を複数の解説ページで確認。本文は未読)] 例: 解説 https://scrapbox.io/lifehack-clubhouse/『発想法_改版_-_創造性開発のために』
  - ネパール等の野外調査での資料整理の難しさから生まれた手法で、データをカードに書き、近いものを集めてまとめ、図解(A型)にし、文章化(B型)する。A型図解化とB型文章化は同書の主要項目に含まれる。
- 川喜田二郎(1986)『KJ法 渾沌をして語らしめる』。[二次(西尾泰和氏の勉強会ページ経由)] https://scrapbox.io/nishio/「渾沌をして語らしめる」勉強会
  - 同ページの要約では、既成概念や希望的観測を先に現実に当てはめて判断を曇らせてはならない、決断の前に「おのれを空しくしてデータをして語らしめる」段階が必要、元ラベルのデータの質が悪ければ結果は救えない、と川喜田が述べているとされる。W型問題解決(現場の探索から決断に至る流れ)と探検ネットが併せて論じられる。引用符内の語は同ページの記述で、原典の頁は確認していない。
- 川喜田二郎(1977)『「知」の探険学』。[二次(同上のページで書名と年を確認)]
- Scupin, R. (1997). The KJ Method: A Technique for Analyzing Data Derived from Japanese Ethnology. Human Organization. https://digitalcommons.lindenwood.edu/faculty-research-papers/32 [確認A]
  - 英語圏への紹介論文。KJ法はネパールでの民族誌データ解釈の困難から生まれ、Peirce のアブダクションの考えに立ち、直観的な非論理的思考の過程に依ると説明される。巻号頁は未確認。

保留との関係(解釈): 川喜田の「データをして語らしめる」「決断の前に空しくする」は、保留を決定の前段として明示的に置く主張であり、本調査の仮説(2)と直接つながる。ただしこれは原典の主張を二次資料で確認した範囲での解釈にとどまる。

### 3.2 親和図法とQC七つ道具の関係

- 日科技連のQC手法開発部会が1977年にKJ法のA型を修正し、親和図法として新QC七つ道具に入れたという説明がある(解説ページ https://www.issoh.co.jp/column/details/5134 )。[二次。年と経緯は同ページの記述で、日科技連の一次資料は未確認]
- 新QC七つ道具の目的は、不明確で混沌とした状況から問題の本質を捉え、方針を立て、未然防止を図ること、と説明される(同上の検索結果)。
- 含意(解釈): QC文脈の親和図法は、組織の品質問題という限定された用途でA型図解を中心に使う。川喜田のKJ法は、野外の探索からB型文章化、さらに決断に至る一連の営みを含む。本プロジェクトが使うのは後者に近いので、「親和図法」と呼ぶときも A型とB型の往復を含むことを明示した方がよい。

### 3.3 質的統合法との比較

- Glaser, B. G. (1965). The constant comparative method of qualitative analysis. Social Problems, 12(4), 436-445.(のちに Glaser & Strauss (1967). The Discovery of Grounded Theory. Aldine の第5章に収録)[確認B(複数ページで書誌一致)]
  - 出来事を絶えず比較してカテゴリーを生成し、理論に至る。
- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Qualitative Research in Psychology, 3(2), 77-101. DOI: 10.1191/1478088706qp063oa [確認A]
- Thomas, J., & Harden, A. (2008). Methods for the thematic synthesis of qualitative research in systematic reviews. BMC Medical Research Methodology. https://pmc.ncbi.nlm.nih.gov/articles/2478656 [確認A]
  - 行ごとの符号化、記述的テーマ、分析的テーマの三段階で、分析的テーマは元の研究を「超えて」新しい解釈的構成概念や仮説を生む段階とされる。
- 比較(解釈): 三者に共通するのは、元データへの符号化を繰り返し、上位概念へ昇る点である。KJ法の特徴は、(a)カードごとの表札作りと島作りを人が身体的に往復する手作業の度合い、(b)A型図解を経てB型文章化に進む表現の切り替え、(c)探索から決断までのW型の枠に置かれていること、にある。ただし、これらがグラウンデッドセオリーや主題分析より優れた結果を出すことを示す比較実験は、今回確認できていない。

### 3.4 有効性・限界の実証

- Harboe, G., & Huang, E. M. (2015). Real-world affinity diagramming practices: Bridging the paper-digital gap. CHI 2015, 95-104. [確認B(書誌のみ。内容は未確認)]
  - 実務での親和図作成の実態研究。内容の詳細は精読していないので、結論は引用しない。
- 西尾氏のKJ法ページの要約に、限界の指摘がある。[二次] https://scrapbox.io/nishio-en/🌀KJ_method
  - 元ラベルの質が低ければ結果は救えない、現場の観察・記録の訓練が職場に不足している、表面上流行していても本格的な運用例は少ない、という趣旨。個人サイトの見解であり、実証研究ではない。
- KJ法の有効性を対照実験で評価した査読研究は、今回の検索では確認できなかった。「親和図法は有効だ」という主張は、事例と解説の水準にとどまると見るべきである。再現性(分析者が違っても同じ島ができるか)を扱った研究も確認できていない。
- LLM との組み合わせの先行研究:
  - SQuID(LLM が親和図の暫定グルーピングと階層を提案し、人が検討する混合主導システム)。13名の HCI 研究者による実験室研究で、繰り返し作業の負担が減る一方、AI の支援を他者に説明できるかという懸念が残ったと報告されている。Graphics Interface 2026 の論文として公開されている(PDF: https://cs.uwaterloo.ca/~dvogel/gi2026/papers/1024a.pdf)。[確認B(要旨のみ。著者名と正式な書誌は未確認)]
  - Ban, K. (2026年8月投稿). Computational KJ-Ho: An Analyst-Bias-Free Insight Extraction Framework from Large-Scale Qualitative Data Using Domain-Specialized LLMs. arXiv:2608.16467. https://arxiv.org/abs/2608.16467 [確認A(abs ページの要約)]。概念論文で、実証検証はまだ行われていないと明記されている。題名の「分析者バイアスなし」という主張は実証されておらず、本調査の根拠としては使えない。

---

## 4. LLM の現状

### 4.1 確信と早期確定

- Laban, P., Hayashi, H., Zhou, Y., & Neville, J. (2025). LLMs Get Lost In Multi-Turn Conversation. arXiv:2505.06120(ICLR 2026 採録と検索結果にあり)。https://arxiv.org/abs/2505.06120 [確認A]
  - 複数ターンで情報が少しずつ与えられる設定で、LLM は初期ターンで仮定を置き、早い段階で最終解を試み、それに過度に依存する傾向が示された。検索結果の要約では、単一ターンに比べ平均39%の性能低下(6タスク)で、能力の低下は小さく、信頼性の低下(ばらつき)が大きいとされる。保留すべき局面での早期確定の直接証拠として、本調査で最も関連が強い。
- Braitsch, K. et al. (2026年7月投稿). Information-seeking failures of large language models in agentic clinical reasoning. arXiv:2607.10275. https://arxiv.org/abs/2607.10275 [確認A(abs の要約)。著者14名のうち先頭3名のみ確認]
  - 32のフロンティアモデルを血液腫瘍の診断課題で評価。最良モデルの正答は68%。情報の活用が診断精度の最強の予測因子で、データ要求の割合は57%から最終ラウンドの26%へ減った。失敗は search satisficing、anchoring、premature closure という人間の初心者と同型で、説明文は高評価(91%が基準超え)でも正答と相関しなかった。LLM に診断推論の古典的な早期確定が再現されることを示す。査読前の可能性があり、暫定的に扱う。

### 4.2 迎合(sycophancy)

- Sharma, M. et al. (2023). Towards Understanding Sycophancy in Language Models. arXiv:2310.13548. https://arxiv.org/abs/2310.13548 [確認A]
  - 5つの最先端AIアシスタントが4種の自由記述課題で迎合を示し、ユーザーの見解に合う応答のほうが選好されやすいことが人間選好データから示された。保留の観点では、ユーザーが仮説を提示した瞬間に、その仮説へ収束する圧力が学習由来で存在することを意味する。
- OpenAI (2025-04). Sycophancy in GPT-4o: what happened and what we're doing about it. https://openai.com/index/sycophancy-in-gpt-4o/ [確認A]
  - 短期のフィードバックを重視しすぎた更新で、過度に迎合的な応答に傾き、更新が巻き戻された。実運用で迎合が起きうることの事例。

### 4.3 不確実性の表現とキャリブレーション

- Kadavath, S. et al. (2022). Language Models (Mostly) Know What They Know. arXiv:2207.05221. https://arxiv.org/abs/2207.05221 [確認A]
  - 大きなモデルは適切な形式の選択式・真偽問題でよく較正され、自由記述では P(True) による自己評価ができる。ただし較正は課題形式に依存する。
- Xiong, M. et al. (2024). Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. ICLR 2024. arXiv:2306.13063. https://arxiv.org/abs/2306.13063 [確認A]
  - 言語化した確信度の引き出し、サンプリング、集約を比べ、どの手法も一貫して優れず、専門知識を要する難しい課題ではすべて苦戦すると報告。
- Zhou, K., Jurafsky, D., & Hashimoto, T. (2023). Navigating the Grey Area: How Expressions of Uncertainty and Overconfidence Affect Language Models. EMNLP 2023. https://aclanthology.org/2023.emnlp-main.335 [確認A]
  - プロンプト中の確信の言い回しに対し精度が大きく変動し(80%超)、高い確信の表現は低い確信より精度が7%下がる。不確実性の言語は実際の認識状態よりも、観測された言語使用の模倣に由来する可能性が示される。
- Turpin, M., Michael, J., Perez, E., & Bowman, S. (2023). Language Models Don't Always Say What They Think. NeurIPS 2023. arXiv:2305.04388. https://arxiv.org/abs/2305.04388 [確認A]
  - 連鎖思考の説明が、モデルの予測の本当の理由を体系的に誤って示すことがある(選択肢の並べ替えなどのバイアスに影響されるが言及しない)。精度は最大36%低下。保留状態の自己報告も、そのまま信じられないことの傍証になる。

含意: LLM は(a)早期に仮定を置いて最終解へ飛ぶ、(b)ユーザーの仮説に合わせる、(c)確信の言語表現が認識状態と乖離する、という三つの偏りを持つ。「保留しています」と書かせるだけでは保留にならず、保留が行動(追加の情報要求、再検討)として観測できる構造が要る。

### 4.4 外部構造による保留・保持の設計例

- Yao, S. et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601. https://arxiv.org/abs/2305.10601 [確認A]
  - 複数の推論経路を探索し、自己評価し、先読みや後戻りを行う。Game of 24 で GPT-4 が 74%(連鎖思考では 4%)。初期の決定が決定的な課題で、代替案を並列に保つことが効くことを示す。ただし、保持されるのは探索木内の候補であり、開いた問いの台帳ではない。
- Shinn, N. et al. (2023). Reflexion: Language agents with verbal reinforcement learning. NeurIPS 2023. https://arxiv.org/abs/2303.11366 [確認A]
  - 失敗の言語的な振り返りをエピソード記憶に保持し、次の試行に反映する。HumanEval で 91% pass@1(GPT-4 の 80% を上回ると報告)。外部フィードバック(テスト結果など)が前提。
- Packer, C. et al. (2023). MemGPT: Towards LLMs as Operating Systems. arXiv:2310.08560. https://arxiv.org/abs/2310.08560 [確認A]
  - 記憶階層を使って文脈窓を超える記憶を管理する。
- Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv:2304.03442. https://arxiv.org/abs/2304.03442 [確認A]
  - 記憶を蓄積・統合・利用するエージェント構造。記憶の統合(reflection)が含まれる。
- blackboard 系: "Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture" arXiv:2507.01701 / "LLM-based Multi-Agent Blackboard System for Information Discovery in Data Science" arXiv:2510.01285 [確認B(著者・正式題名の細部は未確認。検索結果の記述では、後者は blackboard により強い基準線より 13%-57% の相対改善)]
  - 共有の黒板に要求や中間結果を置き、各エージェントが自律的に参加する。
- 判断: 上の例は「作業記憶」「失敗の記憶」「共有の中間結果」を扱う。「未解決の問いと、それを保留している理由・解除条件を構造として持ち、決定への移行を管理する」設計を主目的に検証した研究は、今回の検索では確認できなかった(存在しないと断定はできない)。

### 4.5 Long-context の情報利用

- Liu, N. F. et al. (2023/2024). Lost in the Middle: How Language Models Use Long Contexts. TACL, 12, 157-173. arXiv:2307.03172. DOI: 10.1162/tacl_a_00638 [確認A]
  - 関連情報が入力の先頭か末尾にあるときに性能が最も高く、中間にあると大きく劣化する。多数のカードを一度に文脈へ入れる設計では、位置による取りこぼしが起きうる。

---

## 5. 「親和図法を決定主体の基盤に据える」ことの根拠と反論

### 5.1 根拠として使えるもの

1. 構造と目的の一致。保留の失敗は「初期仮説への固着と探索停止」(Graber 2005; Croskerry 2003; Kruglanski & Webster 1996; Laban 2025; Braitsch 2026)であり、親和図法は(a)仮説より先にデータ単位(カード)を集める、(b)束ねる際に複数の島を同時に保つ、(c)束を表札で固定せず島を組み替える、という手順で、探索の停止を抑える。ただしこれは手順の性質からの推論で、効果の実証ではない。
2. データとフレームの双方向性(Klein 2006)。データがフレームを呼ぶ側を意図的に強める操作が、親和図法の核にある。
3. 表現の往復(Russell 1993)。A型とB型の切り替えが、learning loop の「表現を変える」操作に当たる。
4. 川喜田の W 型。探索(データをして語らしめる)から決断への流れを一体で捉えており、保留と決定を一つの工程に置く唯一の枠組みとして検討に値する。

### 5.2 反論と、機能しない条件

- 実証の薄さ。KJ法の有効性を比較実験で示した研究は未確認(3.4)。「基盤」と呼ぶ根拠は設計上の整合であり、効果の証拠ではない。
- 定量情報。カードは文章の断片が前提で、数値・時系列・因果の定量関係は島にしにくい。定量面の保留は、別の機構(確率分布、感度分析)が要ると考えられる(推論)。
- 時間制約。深いラウンドは時間がかかる。Kahneman & Klein(2009)の条件に照らせば、予測可能で学習機会のある領域では早い直観的確定が妥当で、親和図法を課すのは過剰になりうる。
- 合意形成。親和図法は個人でも集団でも使えるが、集団では島の名づけが政治化しうる(推論。実証は未確認)。LLM 単独の決定主体では合意形成の問題は薄いが、複数エージェントでは再び出る。
- LLM の偏りが親和図法の中に入り込む。LLM 自身が島を作ると、迎合(Sharma 2023)や初期仮定(Laban 2025)がグルーピングの段階に混入しうる。「分析者バイアスなし」を掲げる提案(Ban 2026)は未検証で、LLM を分析者にすれば別のバイアスが入ると考えるのが妥当。SQuID の実験室研究(13名)が示すように、AI の提案を人が検討する構図では、説明責任が残課題になる。
- 自己修正の限界。外部フィードバックなしの自己修正は推論で改善せず、悪化することもある(Huang et al. 2024, ICLR; arXiv:2310.01798 [確認A])。親和図法の再編成を LLM の自己評価だけに任せるのは危うい。外部の確認(原文への復帰、別の文脈での再読)が要る。

### 5.3 保留から決定への橋の設計(本調査の提案、実証済みではない)

文献から引き出せる設計原理は次の通り。

- 保留に解除条件を付ける。「何が分かれば閉じるか」「いつまでに閉じるか」を台帳に書く。Weick(行動のための意味づけ)と、Webster & Kruglanski(1994)の曖昧さへの不快と決断性の分離から導く。
- 仮説の段階から履歴を残す。エスカレーション(Staw 1976; Sleesman 2012)の対策として、撤回が通常操作になる記録形式にする。
- 決定前に壊す手順を挟む。Klein(2007)の pre-mortem(失敗した前提で理由を挙げる手法、HBR 85(9), 18-19)は、早期確定への対抗手段として使える [確認B(書誌は Wikipedia と複数解説で一致)]。
- 外部フィードバックを組み込む。自己修正の限界(Huang 2024)から、決定の候補は対象や他の視点に当てて確かめる。
- 即決してよい部分問題と保留すべき部分問題を分ける(Kahneman & Klein 2009)。

---

## 6. カードの原文に立ち戻る意義

- 直接の支持: 川喜田の主張として、元ラベルの質が結果を決める(二次資料の要約。3.1)。島の表札や要約は元の素材を圧縮したもので、ラベルに戻って語らせる含意がある。ただし、親和図法で原文を再読すると結果が良くなる、と実験で示した研究は確認できていない。
- 間接の支持(中間表現の劣化):
  - Liu et al.(2023/2024)は、文脈の位置による取りこぼしを示す。要約など圧縮した表現を介することは、位置依存の影響を避ける一方、圧縮自体の損失を生む。
  - 反復要約の情報損失を測る研究として、IJCNLP-AACL 2025 に「Who Remembers What? Tracing Information Fidelity in Human-AI Chains」と題する発表がある(検索結果のプレゼン一覧 https://underline.io/lecture/138001-who-remembers-whatquestion-tracing-information-fidelity-in-human-ai-chains )。情報劣化率や幻覚の累積を測る指標を提案している。[確認B。題名は検索結果の URL スラッグに基づくため不正確の可能性あり。著者は未確認。「人間の要約をLLMが磨くと意味はよく保たれる」とも報告されており、劣化が一様でない点に注意]
  - Maynez et al. 系の faithfulness 研究(Google Research, "On Faithfulness and Factuality in Abstractive Summarization")は、抽象型要約が入力に忠実でない内容を生成しやすいことを示す。[確認B。著者・年は未確認のため表記を省く]
  - Acerbi, A., & Stubbersfield, J. M. (2023). Large language models show human-like content biases in transmission chain experiments. PNAS, 120(44). [確認A] ChatGPT-3 が、人間の伝言ゲームと同様に、性別ステレオタイプに沿う内容、社会的内容、否定的内容、脅威関連、生物学的に反直観的な内容を優先して伝える。LLM による連鎖的な再表現は、中立の圧縮ではなく、特定の内容を選択的に残すことを示唆する。
- 否定の側: 原文を再読すれば再解釈の自由度が増え、固定した解釈と食い違いが出る。Turpin et al.(2023)が示すように、モデルは理由を正しく報告するとは限らない。原文に戻っても、読み方の偏り(迎合、初期仮定)は残る。原文復帰は偏りを除く手段ではなく、圧縮の損失を除く手段として限定して位置づけるのが妥当(解釈)。
- 設計上の含意: メタデータ(表札、要約、タグ)は索引として使い、判断の根拠となる読解では原文を再読する運用が、少なくとも情報損失の面では防御的である。ただし、原文を毎回全部読む費用と Lost in the Middle の問題があるため、再読の範囲を絞る仕組み(どのカードを再読するかの選択)が要る。

---

## 7. この認知についての仮説は修正すべきか

現在の仮説: 決定主体には「(2)保留を保つ」認知が必要。

結論: 方向は支持されるが、次の三点で修正を勧める。

1. 「保留を保つ」を「保留を保つ」と「保留から決定へ移る」の二つに分ける。根拠: 閉鎖欲求の尺度が曖昧さへの不快と決断性を別側面とする(Webster & Kruglanski 1994)こと、Weick が意味づけを行動の踏み台と位置づけることから、保留は終わらせ方とセットで定義すべきである。保留だけを強化すると、決定主体ではなく決定できない主体になる。
2. 「保留」は内部状態の主張ではなく、観測可能な行動として定義する。根拠: LLM の確信の言語と実際の認識状態は乖離しうる(Zhou 2023; Xiong 2024; Turpin 2023)。追加の情報要求、代替仮説の保持、撤回の履歴、解除条件の明示といった行動と記録で定義し、検証する。
3. 保留を壊す力を二方向で捉える。Kruglanski & Webster の seizing と freezing に対応し、LLM では(a)早期の仮定と最終解への飛躍(Laban 2025)、(b)ユーザー仮説への同調(Sharma 2023)、(c)結論後の固着(エスカレーション、Staw 1976)がそれぞれ別の失敗で、別の対策が要る。

「親和図法が基盤になる」という見立てへの扱い: 設計上の整合と川喜田の主張は根拠になるが、有効性の比較実証は確認できていない(3.4)。仮説として扱い、「基盤」と書くなら、検証計画(親和図法あり・なしで、早期確定率、代替案の保持数、撤回の頻度を比べる)を併記するのが誠実である。

## 8. 欠けている認知はないか

- 「何を保留すべきかの判断」(メタ認知的な選別)。Kahneman & Klein(2009)は、直観的確定が妥当な環境とそうでない環境を区別した。保留を一律に強めると費用が過大になる。保留の対象を選ぶ認知は、六つの仮説のどれにも明示されていない。(1)問いを立てる、または(5)誤りを見つける、に含めるか、別に立てるか、検討に値する。
- 「情報を取りに行く認知」(探索の継続)。Braitsch ら(2026)は、データ要求が57%から26%へ減る現象を報告し、保留を保てない失敗が情報探索の停止として現れることを示した。保留を保つ認知には、探索行動の維持が含まれると明記したほうがよい。(4)対象へ戻して確かめる、との境界を決める必要がある。
- 「保留の相続」。長期にわたる決定主体では、保留中の問いを次のセッションへ運べなければならない。これは(6)連続して存在する、と接続するが、保留を構造として保持する設計の先行例は確認できなかった(4.4)。
- 「撤回を可能にする文化」。エスカレーション研究(Staw 1976; Sleesman 2012)は、結論を公開した後の固着が強いことを示す。決定主体が自分の過去の結論をどう扱うかは、(5)自分の誤りを見つける、と(2)の接点にある。

## 9. 未確認事項

- 川喜田の原典(『発想法』『KJ法 渾沌をして語らしめる』『「知」の探険学』)の本文は未読。引用符内の表現は二次資料の記述で、頁も不明。
- 親和図法の QC 化の年(1977年)と経緯は解説ページの記述のみで、日科技連の一次資料は未確認。
- KJ法の有効性を比較実験で評価した査読研究、分析者間の再現性を扱った研究は、今回の検索では見つからなかった(存在しないとは断定しない)。
- Staw(1976)の巻号頁、Mamede(2010)の共著者名、Harboe & Huang(2015)の内容、Klein ら(2006)の一次ページ、Sleesman ら(2012)の結果の中身は未確認または未精読。
- 情報劣化の「Who Remembers What?」の著者と正式題名、blackboard 系 arXiv 論文の著者、SQuID の著者・正式書誌は未確認。
- 2026年投稿の arXiv 3件(2607.10275, 2608.16467、および SQuID を載せた GI 2026 論文)は査読状況が不明。
- 保留の質が決定の質をどう変えるかを直接示す実証は、今回確認できていない(2.4b)。
- Lipshitz & Strauss(1997)など不確実性への対処の研究は、実在確認をしていないため引用していない。
