import json, collections, random, math
from pathlib import Path
W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
L = lambda f: [json.loads(l) for l in open(W / f, encoding="utf-8") if l.strip()]
key = lambda r: (r["arm"], r["task"], r["k"])
P = ["T1_vacancy-3","T3_chain_cut-1","T3_chain_cut-3","T4_standpoint-1","T5_four_whys-1","T5_four_whys-2","T6_two_cycles-2","T8_part_whole-2"]

def merged(flash, pro, jev):
    F = {key(r): r.get("hit") for r in L(flash)}
    Pr = {key(r): r.get("hit") for r in L(pro)}
    J = {key(r): r.get("hit_jev") for r in L(jev)}
    return [(k, F.get(k), Pr.get(k), J.get(k)) for k in J if F.get(k) is not None and Pr.get(k) is not None and J.get(k) is not None]

def agree(rows, i, j):
    return sum(1 for r in rows if (r[i] == 2) == (r[j] == 2)) / len(rows)

main = merged("judged-main.jsonl", "judgedpro-main.jsonl", "jev-main.jsonl")
print(f"main rows {len(main)}; agreement on hit==2: flash-pro {agree(main,1,2):.3f}, flash-jev {agree(main,1,3):.3f}, pro-jev {agree(main,2,3):.3f}")
for name, idx in (("flash", 1), ("pro", 2), ("jev", 3)):
    print(f"\n== MAIN primary 8 tasks, judge={name}: per-arm hit2, then task-bootstrap diffs vs B0")
    per = {}
    for arm in ["B0","G","R","N","Fx","Fm","RT"]:
        per[arm] = {}
        for t in P:
            xs = [r[idx] for r in main if r[0][0] == arm and r[0][1] == t]
            if xs: per[arm][t] = sum(1 for x in xs if x == 2) / len(xs)
    print("  " + "  ".join(f"{a}={sum(per[a].values())/len(per[a]):.2f}" for a in per))
    rnd = random.Random(1)
    for a, b in (("Fm","B0"),("Fm","Fx"),("Fm","G"),("Fm","R"),("RT","B0"),("Fx","B0"),("R","B0")):
        ts = [t for t in P if t in per[a] and t in per[b]]
        ds = [per[a][t]-per[b][t] for t in ts]
        ms = sorted(sum(rnd.choice(ds) for _ in ds)/len(ds) for _ in range(4000))
        print(f"  {a}-{b}: {sum(ds)/len(ds):+.3f} [{ms[100]:+.3f},{ms[3900]:+.3f}]")

p2 = merged("judged-p2.jsonl", "judgedpro-p2.jsonl", "jev-p2.jsonl")
# p2 records need set/rep: reload
S = {key(r): (r["set"], r["rep"]) for r in L("gen-p2.jsonl")}
print(f"\np2 rows {len(p2)}; agreement hit==2: flash-pro {agree(p2,1,2):.3f}, flash-jev {agree(p2,1,3):.3f}, pro-jev {agree(p2,2,3):.3f}")
tasks = sorted({r[0][1] for r in p2})
for name, idx in (("flash", 1), ("pro", 2), ("jev", 3)):
    print(f"\n== P2 judge={name}: coverage / single-sample rate")
    cov = {}; sing = {}
    for s in ["PB","PG","PR","PF"]:
        cov[s] = {}; sing[s] = {}
        for t in tasks:
            reps = []; single = []
            for rep in (0, 1):
                xs = [r[idx] for r in p2 if S[r[0]] == (s, rep) and r[0][1] == t]
                if xs:
                    reps.append(int(any(x == 2 for x in xs))); single += [int(x == 2) for x in xs]
            cov[s][t] = sum(reps)/len(reps); sing[s][t] = sum(single)/len(single)
    print("  coverage: " + "  ".join(f"{s}={sum(cov[s].values())/len(tasks):.3f}" for s in cov))
    print("  single:   " + "  ".join(f"{s}={sum(sing[s].values())/len(tasks):.3f}" for s in sing))
    rnd = random.Random(2)
    for a, b in (("PF","PB"),("PF","PG"),("PF","PR")):
        for lab, d in (("cov", cov), ("single", sing)):
            ds = [d[a][t]-d[b][t] for t in tasks]
            ms = sorted(sum(rnd.choice(ds) for _ in ds)/len(ds) for _ in range(4000))
            print(f"  {lab} {a}-{b}: {sum(ds)/len(ds):+.3f} [{ms[100]:+.3f},{ms[3900]:+.3f}]")
