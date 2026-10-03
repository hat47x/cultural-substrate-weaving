"""Selection study (preregistered in 05): generate with FIT / DIST / RAND-selected cards,
then pairwise-judge latent outputs and classify forcing on null outputs (Jev)."""

import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import arms
import jev_pairwise as jp
import jev_router as jr
import jev_stage3 as j3
import judge
import llm
import run_stage3 as s3
from run_generation import parse_questions

W = llm.WORK
picks = json.loads((W / "router-picks.json").read_text(encoding="utf-8"))
CAL = set(json.load(open(jr.T / "calibrated_ids.json")))
LAT = sorted(i for i in jr.TASKS if i in CAL)
NUL = sorted(i for i in jr.TASKS if jr.TASKS[i]["kind"] == "null")


def fw_for(cond, tid, k):
    if cond == "SEL_RAND":
        return random.Random(f"{tid}-{k}-rand").choice(list(jr.FW))
    return picks["FIT" if cond == "SEL_FIT" else "DIST"][tid]["pick"]


def gen(job):
    cond, tid, k = job
    t = jr.TASKS[tid]
    fw = fw_for(cond, tid, k)
    req = arms.REQUEST if t["kind"] == "latent" else s3.REQUEST_A
    user = arms.task_block(t) + arms.PREAMBLE_FW + arms.dossier_card(fw) + "\n\n" + req
    for a in range(3):
        r = llm.call("deepseek", "deepseek-v4-flash", [{"role": "user", "content": user}],
                     tag=f"sel-{cond}-{tid}-{k}-{a}", max_tokens=2000, temperature=1.0)
        if t["kind"] == "latent":
            qs = parse_questions(r["text"])
            if qs:
                return {"arm": cond, "task": tid, "k": k, "fw": fw, "questions": qs, "ok": True}
        else:
            o = s3.parse(r["text"])
            if o is not None:
                return {"arm": cond, "task": tid, "k": k, "fw": fw, "questions": o["questions"], "fit": o.get("fit"), "ok": True}
    return {"arm": cond, "task": tid, "k": k, "fw": fw, "ok": False}


def main():
    jobs = [(c, t, k) for c in ("SEL_FIT", "SEL_DIST", "SEL_RAND") for t in LAT + NUL for k in range(4)]
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(gen, jobs))
    (W / "gen-sel.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in res) + "\n", encoding="utf-8")
    print("generated", sum(1 for r in res if r["ok"]), "/", len(res), f"est ${llm.spent():.3f}")

    # forcing on null outputs (Jev, same instrument as stage 3)
    def force(r):
        t = jr.TASKS[r["task"]]
        st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{j3.qtext(r['questions'])}"
        return {**{k: r[k] for k in ("arm", "task", "k", "fw", "fit")}, "force": j3.decide(st, j3.I_FORCE, j3.C_FORCE)}

    nulls = [r for r in res if r["ok"] and r["task"] in NUL and r["questions"]]
    with ThreadPoolExecutor(max_workers=16) as ex:
        fo = list(ex.map(force, nulls))
    (W / "sel-force.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in fo) + "\n", encoding="utf-8")

    # pairwise on latent outputs
    G = {}
    for l in open(W / "gen-main-latent.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("ok"):
            G[(r["arm"], r["task"], r["k"])] = r["questions"]
    for r in res:
        if r["ok"] and r["task"] in LAT:
            G[(r["arm"], r["task"], r["k"])] = r["questions"]
    PAIRS = [("SEL_FIT", "SEL_RAND"), ("SEL_DIST", "SEL_RAND"), ("SEL_FIT", "SEL_DIST"), ("SEL_FIT", "B0"),
             ("SEL_FIT", "Fm"), ("SEL_FIT", "RT"), ("SEL_DIST", "B0"), ("SEL_RAND", "B0"), ("Fm", "SEL_RAND")]
    pj = [(a, b, t, k) for a, b in PAIRS for t in LAT for k in range(4) if (a, t, k) in G and (b, t, k) in G]

    def pw(j):
        a, b, t, k = j
        tk = jr.TASKS[t]
        qa = [{"q": judge.scrub(q["q"]), "basis": ""} for q in G[(a, t, k)]]
        qb = [{"q": judge.scrub(q["q"]), "basis": ""} for q in G[(b, t, k)]]
        r1, r2 = jp.decide(tk, qa, qb), jp.decide(tk, qb, qa)
        s1 = {"first": 1.0, "tie": 0.5, "second": 0.0}.get(r1)
        s2 = {"first": 0.0, "tie": 0.5, "second": 1.0}.get(r2)
        return {"a": a, "b": b, "task": t, "k": k, "r_fwd": r1, "r_swap": r2, "s_fwd": s1, "s_swap": s2}

    with ThreadPoolExecutor(max_workers=16) as ex:
        pr = list(ex.map(pw, pj))
    (W / "sel-pairwise.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in pr) + "\n", encoding="utf-8")
    print("pairwise", sum(1 for x in pr if x["s_fwd"] is not None and x["s_swap"] is not None), "/", len(pr))


if __name__ == "__main__":
    main()
