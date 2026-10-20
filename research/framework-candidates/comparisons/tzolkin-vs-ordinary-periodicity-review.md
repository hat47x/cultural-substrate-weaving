# Maya calendars と通常のscheduler・周期性分析の能力比較

状態：同一の仮想業務対象を使った机上比較。独立したレビュー、実測因果、runtime採否判断ではない。

## 固定対象

[6時間周期Aと10時間周期Bの構成例](../worked-examples/tzolkin-coupled-cycle.md)を共通入力とする。両jobはt=0で同時開始し、Aは6時間ごと、Bは10時間ごとに実行される。t=30で複合位相が再来する。latency spikeとの因果は未確認である。

## 体系に触れない通常の入口

依頼が「二つの定期jobとlatency spikeの時間関係を調べてください」であれば、普通のscheduler reviewとtime-series analysisを選ぶことは自然である。

### scheduler / recurrence inspection

RFC 5545のRRULEのような一般的なscheduling仕様でも、繰返し間隔と開始時点を明示してrecurrence setを計算する。対象のschedulerがiCalendarを使っているという意味ではなく、**周期とoffsetを明示的に扱うことが標準的な計算問題である**ことの比較根拠として使う。

既知の6時間・10時間周期なら、最小公倍数30を計算し、

- A単独の再来;
- B単独の再来;
- A/Bの同時再来

を最初から分けられる。

### time-series / seasonality inspection

周期が設定から分からずmetricsだけがある場合も、NIST Engineering Statistics Handbookはrun sequence、seasonal subseries、autocorrelation、spectral plotによるseasonality/cyclic structureの検出を説明している。

この普通の分析からも、

- 一つのdominant periodだけで説明しない;
- 複数の周期候補を検出する;
- lagごとの再来を比較する;
- trendとperiodicityを分ける

という問いへ進める。

## 操作ごとの比較

| Maya calendar dossierのde-bound操作 | 普通の手法 | 同一対象での問い | 能力重複 |
| --- | --- | --- | --- |
| coupled-cycle | 複数recurrence rule / modular arithmetic | AとBの位相はいつ同時に揃うか | 大 |
| partial-vs-full recurrence | 各scheduleとLCMの比較 | t=6はAだけ、t=10はBだけ、t=30は両方か | 大 |
| phase-desynchronization | offset / phase comparison | Aが戻った時、Bはどのphaseか | 大 |
| recurrence-distance | LCM・周期検出 | joint stateの再来間隔は何か | 大 |
| multi-scale-time | trend + seasonality /複数時間尺度 | 短期周期の繰返しと長期蓄積を分けるか | 大 |
| cycle-count distinction | timestamp / release-age / monotonic counter | 周期が戻っても経過時間・versionは戻らないか | 大 |

**重要：** 同じ位相座標が戻ることは、対象システムの全状態が戻ることではない。普通のtime-series/scheduler reviewも、queue量、version、traffic、external data等の非周期変数を別に確認できる。

## 文化・数学の境界

Tzolk’in / Chol Q’ijの20 day signsと13-number cycleによる260日、Haabの365日、両者のCalendar Round 18,980日という構造は、Mayaの歴史・現在の暦実践に属する。業務対象の6時間・10時間・30時間は**説明用の別周期**である。

同じLCM計算が使えるというだけで、Maya calendar systemとjob schedulerが歴史的・意味的に同一だとは主張しない。

## 出典

- Smithsonian NMAI, *Living Maya Time — The Calendar System*: https://maya.nmai.si.edu/calendar/calendar-system
- RFC 5545, *Internet Calendaring and Scheduling Core Object Specification*: https://datatracker.ietf.org/doc/html/rfc5545
- NIST/SEMATECH e-Handbook, *Seasonality*: https://itl.nist.gov/div898/handbook/pmc/section4/pmc443.htm
- NIST/SEMATECH e-Handbook, *Spectral Plot*: https://www.itl.nist.gov/div898/handbook/eda/section3/eda33r.htm

**判定：** この固定対象では、普通のscheduler・時系列分析がde-bound操作をほぼ全面的に再現する。これは能力重複の机上証拠であり、体系接触前から実際に同じ方法が選ばれたかは[別資料](tzolkin-discovery-value.md)で扱う。
