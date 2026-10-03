"""Exploratory (post hoc): is the local judge usable with a tuned threshold on P(A)?

The threshold is chosen by leave-one-task-out cross-validation so the agreement figure
is not fitted on the records it is scored on. Also checks record-level and arm-level
rank agreement of the continuous score with the 3-judge consensus.
"""

import collections
import json
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
tag = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5_4b"
val = [json.loads(l) for l in open(W / f"local-val-{tag}.jsonl", encoding="utf-8") if l.strip()]
val = [v for v in val if v["local"].get("label")]
h2 = lambda x: 1 if x == 2 else 0
rows = []
for v in val:
    j = [h2(v["flash"]), h2(v["pro"]), h2(v["jev"])]
    p = v["local"]["p"]
    rows.append({"arm": v["key"][0].split(":")[0], "task": v["key"][1], "pa": p.get("A", 0.0),
                 "ex": 2 * p.get("A", 0) + p.get("B", 0), "maj": 1 if sum(j) >= 2 else 0, "mean": sum(j) / 3})


def best_threshold(train, key):
    cands = sorted({r[key] for r in train})
    best, bt = -1, 0.5
    for t in cands:
        acc = sum((r[key] >= t) == bool(r["maj"]) for r in train) / len(train)
        if acc > best:
            best, bt = acc, t
    return bt


def loto(key):
    tasks = sorted({r["task"] for r in rows})
    ok = 0
    for t in tasks:
        train = [r for r in rows if r["task"] != t]
        th = best_threshold(train, key)
        ok += sum((r[key] >= th) == bool(r["maj"]) for r in rows if r["task"] == t)
    return ok / len(rows), best_threshold(rows, key)


for key in ("pa", "ex"):
    acc, th = loto(key)
    print(f"score={key}: leave-one-task-out agreement with majority {acc:.3f} (full-data threshold {th:.3f})")
print("reference: mean inter-judge agreement ~0.62; always-answer-direct baseline = base rate "
      f"{sum(r['maj'] for r in rows)/len(rows):.3f}")


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for k, i in enumerate(o):
        r[i] = k
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else float("nan")


print(f"record-level Spearman(P(A), consensus mean) = {spearman([r['pa'] for r in rows], [r['mean'] for r in rows]):.3f}")
by = collections.defaultdict(list)
for r in rows:
    by[r["arm"]].append(r)
arms = sorted(by)
pa = [sum(x["pa"] for x in by[a]) / len(by[a]) for a in arms]
cm = [sum(x["mean"] for x in by[a]) / len(by[a]) for a in arms]
print(f"arm-level Spearman(mean P(A), consensus mean) = {spearman(pa, cm):.3f}")
for a, x, y in zip(arms, pa, cm):
    print(f"  {a:3s} meanP(A)={x:.2f} consensus={y:.2f}")
