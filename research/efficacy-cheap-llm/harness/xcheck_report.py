import json, collections
from pathlib import Path
W = Path(__file__).resolve().parents[3] / "local" / "efficacy-cheap-llm"
X = [json.loads(l) for l in open(W / "crosscheck.jsonl") if l.strip()]
P = ["T1_vacancy-3","T3_chain_cut-1","T3_chain_cut-3","T4_standpoint-1","T5_four_whys-1","T5_four_whys-2","T6_two_cycles-2","T8_part_whole-2"]
for scope, ts in (("primary", P), ("all latent", None)):
    print("==", scope)
    for arm in ["B0", "G", "R", "N", "Fx", "Fm", "RT"]:
        xs = [x for x in X if x["arm"] == arm and (ts is None or x["task"] in ts)]
        if not xs:
            continue
        a = sum(1 for x in xs if x["hit"] == 2) / len(xs)
        b = sum(1 for x in xs if x["hit_x"] == 2) / len(xs)
        print(f"  {arm:3s} n={len(xs):3d} flash={a:.2f} pro={b:.2f}")
print(sorted(collections.Counter((x["hit"], x["hit_x"]) for x in X).items()))
