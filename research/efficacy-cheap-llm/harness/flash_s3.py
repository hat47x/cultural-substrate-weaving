"""Sensitivity: re-classify stage-3A outputs (forced / strict hit) with deepseek-v4-flash."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
import jev_stage3 as j3

SYS = "あなたは厳密で一貫した判定者です。出力はJSONのみです。"
def ask(instr, crit, state, tag):
    opts = "\n".join(f"- {k}: {v}" for k, v in crit.items())
    user = f"{instr}\n\n{state}\n\n選択肢:\n{opts}\n\nJSONのキーをこの順に出力: reason（二文以内）, label（選択肢の名前のみ）"
    r = llm.call("deepseek", "deepseek-v4-flash", [{"role": "system", "content": SYS}, {"role": "user", "content": user}],
                 tag=tag, max_tokens=700, temperature=0.0, json_mode=True)
    o = llm.parse_json(r["text"]) or {}
    return o.get("label") if o.get("label") in crit else None

recs = [json.loads(l) for l in open(llm.WORK / "jev-s3.jsonl", encoding="utf-8") if l.strip()]
recs = [r for r in recs if r["part"] == "A" and r["questions"]]
def f(r):
    t = j3.TASKS[r["task"]]; out = dict(r)
    st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{j3.qtext(r['questions'])}"
    tag = f"s3f-{r['arm']}-{r['task']}-{r['k']}"
    out["force_flash"] = ask(j3.I_FORCE, j3.C_FORCE, st, tag + "-f")
    if t["kind"] == "latent":
        st2 = (f"【状況】\n{t['material']}\n\n【鍵】\n{t['key']}\n\n【固有の要素】\n{t.get('signature','')}\n\n【典型的な説明】\n{t['trap']}\n\n【分析者の問い】\n{judge.fmt_questions(r['questions'], with_basis=False)}")
        out["hit_flash"] = ask(j3.I_HIT, j3.C_HIT, st2, tag + "-h")
    return out
with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(f, recs))
(llm.WORK / "flash-s3.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in res) + "\n", encoding="utf-8")
NULLS = [f"N-{i}" for i in range(1, 9)]
print("agreement forced (Jev vs flash), exact:", sum(1 for x in res if x.get("force") == x.get("force_flash")) / len(res))
print("forced-vs-not agreement:", sum(1 for x in res if (x.get("force") == "forced") == (x.get("force_flash") == "forced")) / len(res))
lat = [x for x in res if x["task"] not in NULLS]
print("hit agreement:", sum(1 for x in lat if (x["hit_jev"] == "direct") == (x["hit_flash"] == "direct")) / len(lat))
for arm in ["B0", "G", "R", "N", "Fx", "Fm"]:
    n = [x for x in res if x["arm"] == arm and x["task"] in NULLS]; l = [x for x in lat if x["arm"] == arm]
    fr = lambda xs, k: sum(1 for x in xs if x.get(k) == "forced") / len(xs)
    print(f"  {arm:3s} null forced Jev={fr(n,'force'):.3f} flash={fr(n,'force_flash'):.3f} | latent hit Jev={sum(1 for x in l if x['hit_jev']=='direct')/len(l):.3f} flash={sum(1 for x in l if x['hit_flash']=='direct')/len(l):.3f}")
print(f"est ${llm.spent():.3f}")
