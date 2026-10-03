"""Jev as a framework router (preregistered in 05): FIT and DIST selection per task.

The material alone is the state; ten frameworks are the options, in three different
orders; probabilities are averaged and the arg-max is taken.
"""

import hashlib
import json
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm
from jev_judge import CACHE, MODEL, URL

T = Path(__file__).resolve().parents[1] / "tasks"
TASKS = {t["id"]: t for t in json.loads((T / "tasks.json").read_text(encoding="utf-8"))}

FW = {
    "yijing": "易: 再分節、位置、変化、入れ子。2種の爻、8卦、64卦",
    "wuxing": "五行: 生成と抑制、循環、関係役割。5相、相生・相剋",
    "sankhya": "サーンキヤ: 層、生成順序、観察者と生成物の分離",
    "dependent-origination": "縁起: 条件依存、発生と消滅、介入点",
    "catuskoti": "四句分別: 二値の枠の解体、命題空間の拡張",
    "jain-sevenfold-predication": "ジャイナの多面説: 視点条件、限定付きの叙述",
    "aristotle-four-causes": "アリストテレスの四原因: 「なぜ」の説明軸を分ける",
    "rasa": "ラサ論: 表現と受け手の経験の生成関係",
    "maya-calendars": "マヤ暦: 複数周期、位相差、部分と全体の再来",
    "huayan": "華厳: 全体と部分の相互規定、node視点、差異を残す統合",
}
FIT = ("この状況の構造（役割の集合、循環、条件の連鎖、視点の条件、「なぜ」の種類、周期、受け手、部分と全体など）に、"
       "最も合う体系を一つ選ぶ。")
DIST = ("この状況は、普通に分析すると、原因や担当の問題として見られがちである。その見方から最も構造的に遠い見方を持つ"
        "体系を一つ選ぶ。")
ACCEPT = {  # strict target and the set accepted under the permissive criterion
    "T1_vacancy": ("yijing", {"yijing", "sankhya"}),
    "T3_chain_cut": ("dependent-origination", {"dependent-origination"}),
    "T4_standpoint": ("jain-sevenfold-predication", {"jain-sevenfold-predication", "catuskoti"}),
    "T5_four_whys": ("aristotle-four-causes", {"aristotle-four-causes"}),
    "T6_two_cycles": ("maya-calendars", {"maya-calendars"}),
    "T7_reception": ("rasa", {"rasa"}),
    "T8_part_whole": ("huayan", {"huayan"}),
}


def decide(state, instr, order):
    crit = {k: FW[k] for k in order}
    body = {"model": MODEL, "state": state, "questions": {"q": {"type": "choice", "instructions": instr, "criteria": crit}}}
    key = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    p = CACHE / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text())["answers"]["q"]
    data = json.dumps(body, ensure_ascii=False).encode()
    for a in range(5):
        req = urllib.request.Request(URL, data=data, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {llm._token('openrouter')}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode())
            p.write_text(json.dumps(out))
            return out["answers"]["q"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 402, 403):
                raise RuntimeError(e.read().decode()[:200])
        except Exception:
            pass
        time.sleep(2 ** a)
    return None


def route(tid, instr):
    t = TASKS[tid]
    state = f"【状況】\n{t['material']}"
    acc = {k: 0.0 for k in FW}
    for perm in range(3):
        order = list(FW)
        random.Random(f"{tid}-{perm}").shuffle(order)
        a = decide(state, instr, order)
        for k, v in (a.get("probabilities") or {}).items():
            acc[k] += v / 3
    return max(acc, key=acc.get), acc


def main():
    out = {}
    cal0 = set(json.load(open(T / "calibrated_ids.json")))
    ids = sorted(i for i in TASKS if i in cal0 or TASKS[i]["kind"] == "null")
    with ThreadPoolExecutor(max_workers=8) as ex:
        for name, instr in (("FIT", FIT), ("DIST", DIST)):
            res = list(ex.map(lambda i: route(i, instr), ids))
            out[name] = {i: {"pick": r[0], "p": r[1]} for i, r in zip(ids, res)}
    (llm.WORK / "router-picks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    cal = set(json.load(open(T / "calibrated_ids.json")))
    lat = [i for i in ids if i in cal]
    for name in ("FIT", "DIST"):
        strict = sum(1 for i in lat if out[name][i]["pick"] == ACCEPT[i.split("-")[0]][0])
        perm = sum(1 for i in lat if out[name][i]["pick"] in ACCEPT[i.split("-")[0]][1])
        print(f"{name}: strict {strict}/{len(lat)} = {strict/len(lat):.3f}; permissive {perm}/{len(lat)} = {perm/len(lat):.3f}")
        import collections
        print("   picks:", collections.Counter(out[name][i]["pick"] for i in ids).most_common())
    # RT self-selection from stage 1 for reference
    rt = [json.loads(l) for l in open(llm.WORK / "gen-main-latent.jsonl", encoding="utf-8")]
    rt = [r for r in rt if r["arm"] == "RT" and r.get("ok")]
    m = sum(1 for r in rt if r.get("matched"))
    print(f"RTSELF (stage 1): contains matched framework in {m}/{len(rt)} = {m/len(rt):.3f}")


if __name__ == "__main__":
    main()
