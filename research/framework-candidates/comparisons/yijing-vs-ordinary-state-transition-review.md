# 易経の位置変化と、通常の状態遷移・モデルベーステストの比較

状態：同一の架空データ移行を使った能力比較。独立した実験やruntime判断ではない。

## 固定対象

[易経の正例](../worked-examples/yijing-positioned-transition.md)にある6つの仮feature flag（read/write compatibility、dual-write、backfill検証、read switch、rollback route）を共有する。位置1–6を左→右で表した初期`110001`、終点`111101`への切替を考える。

- 第3位置→第4位置：`110001 → 111001 → 111101`
- 第4位置→第3位置：`110001 → 110101 → 111101`

中間状態の有効性・実際の実施順・データ副作用は未知である。同じ最終構成に到着できることは中間作業の可換性を保証しない。

## 体系に触れない場合の自然な専門手法

この依頼を「feature flagを段階的に切り替える際の安全条件を確認する」と表現した場合、ソフトウェアエンジニアリングの普通の方法として、状態遷移図、dependency ordering、decision table、configuration / pairwise testing、モデルベーステストが自然に選ばれる。

- State transition testingは、状態だけではなくイベント・遷移の許否と、到達できる経路を扱う。
- Model-based testingは抽象的な状態機械から試験や経路を導く。割り当てた状態と実装が一致するという証明には、別のテスト実行証拠を要する。
- 普通のrollout reviewは、各flagの依存関係、バックフィルと進行中更新の順序、cutover中の整合性、rollback可否を確認する。

よって普通の分析でも、最終ベクトルだけでなく中間状態 `111001` と `110101` を検査できる。易経へ接触して初めて順序問題が存在すると示すことはできない。

## 対象に返す操作の重複

| 易経に由来する限定操作 | 普通の技法 | 対象側での対応する問い | 重複 |
| --- | --- | --- | --- |
| positioned configuration | state vector / state machine | 第3・第4の意味と位置、独立した切替可能性は何か | 大 |
| single-line flip（CSW探索用） | toggle / one-factor sensitivity | 第3位置だけ変えると、何が変わるか | 大 |
| upper/lower recomposition | subsystem decomposition / component grouping | 読書互換とデータ同期の関係は何か | 対象の分割根拠がなければ強制不可 |
| transformed configuration | state-transition graph | 同じ終点へ至る両経路の中間状態は何か | 大 |
| counter-view | negative-state / alternate-path test | backfill確認より前にdual-writeを始める場合の確認は何か | 大 |

2^6の配置の全列挙は64通りだが、**すべて対象で到達可能とは限らない**。標準のconfiguration testingでも64通りや部分網羅を調べられる。易経の六十四卦との数値一致は、歴史的な卦の意味を対象へ移してよい根拠ではない。

## 終点が同じでも経路が違う理由

**数学**：固定された二つの異なる位置のbit反転は交換可能で、終点は同じである。  
**対象システム**：その途中で「backfillが済んだ」「dual-writeを始めた」に伴う副作用は、仕様・ログ・データ更新に依存する。したがって中間状態を別に検証する必要がある。

ここでCSWの変化操作は問いを生むが、普通の状態遷移分析も全く同じ中間差を扱える。実環境で危険が起きたとは主張しない。

## 文化・解釈の境界

易経は多層の文献・注釈史を持つ。古典の符号構造・卦辞・爻辞・後代の変化の解釈を一つの普遍的なbinary algorithmと同一視しない。線を下から上へ読むという位置の規則と、CSWが選んだ6つのfeature flagの意味は別である。

引用できる出典：
- Stanford Encyclopedia of Philosophy, *Chinese Philosophy of Change (Yijing)*: https://plato.stanford.edu/entries/chinese-change/
- Stanford, *Yijing Appendices* (trigrams/hexagrams and bottom-up lines): https://plato.stanford.edu/entries/chinese-change/appendix.html
- Chinese Text Project, *Book of Changes — Xi Ci I*: https://ctext.org/book-of-changes/xi-ci-shang
- ISTQB CTFL v4.0 syllabus, state-transition testing: https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/

**判定：** 同一の仮想移行では通常の状態遷移テストが能力面を大きく再現する。次の[発見価値の比較](yijing-discovery-value.md)で、接触前の方法選択を別途扱う。これだけで採用継続・降格は判断しない。
