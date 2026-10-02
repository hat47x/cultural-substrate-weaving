"""Post-hoc sensitivity: consensus (mean of three judges' hit==2 indicators)."""
import json, random
from pathlib import Path
W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
L = lambda f: [json.loads(l) for l in open(W / f, encoding="utf-8") if l.strip()]
key = lambda r: (r["arm"], r["task"], r["k"])
P = ["T1_vacancy-3","T3_chain_cut-1","T3_chain_cut-3","T4_standpoint-1","T5_four_whys-1","T5_four_whys-2","T6_two_cycles-2","T8_part_whole-2"]

def table(flash, pro, jev):
    F = {key(r): r.get("hit") for r in L(flash)}; Pr = {key(r): r.get("hit") for r in L(pro)}
    J = {key(r): r.get("hit_jev") for r in L(jev)}
    out = {}
    for k in J:
        v = [F.get(k), Pr.get(k), J.get(k)]
        if None not in v:
            out[k] = sum(1 for x in v if x == 2) / 3
    return out

def boot(per_a, per_b, tasks, seed=5, n=5000):
    ts = [t for t in tasks if t in per_a and t in per_b]
    ds = [per_a[t] - per_b[t] for t in ts]
    rnd = random.Random(seed)
    ms = sorted(sum(rnd.choice(ds) for _ in ds) / len(ds) for _ in range(n))
    return sum(ds) / len(ds), ms[int(.025 * n)], ms[int(.975 * n)], sum(d > 0 for d in ds), sum(d < 0 for d in ds)

c = table("judged-main.jsonl", "judgedpro-main.jsonl", "jev-main.jsonl")
per = {}
for arm in ["B0","G","R","N","Fx","Fm","RT"]:
    per[arm] = {}
    for t in P:
        xs = [v for k, v in c.items() if k[0] == arm and k[1] == t]
        if xs: per[arm][t] = sum(xs) / len(xs)
print("CONSENSUS main (primary 8 tasks): " + "  ".join(f"{a}={sum(per[a].values())/len(per[a]):.3f}" for a in per))
for a, b in (("Fm","B0"),("Fm","Fx"),("Fm","G"),("Fm","R"),("Fm","N"),("N","B0"),("RT","B0"),("Fx","B0"),("R","B0"),("G","B0")):
    m, lo, hi, p, n = boot(per[a], per[b], P)
    print(f"  {a}-{b}: {m:+.3f} [{lo:+.3f},{hi:+.3f}] +{p} -{n}")

c2 = table("judged-p2.jsonl", "judgedpro-p2.jsonl", "jev-p2.jsonl")
S = {key(r): (r["set"], r["rep"]) for r in L("gen-p2.jsonl")}
tasks = sorted({k[1] for k in c2})
sing = {s: {} for s in ["PB","PG","PR","PF"]}
for s in sing:
    for t in tasks:
        xs = [v for k, v in c2.items() if S[k][0] == s and k[1] == t]
        sing[s][t] = sum(xs) / len(xs)
print("\nCONSENSUS p2 single-sample: " + "  ".join(f"{s}={sum(sing[s].values())/len(tasks):.3f}" for s in sing))
for a, b in (("PF","PB"),("PF","PG"),("PF","PR"),("PR","PB"),("PG","PB")):
    m, lo, hi, p, n = boot(sing[a], sing[b], tasks)
    print(f"  {a}-{b}: {m:+.3f} [{lo:+.3f},{hi:+.3f}] +{p} -{n}")
