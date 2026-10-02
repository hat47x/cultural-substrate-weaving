"""Build the synthetic latent-structure task bank (24 latent + 8 null tasks).

The writer model is told the structure to plant but must not name it. A second,
independent call checks that the key is derivable from the material alone and
that no structure-naming terms leak. Raw writer outputs stay in local/; the
accepted bank is written to tasks/tasks.json (synthetic, public-safe).
"""

from __future__ import annotations

import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm  # noqa: E402

OUT = Path(os.environ.get("CSW_TASKS", str(Path(__file__).resolve().parents[1] / "tasks" / "tasks.json")))

TYPES = {
    "T1_vacancy": {
        "framework": "yijing",
        "plant": (
            "閉じた役割（機能）の集合が一つの流れを成しており、そのうち一つの機能だけが誰の担当にもなっていない（空位）。"
            "症状は、その機能が本来つなぐはずの前後の工程の境目に現れる。"
            "典型的な分析は、既存の担当者の能力・人数・負荷の不足を原因とする。"
        ),
        "domains": ["入院患者の退院調整チーム", "ソフトウェアのリリース工程", "地域の秋祭りの実行委員会"],
        "banned": ["空位", "欠員", "空席", "担当者がいない機能"],
    },
    "T2_gen_inhibit": {
        "framework": "wuxing",
        "plant": (
            "五つの要素が一巡する関係にあり、各要素を強める施策は次の要素を押し上げる一方で、二つ先の要素を押さえ込む。"
            "そのため、ある指標を改善する施策を打つたびに別の指標が悪化し、その是正が今度はまた別の指標を悪化させる、という悪化の巡回が観測される。"
            "典型的な分析は、各指標を独立の変動・季節性・担当者の問題として扱う。"
        ),
        "domains": ["カフェチェーンの店舗運営", "大学の研究室運営", "オンラインコミュニティの運営"],
        "banned": ["循環", "巡回", "相生", "相剋", "生成と抑制", "連鎖反応"],
    },
    "T3_chain_cut": {
        "framework": "dependent-origination",
        "plant": (
            "症状は、複数の条件が順に成立することで生じており、最上流の条件（ある約束・仕様・判断）が成立しなければ全体が止まる。"
            "下流の対策は一時的に症状を減らすが、上流の条件が残る限り再び発生する。観察・変更できる介入点は症状の位置とは別にある。"
            "典型的な分析は、症状が出ている現場の担当者の教育や増員で対処しようとする。"
        ),
        "domains": ["カスタマーサポートへの苦情増加", "製造ラインの不良率上昇", "中学校の欠席増加"],
        "banned": ["条件", "連鎖", "上流", "根本原因", "因果の鎖"],
    },
    "T4_standpoint": {
        "framework": "jain-sevenfold-predication",
        "plant": (
            "二つの陣営が「Xは有効だ」「Xは有効でない」と対立しているが、どちらの主張も自分の測定では正しい。"
            "食い違いは、測っている対象の層・時間幅・指標・定義の違いから生じており、主張に省略された条件を戻せば両立する。"
            "典型的な分析は、どちらのデータが正しいか、あるいは両者の中間の結論を探す。"
        ),
        "domains": ["新機能の効果をめぐる二部署の対立", "在宅勤務の生産性をめぐる意見対立", "夜間診療枠の有効性をめぐる議論"],
        "banned": ["視点", "立場", "条件つき", "観点の違い", "前提の違い"],
    },
    "T5_four_whys": {
        "framework": "aristotle-four-causes",
        "plant": (
            "関係者が「なぜ遅れた（失敗した）のか」について異なる答えを述べ、互いに相手を誤りだと考えている。"
            "実際には、各人の答えは、何からできているか、どんな構造か、誰がいつ動かしたか、何のためか、という別種の「なぜ」に答えており、どれも同時に成り立ち得る。"
            "典型的な分析は、唯一の原因を特定して他を退けようとする。"
        ),
        "domains": ["新規プロジェクトの遅延原因をめぐる会議", "橋梁補修工事の遅れ", "通販商品の返品増加の原因論争"],
        "banned": ["原因の種類", "多面的", "どれも正しい", "別の種類の原因", "別種の原因"],
    },
    "T6_two_cycles": {
        "framework": "maya-calendars",
        "plant": (
            "周期の異なる二つの定期的な過程（たとえば当番の巡回と定期処理、保守と検査）が並行して走っており、不具合は二つの周期の位相が重なる日にだけ起きる。"
            "不具合の発生日は一見不規則だが、日付を並べると二つの周期の最小公倍数に沿っている。両方の周期の長さと、不具合の発生日を材料に具体的に載せる。"
            "典型的な分析は、不具合を偶発事象、または単一の原因の気まぐれとして扱う。"
        ),
        "domains": ["当番制の運用と夜間バッチ処理", "機械の定期保守と品質検査", "給与支払日と定期キャンペーン"],
        "banned": ["周期", "最小公倍数", "位相", "重なる日", "同期"],
    },
    "T7_reception": {
        "framework": "rasa",
        "plant": (
            "発信側は内容の質・正確さ・頻度のどれも十分に整えているのに、受け手の行動が変わらない。"
            "原因は発信の質ではなく、情報が届く瞬間の受け手の状態（時間帯・負荷・気分・場所・直前の出来事）にあり、同じ内容でも受け取る状態が違う人では反応が分かれている。"
            "典型的な分析は、内容の改善、頻度の増加、受け手の意識の低さへの帰責を行う。"
        ),
        "domains": ["社内通達が読まれず手続が遅れる問題", "診療所の服薬指導資料", "自治体の防災情報メール"],
        "banned": ["受け手の状態", "受容", "受け取る側", "受け手側", "発信側"],
    },
    "T8_part_whole": {
        "framework": "huayan",
        "plant": (
            "一つの小さな部分（一人の行動、一つの会議、一枚の書類）に現れている癖や不具合が、"
            "より大きな単位（チーム、部門、組織全体）にも、さらに小さな単位（個々の作業）にも同じ形で現れており、部分が全体の状態を映している。"
            "典型的な分析は、その部分の個別の問題として局所的に対処しようとする。"
        ),
        "domains": ["小さな支店の朝会で見られる癖", "一つのチームの引き継ぎ書の書き方", "一つのクラスの授業中の様子"],
        "banned": ["全体を映", "縮図", "入れ子", "フラクタル", "全体の反映"],
    },
}

NULL_DOMAINS = [
    ("サーバのディスクが満杯になって業務システムが停止した", "ディスク容量の枯渇が直接の原因である。"),
    ("値上げ後に特定商品の売上が減った", "値上げによる価格弾力性の影響で足りる。"),
    ("センサの故障で温度記録が欠けた", "センサの故障という単純な機器不良である。"),
    ("インフルエンザ流行期に外来の待ち時間が延びた", "患者数の増加と欠勤による人手不足で説明できる。"),
    ("設定ファイルの誤記で配信メールが送れなかった", "設定の誤記という単純な人為ミスである。"),
    ("仕入先の納期遅れで工事が三日延びた", "仕入先の納期遅れという外的要因で足りる。"),
    ("新人研修を省略した部署で入力ミスが増えた", "研修不足という素直な因果で足りる。"),
    ("豪雨で道路が冠水し配送が遅れた", "気象という単純な外的要因で足りる。"),
]

WRITER_SYS = (
    "あなたは合成ケーススタディの作成者です。指定された潜在構造を、状況の記述だけから読み取れる形で埋め込みます。"
    "構造の名前や、答えを直接言い当てる説明語は使いません。登場する人物と組織は架空です。出力はJSONのみです。"
)

WRITER_USER = """次の条件でケーススタディを一つ作ってください。

領域: {domain}
埋め込む潜在構造: {plant}

要件:
- material: 日本語で450〜750字。観察・数値・日付・発言などの事実を平易に書く。潜在構造を裏づける事実は、材料の中に必ず含める。ただし構造を名指す説明や結論は書かない。
- trap: 多くの分析者が最初に出す典型的な説明を1〜2文で書く。
- key: 潜在構造そのものを、この状況に即して2文以内で書く。
- evidence: key を裏づける材料内の記述を、材料から一字一句そのまま引用して2〜4個挙げる。
- 次の語を material に使わない: {banned}

JSONのキー: material, trap, key, evidence（evidenceは文字列の配列）"""

NULL_USER = """次の条件でケーススタディを一つ作ってください。これは潜在構造を含まない対照用の課題です。

出来事: {event}
正しい説明: {truth}

要件:
- material: 日本語で450〜750字。出来事の経過と、標準的な説明を支える事実を平易に書く。隠れた構造や意外な関係は入れない。余計な示唆や伏線も入れない。
- trap: 「標準的な説明で十分である」ことを1文で書く。
- key: 「潜在構造はなく、標準的な説明で足りる」とその説明の内容を2文以内で書く。
- evidence: 標準的な説明を裏づける材料内の記述を、材料から一字一句そのまま引用して2〜3個挙げる。

JSONのキー: material, trap, key, evidence（evidenceは文字列の配列）"""

CHECK_SYS = "あなたは厳密な査読者です。出力はJSONのみです。"
CHECK_USER = """次のケースについて、二点を判定してください。

材料:
{material}

鍵（潜在構造）:
{key}

判定:
1. derivable: 鍵は、材料の記述だけから（外部の専門知識に頼らずに）導けるか。true/false
2. leaks: 材料の中に、鍵の構造そのものを名指して説明している文があるか。true/false
3. note: 理由を一文で。

JSONのキー: derivable, leaks, note"""


def write_one(spec: dict) -> dict | None:
    for attempt in range(8):
        if spec["kind"] == "latent":
            user = WRITER_USER.format(
                domain=spec["domain"], plant=spec["plant"], banned="、".join(spec["banned"])
            )
        else:
            user = NULL_USER.format(event=spec["event"], truth=spec["truth"])
        r = llm.call(
            "deepseek",
            "deepseek-v4-pro",
            [{"role": "system", "content": WRITER_SYS}, {"role": "user", "content": user}],
            tag=f"writer-{spec['id']}-{attempt}",
            max_tokens=2500,
            temperature=0.8,
            json_mode=True,
        )
        obj = llm.parse_json(r["text"])
        if not isinstance(obj, dict) or not all(k in obj for k in ("material", "trap", "key", "evidence")):
            continue
        material = obj["material"]
        lo = 350 if spec["kind"] == "latent" else 260
        if not isinstance(material, str) or not (lo <= len(material) <= 1000):
            continue
        if spec["kind"] == "latent" and any(b in material for b in spec["banned"]):
            continue
        ev = obj["evidence"]
        if not isinstance(ev, list) or not all(isinstance(e, str) and e in material for e in ev):
            continue
        c = llm.call(
            "deepseek",
            "deepseek-v4-flash",
            [
                {"role": "system", "content": CHECK_SYS},
                {"role": "user", "content": CHECK_USER.format(material=material, key=obj["key"])},
            ],
            tag=f"check-{spec['id']}-{attempt}",
            max_tokens=4000,
            temperature=0.0,
            thinking=True,
            json_mode=True,
        )
        chk = llm.parse_json(c["text"]) or {}
        if chk.get("derivable") is True and (spec["kind"] == "null" or chk.get("leaks") is False):
            task = {k: spec[k] for k in ("id", "kind", "type", "domain", "framework") if k in spec}
            task.update(
                material=material, trap=obj["trap"], key=obj["key"], evidence=ev, check=chk, attempt=attempt
            )
            return task
    return None


def main() -> None:
    specs = []
    for tname, t in TYPES.items():
        for i, dom in enumerate(t["domains"]):
            specs.append(
                dict(
                    id=f"{tname}-{i + 1}", kind="latent", type=tname, domain=dom, framework=t["framework"],
                    plant=t["plant"], banned=t["banned"],
                )
            )
    for i, (event, truth) in enumerate(NULL_DOMAINS):
        specs.append(dict(id=f"N-{i + 1}", kind="null", type="null", domain=event, event=event, truth=truth))

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(write_one, specs))
    tasks = [r for r in res if r]
    failed = [s["id"] for s, r in zip(specs, res) if not r]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tasks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"accepted {len(tasks)}/{len(specs)}; failed: {failed}; est. spend ${llm.spent():.3f}")


if __name__ == "__main__":
    main()
