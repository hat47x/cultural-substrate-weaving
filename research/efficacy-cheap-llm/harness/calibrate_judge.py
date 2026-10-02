"""Judge calibration: synthetic positive/negative outputs per latent task.

POS: five questions, one of which genuinely probes the planted structure.
NEG: five questions asked from the standard (trap) view only.
A usable judge scores POS as 2 and NEG as 0 for nearly all tasks.
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge  # noqa: E402
import llm  # noqa: E402
from run_generation import parse_questions  # noqa: E402

tasks = [t for t in json.loads(judge.TASKS.read_text(encoding="utf-8")) if t["kind"] == "latent"]

POS = """次の状況について、問いを五つ作ってください。うち一つは、次の「鍵」が指す構造そのものを調べる問いにしてください。鍵の言葉をそのまま使わず、状況の言葉で書いてください。残りの四つは、一般的な分析で出る問いで構いません。

【状況】
{material}

【鍵】
{key}

出力はJSONのみ: {{"questions":[{{"q":"問い","basis":"根拠となる材料内の記述"}}]}}"""

NEG = """次の状況について、問いを五つ作ってください。次の「典型的な説明」の立場に立った問いだけにし、他の構造や関係には触れないでください。

【状況】
{material}

【典型的な説明】
{trap}

出力はJSONのみ: {{"questions":[{{"q":"問い","basis":"根拠となる材料内の記述"}}]}}"""


def run(t):
    res = {}
    for kind, tpl in (("POS", POS), ("NEG", NEG), ("NEG2", NEG)):
        r = llm.call(
            "deepseek", "deepseek-v4-flash",
            [{"role": "user", "content": tpl.format(material=t["material"], key=t["key"], trap=t["trap"])}],
            tag=f"calib-{kind}-{t['id']}", max_tokens=1500, temperature=0.7, json_mode=True,
        )
        qs = parse_questions(r["text"])
        res[kind] = judge.judge_hit(t, qs, tag=f"calib-{kind}-{t['id']}") if qs else None
    return t["id"], res


with ThreadPoolExecutor(max_workers=10) as ex:
    out = dict(ex.map(run, tasks))

pos = [v["POS"] for v in out.values()]
neg = [v["NEG"] for v in out.values()]
acc = [k for k, v in out.items() if v["POS"] == 2 and v["NEG"] == 0 and v["NEG2"] == 0]
print("ACCEPTED", len(acc), acc)
json.dump(acc, open(judge.TASKS.with_name(judge.TASKS.stem + "_calibrated_ids.json"), "w"))
print("POS scores:", pos)
print("NEG scores:", neg)
print(f"POS==2: {sum(1 for x in pos if x == 2)}/{len(pos)}  NEG==0: {sum(1 for x in neg if x == 0)}/{len(neg)}")
for k, v in out.items():
    if k not in acc:
        print("  flag", k, v)
print(f"est. spend ${llm.spent():.3f}")
