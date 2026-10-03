"""Re-read existing results through the typology (post hoc, descriptive).

1. SEL_RAND vs B0 pairwise score by relation of the randomly given framework to the task:
   target-structure match / same super-family but no match / other super-family.
2. Per-framework mean score of SEL_RAND vs B0 (descriptive; n is small).
3. Fm vs B0 / Fx / R pairwise score by target-structure type (two tasks each).
"""

import collections
import json
import random
from pathlib import Path

H = Path(__file__).resolve().parent
W = H.parents[2] / "local" / "efficacy-cheap-llm"
TYP = json.loads((H.parent / "framework-typology.json").read_text(encoding="utf-8"))
ALIAS = {"maya-calendars": "tzolkin"}
FW = {f["id"]: f for f in TYP["frameworks"]}
fw = lambda i: FW[ALIAS.get(i, i)]
TASKS = {}
for f in ("tasks.json", "tasks_v2.json"):
    for t in json.loads((H.parent / "tasks" / f).read_text(encoding="utf-8")):
        TASKS[t["id"]] = t
TS_OF = {"T1_vacancy": "TS-closed-set-vacancy", "T3_chain_cut": "TS-condition-chain", "T4_standpoint": "TS-standpoint-conditional",
         "T5_four_whys": "TS-explanation-plurality", "T6_two_cycles": "TS-coupled-periodicity", "T7_reception": "TS-reception-gap",
         "T8_part_whole": "TS-whole-part-mirroring"}
ts_of_task = lambda tid: TS_OF[tid.split("-")[0]]

gen = {}
for l in open(W / "gen-sel.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r.get("ok"):
        gen[(r["arm"], r["task"], r["k"])] = r["fw"]
PW = [json.loads(l) for l in open(W / "sel-pairwise.jsonl", encoding="utf-8") if l.strip()]
PW = [r for r in PW if r["s_fwd"] is not None and r["s_swap"] is not None]
for r in PW:
    r["score"] = (r["s_fwd"] + r["s_swap"]) / 2


def relation(f, tid):
    ts = ts_of_task(tid)
    matched = TASKS[tid]["framework"]
    if ts in fw(f)["ts"]:
        return "TS-match"
    if fw(f)["sf"] == fw(matched)["sf"]:
        return "same-family, no match"
    return "other family"


def boot(xs, n=4000, seed=5):
    rnd = random.Random(seed)
    ms = sorted(sum(rnd.choice(xs) for _ in xs) / len(xs) for _ in range(n))
    return ms[int(.025 * n)], ms[int(.975 * n)]


print("== 1. SEL_RAND vs B0 (score of the framework arm; 0.5 = no difference), by relation to the task")
rows = [(relation(gen[("SEL_RAND", r["task"], r["k"])], r["task"]), r["task"], r["score"]) for r in PW if r["a"] == "SEL_RAND" and r["b"] == "B0"]
by = collections.defaultdict(list)
for rel, tid, s in rows:
    by[rel].append((tid, s))
for rel, xs in sorted(by.items()):
    per = collections.defaultdict(list)
    for tid, s in xs:
        per[tid].append(s)
    tm = [sum(v) / len(v) for v in per.values()]
    lo, hi = boot(tm)
    print(f"  {rel:24s} pairs={len(xs):3d} tasks={len(tm):2d} mean={sum(s for _, s in xs)/len(xs):.3f} task-level {sum(tm)/len(tm):.3f} [{lo:.3f},{hi:.3f}]")

print("\n== 2. per-framework mean (SEL_RAND vs B0), descriptive")
pf = collections.defaultdict(list)
for r in PW:
    if r["a"] == "SEL_RAND" and r["b"] == "B0":
        pf[gen[("SEL_RAND", r["task"], r["k"])]].append(r["score"])
for f, xs in sorted(pf.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
    print(f"  {f:30s} sf={fw(f)['sf']} n={len(xs):2d} mean={sum(xs)/len(xs):.3f}")

print("\n== 2b. same table for the framework FIT and DIST each used (nearly a single framework)")
for arm in ("SEL_FIT", "SEL_DIST"):
    c = collections.Counter(gen[(arm, r['task'], r['k'])] for r in PW if r["a"] == arm and r["b"] == "B0")
    sc = [r["score"] for r in PW if r["a"] == arm and r["b"] == "B0"]
    print(f"  {arm}: frameworks {dict(c)}; mean score vs B0 {sum(sc)/len(sc):.3f}")

print("\n== 3. Fm vs B0 / Fx / R by target-structure type (stage-1 pairwise, two tasks per type)")
S1 = [json.loads(l) for l in open(W / "jev-pairwise.jsonl", encoding="utf-8") if l.strip()]
S1 = [r for r in S1 if r.get("s_fwd") is not None and r.get("s_swap") is not None]
print("  type                         Fm-B0   Fm-Fx   Fm-R    Fm-G    RT-B0   (tasks)")
types = sorted({r["task"].split("-")[0] for r in S1})
for ty in types:
    cells = []
    for a, b in (("Fm", "B0"), ("Fm", "Fx"), ("Fm", "R"), ("Fm", "G"), ("RT", "B0")):
        xs = [(r["s_fwd"] + r["s_swap"]) / 2 for r in S1 if r["a"] == a and r["b"] == b and r["task"].split("-")[0] == ty]
        cells.append(f"{sum(xs)/len(xs):.2f}" if xs else " n/a")
    n = len({r["task"] for r in S1 if r["task"].split("-")[0] == ty})
    print(f"  {ty:28s} " + "    ".join(cells) + f"   ({n})")
