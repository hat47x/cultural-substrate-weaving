"""Extended task bank (v2): six new domains per structure type, T2 spec tightened.

Run with CSW_TASKS=.../tasks/tasks_v2.json so that build_tasks writes the v2 bank.
Task ids carry a `-v2` infix so they never collide with the v1 bank.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_tasks as b  # noqa: E402

DOMAINS = {
    "T1_vacancy": ["介護施設の入居受け入れ手順", "書籍の企画から出版までの工程", "市役所の転入手続きの窓口",
                   "飲食店の仕込みから提供までの分担", "研究室の論文投稿フロー", "小売店の新商品導入手順"],
    "T2_gen_inhibit": ["郊外の小売店舗の運営", "学習塾の運営", "農産物直売所の運営",
                       "創業三年目のスタートアップの組織運営", "地域の共同農園の運営", "認可保育園の運営"],
    "T3_chain_cut": ["宅配便の再配達の増加", "病院の外来待ち時間への苦情", "新入社員の早期離職",
                     "工場の納期遅延", "アプリの解約率の上昇", "図書館の延滞の増加"],
    "T4_standpoint": ["商店街の歩行者数をめぐる議論", "学習アプリの効果をめぐる議論", "残業削減策の成否をめぐる議論",
                     "値下げの効果をめぐる議論", "防災訓練の成果をめぐる議論", "社員研修の効果をめぐる議論"],
    "T5_four_whys": ["ダム工事の遅れの原因論争", "アプリの品質問題の原因論争", "学校統廃合に至った理由の論争",
                     "製品の欠陥が生じた理由の論争", "事業の赤字の原因論争", "営業成績の低迷の原因論争"],
    "T6_two_cycles": ["病棟の夜勤交代と投薬時刻", "配送の曜日便と倉庫の棚卸し", "サーバのログ圧縮とバックアップ",
                      "学校の時間割と清掃当番", "牧場の給餌と搾乳の作業", "鉄道の定期点検と臨時ダイヤ"],
    "T7_reception": ["社内研修の資料の活用", "地域の健康診断の案内", "保護者向けのお知らせ",
                     "製品マニュアルの活用", "災害時の避難指示", "税務の通知書への対応"],
    "T8_part_whole": ["一つの会議の議事録の書き方", "一人の新人のミスの出方", "一件の苦情対応の経過",
                      "一つの店舗の陳列の癖", "一つのプロジェクトの会議運営", "一つの契約書の文言の癖"],
}
for tname, doms in DOMAINS.items():
    b.TYPES[tname]["domains"] = doms

b.TYPES["T2_gen_inhibit"]["plant"] = (
    "五つの要素A、B、C、D、Eがこの順に一巡する関係にある。各要素を強める施策は、次の要素（AならB）を押し上げる一方で、"
    "二つ先の要素（AならC）を押さえ込む。この関係が五つすべてにあるため、Aを改善するとCが悪化し、Cを是正するとEが悪化し、"
    "Eを是正するとBが悪化する、というように、二つ飛びで悪化の対象が巡回する。材料には、各施策の時期と、その後に悪化した指標を"
    "具体的に載せる。典型的な分析は、各指標を独立の変動・季節性・担当者の問題として扱う。"
)

_orig = b.main


def main() -> None:
    # Rename ids to carry the v2 infix, then run the standard pipeline.
    import json

    specs_before = b.OUT
    _orig()
    tasks = json.loads(specs_before.read_text(encoding="utf-8"))
    for t in tasks:
        t["id"] = t["id"].replace("-", "-v2-", 1)
    specs_before.write_text(json.dumps(tasks, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
