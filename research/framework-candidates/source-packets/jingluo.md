# Jingluo source packet

Status: research-only / medical-tradition-sensitive / pre-profile

## 目的

Jingluo（経絡）を、main route / collateral / branching / route networkという認知構造として検討する前に、伝統医学上の体系記述と、現代の解剖学・生理学上の主張を分離する。

このpacketは診断・治療・医学的有効性を扱わない。

## Source layers

### 1. Classical text layer

Chinese Text Project, 《黃帝內經・靈樞經・經脈》

https://ctext.org/huangdi-neijing/jing-mai/zh

この章では十二経脈、絡脈、分岐・接続・走行が古典本文の中で記述される。CSWでは、**main route / collateral / branch / connection** という伝統内部のnetwork vocabularyを確認する一次資料層として使う。

Chinese Text Projectには現代英訳表示もあるが、その英訳自体を権威的翻訳として採用しない。中国語本文、底本情報、影印参照を主たる根拠とし、現代語への要約はCSW側のde-bindingとして明示する。

### 2. Institutional terminology standards

World Health Organization, WHO international standard terminologies on traditional Chinese medicine (2022)

https://www.who.int/publications-detail-redirect/9789240042322

WHO文書は伝統中医学の用語を国際的に揃えるための標準であり、伝統体系のtheoretical frameworkを保った定義を提供する。CSWでは用語・体系内部の構造を確認する資料として使う。

WHO Standard Acupuncture Nomenclature, Part 2 (1991)

https://iris.who.int/bitstream/handle/10665/207637/Standard_acupuncture_nomenclature_1991_partII_eng.pdf?sequence=1

この用語標準は Jing / Luo / Jingluo をそれぞれ meridian / collateral / meridian and collateral として区別しており、近代国際標準化で用いられた英語対応を確認する資料として使う。

ISO/TS 16843-4:2017, Health informatics — Categorial structures for representation of acupuncture — Part 4: Meridian and collateral channels

https://www.iso.org/standard/68587.html

ISO文書はmeridian / collateral subject fieldをhealth-informatics上で表現するためのcategorial structureを規定する。CSWでは「標準化された概念表現が存在する」ことを確認するために使い、解剖学的実在性や治療効果の証拠には使わない。

これらの標準が存在すること自体を、経絡の現代生物医学的実在性の証明とは扱わない。

### 3. Biomedical indexing reference

NCBI MeSH, Meridians

https://www.ncbi.nlm.nih.gov/mesh/68016740

MeSHはmeridiansをacupunctureの古典的lociとして索引し、main and collateral channels / network of passagesという伝統的構造を記述している。

これはbibliographic indexing / terminology referenceであり、解剖学的構造の確証ではない。

### 4. Scholarly review of the concept boundary

“A 4D systemic view on meridian essence: Substantial, functional, chronological and cultural attributes”

https://pubmed.ncbi.nlm.nih.gov/34896049/

このreview自身が、meridianの「essence」は依然として不明確で議論があると明記し、substantial / functional / chronological / cultural dimensionsを分けて検討している。

CSWではこの資料を、伝統的network structureと現代の物質的・機能的仮説を同一視しないための境界資料として使う。

Historical Review about Research on “Bonghan System” in China

https://pmc.ncbi.nlm.nih.gov/articles/PMC3687598/

このreviewは、Bonghan / primo vascular systemとmeridian-collateral systemの対応についてproved evidenceがないと結論している。CSWでは、**伝統的route modelを現代解剖学の構造へ同定しない**という禁止線を補強する資料としてのみ用いる。

## 現時点で保持できる構造核

sourceから安全に保持できる最小構造は、

- main routeとcollateral routeの区別;
- route / passage / connectionというnetwork vocabulary;
- branching / connection topology;
- TCM内部でのchannel systemという位置づけ;

までである。

次はまだ保持しない。

- 経路が現代解剖学上どの組織に対応するか;
- qi flowを現代生理学的flowとして同定すること;
- 診断・治療上の有効性;
- 特定acupoint / channel correspondenceの一般領域への移植。

## CSW候補operation

- main-vs-collateral pass;
- route-before-node reframe;
- branching-path probe;
- alternate-path / bypass question;
- route discontinuity;
- connection-topology externalization.

これらは「経絡が対象に実在する」と言うためではなく、tree / list / simple causal chainで見落とした経路構造を問うための候補である。

## 非医療target-return worked example

例として、文書公開フローを考える。

target-side material:

- draft → review → approval → publish が主経路;
- security review / legal review / exception handling は条件により分岐する副経路;
- 一部の副経路は主経路へ再合流する;
- 緊急公開では通常の一部経路を迂回する;
- どこかのhandoffが欠けると公開までのrouteが切れる。

Jingluo由来の問いとして残せるのは、

- main routeとcollateral routeを分ける;
- node一覧より先にroute continuityを見る;
- 分岐・再合流・迂回を明示する;
- 「主経路が正常でも副経路が切れている」状態を別に見る;

までである。

ここに qi / zang-fu / acupoint / diagnosis / treatment 等の医学語彙は持ち込まない。経絡がこの業務フローに「対応する」とも主張しない。残すのは **route class / branching / reconvergence / discontinuity** というde-bound operationだけである。

## profile-ready判断

今回の補強で、

1. 古典本文層;
2. 現代のWHO / ISO terminology層;
3. modern biomedical anatomyとの非同一性を示す境界資料;
4. 非医療target-return worked example;

を分離して保持できた。

したがってresearch-onlyのpre-profile段階から、**profile-ready / medical-tradition-sensitive** へ進める。ただしruntime採用は行わない。

runtime前に残る課題:

- Jing / Luo / Jingluo の用語史を、古典本文・近代翻訳・20世紀以後の国際標準化に分けてさらに厚くする;
- Huangdi Neijing内部でも篇・時代・注釈層を一枚岩にしない文献史境界を追加する;
- route-network operationがgeneric graph inspectionとどこで異なるかをnear-neighbor資料で固定する;
- 医療上の診断・治療・効果判定をruntime dossierへ持ち込まない。
