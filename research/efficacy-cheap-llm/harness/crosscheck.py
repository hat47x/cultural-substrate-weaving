"""Cross-family hit re-judging on every 3rd latent record (free OpenRouter model)."""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm

W = llm.WORK
tasks = {t["id"]: t for t in json.loads(judge.TASKS.read_text(encoding="utf-8"))}
recs = [json.loads(l) for l in open(W / "judged-main.jsonl", encoding="utf-8")]
lat = [r for r in recs if r["task"] in tasks and tasks[r["task"]]["kind"] == "latent" and r.get("hit") is not None][::3]
MODEL = sys.argv[1] if len(sys.argv) > 1 else "deepseek-v4-pro"
PROV = sys.argv[2] if len(sys.argv) > 2 else "deepseek"

def f(r):
    t = tasks[r["task"]]
    tag = f"x-{r['arm']}-{r['task']}-{r['k']}-{r['model']}"
    try:
        h = judge.judge_hit(t, r["questions"], PROV, MODEL, tag)
    except RuntimeError as e:
        h = None
    return {**{k: r[k] for k in ("arm", "task", "k", "hit")}, "hit_x": h}

with ThreadPoolExecutor(max_workers=12) as ex:
    out = list(ex.map(f, lat))
(W / "crosscheck.jsonl").write_text("\n".join(json.dumps(o) for o in out), encoding="utf-8")
ok = [o for o in out if o["hit_x"] is not None]
agree = sum(1 for o in ok if o["hit_x"] == o["hit"]) / len(ok)
agree2 = sum(1 for o in ok if (o["hit_x"] == 2) == (o["hit"] == 2)) / len(ok)
print(f"judged {len(ok)}/{len(out)}; exact agreement {agree:.3f}; agreement on hit==2 {agree2:.3f}")
