import json, collections, random
from pathlib import Path
W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
R = [json.loads(l) for l in open(W / "jev-s3.jsonl", encoding="utf-8") if l.strip()]
NULLS = [f"N-{i}" for i in range(1, 9)]
P = ["T1_vacancy-3","T3_chain_cut-1","T3_chain_cut-3","T4_standpoint-1","T5_four_whys-1","T5_four_whys-2","T6_two_cycles-2","T8_part_whole-2"]
A = [r for r in R if r["part"] == "A"]; B = [r for r in R if r["part"] == "B"]
ARMS = ["B0", "G", "R", "N", "Fx", "Fm"]

def per_task(rows, tasks, pred):
    d = {}
    for t in tasks:
        xs = [r for r in rows if r["task"] == t]
        if xs: d[t] = sum(1 for r in xs if pred(r)) / len(xs)
    return d
def mean(d): return sum(d.values()) / len(d)
def boot(a, b, n=4000, seed=7):
    ts = [t for t in a if t in b]; ds = [a[t] - b[t] for t in ts]
    rnd = random.Random(seed); ms = sorted(sum(rnd.choice(ds) for _ in ds) / len(ds) for _ in range(n))
    return sum(ds) / len(ds), ms[int(.025 * n)], ms[int(.975 * n)]

print("== 3A null tasks (8): forced / hedged / clean rate; declared poor|none fit; mean #questions")
res = {}
for arm in ARMS:
    rows = [r for r in A if r["arm"] == arm and r["task"] in NULLS]
    forced = per_task(rows, NULLS, lambda r: r.get("force") == "forced")
    hedged = per_task(rows, NULLS, lambda r: r.get("force") == "hedged")
    decl = per_task(rows, NULLS, lambda r: r.get("fit") in ("poor", "none") and arm != "B0")
    nq = sum(len(r["questions"]) for r in rows) / len(rows)
    res[arm] = forced
    print(f"  {arm:3s} forced={mean(forced):.3f} hedged={mean(hedged):.3f} clean={1-mean(forced)-mean(hedged):.3f} declared_poor/none={mean(decl):.3f} nQ={nq:.2f}")
for a in ["R", "N", "Fx", "Fm"]:
    m, lo, hi = boot(res[a], res["B0"]); print(f"  forced {a}-B0: {m:+.3f} [{lo:+.3f},{hi:+.3f}]")
fw = {t: sum(res[a][t] for a in ["R","N","Fx","Fm"]) / 4 for t in NULLS}
m, lo, hi = boot(fw, res["B0"]); print(f"  forced (framework arms avg)-B0: {m:+.3f} [{lo:+.3f},{hi:+.3f}]")
dec_avg = sum(mean(per_task([r for r in A if r["arm"] == a and r["task"] in NULLS], NULLS, lambda r: r.get("fit") in ("poor","none"))) for a in ["R","N","Fx","Fm"]) / 4
print(f"  H8b declared poor/none, framework arms avg on null: {dec_avg:.3f}")

print("\n== 3A latent tasks (8): strict direct hit (Jev), forcing-as-forced, declared poor|none, #questions")
hres = {}
for arm in ARMS:
    rows = [r for r in A if r["arm"] == arm and r["task"] in P]
    hit = per_task(rows, P, lambda r: r.get("hit_jev") == "direct"); hres[arm] = hit
    frc = per_task(rows, P, lambda r: r.get("force") == "forced")
    dec = per_task(rows, P, lambda r: r.get("fit") in ("poor", "none") and arm != "B0")
    nq = sum(len(r["questions"]) for r in rows) / len(rows)
    print(f"  {arm:3s} hit_direct={mean(hit):.3f} forced={mean(frc):.3f} declared_poor/none={mean(dec):.3f} nQ={nq:.2f}")
for a, b in [("Fm","B0"),("Fm","Fx"),("Fm","R"),("Fm","G"),("Fm","N"),("N","B0"),("R","B0"),("Fx","B0"),("G","B0")]:
    m, lo, hi = boot(hres[a], hres[b]); print(f"  hit {a}-{b}: {m:+.3f} [{lo:+.3f},{hi:+.3f}]")

print("\n== 3B delegation compliance (Jev used/not_used, and self-report)")
for kind, tasks in (("null", NULLS), ("latent", P)):
    for arm in ["OFF", "AUTO", "ON"]:
        rows = [r for r in B if r["arm"] == arm and r["task"] in tasks]
        u = per_task(rows, tasks, lambda r: r.get("use_jev") == "used")
        s = per_task(rows, tasks, lambda r: r.get("used_self") is True)
        print(f"  {kind:6s} {arm:4s} used(Jev)={mean(u):.3f} used(self)={mean(s):.3f} n={len(rows)}")
ua = per_task([r for r in B if r["arm"]=="AUTO" and r["task"] in P], P, lambda r: r.get("use_jev")=="used")
un = per_task([r for r in B if r["arm"]=="AUTO" and r["task"] in NULLS], NULLS, lambda r: r.get("use_jev")=="used")
print(f"  H12 AUTO latent-null use gap: {mean(ua)-mean(un):+.3f}")
# frameworks chosen under ON/AUTO
c = collections.Counter(f for r in B if r["arm"] in ("ON","AUTO") for f in (r.get("framework") or []))
print("  chosen:", c.most_common(8))
