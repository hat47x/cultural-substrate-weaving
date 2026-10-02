"""Generate five questions per (task, arm, sample) and store results as JSONL.

Usage: python3 run_generation.py --stage pilot --arms B0 --n 3 [--model deepseek-v4-flash]
Raw outputs go to local/efficacy-cheap-llm/ (not committed).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import arms  # noqa: E402
import llm  # noqa: E402

TASKS = Path(os.environ.get("CSW_TASKS", str(Path(__file__).resolve().parents[1] / "tasks" / "tasks.json")))


def parse_questions(text: str):
    obj = llm.parse_json(text)
    if isinstance(obj, dict):
        qs = obj.get("questions")
    else:
        qs = obj
    if not isinstance(qs, list) or len(qs) < 3:
        return None
    out = []
    for q in qs[:5]:
        if isinstance(q, dict) and isinstance(q.get("q"), str):
            out.append({"q": q["q"], "basis": str(q.get("basis", ""))})
    return out if len(out) >= 3 else None


def one(job: dict) -> dict:
    task, arm, k = job["task"], job["arm"], job["k"]
    provider, model = job["provider"], job["model"]
    tag = f"{job['stage']}-{arm}-{task['id']}-{k}"
    meta = {"stage": job["stage"], "arm": arm, "task": task["id"], "k": k, "model": model}
    for attempt in range(3):
        try:
            if arm == "RT":
                sysmsg = {"role": "system", "content": arms.runtime_system()}
                base = arms.task_block(task) + arms.RT_CHOOSE
                r1 = llm.call(provider, model, [sysmsg, {"role": "user", "content": base}],
                              tag=tag + f"-c{attempt}", max_tokens=800, temperature=1.0)
                choice_obj = llm.parse_json(r1["text"]) or {}
                chosen = [c for c in choice_obj.get("choice", []) if c in arms.RT_FW_IDS][:2]
                if chosen:
                    dossiers = "\n\n".join(arms.dossier_card(c) for c in chosen)
                    follow = (
                        "【依頼2】選んだ体系の資料を渡します。仮に走らせたうえで、次の依頼に答えてください。"
                        "体系から出た問いには「この系として見るなら」と添えてください。"
                        "材料に支えのない構造を事実として断定しないでください。\n\n"
                        + dossiers + "\n\n" + arms.REQUEST
                    )
                else:
                    follow = "【依頼2】体系は使わないことにしたので、体系なしで次の依頼に答えてください。\n\n" + arms.REQUEST
                msgs = [sysmsg, {"role": "user", "content": base},
                        {"role": "assistant", "content": r1["text"]},
                        {"role": "user", "content": follow}]
                r = llm.call(provider, model, msgs, tag=tag + f"-g{attempt}", max_tokens=2000, temperature=1.0)
                meta["chosen"] = chosen
                meta["matched"] = task.get("framework") in chosen if task["kind"] == "latent" else None
            else:
                msgs = arms.build(arm, task)
                r = llm.call(provider, model, msgs, tag=tag + f"-g{attempt}", max_tokens=2000, temperature=1.0)
            qs = parse_questions(r["text"])
            if qs:
                meta.update(questions=qs, ok=True, usage=r.get("usage"))
                return meta
        except RuntimeError as e:
            meta["error"] = str(e)[:200]
            if "budget" in str(e):
                break
    meta.update(ok=False)
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--arms", required=True)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--provider", default="deepseek")
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--tasks", default="")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    if a.tasks:
        ids = set(a.tasks.split(","))
        tasks = [t for t in tasks if t["id"] in ids]
    jobs = [
        dict(task=t, arm=arm, k=k, stage=a.stage, provider=a.provider, model=a.model)
        for t in tasks for arm in a.arms.split(",") for k in range(a.n)
    ]
    out = Path(a.out) if a.out else llm.WORK / f"gen-{a.stage}-{a.model.replace('/', '_')}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(one, jobs))
    with out.open("a", encoding="utf-8") as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(1 for r in res if r.get("ok"))
    print(f"{ok}/{len(res)} ok -> {out}; est. spend ${llm.spent():.3f}")


if __name__ == "__main__":
    main()
