"""Pairwise Jev comparison on existing stage-1 outputs (preregistered in 04).

Each pair (target arm vs reference arm, same task and sample index) is judged twice with
the order swapped. Score per pair = mean over the two orders of 1/0.5/0 for the target.
"""

import hashlib
import json
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge  # noqa: E402
import llm  # noqa: E402
from jev_judge import CACHE, MODEL, URL  # noqa: E402

TASKS = {t["id"]: t for t in json.loads((Path(__file__).resolve().parents[1] / "tasks" / "tasks.json").read_text(encoding="utf-8"))}
PRIMARY = ["T1_vacancy-3", "T3_chain_cut-1", "T3_chain_cut-3", "T4_standpoint-1", "T5_four_whys-1", "T5_four_whys-2", "T6_two_cycles-2", "T8_part_whole-2"]
PAIRS = [("Fm", "B0"), ("Fm", "Fx"), ("Fm", "R"), ("Fm", "G"), ("Fm", "N"), ("RT", "B0"), ("R", "B0"), ("Fx", "B0")]

INSTR = ("同じ状況について、二つの問いの組（先と後）がある。課題の『固有の要素』を、より直接調べているのはどちらかを判定する。"
         "要素を名指すか明確に前提とした問いを、直接とする。典型的な説明を疑うだけの問い、一般的な原因探しの問い、"
         "隣接する話題の問いは、直接とは数えない。どちらも同程度なら同等とする。")
CRIT = {
    "first": "先の組の方が、固有の要素をより直接調べている",
    "second": "後の組の方が、固有の要素をより直接調べている",
    "tie": "二つの組で、固有の要素を調べる直接さは同程度である",
}


def decide(task: dict, qa: list[dict], qb: list[dict]) -> str | None:
    state = (f"【状況】\n{task['material']}\n\n【鍵】\n{task['key']}\n\n【固有の要素】\n{task.get('signature', '')}\n\n"
             f"【典型的な説明】\n{task['trap']}\n\n【先の組の問い】\n{judge.fmt_questions(qa, with_basis=False)}\n\n"
             f"【後の組の問い】\n{judge.fmt_questions(qb, with_basis=False)}")
    body = {"model": MODEL, "state": state, "questions": {"q": {"type": "choice", "instructions": INSTR, "criteria": CRIT}}}
    key = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    p = CACHE / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text())["answers"]["q"]["choice"]
    data = json.dumps(body, ensure_ascii=False).encode()
    for a in range(5):
        req = urllib.request.Request(URL, data=data, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {llm._token('openrouter')}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode())
            p.write_text(json.dumps(out))
            return out["answers"]["q"]["choice"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 402, 403):
                raise RuntimeError(e.read().decode()[:200])
        except Exception:
            pass
        time.sleep(2 ** a)
    return None


def main() -> None:
    W = llm.WORK
    gen = {}
    for l in open(W / "gen-main-latent.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("ok"):
            gen[(r["arm"], r["task"], r["k"])] = r["questions"]
    jobs = []
    for a, b in PAIRS:
        for tid in sorted({k[1] for k in gen}):
            for k in range(6):
                if (a, tid, k) in gen and (b, tid, k) in gen:
                    jobs.append((a, b, tid, k))
    print(len(jobs), "pairs;", 2 * len(jobs), "judgments")

    def f(j):
        a, b, tid, k = j
        t = TASKS[tid]
        qa = [{"q": judge.scrub(q["q"]), "basis": ""} for q in gen[(a, tid, k)]]
        qb = [{"q": judge.scrub(q["q"]), "basis": ""} for q in gen[(b, tid, k)]]
        try:
            r1 = decide(t, qa, qb)   # target first
            r2 = decide(t, qb, qa)   # target second
        except RuntimeError as e:
            return {"a": a, "b": b, "task": tid, "k": k, "error": str(e)[:100]}
        s1 = {"first": 1.0, "tie": 0.5, "second": 0.0}.get(r1)
        s2 = {"first": 0.0, "tie": 0.5, "second": 1.0}.get(r2)
        return {"a": a, "b": b, "task": tid, "k": k, "r_fwd": r1, "r_swap": r2, "s_fwd": s1, "s_swap": s2}

    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(f, jobs))
    (W / "jev-pairwise.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in res) + "\n", encoding="utf-8")
    print("done", sum(1 for x in res if x.get("s_fwd") is not None and x.get("s_swap") is not None), "complete pairs")


if __name__ == "__main__":
    main()
