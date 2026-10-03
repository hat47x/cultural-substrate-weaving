"""Acceptance analysis of the local judge (criteria fixed in 21-local-decision-model-options.md):
1. calibration set: POS -> direct (A), NEG -> none (C)
2. agreement with the 3-judge majority is not below inter-judge agreement
3. arm ordering and contrast directions do not contradict the consensus
"""

import collections
import json
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
tag = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5_4b"
val = [json.loads(l) for l in open(W / f"local-val-{tag}.jsonl", encoding="utf-8") if l.strip()]
val = [v for v in val if v["local"].get("label")]
print(f"validation records with a label: {len(val)}")

secs = [v["local"]["secs"] for v in val]
print(f"seconds per decision: mean {sum(secs)/len(secs):.1f}, max {max(secs):.1f}")

h2 = lambda x: 1 if x == 2 else 0
rows = []
for v in val:
    j = [h2(v["flash"]), h2(v["pro"]), h2(v["jev"])]
    rows.append({"arm": v["key"][0].split(":")[0], "task": v["key"][1], "loc": h2(v["local"]["score"]),
                 "pa": v["local"]["p"].get("A", 0.0), "j": j, "maj": 1 if sum(j) >= 2 else 0, "mean": sum(j) / 3})

agree = lambda f: sum(f(r) for r in rows) / len(rows)
pairs = {"flash-pro": (0, 1), "flash-jev": (0, 2), "pro-jev": (1, 2)}
print("\n== agreement on hit==2")
inter = {}
for name, (a, b) in pairs.items():
    inter[name] = agree(lambda r: r["j"][a] == r["j"][b])
    print(f"  {name:10s} {inter[name]:.3f}")
mean_inter = sum(inter.values()) / 3
print(f"  mean inter-judge {mean_inter:.3f}")
for i, name in enumerate(("flash", "pro", "jev")):
    print(f"  local-{name:5s} {agree(lambda r: r['loc'] == r['j'][i]):.3f}")
loc_maj = agree(lambda r: r["loc"] == r["maj"])
print(f"  local-majority {loc_maj:.3f}   (criterion 2: >= {mean_inter:.3f}) -> {'PASS' if loc_maj >= mean_inter else 'FAIL'}")
print(f"  base rate of majority hit==2: {sum(r['maj'] for r in rows)/len(rows):.3f}")


def auc(pos, neg):
    if not pos or not neg:
        return float("nan")
    s = 0.0
    for p in pos:
        for n in neg:
            s += 1.0 if p > n else 0.5 if p == n else 0.0
    return s / (len(pos) * len(neg))


print(f"  AUC of P(A) vs majority: {auc([r['pa'] for r in rows if r['maj']], [r['pa'] for r in rows if not r['maj']]):.3f}")

print("\n== per-arm hit==2 rate: local vs 3-judge mean (subset)")
by = collections.defaultdict(list)
for r in rows:
    by[r["arm"]].append(r)
tab = []
for arm, rs in sorted(by.items()):
    l = sum(x["loc"] for x in rs) / len(rs)
    c = sum(x["mean"] for x in rs) / len(rs)
    tab.append((arm, len(rs), l, c))
    print(f"  {arm:5s} n={len(rs):3d} local={l:.2f} consensus={c:.2f}")


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for k, i in enumerate(o):
        r[i] = k
    return r


a, b = rank([t[2] for t in tab]), rank([t[3] for t in tab])
n = len(tab)
rho = 1 - 6 * sum((x - y) ** 2 for x, y in zip(a, b)) / (n * (n * n - 1))
print(f"  Spearman rho of arm order (local vs consensus) = {rho:.2f}")

try:
    cal = [json.loads(l) for l in open(W / f"local-calib-{tag}.jsonl", encoding="utf-8") if l.strip()]
    cal = [c for c in cal if c["local"].get("label")]
    pos = [c for c in cal if c["kind"] == "POS"]
    neg = [c for c in cal if c["kind"] == "NEG"]
    pa = sum(1 for c in pos if c["local"]["label"] == "A") / len(pos)
    nc = sum(1 for c in neg if c["local"]["label"] == "C") / len(neg)
    print(f"\n== calibration set: POS judged A {pa:.3f} (n={len(pos)}), NEG judged C {nc:.3f} (n={len(neg)})")
    print(f"  AUC P(A): POS vs NEG {auc([c['local']['p'].get('A', 0) for c in pos], [c['local']['p'].get('A', 0) for c in neg]):.3f}")
    print(f"  criterion 1 (both clearly separated): {'PASS' if pa >= 0.8 and nc >= 0.6 else 'FAIL'} (thresholds POS>=0.8, NEG>=0.6, set before the run)")
except FileNotFoundError:
    print("\n(no calibration file yet)")
