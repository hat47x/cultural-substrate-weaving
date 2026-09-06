# Affinity Synthesis Method Definition

Status: research candidate

## Purpose

異種・不揃い・相互に緊張を含む材料から、分析者が先に分類体系を置かずに意味単位と関係を立ち上げ、元材料へ戻しながら全体像を統合する。

方法の成果は、きれいなテーマ一覧そのものではない。材料から支持される構造と、なお残る孤立、対立、空白、未解決を、後から再検査できる形で残すことである。

## Lineage and scope

本方法はKJ法、親和図法、質的統合法の系譜から学ぶ。ただし、Agent Skill realizationには生成AI向けの独自補正を含むため、これら既存方法の公式実装または完全な再現とは位置づけない。

歴史的系譜と、現在の実装上の補正を混同しない。

### 系譜から保持する核

- 先験的な分類体系へ材料を押し込めず、材料側から構造を立ち上げる。
- ラベル／表札は単なるカテゴリ名ではなく、まとまりが訴えることを表す。
- 孤立した材料を無理に既存群へ入れない。
- 関係を空間・図解として外在化し、そこから叙述する。
- 統合結果を元材料へ戻して確かめる。

### 生成AI向け補正

- meaning-bearing unit と epistemic seam を同時に守るカード境界。
- source provenance と discovery route の分離。
- derivation lineage による二重計上防止。
- 流暢な補完で入りやすい因果、人物内面、一般化、評価方向、確度変更等の戻し検査。
- 図解と叙述の双方向差分検査。
- 変換後の意味を `inherited / emergent / residual` として監査し、新しい意味を元材料へ遡及させない。
- private chain-of-thoughtではなく、外部から再検査できる成果物・来歴・残差を残す。

## Applicability

適用しやすい場面:

- qualitative synthesis
- open-ended research
- heterogeneous document / note synthesis
- conflicting observations or accounts
- material-led structure discovery
- creative or analytical projects in which source texture and residual difference matter

適用しにくい場面:

- fixed taxonomy coding
- simple summarization
- deterministic classification
- tasks whose only need is bottom-up theme clustering
- tasks whose primary goal is recommendation ranking or decision authority

## Inputs

方法定義として許容する入力概念は広く保つ。

- source material
- observation
- quote / reported statement
- note
- document fragment
- prior meaning-bearing card
- explicit hypothesis or unresolved item, if its status remains visible

入力形式はJSON、Markdown、canvas、databaseなど特定の媒体へ固定しない。

## Outputs

- meaning-bearing card
- group / bundle
- label / higher-order meaning unit
- relational structure
- narrative synthesis
- singleton
- tension / conflict
- unresolved item
- gap-as-question
- provenance / derivation references
- cross-check result

`gap` は「実在する欠落要素」ではなく、「配置から見え、次に確かめる価値がある空所」を含む。そのため事実と同じ地位へ自動昇格させない。

## Invariants

### I1. Material-led structure

意味距離は材料内容から立ち上げる。出所、話者属性、陣営、カード種別、既存taxonomyを最初の grouping geometry にしない。

### I2. Meaning-bearing unit

カードは機械的に最小のfact fragmentへ分解しない。

一つの経験・判断・因果の運動が、分割すると意味の生命を失うなら一体として保つ。

### I3. Epistemic seam

観察／解釈、確認／推測、本人の発言／第三者の意味づけ等、認識状態の境界を黙って潰さない。

I2とI3が衝突する場合は、意味の一体性と証拠状態の双方を損なわない表現または分割を探す。

### I4. Same integration kernel across granularity

カード化、表札化、上位表札化、精選、意味重複整理は別々の根幹技術とみなさず、材料から意味単位を立てる同じ核操作を粒度を変えて用いる。

核操作:

1. 境界を見る。
2. 何を失えば同じ意味でなくなるかを見る。
3. 複数材料から一つの意味単位が立つ場合のみ統合候補を作る。
4. 元材料へ戻し、意味の発明・欠落・確度変化を確認する。

### I5. Cluster before naming

束が立つ前にテーマ名を先置きしない。

### I6. Label is advocacy, not class name

表札は、その束にしか載らない程度に具体的な訴えを持つ。一般カテゴリ名へ逃げない。

ただし「別束にも載れば即失格」のような機械判定にしない。可搬性は分類名へ退行していないかを見る警告である。

### I7. Return to source and audit transformation

各変換は元材料へ戻せる。戻したときに違和感があれば、その違和感を修正対象または残差として扱う。

変換後の意味は、必要に応じて次の三つを区別する。

- **inherited**: 入力材料から直接保持された意味。
- **emergent**: 複数材料の接触・配置・叙述によって新しく立った意味。創発そのものは許容するが、元材料が最初から述べていたことへ書き換えない。
- **residual**: 統合へ入れなかった差、矛盾、温度、未解決、または意図して落とした具体。

これはカードを先験的な三分類へ分ける規則ではない。**変換後に、何がどこから生じたかを監査するための区別**である。

### I8. Provenance is audit, not geometry

source provenance、discovery route、derivation、必要に応じた採取時点等は、監査と復元のために保つ。意味距離を決める先験分類にはしない。

### I9. No false independent repetition

同一資料の転載、同一出来事の再紹介、一つのカードから派生した複数カードを、独立した支持の反復として数えない。

独立corroborationとderivationを区別する。

### I10. Preserve singleton and conflict

どの束にも入らない材料、相反する材料、理由のまだ分からない違和感を、統合の完成感のために消さない。

### I11. Diagram and narrative remain mutually checkable

関係図解と叙述の一方だけを唯一の正本にしない。叙述で新しい関係が生じた場合は図解・材料へ戻し、図解で示した関係が文章で落ちた場合も確認する。

### I12. Residual is not failure

残差、空白、対立、未解決は、統合失敗の証拠とは限らない。現在の材料が語れる範囲を明示する成果物であり得る。

## Frequent AI failure modes

- 流暢な言い換えで材料固有の語感・温度を消す。
- 原材料にない因果を接続詞で補う。
- 行為者を落とし、選択を自然発生した出来事へ変える。
- 人物内面をもっともらしく補う。
- 推測・伝聞・仮説を断定へ上げる。
- 一つの vivid case を一般傾向へ変える。
- 派生カードを独立した多数意見のように扱う。
- 大きいclusterを重要・真実と同一視する。
- 表札の巧さで弱いgroup coherenceを覆う。
- 文章を整える過程で、図解にない論理を足す。
- 後のroundで生じた洞察を、最初のカードがすでに語っていた意味へ遡及させる。

## Relationship to external methods and skills

### Affinity Mapping / Affinity Diagramming

共通する中心操作は、predefined bucketsを避け、cluster before namingでまとまりを立てること。

本方法はそれに加えて、意味単位境界、証拠状態、上位意味統合、関係図解、叙述、戻し検査を一つのroundとして扱う。

したがって、単純なtheme clusteringだけが必要なら専用Affinity Mapping Skillへ委譲できる。

### Concept Mapping

概念化済みの項目間の関係を明示命題へする段階では補助的に利用できる。ただし、材料を早期にconcept nodeへ変換することを本方法の標準にはしない。

### Evidence / Inference auditing

完成した成果物の独立監査には利用できる。カードを作る前に全材料を閉じたclaim taxonomyへ入れることは本方法の標準にはしない。

## Realization boundary

Method Definitionは、特定のAgent Skill文面、モデル、プロンプト、ツール、UI、カード枚数、文字数、canvas geometryを所有しない。

Agent Skill realizationはこのMethod Definitionを満たす一つの実装である。

外部Skillが将来これらのinvariantsとevaluation fixturesを満たすなら、外部Skillをrealizationとして採用し、独自Skillを縮小または廃止できる。

## Separation from iterative inquiry

このMethod Definitionは一回の統合roundまでを所有する。

次の材料収集、次の問い、再検索、再開条件、round間の差分、停止判断は別の反復探索方法へ委ねる。
