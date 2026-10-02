import collections, json, math, random, sys
from pathlib import Path
W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
R = [json.loads(l) for l in open(W / "judged-p2.jsonl", encoding="utf-8") if l.strip()]
tasks = sorted({r["task"] for r in R})
SETS = ["PB", "PG", "PR", "PF"]
cov = {s: {} for s in SETS}      # coverage: any hit==2 among the 4 singles, mean over 2 reps
mean_hit = {s: {} for s in SETS} # single-sample hit rate (mean over all 8)
for s in SETS:
    for t in tasks:
        reps = []
        singles = []
        for rep in (0, 1):
            xs = [r["hit"] for r in R if r["set"] == s and r["task"] == t and r["rep"] == rep and r.get("hit") is not None]
            if xs:
                reps.append(int(any(h == 2 for h in xs)))
            singles += [int(h == 2) for h in xs]
        cov[s][t] = sum(reps) / len(reps)
        mean_hit[s][t] = sum(singles) / len(singles)

def boot(a, b, n=5000, seed=3):
    ds = [a[t] - b[t] for t in tasks]
    rnd = random.Random(seed)
    ms = sorted(sum(rnd.choice(ds) for _ in ds) / len(ds) for _ in range(n))
    pos = sum(d > 0 for d in ds); neg = sum(d < 0 for d in ds); m = pos + neg
    p = 1.0 if not m else min(1.0, 2 * sum(math.comb(m, i) for i in range(min(pos, neg) + 1)) / 2 ** m)
    return sum(ds) / len(ds), ms[int(.025 * n)], ms[int(.975 * n)], pos, neg, p

print(f"tasks={len(tasks)}")
for name, d in (("COVERAGE (any hit=2 among 4)", cov), ("SINGLE-SAMPLE hit=2 rate", mean_hit)):
    print("\n==", name)
    for s in SETS:
        print(f"  {s} {sum(d[s].values())/len(tasks):.3f}")
    for a, b in (("PF", "PB"), ("PF", "PG"), ("PF", "PR"), ("PR", "PB"), ("PG", "PB")):
        m, lo, hi, p_, n_, p = boot(d[a], d[b])
        print(f"  {a}-{b}: {m:+.3f} [{lo:+.3f},{hi:+.3f}] +{p_} -{n_} p={p:.3f}")
print("\nper-task coverage")
print("  task                      " + " ".join(f"{s:>4s}" for s in SETS))
for t in tasks:
    print(f"  {t:26s}" + " ".join(f"{cov[s][t]:4.1f}" for s in SETS))
# by type
bytype = collections.defaultdict(lambda: collections.defaultdict(list))
for t in tasks:
    for s in SETS:
        bytype[t.split("-")[0]][s].append(cov[s][t])
print("\nby type (mean coverage)")
for ty, d in bytype.items():
    print(f"  {ty:16s} n={len(d['PB'])} " + " ".join(f"{s}={sum(d[s])/len(d[s]):.2f}" for s in SETS))
