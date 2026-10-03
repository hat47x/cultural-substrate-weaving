"""Does the pairwise 'directness' advantage coincide with forcing?

Classify every stage-1 latent output (Jev, same instrument as stage 3: forced / hedged / clean),
then join with the stage-1 pairwise results.
"""

import collections
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import jev_stage3 as j3
import llm

W = llm.WORK
gen = {}
for l in open(W / "gen-main-latent.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r.get("ok") and r["questions"]:
        gen[(r["arm"], r["task"], r["k"])] = r["questions"]


def f(item):
    key, qs = item
    t = j3.TASKS[key[1]]
    st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{j3.qtext(qs)}"
    return key, j3.decide(st, j3.I_FORCE, j3.C_FORCE)


with ThreadPoolExecutor(max_workers=16) as ex:
    force = dict(ex.map(f, gen.items()))
(W / "s1-force.json").write_text(json.dumps({"|".join(map(str, k)): v for k, v in force.items()}, ensure_ascii=False), encoding="utf-8")

print("== forced rate on latent tasks (stage-1 outputs, all 14 tasks)")
for arm in ["B0", "G", "R", "N", "Fx", "Fm", "RT"]:
    v = [force[k] for k in force if k[0] == arm]
    c = collections.Counter(v)
    print(f"  {arm:3s} n={len(v):3d} forced={c['forced']/len(v):.3f} hedged={c['hedged']/len(v):.3f} clean={c['clean']/len(v):.3f}")

PW = [json.loads(l) for l in open(W / "jev-pairwise.jsonl", encoding="utf-8") if l.strip()]
PW = [r for r in PW if r.get("s_fwd") is not None and r.get("s_swap") is not None]
print("\n== pairwise score of the target arm, split by forcing status of target / reference output")
print("   (rows: target forced?, reference forced?; value = mean score, n pairs)")
cells = collections.defaultdict(list)
for r in PW:
    ft = force.get((r["a"], r["task"], r["k"]))
    fr = force.get((r["b"], r["task"], r["k"]))
    if ft is None or fr is None:
        continue
    cells[(ft == "forced", fr == "forced")].append((r["s_fwd"] + r["s_swap"]) / 2)
for (tf, rf), xs in sorted(cells.items()):
    print(f"   target forced={str(tf):5s} reference forced={str(rf):5s}  mean {sum(xs)/len(xs):.3f}  n={len(xs)}")

print("\n== Fm vs B0 only")
cc = collections.defaultdict(list)
for r in PW:
    if (r["a"], r["b"]) == ("Fm", "B0"):
        ft = force.get(("Fm", r["task"], r["k"])); fr = force.get(("B0", r["task"], r["k"]))
        if ft and fr:
            cc[(ft == "forced", fr == "forced")].append((r["s_fwd"] + r["s_swap"]) / 2)
for (tf, rf), xs in sorted(cc.items()):
    print(f"   Fm forced={str(tf):5s} B0 forced={str(rf):5s}  mean {sum(xs)/len(xs):.3f}  n={len(xs)}")

# overall association: pair score vs (target forced - reference forced)
import math
xs, ys = [], []
for r in PW:
    ft = force.get((r["a"], r["task"], r["k"])); fr = force.get((r["b"], r["task"], r["k"]))
    if ft and fr:
        xs.append((ft == "forced") - (fr == "forced")); ys.append((r["s_fwd"] + r["s_swap"]) / 2)
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
print(f"\ncorrelation between pair score and (target forced - reference forced): r = {cov/den:.3f} over {len(xs)} pairs")
print(f"est spend ${llm.spent():.3f}")
