import collections
import json
import random
from pathlib import Path

W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
PR = [json.loads(l) for l in open(W / "sel-pairwise.jsonl", encoding="utf-8") if l.strip()]
PR = [r for r in PR if r["s_fwd"] is not None and r["s_swap"] is not None]
for r in PR:
    r["score"] = (r["s_fwd"] + r["s_swap"]) / 2
tasks = sorted({r["task"] for r in PR})
print(f"{len(PR)} complete pairs over {len(tasks)} latent tasks; order consistency "
      f"{sum(1 for r in PR if r['s_fwd'] == r['s_swap']) / len(PR):.3f}")
rnd = random.Random(3)
print("\npairwise score of first arm over second (0.5 = no difference), CI over tasks")
for a, b in [("SEL_FIT", "SEL_RAND"), ("SEL_DIST", "SEL_RAND"), ("SEL_FIT", "SEL_DIST"), ("SEL_FIT", "B0"),
             ("SEL_FIT", "Fm"), ("SEL_FIT", "RT"), ("SEL_DIST", "B0"), ("SEL_RAND", "B0"), ("Fm", "SEL_RAND")]:
    d = {}
    for t in tasks:
        xs = [r["score"] for r in PR if r["a"] == a and r["b"] == b and r["task"] == t]
        if xs:
            d[t] = sum(xs) / len(xs)
    v = list(d.values())
    ms = sorted(sum(rnd.choice(v) for _ in v) / len(v) for _ in range(5000))
    print(f"  {a:8s} vs {b:8s} {sum(v)/len(v):.3f} [{ms[125]:.3f},{ms[4875]:.3f}] +{sum(x > .5 for x in v)}/-{sum(x < .5 for x in v)} (n tasks {len(v)})")

FO = [json.loads(l) for l in open(W / "sel-force.jsonl", encoding="utf-8") if l.strip()]
print("\nforcing on null tasks (Jev): forced / hedged / clean; declared poor|none fit")
for arm in ("SEL_FIT", "SEL_DIST", "SEL_RAND"):
    xs = [x for x in FO if x["arm"] == arm]
    f = lambda v: sum(1 for x in xs if x["force"] == v) / len(xs)
    dec = sum(1 for x in xs if x.get("fit") in ("poor", "none")) / len(xs)
    print(f"  {arm:8s} n={len(xs)} forced={f('forced'):.3f} hedged={f('hedged'):.3f} clean={f('clean'):.3f} declared={dec:.3f}")
print("  (stage 3 reference: B0 forced 0.167, Fm 0.583, Fx 0.521, R 0.562, N 0.187)")

G = [json.loads(l) for l in open(W / "gen-sel.jsonl", encoding="utf-8")]
print("\nframeworks used by SEL_RAND:", collections.Counter(r["fw"] for r in G if r["arm"] == "SEL_RAND").most_common(10))
print("frameworks used by SEL_FIT:", collections.Counter(r["fw"] for r in G if r["arm"] == "SEL_FIT").most_common(4))
print("frameworks used by SEL_DIST:", collections.Counter(r["fw"] for r in G if r["arm"] == "SEL_DIST").most_common(4))
