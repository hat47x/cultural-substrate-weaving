"""Return step on existing stage-3A outputs: per-question grounding (Jev), then
re-judge forcing and strict hit on the surviving questions only."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
import jev_stage3 as j3

I_GR = "分析者の一つの問いについて、材料の中に、その問いの答えを確かめる手がかり（事実、数値、記述）が含まれているかを判定する。問い自体が仮説的であることは問わない。"
C_GR = {"supported": "材料に、この問いを確かめる手がかりが含まれている（材料を調べれば、肯定にも否定にも傾く証拠が見つかる）",
        "forced": "材料には、この問いを確かめる手がかりがない（外部の観察や調査が別に必要である）"}
recs = [json.loads(l) for l in open(llm.WORK / "jev-s3.jsonl", encoding="utf-8") if l.strip()]
recs = [r for r in recs if r["part"] == "A" and r["questions"]]
def f(r):
    t = j3.TASKS[r["task"]]; out = dict(r); keep = []
    for i, q in enumerate(r["questions"]):
        st = f"【状況】\n{t['material']}\n\n【問い】\n{j3.scrub(q['q']) if hasattr(j3,'scrub') else judge.scrub(q['q'])}\n根拠: {judge.scrub(q.get('basis',''))}"
        c = j3.decide(st, I_GR, C_GR)
        if c == "supported": keep.append(i)
    out["survivors"] = keep
    qs = [r["questions"][i] for i in keep]
    if not qs:
        out["force_after"] = "clean"; out["hit_after"] = "not_direct" if t["kind"] == "latent" else None; return out
    st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{j3.qtext(qs)}"
    out["force_after"] = j3.decide(st, j3.I_FORCE, j3.C_FORCE)
    if t["kind"] == "latent":
        st2 = (f"【状況】\n{t['material']}\n\n【鍵】\n{t['key']}\n\n【固有の要素】\n{t.get('signature','')}\n\n【典型的な説明】\n{t['trap']}\n\n【分析者の問い】\n{judge.fmt_questions(qs, with_basis=False)}")
        out["hit_after"] = j3.decide(st2, j3.I_HIT, j3.C_HIT)
    return out
with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(f, recs))
(llm.WORK / "jev-return2.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in res) + "\n", encoding="utf-8")
NULLS = [f"N-{i}" for i in range(1, 9)]
print("arm  | null: forced before->after, kept q/5 | latent: hit before->after, forced before->after")
for arm in ["B0", "G", "R", "N", "Fx", "Fm"]:
    n = [x for x in res if x["arm"] == arm and x["task"] in NULLS]; l = [x for x in res if x["arm"] == arm and x["task"] not in NULLS]
    m = lambda xs, k, v: sum(1 for x in xs if x.get(k) == v) / len(xs)
    kept_n = sum(len(x["survivors"]) for x in n) / len(n)
    print(f"  {arm:3s} | {m(n,'force','forced'):.3f}->{m(n,'force_after','forced'):.3f}, kept {kept_n:.2f} | hit {m(l,'hit_jev','direct'):.3f}->{m(l,'hit_after','direct'):.3f}, forced {m(l,'force','forced'):.3f}->{m(l,'force_after','forced'):.3f}")
