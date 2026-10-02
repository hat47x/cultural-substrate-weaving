"""Prompt construction for each study arm.

Fm / Fx use the repository's own dossiers (src/ja-JP/frameworks/*.md), trimmed to the
"core structure" and "strong cognitive operations" sections so that card length is
comparable across frameworks. R uses unrelated, non-cultural concept cards written in
the same template. RT approximates the shipped runtime (ROUTER + discovery pathway +
portfolio index; the model picks frameworks, then receives the chosen dossiers).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "ja-JP"

FW_NAME = {
    "yijing": "易（八卦・六十四卦）",
    "wuxing": "五行",
    "dependent-origination": "縁起",
    "jain-sevenfold-predication": "ジャイナの多面説・七分法",
    "aristotle-four-causes": "アリストテレスの四原因",
    "maya-calendars": "マヤ暦体系",
    "rasa": "ラサ論",
    "huayan": "華厳",
}
# Mismatched framework per matched framework (chosen to be structurally distant).
MISMATCH = {
    "yijing": "dependent-origination",
    "wuxing": "jain-sevenfold-predication",
    "dependent-origination": "rasa",
    "jain-sevenfold-predication": "huayan",
    "aristotle-four-causes": "wuxing",
    "maya-calendars": "aristotle-four-causes",
    "rasa": "yijing",
    "huayan": "maya-calendars",
}
FW_ORDER = list(FW_NAME)

PREAMBLE_FW = (
    "【補助】次の体系の構造核と認知操作を、この状況に仮に走らせてみてください。"
    "体系から出た問いには「この系として見るなら」と添えてください。"
    "ただし、材料に支えのない構造を事実として断定しないでください。\n\n"
)
PREAMBLE_R = (
    "【補助】次の概念の構造核と操作を、この状況に仮に走らせてみてください。"
    "その概念から出た問いには「この概念として見るなら」と添えてください。"
    "ただし、材料に支えのない構造を事実として断定しないでください。\n\n"
)

REQUEST = (
    "【依頼】この状況について、まだ調べられていない、または確かめる価値のある問いを五つ挙げてください。"
    "各問いには、材料のどの記述に基づくかを一文で添えてください。\n"
    '出力はJSONのみ: {"questions":[{"q":"問い","basis":"根拠となる材料内の記述"}, ...]}'
)

GENERIC_LENS = (
    "【補助】通常の分析の枠から一度離れ、異なる観点から問いを立ててください。"
    "ただし、材料に支えのない主張を事実として断定しないでください。\n\n"
)


GENERIC_LENSES = [
    GENERIC_LENS,
    "【補助】この状況を、まだ誰も試していない角度から見て、問いを立ててください。"
    "ただし、材料に支えのない主張を事実として断定しないでください。\n\n",
    "【補助】典型的な説明をいったん脇に置き、見落とされていそうな構造や関係に注目して問いを立ててください。"
    "ただし、材料に支えのない主張を事実として断定しないでください。\n\n",
    "【補助】この状況を、専門外の人の目で見直し、素朴だが核心を突く問いを立ててください。"
    "ただし、材料に支えのない主張を事実として断定しないでください。\n\n",
]


def portfolio_for(task: dict, k: int = 4) -> dict:
    """Deterministic catalyst sets of equal size k for the portfolio study."""
    import random

    rnd = random.Random(sum(ord(c) for c in task["id"]))
    fws = list(FW_NAME)
    if task["kind"] == "latent":
        matched = task["framework"]
        others = [f for f in fws if f != matched]
        rnd.shuffle(others)
        fw_set = [matched] + others[: k - 1]
    else:
        rnd.shuffle(fws)
        fw_set = fws[:k]
    rc = list(R_CARDS)
    rnd.shuffle(rc)
    return {
        "PF": [f"FW:{f}" for f in fw_set],
        "PR": [f"RC:{c}" for c in rc[:k]],
        "PG": [f"GL:{i}" for i in range(k)],
        "PB": ["B0"] * k,
    }


def _sections(text: str, wanted: tuple[str, ...]) -> str:
    out = []
    for block in re.split(r"(?m)^(?=## )", text):
        head = block.split("\n", 1)[0]
        if any(w in head for w in wanted):
            out.append(block.strip())
    title = text.split("\n", 1)[0].strip()
    return title + "\n\n" + "\n\n".join(out)


def dossier_card(fw: str) -> str:
    text = (SRC / "frameworks" / f"{fw}.md").read_text(encoding="utf-8")
    return _sections(text, ("採用する構造核", "強い認知操作"))


def dossier_full(fw: str) -> str:
    text = (SRC / "frameworks" / f"{fw}.md").read_text(encoding="utf-8")
    text = re.split(r"(?m)^## 再確認用資料", text)[0]
    return text.strip()


R_CARDS = {
    "発酵": """# 発酵

## 構造核
発酵は、仕込んだ材料の中で微生物が働き、時間をかけて別のものへ変わっていく過程である。温度、塩分、水分、空気の量が条件になり、同じ材料でも条件が違えば発酵にも腐敗にもなる。種菌や酵母を次の仕込みへ引き継ぐことで、性質が受け継がれる。

## 強い認知操作
- 仕込み条件の特定: 結果を、仕込んだときの条件へ遡って問う。
- 熟成の見守り: 急いで変えず、時間をおいたときに何が現れるかを見る。
- 発酵と腐敗の境界: 同じ変化が良い方向と悪い方向に分かれる条件を探す。
- 種の引き継ぎ: 前の仕込みから何が次へ持ち越されているかを見る。
- 条件替えの比較: 同じ材料を別の条件に置いたら何が変わるかを考える。""",
    "折り紙": """# 折り紙

## 構造核
折り紙は、一枚の紙に折り線を入れて立体や形を作る技法である。折り線の配置が展開図として残り、どの線を谷折り、どの線を山折りにするかで形が決まる。切らずに一枚の連続した面のまま変形するという制約がある。

## 強い認知操作
- 展開図への還元: 完成形を、折る前の一枚の面と折り線の配置へ戻して見る。
- 谷と山の区別: 同じ線でも折る向きで結果が逆になることを問う。
- 連続性の制約: 切り離さずに変形するとき、どの部分が引っ張られて動くかを見る。
- 折り順の依存: 先に折った線が、後の折りを可能にも不可能にもすることを探す。
- 折り直し: 一度折った形を開いて、跡として何が残るかを見る。""",
    "鍛冶": """# 鍛冶

## 構造核
鍛冶は、金属を熱して叩き、形と性質を整える技である。熱して柔らかくし、叩いて形を作り、急に冷やして硬くし（焼き入れ）、再び加熱して粘りを戻す（焼き戻し）。硬さと粘りは両立しにくく、工程の温度と順序で釣り合いが決まる。

## 強い認知操作
- 熱と冷の切り替え: 変化を促す段階と、固定する段階を分けて見る。
- 叩く場所の選択: どこに力を加えると全体の形が変わるかを問う。
- 硬さと粘りの釣り合い: 一つの性質を強めたときに失われる性質を探す。
- 焼き戻し: 一度固めたものを少し緩めて、使える状態に戻す工程を考える。
- 不純物の叩き出し: 叩く過程で外へ出ていくものは何かを見る。""",
    "地層": """# 地層

## 構造核
地層は、時間とともに堆積物が積み重なってできる層の並びである。下の層ほど古いという順序があり、各層の厚さや含まれるものが当時の環境を伝える。層の途中が削られて欠けている不整合や、断層によるずれがある。

## 強い認知操作
- 積み重なりの読み取り: 現在の状態を、古い順に重なった履歴として読む。
- 層の厚さの比較: 変化が速かった時期と遅かった時期を見分ける。
- 不整合の探索: 記録が途切れている箇所と、その間に失われたものを探す。
- 含有物の手がかり: 各層に混じっているものから、その時点の環境を推し量る。
- 断層のずれ: 連続していたものが途中でずれた位置を探す。""",
    "織物": """# 織物

## 構造核
織物は、縦糸と横糸を交差させて面を作る。縦糸は先に張られて骨組みになり、横糸がそれを上下にくぐって模様と強度を生む。織り方（平織、綾織、繻子織）によって、見える糸と隠れる糸の割合が変わる。一本の糸が切れると、ほつれが広がる。

## 強い認知操作
- 縦と横の区別: 先に張られた骨組みと、後から通される要素を分ける。
- 織り目の観察: 交差する箇所で、どちらが上にどちらが下になっているかを見る。
- 見える糸と隠れる糸: 表に出ていない部分が全体の強度を担っていないかを問う。
- ほつれの起点: 一本の切れ目から広がるほつれの出発点を探す。
- 織り方の違い: 同じ糸でも織り方で全体の性質がどう変わるかを比べる。""",
    "蜂の巣": """# 蜂の巣

## 構造核
蜂の巣は、六角形の小部屋を隙間なく敷き詰めた構造である。各部屋は育児、貯蜜、花粉の保管など別の用途に使われ、巣の中心に育児が、外側に貯蜜が置かれる傾向がある。蜂群が増えると分蜂が起きて、新しい巣へ移る。

## 強い認知操作
- 隙間なく敷き詰める: 無駄な空間を残さない配置の制約を見る。
- 部屋ごとの用途: 同じ形の部屋が、場所によって別の役割を持っていないかを問う。
- 中心と外側: 重要なものが巣のどこに置かれているかの偏りを探す。
- 蜂群の増加と分かれ: 手狭になったときに群れが分かれる条件を考える。
- 蜜と花粉の貯蔵量: 蓄えがどれだけあるかで、巣の活動がどう変わるかを見る。""",
    "潮汐": """# 潮汐

## 構造核
潮汐は、月と太陽の引力によって海面が上下する現象である。満ち潮と引き潮が一日に二度ほど繰り返され、月の満ち欠けに合わせて大潮と小潮が現れる。湾の形や海底の地形によって、同じ潮でも水位の振れ幅が増幅される。

## 強い認知操作
- 満ち引きの把握: 上がる時と下がる時の両方で何が見えるかを問う。
- 基準面の確認: 水位を測る基準がどこに置かれているかを見る。
- 地形による増幅: 同じ力が場所の形によって大きくも小さくもなることを探す。
- 干潮時に現れるもの: 水が引いたときにだけ見える底の構造を探す。
- 大潮と小潮: 振れが大きい時期と小さい時期の違いを見る。""",
    "渡り鳥の編隊": """# 渡り鳥の編隊

## 構造核
渡り鳥の群れは、先頭の一羽が全体を導くのではなく、各個体が隣の個体との距離と向きを合わせるという局所の規則から、V字などの全体の形を作る。先頭は交代し、気流を利用して体力を節約する。環境が変わると群れの形が組み変わる。

## 強い認知操作
- 局所の規則から全体を見る: 全体の形が、隣との関係だけから生まれていないかを問う。
- 先頭の交代: 負担の大きい位置が順に入れ替わる仕組みを探す。
- 気流の利用: 前の個体が作る流れを後ろが利用している関係を見る。
- 隊形の組み替え: 環境の変化に応じて群れの形が変わる条件を考える。
- はぐれた個体: 群れから離れた個体に何が起きているかを見る。""",
}
R_ORDER = list(R_CARDS)


def r_card_for(task_id: str) -> tuple[str, str]:
    idx = sum(ord(c) for c in task_id) % len(R_ORDER)
    name = R_ORDER[idx]
    return name, R_CARDS[name]


def task_block(task: dict) -> str:
    return f"【状況】\n{task['material']}\n\n"


def build(arm: str, task: dict) -> list[dict]:
    """Return chat messages for single-turn arms. RT is handled in run_generation."""
    fw = task.get("framework")
    # For null tasks, assign framework by id so every framework is equally "forced".
    if fw is None or task["kind"] == "null":
        n = int(task["id"].split("-")[-1]) - 1
        fw = FW_ORDER[n % len(FW_ORDER)]
    base = task_block(task)
    if arm == "B0":
        user = base + REQUEST
    elif arm == "G":
        user = base + GENERIC_LENS + REQUEST
    elif arm == "R":
        _, card = r_card_for(task["id"])
        user = base + PREAMBLE_R + card + "\n\n" + REQUEST
    elif arm == "N":
        user = (
            base
            + f"【補助】{FW_NAME[fw]}の見方を、この状況に仮に当ててみてください。"
            + "体系から出た問いには「この系として見るなら」と添えてください。"
            + "ただし、材料に支えのない構造を事実として断定しないでください。\n\n"
            + REQUEST
        )
    elif arm == "Fm":
        user = base + PREAMBLE_FW + dossier_card(fw) + "\n\n" + REQUEST
    elif arm == "Fx":
        user = base + PREAMBLE_FW + dossier_card(MISMATCH[fw]) + "\n\n" + REQUEST
    elif arm.startswith("FW:"):  # explicit framework catalyst (portfolio study)
        user = base + PREAMBLE_FW + dossier_card(arm[3:]) + "\n\n" + REQUEST
    elif arm.startswith("RC:"):  # explicit random-concept catalyst
        user = base + PREAMBLE_R + R_CARDS[arm[3:]] + "\n\n" + REQUEST
    elif arm.startswith("GL:"):  # generic lens variant i
        user = base + GENERIC_LENSES[int(arm[3:])] + REQUEST
    else:
        raise ValueError(arm)
    return [{"role": "user", "content": user}]


def runtime_system() -> str:
    parts = [
        (SRC / "ROUTER.md").read_text(encoding="utf-8"),
        (SRC / "core" / "discovery-pathway.md").read_text(encoding="utf-8"),
        (SRC / "frameworks" / "portfolio.md").read_text(encoding="utf-8"),
    ]
    return (
        "あなたは次のスキル定義（cultural-substrate-weaving）に従って作業するアシスタントです。\n\n"
        + "\n\n---\n\n".join(parts)
    )


RT_FW_IDS = {
    "yijing": "易", "wuxing": "五行", "sankhya": "サーンキヤ", "dependent-origination": "縁起",
    "catuskoti": "四句分別", "jain-sevenfold-predication": "ジャイナの多面説・七分法",
    "aristotle-four-causes": "アリストテレスの四原因", "rasa": "ラサ論", "maya-calendars": "マヤ暦体系",
    "huayan": "華厳",
}

RT_CHOOSE = (
    "【依頼1】この状況について、使えそうな文化体系をポートフォリオから0個から2個選んでください。"
    "使わない選択も可能です。選ぶ場合は、その体系のどの操作をこの状況に使うかを一文で添えてください。\n"
    f"選べるid: {', '.join(RT_FW_IDS)}\n"
    '出力はJSONのみ: {"choice":["id", ...], "reason":"理由"}'
)
