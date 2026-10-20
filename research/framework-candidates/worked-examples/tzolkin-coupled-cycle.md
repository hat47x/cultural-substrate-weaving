# Maya calendars：部分再来と複合再来を対象へ戻す構成例

状態：仮想の業務システム例。Maya暦の儀礼・占断の再現でも、障害原因の実証でもない。

## 固定対象

ある架空の決済システムでは、二つの定期処理が同じデータストア周辺で実行される。

- schedule A: 6時間ごとに集計cacheを再構築する。
- schedule B: 10時間ごとに外部settlementデータを取り込む。
- 両scheduleは時刻 t=0 で同時に開始した。
- t=6, 12, 18, 24ではAだけが再来する。
- t=10, 20ではBだけが再来する。
- t=30ではAとBが再び同時に実行される。
- 実行ログには一部のlatency spikeがあるが、どの処理が原因か、同時実行が必要条件かは未確認である。

この対象でいう「6」「10」「30」は業務側の周期であり、Tzolk’inの13×20やCalendar Roundの260×365を縮小対応したものではない。

## 体系接触で開く問い

Maya calendar dossierから借りるのは、**複数周期を別々の座標として保持し、一方だけの再来と複合状態全体の再来を分ける**という操作に限る。

### partial recurrence

t=6ではAの位相は戻るがBは戻らない。  
t=10ではBの位相は戻るがAは戻らない。

したがって「また同じ時間帯の処理が来た」という記述を、全体状態の再来と同一視しない。

### full recurrence

6と10の最小公倍数は30なので、開始位相が固定され両方がその周期で進む限り、t=30でA/Bの複合位相が初めてt=0と同じになる。

ただし、**同じ位相が戻ることはシステム状態全体が同一になることではない**。データ量、version、queue backlog、外部応答、configuration等は変化し得る。

### multi-scale view

- 短い周期：AまたはB単独の再来。
- 複合周期：A/Bの同時位相。
- 長い時間座標：releaseからの経過時間や累積処理件数。

短周期のパターンが繰り返しても、長期的にqueueやデータ量が蓄積しているなら、完全な「同じ状況」ではない。

## 対象へ返す問い

- latency spikeはAの実行時すべてで現れるか、Bだけでも現れるか、A/B同時時にだけ強くなるか。
- t=0とt=30で、同じなのはschedule位相だけか。処理件数・version・queue状態も同じか。
- 「6時間周期の問題」と呼ぶことで、10時間周期との位相差を落としていないか。
- 長期的な増加傾向を、周期の繰り返しとして誤認していないか。
- scheduleの開始offsetが変わった場合、次の同時実行時刻はどう変わるか。

## 必要な対象側証拠

| 問い | 必要な資料 |
| --- | --- |
| scheduleの周期・offset | scheduler設定、実行履歴 |
| partial/full recurrence | timestamp付きjob logs |
| latencyとの対応 | request/metric時系列、job window |
| 同時実行が原因か | 単独実行との比較、再現・切分け試験 |
| 長期変化 | release/version、queue、処理量の履歴 |

## 文化的な範囲

Smithsonian NMAIのLiving Maya Timeが示すTzolk’in / Chol Q’ij、Haab、Calendar Round、Long Countは、Maya communitiesの歴史と現在の実践に結びついた暦体系である。CSWはそのcalendar mechanicsから周期・複合再来という質問構造だけを一時的に借りる。

- day signを業務ジョブの意味へ対応させない。
- 人格・fortune・将来予測を導入しない。
- communityごとの実践やday keeperの権威を一般化しない。
- 260、365、18,980という文化的に記録された周期を、6、10、30の業務周期と同一視しない。

**結論の範囲：** この構成例はpartial/full recurrenceと位相差を対象語へ戻せることを示すだけである。通常のscheduler分析・最小公倍数・時系列分析に対する追加発見はまだ示していない。

出典：Smithsonian National Museum of the American Indian, Living Maya Time — The Calendar System: https://maya.nmai.si.edu/calendar/calendar-system
