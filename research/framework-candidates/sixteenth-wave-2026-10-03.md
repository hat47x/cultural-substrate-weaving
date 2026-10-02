# Framework corpus sixteenth wave — 2026-10-03

Status: candidate-quality expansion / no runtime adoption

## Decision

Pāṇini『アシュターディヤーイー』の規則構造を、新しいprofile-ready候補として追加する。

中心的なoperationは、省略された継承文脈の展開、規則scopeの復元、一般則と限定規則の相互作用、対象規則とメタ規則の分離である。規則の順序も点検対象にするが、「後に書かれた規則が常に勝つ」という汎用原則にはしない。

## Why this fills a real corpus gap

既存のMīmāṃsā hermeneuticsは、規定文の単位、目的、文脈補完、規範衝突の解釈に強い。Vedic recitation pathasは、同じ系列の複数表現を照合して、順序や境界の保持を点検する。

今回の候補は、そのどちらとも異なり、規則が周囲から何を継承し、複数規則が同じ対象にどう適用され、どの規則が規則同士の関係を制御するかを開く。この差がde-binding後にも残るため、coverage mapへ独立したoperation familyとして追加する。

## Product-value effect

SIerの要件、設定、検証ルール、ポリシーでは、章見出しや共通節に書かれた条件を個別規則が暗黙に引き継ぐことがある。文書を分割したり設定へ移したりすると、その継承条件だけが失われる場合がある。

この候補は、その種の欠落をPāṇiniの規則で決めるのではなく、個別規則へ展開すると何が暗黙条件として残っていたか、一般規則と限定規則が同じ対象へ適用されるか、優先関係や順序は対象仕様で明示されているか、競合解消をどのテストで確認できるか、という問いへ変換する。

CSWの出口は、対象側の問い、見落とし候補、回帰テスト候補であり、要件や設計判断そのものではない。

## Historical boundary

Pāṇinian grammarを現代のcompilerやrule engineと同一視しない。

anuvṛtti、一般則と限定規則、規則順序、paribhāṣāは、同じ時代の単一な実装仕様としてまとめない。後代の解釈層は区別して保持する。

## Runtime decision

runtimeへは採用しない。

次の段階では、一般的なrule-engine reviewとMīmāṃsāを対照にし、継承scope、blocking、metarule分離が本当に異なる問いを生むかを確かめる。広いefficacy benchmarkはまだ開始しない。
