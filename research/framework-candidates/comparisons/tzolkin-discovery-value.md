# Maya calendars：接触前の方法選択と発見価値

状態：2026-10-20 desk review。独立した初回回答、実システムの観測、効果測定、採用・降格判断は未実施。

## 同一対象

[固定例](../worked-examples/tzolkin-coupled-cycle.md)の二つの定期jobを使う。

- A: 6時間ごと;
- B: 10時間ごと;
- t=0で同時開始;
- 一部timestampにlatency spikeがある;
- 原因は未確認。

通常側から周期情報を隠して、Maya calendar contact側だけに複数周期を与えるような比較はしない。

## A — 体系名を伏せた普通の初回依頼

> 二つの定期処理A/Bが6時間・10時間間隔で動き、latency spikeとの関係が疑われている。周期・位相・実行履歴から、最初に何を調べるか。

この依頼から、schedule設定、開始offset、同時実行、LCM、time-series seasonality、metric/log correlationを選ぶことは自然である。

特に周期が**すでに明示されている対象**では、「一方だけの再来」と「二つが同時に戻る再来」を分けるために文化体系へ接触する必要はない。6と10から30を求め、t=6 / t=10 / t=30を比較することは普通の運用分析である。

## B — Maya calendar mechanicsとの接触

adopted dossierは、Tzolk’in/Chol Q’ij、Haab、Calendar Round、Long Countを「異なる周期・複合再来・長期座標」として区別する。

CSWで対象へ戻すと、

- 「Aが戻った」だけを「同じ状況」と呼んでいないか;
- A/B両方が揃った時点と片方だけの再来を区別したか;
- 短周期が戻ってもrelease ageや累積負荷が違わないか

という問いになる。

しかし今回のscheduler targetでは、これらはAの通常分析が自然に開く。

## 発見として数えないもの

- 6と10のLCMを30と計算したこと;
- 「複数周期がある」と言い換えたこと;
- t=30のcoincidenceを見つけただけで原因としたこと;
- Mayaの260/365/18,980を業務周期へ対応させたこと;
- day sign・ritual meaning・fortuneを対象へ持ち込んだこと。

## まだ開いている問い

Maya calendar contactが、**対象が一つのdominant cycleだけだと思われている状況で、別の独立周期の存在そのものを探索する契機**になる可能性はある。

ただし、これを支持するには：

1. 複数周期を明示しない固定対象;
2. 通常の初回分析者が自然に選んだ方法と質問;
3. framework contact後に追加された、実際に検証可能な第二周期の質問;
4. logs/metricsでその周期が支持・反証された結果

が必要である。

後から「普通の分析者は一周期しか見ないはず」と仮定して作った例は、発見価値の証拠にならない。

## 非活性化

[非適用例](../worked-examples/tzolkin-non-activation.md)に従い、通常のscheduler/time-series reviewが最初から複数周期、offset、partial/full recurrence、長期trendを扱う場合は使わない。

## 現時点の判断

**能力重複は非常に大きく、この対象ではordinary ex-ante selectionも強い。** したがって追加発見を支持する証拠はまだない。

一方、独立した初回レビューを実施していないため、これは測定済みのdiscovery overlapでも正式なruntime demotionでもない。`tzolkin`は`adopted`、`discovery_hypothesis.evidence_state=unreviewed_hypothesis`を維持する。

出典：Smithsonian NMAI *Living Maya Time*、RFC 5545 recurrence rule、NIST Engineering Statistics Handbook seasonality / spectral analysis。
