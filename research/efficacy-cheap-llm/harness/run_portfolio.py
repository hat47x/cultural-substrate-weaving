"""Stage 2: catalyst portfolios (PF/PR/PG/PB), k=4 single samples each, 2 replicates."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import arms, llm, run_generation as rg

tasks = {t["id"]: t for t in json.loads(rg.TASKS.read_text(encoding="utf-8"))}
ids = json.loads((rg.TASKS.parent / "tasks_v2_headroom_ids.json").read_text())
jobs = []
for tid in ids:
    t = tasks[tid]
    for sname, cats in arms.portfolio_for(t).items():
        for rep in range(2):
            for j, c in enumerate(cats):
                jobs.append(dict(task=t, arm=c, k=rep * 10 + j, stage="p2", provider="deepseek",
                                 model="deepseek-v4-flash", set=sname, rep=rep))

def f(job):
    r = rg.one(job)
    r["set"], r["rep"] = job["set"], job["rep"]
    return r

with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(f, jobs))
out = llm.WORK / "gen-p2.jsonl"
out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in res) + "\n", encoding="utf-8")
print(sum(1 for r in res if r.get("ok")), "/", len(res), "ok ->", out, f"est ${llm.spent():.3f}")
