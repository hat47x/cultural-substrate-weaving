"""Analysis for the preregistered comparisons (task-level bootstrap + sign test)."""

import collections
import json
import math
import random
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
path = sys.argv[1] if len(sys.argv) > 1 else str(W / "judged-main.jsonl")
recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]

PRIMARY = ["T1_vacancy-3", "T3_chain_cut-1", "T3_chain_cut-3", "T4_standpoint-1",
           "T5_four_whys-1", "T5_four_whys-2", "T6_two_cycles-2", "T8_part_whole-2"]
ARMS = ["B0", "G", "R", "N", "Fx", "Fm", "RT"]
latent_all = sorted({r["task"] for r in recs if not r["task"].startswith("N-")})
ceiling = [t for t in latent_all if t not in PRIMARY]
nulls = sorted({r["task"] for r in recs if r["task"].startswith("N-")})


def rate(arm, tasks, key, pred):
    per = {}
    for t in tasks:
        xs = [r[key] for r in recs if r["arm"] == arm and r["task"] == t and r.get(key) is not None]
        if xs:
            per[t] = sum(1 for x in xs if pred(x)) / len(xs)
    return per


def mean(d):
    return sum(d.values()) / len(d) if d else float("nan")


def boot_diff(a, b, n=5000, seed=1):
    ts = [t for t in a if t in b]
    diffs = [a[t] - b[t] for t in ts]
    rnd = random.Random(seed)
    ms = sorted(sum(rnd.choice(diffs) for _ in diffs) / len(diffs) for _ in range(n))
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    m = pos + neg
    p = 1.0
    if m:
        k = min(pos, neg)
        p = min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)
    return sum(diffs) / len(diffs), ms[int(0.025 * n)], ms[int(0.975 * n)], pos, neg, p


def table(title, tasks, key, pred):
    print(f"\n== {title} (tasks={len(tasks)})")
    res = {}
    for arm in ARMS:
        per = rate(arm, tasks, key, pred)
        res[arm] = per
        print(f"  {arm:3s} mean={mean(per):.3f}  n_tasks={len(per)}")
    return res


hit2 = lambda x: x == 2
hit1 = lambda x: x >= 1
res = table("PRIMARY hit=2", PRIMARY, "hit", hit2)
print("\n-- primary comparisons (diff, 95% CI over tasks, +tasks, -tasks, sign p)")
for a, b in [("Fm", "B0"), ("Fm", "Fx"), ("Fm", "G"), ("Fm", "R")]:
    d = boot_diff(res[a], res[b])
    print(f"  {a} - {b}: {d[0]:+.3f} [{d[1]:+.3f},{d[2]:+.3f}] +{d[3]} -{d[4]} p={d[5]:.3f}")
print("\n-- exploratory (hit=2, primary tasks)")
for a, b in [("N", "B0"), ("Fx", "B0"), ("G", "B0"), ("R", "B0"), ("RT", "B0"), ("Fm", "N"), ("Fm", "RT"), ("RT", "G")]:
    d = boot_diff(res[a], res[b])
    print(f"  {a} - {b}: {d[0]:+.3f} [{d[1]:+.3f},{d[2]:+.3f}] +{d[3]} -{d[4]} p={d[5]:.3f}")

res1 = table("hit>=1 (primary)", PRIMARY, "hit", hit1)
table("ceiling latent tasks hit=2", ceiling, "hit", hit2)
ress = table("survivor hit=2 (primary)", PRIMARY, "hit_surv", hit2)
for a, b in [("Fm", "B0"), ("Fm", "Fx"), ("Fm", "G"), ("Fm", "R")]:
    d = boot_diff(ress[a], ress[b])
    print(f"  surv {a} - {b}: {d[0]:+.3f} [{d[1]:+.3f},{d[2]:+.3f}] +{d[3]} -{d[4]} p={d[5]:.3f}")

# Spurious assertion rate: share of outputs with at least one asserted unsupported structure.
for title, tasks in (("NULL tasks: spurious assertion rate", nulls), ("LATENT primary: spurious rate", PRIMARY)):
    sp = table(title, tasks, "spur", lambda x: x >= 1)
    sps = table(title + " (after return filter)", tasks, "spur_surv", lambda x: x >= 1)

# Mean grounded fraction
print("\n== grounded fraction (all tasks)")
for arm in ARMS:
    xs = [sum(r["grounded"]) / len(r["grounded"]) for r in recs if r["arm"] == arm and r.get("grounded")]
    print(f"  {arm:3s} {sum(xs)/len(xs):.3f}")

# RT routing
print("\n== RT routing")
rt = [r for r in recs if r["arm"] == "RT"]
lat = [r for r in rt if not r["task"].startswith("N-")]
print("  latent: chose matched framework:", sum(1 for r in lat if r.get("matched")), "/", len(lat))
print("  latent: chose any framework:", sum(1 for r in lat if r.get("chosen")), "/", len(lat))
print("  null:   chose any framework:", sum(1 for r in rt if r["task"].startswith("N-") and r.get("chosen")), "/", sum(1 for r in rt if r["task"].startswith("N-")))
print("  chosen distribution:", collections.Counter(c for r in rt for c in r.get("chosen", [])).most_common())
mt = [r for r in lat if r.get("matched") and r.get("hit") is not None]
nm = [r for r in lat if not r.get("matched") and r.get("hit") is not None]
f = lambda xs: sum(1 for r in xs if r["hit"] == 2) / len(xs) if xs else float("nan")
print(f"  RT hit=2 when matched {f(mt):.3f} (n={len(mt)}), when not matched {f(nm):.3f} (n={len(nm)})")

# Per-task primary table
print("\n== per-task hit=2 (primary)")
print("  task              " + " ".join(f"{a:>5s}" for a in ARMS))
for t in PRIMARY:
    print(f"  {t:18s}" + " ".join(f"{res[a].get(t, float('nan')):5.2f}" for a in ARMS))
