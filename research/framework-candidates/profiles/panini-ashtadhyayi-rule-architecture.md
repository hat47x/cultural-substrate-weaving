# Pāṇini Aṣṭādhyāyī rule architecture candidate profile

Status: profile-ready / research-only / classical-text-and-commentarial-layer-sensitive

## Identity

- names: Pāṇini Aṣṭādhyāyī rule architecture / Pāṇinian grammatical rule system / パーニニ『アシュターディヤーイー』の規則構造
- current scope: 『アシュターディヤーイー』の規則記述から確認できる文脈継承、規則適用範囲、一般則と限定された規則の相互作用、派生上の順序、対象規則とメタ規則の区別
- intended CSW use: 要件、ポリシー、設定、検証規則を、個別の文だけでなく継承条件と適用関係を含む規則系として見直す
- not intended use: サンスクリット文法の判定、Pāṇinian traditionの権威の代行、現代のルールエンジンとの歴史的同一視

## Source basis

### Paul Kiparsky, “Pāṇini”

https://web.stanford.edu/~kiparsky/Papers/panini_hist_of_phon_handbook.pdf

規則の種類、見出し、メタ規則、anuvṛttiによる省略と継承を含む記述構造を確認する。

### Paul Kiparsky, “On the Architecture of Pāṇini’s Grammar”

https://www.researchgate.net/publication/221145943_On_the_Architecture_of_Panini%27s_Grammar

見出しからの条件継承、一般的な規則と限定された規則の相互作用、適用順序を考えるための資料として使う。

### Sanskrit Library, Aṣṭādhyāyī 1.4.2

https://www.sanskritlibrary.org/grammatical/data/A.1.4.2.html

規則1.4.2の一次資料アンカーとして使う。この一規則を汎用の「後勝ち」アルゴリズムへ置き換えない。

### Study of Pāṇinian metarules

https://www.researchgate.net/publication/47930745_The_paribhasas_arthavadgrahane_nanarthakasya_laksanapratipadoktayoh_pratipadoktasyaiva_grahanam_and_ekadesavikrtam_ananyavat_Studies_on_some_Metarules_in_Paninian_system

後代のparibhāṣāを含む解釈層を、Pāṇini本人の明示規則と区別するために参照する。

## Structural core

再利用する構造核は「複雑な規則を短く書くこと」ではない。

一つの規則系の中で、明示されていない条件が周囲から継承され、複数規則の適用範囲が重なり、限定された規則が一般的な規則と相互作用し、さらに規則同士の関係を扱うメタ規則が存在しうる点にある。

CSWでは、継承された条件、適用scope、一般則と限定規則、順序、対象規則とメタ規則を分けて扱う。

## Native operation candidates

### inherited-context-expansion

見出しや先行規則から継承されている条件を、対象規則ごとに展開する。

### rule-scope-reconstruction

各規則が適用される対象、条件、終了点を対象側の材料から復元する。

### general-specific-blocking-probe

同じ対象に適用できる規則が複数あるとき、一方がより狭い条件を持つかを確認し、実際の優先関係は対象側の仕様へ戻して確かめる。

### derivation-order-audit

規則の抽出、並び替え、分割、統合によって、対象側で定義された処理結果が変わるかを確認する。

### metarule-object-rule-separation

業務やデータを直接変える規則と、規則の選択、優先、競合解消を制御する規則を分ける。

### implicit-dependency-reveal

単独では完結して見える規則について、前段の見出し、定義、メタ規則への依存を明示する。

## Target-return questions

- この規則は、本文に書かれていないどの条件を周囲から引き継いでいるか。
- 継承される条件はどこから始まり、どこで終わるか。
- 同じ対象ケースに複数の規則が適用されるか。
- 一方の規則は、他方より狭い対象集合や条件を持つか。
- 優先関係は対象の仕様で明示されているか、それとも読み手が推測しているだけか。
- 規則の順序は対象システムで意味を持つか。
- 規則そのものと、競合解消や適用順を決める規則を分けられるか。
- 競合や順序の疑問を、どの仕様、テスト、実行結果で解消できるか。
- Pāṇinian terminologyを外した後にも、対象側に確認すべき曖昧さや欠陥が残るか。

## Near-neighbor differentiation

### Pāṇini rule architecture vs Mīmāṃsā hermeneutics

Mīmāṃsā候補は、規定文をどこまで一つの意味単位として読むか、目的や文脈から何を補うか、規範衝突をどう分解するかを主に扱う。

この候補は、規則を適用関係として追い、継承されたscope、一般則と限定規則、派生順序、メタ規則を明示する。規定文の解釈一般へ広げない。

### Pāṇini rule architecture vs Vedic recitation pathas

Vedic recitation pathas候補は、同じ系列を複数の明示表現で照合し、順序や境界の保持を点検する。

この候補では、順序は規則系の一要素にすぎない。中心は、どの規則がどの条件を継承し、同じ対象へどう適用されるかである。

### Pāṇini rule architecture vs generic rule-engine review

現代のルールエンジンがscope、priority、dependencyを既に明示し、対象側のテストも十分なら、Pāṇini由来の探索操作を加える必要はない。

価値が出る可能性があるのは、短い規則記述や文書分割によって、継承条件や優先関係が読み手の暗黙知へ落ちている場合である。

## Historical and epistemic boundaries

- 『アシュターディヤーイー』を現代のコンパイラ、production rule system、DSLと歴史的に同一視しない。
- anuvṛttiを、あらゆる文書で使える単純な継承構文として一般化しない。
- 後代のparibhāṣāを、Pāṇini本人が明示した単一のメタ規則集合として扱わない。
- 1.4.2を、あらゆる規則競合に対する無条件の「後勝ち」として使わない。
- Pāṇinian grammar内部の分析結果を、対象ドメインの事実や正しさへ移さない。
- Sanskritの文法カテゴリーを、対象の分類体系としてそのまま採用しない。

## De-binding route

1. Pāṇini、Sanskrit、文法伝統の用語を、対象向けの最終出力から外す。
2. 対象側で実在する規則、見出し、scope、priority、処理順だけを抽出する。
3. 継承される条件がある場合は各規則へ展開し、出典となる対象文書を残す。
4. 同じ対象へ複数規則が適用される場合だけ、一般／限定、priority、順序を点検する。
5. 競合解消の規則を、業務やデータを直接変える規則から分ける。
6. 規則の解釈を決めず、仕様、テスト、実行結果へ疑問を返す。
7. 対象側ですでにscopeとpriorityが完全に明示され、順序非依存も検証済みなら、このframeworkを使わない。

## Profile-ready decision

資料上の構造核、operation、歴史層の境界、de-binding、target-return questions、正例と負例を揃えられるため、research上はprofile-readyとする。

runtimeには採用しない。次の検証では、一般的なrule-engine reviewやMīmāṃsāによる規定文読解と比べ、継承scopeと規則相互作用に固有の探索差が残るかを確認する。

Worked examples:

- `research/framework-candidates/worked-examples/panini-ashtadhyayi-rule-architecture.md`
- `research/framework-candidates/worked-examples/panini-ashtadhyayi-rule-architecture-negative.md`
