import collections
import json
import random
from pathlib import Path

W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
R = [json.loads(l) for l in open(W / "jev-pairwise.jsonl", encoding="utf-8") if l.strip()]
R = [r for r in R if r.get("s_fwd") is not None and r.get("s_swap") is not None]
PRIMARY = ["T1_vacancy-3", "T3_chain_cut-1", "T3_chain_cut-3", "T4_standpoint-1", "T5_four_whys-1", "T5_four_whys-2", "T6_two_cycles-2", "T8_part_whole-2"]
for r in R:
    r["score"] = (r["s_fwd"] + r["s_swap"]) / 2

cons = sum(1 for r in R if r["s_fwd"] == r["s_swap"]) / len(R)
# order consistency: both orders pick the same arm (tie in both counts as consistent; tie vs win does not)
print(f"pairs {len(R)}; order consistency (same score in both orders): {cons:.3f}")
first_bias = sum(1 for r in R if r["r_fwd"] == "first") / len(R), sum(1 for r in R if r["r_swap"] == "first") / len(R)
print(f"share choosing 'first' when target is first / second: {first_bias[0]:.3f} / {first_bias[1]:.3f}")
ties = sum(1 for r in R if r["r_fwd"] == "tie") / len(R), sum(1 for r in R if r["r_swap"] == "tie") / len(R)
print(f"tie share: {ties[0]:.3f} / {ties[1]:.3f}")


def per_task(a, b, tasks):
    d = {}
    for t in tasks:
        xs = [r["score"] for r in R if r["a"] == a and r["b"] == b and r["task"] == t]
        if xs:
            d[t] = sum(xs) / len(xs)
    return d


def boot(d, n=5000, seed=3):
    v = list(d.values())
    rnd = random.Random(seed)
    ms = sorted(sum(rnd.choice(v) for _ in v) / len(v) for _ in range(n))
    return sum(v) / len(v), ms[int(.025 * n)], ms[int(.975 * n)], sum(x > 0.5 for x in v), sum(x < 0.5 for x in v)


all_tasks = sorted({r["task"] for r in R})
print("\nscore = target's win rate against reference (0.5 = no difference); CI over tasks")
print(f"{'pair':8s} {'primary(8)':>34s}   {'all 14':>34s}")
for a, b in [("Fm", "B0"), ("Fm", "G"), ("Fm", "Fx"), ("Fm", "R"), ("Fm", "N"), ("RT", "B0"), ("R", "B0"), ("Fx", "B0")]:
    p = boot(per_task(a, b, PRIMARY)); q = boot(per_task(a, b, all_tasks))
    print(f"{a}-{b:3s}   {p[0]:.3f} [{p[1]:.3f},{p[2]:.3f}] +{p[3]}/-{p[4]}   {q[0]:.3f} [{q[1]:.3f},{q[2]:.3f}] +{q[3]}/-{q[4]}")

print("\nper-task Fm vs B0 / Fm vs Fx / Fm vs R (primary tasks)")
for t in PRIMARY:
    row = [per_task(a, b, [t]).get(t, float("nan")) for a, b in (("Fm", "B0"), ("Fm", "Fx"), ("Fm", "R"))]
    print(f"  {t:18s} " + " ".join(f"{x:.2f}" for x in row))
