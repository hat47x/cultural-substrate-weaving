# 神社参拝の境界・清めと通常の本番変更管理の比較

状態：定性的な机上比較。対象は[既存の構成例](../worked-examples/shinto-threshold-purification.md)。実業務の観測・効果実験ではない。

## 同じ対象、異なる入口

仮想の本番変更を扱う。開始前に権限・対象環境・バックアップの確認が必要とされるが、どの経路が実装済みか、実際に違反できるかは未知とする。

体系に**触れる前から**、本番変更の設計レビューなら、変更要求、影響分析、事前テスト、承認、実行、変更後の確認を自然に扱う。NIST SP 800-128はconfiguration change controlでこのような段階を明示する。Google SREのリリース資料も、展開前の評価、部分展開、段階的な判定、復帰可能性を扱う。

したがって、通常の変更管理は、神社参拝の構造に触れていなくても次を問える。

- 承認と本番領域への入場は別の状態か。
- 作業開始前に何の準備が必要で、何を確認してから次へ進めるか。
- 変更を実行してよい主体と環境の境界はどこか。
- 終了、差戻し、復旧、再入場にはどの状態遷移があるか。

## 体系に触れた場合

採用範囲は、現代の参拝案内に見られる「鳥居の境界、参道の接近、手水による準備、中心の参拝」であり、祓や禊などの諸儀礼を同一の手順に統合しない。祭儀の実施状況や宗教上の効力を業務側へ投影しない。

この接触で得られる対象向けの問いは「移行開始の印と、中心操作を許されるための準備が混ざっていないか」「退出や再入場の条件を一つの完了状態へ潰していないか」である。これらは有用な問いになり得るが、**同じ対象ではNIST型change controlや通常のrelease readiness reviewでも問える**。

## 能力の比較

| 対象への問い | 通常の変更管理 | 神社参拝構造からの再記述 | 差分 |
| --- | --- | --- | --- |
| 状態が切り替わる時点 | 承認・展開・完了の状態管理 | threshold-marking | 基本的に重複 |
| 主要操作の前段階 | preflight・権限・バックアップ | before-entry-preparation | 重複 |
| 接近経路 | 変更要求→承認→実行→検証 | path-to-center | 重複 |
| 実施行為の後に何が許されるか | evidence-based readiness / authorization | state-transition-by-practice | 状態の意味は異なる。対象上は再現可能 |
| 終了・戻し・再入場 | closeout・rollback・再実行 | closure-and-return | 重複 |

ここで「重複」とは**対象に返した問いの操作能力の重複**であって、神道と変更管理に歴史的・宗教的な同一性があるという意味ではない。

## 判断範囲

- **能力重複**：この本番変更の構成例では大きい。
- **方法選択前の発見価値**：別途検討する。ただし対象が本番変更なので、変更管理そのものをex-anteに選ぶことは自然であり、恣意的に弱い比較対象へ落とさない。
- **対象事実**：変更開始、チェック、承認、rollback等の実装・運用記録が提供されていないため、欠陥や漏れは認定しない。
- **非活性化**：[使わない例](../worked-examples/shinto-threshold-non-activation.md)参照。

## 出典・適用範囲

- 神社本庁, *Entering a Jinja*: https://www.jinjahoncho.or.jp/en/at-a-jinja/entering/
- 國學院大學, *Temizuya*: https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9671
- 國學院大學, *Shubatsu*: https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9053
- NIST SP 800-128, §3.3.2 *Configuration Change Control*: https://doi.org/10.6028/NIST.SP.800-128
- Google SRE Workbook, *Canarying Releases*: https://sre.google/workbook/canarying-releases/

参照資料は典型的な構造を示すものであり、対象プロジェクトへの採用・遵守を示す証拠ではない。本比較だけでruntimeの保持・降格は行わない。
