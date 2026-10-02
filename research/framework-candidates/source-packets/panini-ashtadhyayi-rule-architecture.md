# Pāṇini Aṣṭādhyāyī rule architecture source packet

Status: source packet / profile-ready support / research-only

## Scope

この候補で扱うのは、サンスクリット文法の正しさそのものではなく、『アシュターディヤーイー』の規則記述に見られる文脈継承、規則の適用範囲、一般則とより限定された規則の相互作用、規則適用の順序、対象規則とメタ規則の区別である。

CSWでは、これらを要件定義、設定、検証規則、ポリシー記述などの見直しに使える探索操作へ変換する。ただし、Pāṇiniの体系を現代のコンパイラや業務ルールエンジンと同一視しない。

## Source observations

### Paul Kiparsky, “Pāṇini”

https://web.stanford.edu/~kiparsky/Papers/panini_hist_of_phon_handbook.pdf

Kiparskyは、『アシュターディヤーイー』が派生規則だけでなく、定義、見出し、メタ規則を含む体系として構成されていることを整理している。また、反復される要素を後続規則へ持ち越すanuvṛttiを、記述上の重要な仕組みとして扱っている。

CSWでは、ここから「規則単体を読む前に、継承された条件を展開する」という操作を抽出する。

### Paul Kiparsky, “On the Architecture of Pāṇini’s Grammar”

https://www.researchgate.net/publication/221145943_On_the_Architecture_of_Panini%27s_Grammar

この研究は、見出しの下に置かれた規則が条件を引き継ぐ構造、一般的な規則とより限定された規則の相互作用、規則の順序や適用構造を論じている。

CSWでは、「暗黙の適用範囲」「一般則と狭い規則」「順序依存」を別々に点検するために使う。

### Aṣṭādhyāyī 1.4.2

https://www.sanskritlibrary.org/grammatical/data/A.1.4.2.html

Sanskrit Libraryのデジタル版を、規則1.4.2「vipratiṣedhe paraṃ kāryam」の一次資料アンカーとして使う。

この規則を「競合したら常に後ろの規則が勝つ」という汎用原則へ単純化しない。Pāṇinian grammar内部での適用や後代の解釈を含め、競合解消の扱い自体を研究対象として残す。

### Later metagrammatical interpretation

https://www.researchgate.net/publication/47930745_The_paribhasas_arthavadgrahane_nanarthakasya_laksanapratipadoktayoh_pratipadoktasyaiva_grahanam_and_ekadesavikrtam_ananyavat_Studies_on_some_Metarules_in_Paninian_system

Pāṇinian traditionでは、paribhāṣāを含むメタ文法的な解釈が後代の文献層でも発達している。CSWは、それらをPāṇini本人の明示規則と一つの歴史層へまとめない。

## Distinctive operation hypothesis

この候補が既存portfolioへ追加する中心的な仕事は、規則本文に省略された継承文脈の復元、同じ対象へ適用される一般則と限定規則の分離、対象規則とメタ規則の分離である。

Mīmāṃsā候補は規定文の単位、目的、文脈補完、規範衝突の解釈を主に扱う。今回の候補は、規則適用系を実行可能な関係として追い、継承範囲、blocking、順序、メタ規則を点検する点を中心にする。

## Adoption hold

現時点ではruntimeへ採用しない。

通常のrule-engine reviewとの差、Mīmāṃsāとの差、Pāṇinian commentarial traditionの層差を保ったままde-bindingできることを追加検証する。
