# Maya calendars：周期分析を使わない／追加しない判断

状態：仮想の非適用例。文化的価値の評価でもruntime採否判断でもない。

## ケースA：通常のscheduler分析で同じ問いが既に出ている

[6時間周期と10時間周期の構成例](tzolkin-coupled-cycle.md)について、初回の通常レビューが次を既に扱っているとする。

- A/B各jobの周期と開始offset;
- 6、10、30時間での単独／同時実行;
- timestamp付きmetricsとjob windowの照合;
- 長期trendとperiodicityの分離;
- schedule変更時の次回coincidence計算。

この場合、partial recurrence、full recurrence、phase desynchronizationをMaya calendar dossierから追加しても、新しい検証可能な問いが増えない。**非活性化**し、普通のscheduler・time-series・modular arithmeticへ戻る。

## ケースB：周期が対象に存在しない

一度だけ実行するデータ修正について、実行順序や依存関係はあっても周期的な再来がない場合、「何日周期か」を無理に作らない。単発の状態遷移は別の分析対象である。

## ケースC：周期座標を因果に変換しそうな場合

- A/Bが同時実行されたという時刻だけで、障害原因と決める。
- 過去の同じ位相で障害が起きたから、次の同位相でも障害が起きると予言する。
- Maya calendarのday signやritual meaningを業務severityへ対応させる。
- 260日・365日・Calendar Roundを、根拠なく対象の6時間・10時間周期へ写像する。

これらはすべて撤回する。

**非活性化は、対象に周期効果がないという意味ではない。** 普通のログ・scheduler・時系列データで周期性・相関・因果を検査する作業は継続する。

参照：[正例](tzolkin-coupled-cycle.md)、[通常手法との比較](../comparisons/tzolkin-vs-ordinary-periodicity-review.md)、[接触前の発見価値](../comparisons/tzolkin-discovery-value.md)。
