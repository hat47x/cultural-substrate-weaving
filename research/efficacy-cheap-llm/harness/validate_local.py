"""Acceptance test for the local judge against the existing multi-judge labels.

Usage: python3 validate_local.py MODEL N [--calib]
Runs sequentially, grouped by task, so ollama can reuse the shared prompt prefix.
"""

import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm  # noqa: E402
import local_judge as lj  # noqa: E402
from run_generation import parse_questions  # noqa: E402

W = llm.WORK
T = Path(__file__).resolve().parents[1] / "tasks"
TASKS = {}
for f in ("tasks.json", "tasks_v2.json"):
    for t in json.loads((T / f).read_text(encoding="utf-8")):
        TASKS[t["id"]] = t

L = lambda f: [json.loads(x) for x in open(W / f, encoding="utf-8") if x.strip()]
key = lambda r: (r["arm"], r["task"], r["k"])


def build_records():
    out = []
    for gen, fl, pr, jv in (
        ("gen-main-latent.jsonl", "judged-main.jsonl", "judgedpro-main.jsonl", "jev-main.jsonl"),
        ("gen-p2.jsonl", "judged-p2.jsonl", "judgedpro-p2.jsonl", "jev-p2.jsonl"),
    ):
        G = {key(r): r for r in L(gen) if r.get("ok")}
        F = {key(r): r.get("hit") for r in L(fl)}
        P = {key(r): r.get("hit") for r in L(pr)}
        J = {key(r): r.get("hit_jev") for r in L(jv)}
        for k, r in G.items():
            if None in (F.get(k), P.get(k), J.get(k)):
                continue
            out.append({"key": list(k), "set": gen, "questions": r["questions"], "flash": F[k], "pro": P[k], "jev": J[k]})
    return out


def calib_records():
    src = open(Path(__file__).parent / "calibrate_judge.py", encoding="utf-8").read()
    POS = re.search(r'POS = """(.*?)"""', src, re.S).group(1)
    NEG = re.search(r'NEG = """(.*?)"""', src, re.S).group(1)
    out = []
    for tid, t in TASKS.items():
        if t["kind"] != "latent":
            continue
        for kind, tpl in (("POS", POS), ("NEG", NEG)):
            r = llm.call("deepseek", "deepseek-v4-flash",
                         [{"role": "user", "content": tpl.format(material=t["material"], key=t["key"], trap=t["trap"])}],
                         tag=f"calib-{kind}-{tid}", max_tokens=1500, temperature=0.7, json_mode=True)
            qs = parse_questions(r["text"])
            if qs:
                out.append({"key": [kind, tid, 0], "kind": kind, "questions": qs})
    return out


def run(model, items, label, out_path):
    """Append one JSON line per finished item; skip items already present (resumable)."""
    items = sorted(items, key=lambda x: (x["key"][1], x["key"][0], x["key"][2]))
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(tuple(json.loads(line)["key"]))
    todo = [it for it in items if tuple(it["key"]) not in done]
    print(f"  {label}: {len(done)} already done, {len(todo)} to do", flush=True)
    last, t0 = None, time.time()
    with out_path.open("a", encoding="utf-8") as f:
        for i, it in enumerate(todo):
            task = TASKS[it["key"][1]]
            first = task["id"] != last
            if first:
                lj.prefill(model, task)
            r = lj.ask(model, task, it["questions"])
            r["first_in_task"] = first
            last = task["id"]
            f.write(json.dumps({**it, "local": r}, ensure_ascii=False) + "\n")
            f.flush()
            if (i + 1) % 10 == 0:
                print(f"  {label} {i+1}/{len(todo)} elapsed {time.time()-t0:.0f}s, last {r['secs']:.1f}s", flush=True)


if __name__ == "__main__":
    model = sys.argv[1]
    n = int(sys.argv[2])
    recs = build_records()
    rnd = random.Random(11)
    by_arm = {}
    for r in recs:
        by_arm.setdefault(r["key"][0].split(":")[0] if r["set"] == "gen-p2.jsonl" else r["key"][0], []).append(r)
    sample = []
    per = max(1, n // len(by_arm))
    for arm, rs in sorted(by_arm.items()):
        sample += rnd.sample(rs, min(per, len(rs)))
    tag = model.replace(":", "_").replace("/", "_")
    run(model, sample, "val", W / f"local-val-{tag}.jsonl")
    if "--calib" in sys.argv:
        run(model, calib_records(), "calib", W / f"local-calib-{tag}.jsonl")
    print("done")
