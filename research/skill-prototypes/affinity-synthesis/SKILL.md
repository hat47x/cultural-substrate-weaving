---
name: affinity-synthesis
description: Integrates heterogeneous source material bottom-up into traceable meaning-bearing cards, emergent groups, relational structure, and narrative, then checks each transformation back against the source. Use when the structure should emerge from the material rather than a predefined taxonomy, and when preserving contradictions, epistemic seams, provenance, and residuals matters. Do not use for simple fixed-category sorting, ordinary summarization, or multi-round inquiry orchestration.
---

# Affinity Synthesis

多数または異種の材料から、分析者が先に分類体系を置かずに構造を立ち上げる。

このSkillは一回の統合ラウンドを担当する。材料の再収集、次の問いの決定、複数ラウンドの進行管理は担当しない。

KJ法、親和図法、質的統合法の系譜を参照しつつ、生成AIで起きやすい過剰細分化、流暢な上書き、来歴消失、派生物の二重計上を防ぐための補正を加えた realization である。特定の伝統的方法の公式実装や完全な再現を称しない。

## When to Use

次の条件が重なるときに使う。

- 記事、発言、観察、メモ、資料、仮説など、粒度や証拠状態の異なる材料を統合したい。
- 正しい分類軸が事前には分からず、材料側からまとまりを立ち上げたい。
- 単なるテーマ一覧ではなく、束どうしの関係と、それを読んだ叙述まで必要である。
- 元材料へ戻れることが重要である。
- 孤立、対立、弱い違和感、未解決を消さずに扱いたい。

## When NOT to Use

次の場合は、このSkillを優先しない。

- 固定taxonomy、法定分類、既知カテゴリへの仕分けが目的である。
- 数個の項目を単純に要約・整形すれば足りる。
- 多数の既存項目を創発テーマへ束ねるだけでよく、関係図解・叙述・戻し検査までは不要である。この場合は専用のAffinity Mapping Skillを優先できる。
- 完成した主張をEvidence / Inference / Assumptionへ分類監査すること自体が目的である。
- 追加検索、問いの変更、複数ラウンドの継続判断を含む探索全体を管理したい。この責務は反復探索統合側に置く。

項目数だけで適用可否を決めない。少数でも、一つの意味の境界や対立を丁寧に統合する必要があれば適用できる。

## Core Contract

### 1. Cluster before naming

束の名前を先に作らない。先に材料を読み、互いに訴えの近いものがあるかを見る。

分類名が先に浮かんだ場合は、それを仮置きせず、いったん材料へ戻る。

### 2. Preserve meaning-bearing units

カードは「最小の事実断片」ではなく、単独で何を訴えているか読める意味単位とする。

境界は長さで決めない。

- 一つの体験・判断・因果の運動として不可分なら、機械的に切らない。
- 観察と解釈、確認と推測、本人の発言と第三者の意味づけなど、証拠状態が切り替わる継ぎ目では分ける。

**意味の一体性を守るためには結合し、証拠状態を守るためには分割する。**

### 3. Keep provenance audit separate from grouping geometry

各カードは必要に応じて元材料へ戻れる参照を保つ。

少なくとも、区別が必要な場合は次を混同しない。

- source provenance: 内容がどこから来たか。
- discovery route: その資料をどの経路で見つけたか。
- derivation: 他のカードや統合物から派生したか。

これらのメタデータを、最初の束ねの分類軸にはしない。

同じ出来事の転載、同じ元カードから派生した複数カード、同一資料の再紹介を、独立した複数の支持として数えない。

### 4. Group by what the cards are saying

訴えの近いカードを小さく集め、必要なら段階的に上位へ統合する。

固定の束サイズや最終テーマ数へ合わせない。

どの束にも入らないカードは残す。対立するカードを、上位概念へ丸めて同じ意味にしない。

現在の表札や構造に合わない材料を、単にnoiseとして扱わない。入力済み材料の中に反証的・矛盾的なcardがないかを意図的に再確認する。追加の反証資料を外部へ探しに行く必要がある場合は、次roundの探索へ渡す。

clusterの大きさや同じ表現の反復は、それ自体ではtruth、importance、independent supportを意味しない。必要ならlineageと独立性を確認する。

一枚のカードが複数の束へ意味上響く場合、実装上必要なら次を区別してよい。

- **primary placement**: 現在のworking geometryで最も強く寄る主配置。
- **secondary resonance**: カードを複製せず、別の束・関係にも響くことを示すcross-link。

secondary resonanceは新しいカードでも独立supportでもない。cluster sizeやsupport countを増やさない。主配置を必ず一つ持つこと自体もMethod Definitionの絶対条件にはしない。

全カードが綺麗に既存groupへ入った場合ほど、borderline memberが分類名の力で押し込まれていないかを戻し検査する。

### 5. Form labels by integration, not categorization

表札はカテゴリ名ではなく、その束が共同して言おうとしていることの代弁とする。

表札づくりが難しい場合は、次の操作を使う。

1. 各材料が何を失えば同じ意味でなくなるかを見て、核を短く取る。
2. 元材料をいったん視野の外へ置き、核だけを同時に見る。
3. 核どうしを接続詞で連結するのではなく、一つの新しい意味単位として立つ文を作る。
4. 元材料を再び開き、歪みを直す。

元材料を伏せる操作は、分析者の語彙が入り込む危険も増やす。したがって戻し検査を省略しない。

### 6. Check every synthesis back against source

カード、表札、上位表札、叙述を作った後は、入力へ戻す。

特に次を点検する。

- 元にない因果を足していないか。
- 人物の内面や意図を補っていないか。
- 一事例を一般化していないか。
- 評価の向きを変えていないか。
- 推測を断定へ、伝聞を確認済み事実へ変えていないか。
- 行為者や責任の向きを落としていないか。
- 材料を弱める、ぼかす、断定を不用意に下げるなど、意味の方向を変える編集をしていないか。
- 材料に固有の温度、身体感覚、場面、両義性を不要に消していないか。

この一覧は閉じた分類表ではない。戻したときに材料側から「違う」と返るものを探す。

変換後は必要に応じて、意味を次のように監査する。

- **inherited**: 入力材料から直接保持された意味。
- **emergent**: 複数材料の接触で新しく立った意味。創発は許容するが、元材料が最初から述べていたことへ遡及させない。
- **residual**: 統合へ入れなかった差、矛盾、温度、未解決。

これは入力カードを先に三分類する規則ではなく、**統合した後に変換で何が起きたかを見る検査**である。

### 7. Build relational structure after grouping

安定した束・表札を、関係のある位置へ置く。

必要に応じて、因果、相互作用、対立、時間の前後、条件、循環などを区別する。ただし関係名を先に用意して束を従わせない。

関係を主張する場合は、後から `source - relation - target` の意味を読み返して検査できる程度に明示する。すべての近接を命題化する必要はないが、何を意味する線なのか不明なまま強い関係を主張しない。

明示的なrelationを置いた場合は、少なくとも一度、endpoint + predicate + directionを自然な一文へ戻して読む。文として不自然、向きが逆、またはbasisへ戻ると支えられない場合は、線を保つためにpredicateを作文しない。stateを弱める、relationを撤回する、またはまだ気になる接続をquestionable relation candidateとして`Q`へ戻す。

「この二つには何か線がありそうだ」という段階はrelation assertionではない。layout上の近接、secondary resonance、叙述で生じた違和感だけを根拠に`R`へ昇格させず、何があれば支持・反証できるかを問いとして残せる。

結ばれない束、広い空白、片側だけに伸びる関係は、そのまま観察する。空白から推測した内容を事実として埋めない。

#### Representation rule

成果物へ外在化するときは、少なくとも次を区別する。

- **membership**: card / lower groupがgroupを構成する。
- **explicit relation**: 二つの意味単位の間に、読み返せるpredicateを置く。
- **secondary resonance**: membershipや独立supportを増やさず別groupにも響く。
- **layout**: 図での近接・離隔・上下左右・囲み等。

relationを固定edge-type taxonomyへ押し込めず、短い自然言語predicateとして残す。方向は `-> / <-> / --` 等で別に表せるが、`->` 自体を因果と解釈しない。

compact notation、inventory table、machine-readable JSON、diagram projectionの標準候補は `references/REPRESENTATION.md` を読む。

### 8. Narrate from the relational structure

図解・関係構造を読んで文章化する。

文章の流暢さを優先して、図にない因果や順序を補わない。

叙述によって新しい関係が見えた場合は、それを完成済みの洞察として採用せず、図解と元材料へ戻して確かめる。

### 9. Cross-check source, map, and narrative

最終化の前に少なくとも三方向を見る。

- **source → synthesis**: 元材料の重要な訴えが落ちていないか。
- **synthesis → source**: 統合側が元材料にない意味を発明していないか。
- **map ↔ narrative**: 図解にある関係が文章で落ちていないか、文章だけに新しい関係が増えていないか。

差分がゼロであることを成功条件にしない。差分があれば理由を明示し、支持された修正か、emergent meaningか、residual / unresolvedかを区別する。

### 10. Render diagrams only as projections

図が有効な場合、semantic recordからdiagram projectionを作ってよい。

推奨view:

- **group relationship map**: 表札とexplicit relationを中心にしたoverview。
- **membership map**: group boundary、card membership、secondary resonanceの監査。
- **lineage map**: source → card → group / relation / narrative claim の来歴監査。
- **spatial map**: 近接、離隔、空白等、配置そのものを保持する必要がある場合。

Mermaidはtopology projectionに向く。自動layoutで元の空間配置が変わるため、配置自体に分析上の意味がある場合はMermaidだけを正本にしない。必要なら位置情報を別に保持し、自由配置できるformatへ投影する。

rendering toolが使える場合は、syntaxだけでなく視覚的な誤読も確認する。図の見栄えのためにsemantic relationを追加・削除・強化しない。

## Output Contract

成果物には、用途に応じて少なくとも次を追跡可能にする。

1. synthesis subject / question
2. source material references
3. meaning-bearing cards
4. groups and labels
5. singleton / tension / unresolved cards
6. relational structure with readable predicates where relations are asserted
7. membership / relation / secondary resonance / layout distinction when relevant
8. narrative synthesis
9. source ↔ synthesis ↔ narrative cross-check
10. inherited / emergent / residual meaning when transformation provenance matters
11. intentionally omitted differences or unresolved residuals
12. diagram projection and projection-integrity note when a figure is produced

特定の表形式やcanvas geometryを必須にはしない。標準形が必要な場合は `references/TEMPLATE.md` を使う。machine-readable interchangeやdiagram grammarが必要なら `references/REPRESENTATION.md` を使う。

## Quality Checklist

最終化前に確認する。

- [ ] group名を先に作らず、cluster before namingを守った。
- [ ] カードを文字数や一文一命題で機械的にatomic化していない。
- [ ] epistemic seamを跨いで事実と推論を一枚へ混ぜていない。
- [ ] provenance / discovery route / derivationを必要な箇所で追跡できる。
- [ ] 派生・転載を独立反復として二重計上していない。
- [ ] cluster sizeや反復数をtruth / importance / independent supportへ自動変換していない。
- [ ] singleton、対立、理由のまだ分からない違和感を消していない。
- [ ] 現在の表札・構造に合わない入力済みcardを見直した。
- [ ] 全カードが綺麗に収まった場合、borderline memberやsecondary resonanceを再確認した。
- [ ] secondary resonanceをカード複製・独立supportとして数えていない。
- [ ] membership / relation / resonance / layoutを混同していない。
- [ ] 表札が他の束にも載る一般カテゴリ名へ逃げていない。
- [ ] 強い表札名が弱い束のまとまりを隠していない。
- [ ] 元材料にない因果・内面・一般化・評価方向・確度変更を点検した。
- [ ] 材料の弱化、ぼかし、行為者脱落を点検した。
- [ ] emergent meaningを、元材料に最初からあった意味へ遡及させていない。
- [ ] 強い関係線は、その意味を後から読み返して検査できる。
- [ ] explicit relationをendpoint + predicate + directionの一文として読み返し、basisへ戻っても支持できることを確認した。
- [ ] questionable / missing relation candidateを、return-checkなしに`R`へ昇格させていない。
- [ ] relation predicateを、描画都合の固定edge typeへ不必要に縮めていない。
- [ ] 図解と叙述を相互に戻して確認した。
- [ ] diagramを作った場合、図だけに新しい線・包含・順序・重要度が増えていない。
- [ ] 自動layout上の近接をsemantic relationへ読み替えていない。
- [ ] 直接引用が必要な場合、実在する原文だけを引用し、モデルが引用文を創作していない。
- [ ] residual / gapを、存在確認済みの事実へ格上げしていない。

## Progressive References

必要なときだけ読む。

- 方法の不変条件と系譜: `references/METHOD.md`
- 書式・ID・relation grammar・machine-readable map・diagram projection: `references/REPRESENTATION.md`
- 標準成果物: `references/TEMPLATE.md`
- machine-readable schema候補: `references/affinity-map.schema.json`
- 評価・反例: `evals/CASES.md`
- 公開時の根拠と限界: `evidence/dossier.md`
