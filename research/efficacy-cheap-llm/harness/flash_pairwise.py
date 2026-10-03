"""Sensitivity (not preregistered): pairwise judging of the four primary contrasts with flash."""
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge
import llm
from jev_pairwise import CRIT, INSTR, PRIMARY, TASKS

PAIRS = [("Fm", "B0"), ("Fm", "G"), ("Fm", "Fx"), ("Fm", "R")]
SYS = "あなたは厳密で一貫した判定者です。出力はJSONのみです。"
gen = {}
for l in open(llm.WORK / "gen-main-latent.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r.get("ok"):
        gen[(r["arm"], r["task"], r["k"])] = r["questions"]


def ask(t, qa, qb, tag):
    opts = "\n".join(f"- {k}: {v}" for k, v in CRIT.items())
    user = (f"{INSTR}\n\n【状況】\n{t['material']}\n\n【鍵】\n{t['key']}\n\n【固有の要素】\n{t.get('signature', '')}\n\n"
            f"【典型的な説明】\n{t['trap']}\n\n【先の組の問い】\n{judge.fmt_questions(qa, with_basis=False)}\n\n"
            f"【後の組の問い】\n{judge.fmt_questions(qb, with_basis=False)}\n\n選択肢:\n{opts}\n\n"
            "JSONのキーをこの順に出力: reason（二文以内）, label（first, second, tieのいずれか）")
    r = llm.call("deepseek", "deepseek-v4-flash", [{"role": "system", "content": SYS}, {"role": "user", "content": user}],
                 tag=tag, max_tokens=700, temperature=0.0, json_mode=True)
    o = llm.parse_json(r["text"]) or {}
    return o.get("label") if o.get("label") in CRIT else None


jobs = [(a, b, t, k) for a, b in PAIRS for t in PRIMARY for k in range(6) if (a, t, k) in gen and (b, t, k) in gen]


def f(j):
    a, b, t, k = j
    qa = [{"q": judge.scrub(q["q"]), "basis": ""} for q in gen[(a, t, k)]]
    qb = [{"q": judge.scrub(q["q"]), "basis": ""} for q in gen[(b, t, k)]]
    r1 = ask(TASKS[t], qa, qb, f"pw-{a}-{b}-{t}-{k}-f")
    r2 = ask(TASKS[t], qb, qa, f"pw-{a}-{b}-{t}-{k}-s")
    s1 = {"first": 1.0, "tie": 0.5, "second": 0.0}.get(r1)
    s2 = {"first": 0.0, "tie": 0.5, "second": 1.0}.get(r2)
    return a, b, t, k, r1, r2, s1, s2


with ThreadPoolExecutor(max_workers=16) as ex:
    res = [x for x in ex.map(f, jobs) if x[6] is not None and x[7] is not None]
print(len(res), "complete pairs; est spend", round(llm.spent(), 3))
print("order consistency", round(sum(1 for x in res if x[6] == x[7]) / len(res), 3),
      "| first chosen when target first/second:",
      round(sum(1 for x in res if x[4] == "first") / len(res), 3), round(sum(1 for x in res if x[5] == "first") / len(res), 3),
      "| tie share", round(sum(1 for x in res if x[4] == "tie") / len(res), 3))
rnd = random.Random(3)
for a, b in PAIRS:
    d = {}
    for t in PRIMARY:
        xs = [(x[6] + x[7]) / 2 for x in res if x[0] == a and x[1] == b and x[2] == t]
        if xs:
            d[t] = sum(xs) / len(xs)
    v = list(d.values())
    ms = sorted(sum(rnd.choice(v) for _ in v) / len(v) for _ in range(5000))
    print(f"{a}-{b}: {sum(v)/len(v):.3f} [{ms[125]:.3f},{ms[4875]:.3f}] +{sum(x > .5 for x in v)}/-{sum(x < .5 for x in v)}")
