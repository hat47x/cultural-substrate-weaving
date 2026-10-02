"""Jev 1.13 (TypeSafe decisions model) as a third, cross-family hit judge.

Endpoint: POST https://openrouter.ai/api/alpha/decisions with
{model, state, questions:{q:{type:'choice', instructions, criteria:{label: description}}}}.
Returns a typed choice with probabilities. Cost ~ $0.00001 per call.
"""
import hashlib, json, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm

URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = "typesafe/jev-1.13"
CACHE = llm.WORK / "jevcache"; CACHE.mkdir(parents=True, exist_ok=True)

INSTR = ("分析者の問いのうち、『鍵に到達する問いが調べるべき固有の要素』を直接調べているものがあるかを判定する。"
         "典型的な説明を疑うだけの問い、一般的な原因探しの問いは直接調べているとは数えない。")
CRIT = {
    "direct": "問いのいずれかが、固有の要素を直接調べる内容になっている（名指すか、明確に前提としている）",
    "partial": "固有の要素の一部に触れるか隣接する方向だが、要素そのものは調べていない",
    "none": "該当する問いがない。典型的な説明の範囲の問いだけである",
}
MAP = {"direct": 2, "partial": 1, "none": 0}

def decide(task, qs, tag):
    state = (f"【状況】\n{task['material']}\n\n【鍵】\n{task['key']}\n\n"
             f"【鍵に到達する問いが調べるべき固有の要素】\n{task.get('signature','')}\n\n"
             f"【典型的だが鍵に届かない説明】\n{task['trap']}\n\n【分析者の問い】\n{judge.fmt_questions(qs, with_basis=False)}")
    body = {"model": MODEL, "state": state,
            "questions": {"hit": {"type": "choice", "instructions": INSTR, "criteria": CRIT}}}
    key = hashlib.sha256((json.dumps(body, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
    p = CACHE / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text())
    data = json.dumps(body, ensure_ascii=False).encode()
    for a in range(5):
        req = urllib.request.Request(URL, data=data, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {llm._token('openrouter')}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode())
            p.write_text(json.dumps(out)); return out
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:200]
            if e.code in (400, 401, 402, 403): raise RuntimeError(msg)
        except Exception:
            pass
        time.sleep(2 ** a)
    raise RuntimeError("jev failed")

def run(inp, out, tasks_path):
    tasks = {t["id"]: t for t in json.loads(Path(tasks_path).read_text(encoding="utf-8"))}
    recs = [json.loads(l) for l in open(inp, encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r.get("ok") and tasks[r["task"]]["kind"] == "latent"]
    def f(r):
        try:
            o = decide(tasks[r["task"]], r["questions"], "")
            ch = o["answers"]["hit"]["choice"]
            return {**{k: r.get(k) for k in ("arm", "task", "k", "set", "rep", "chosen", "matched")}, "hit_jev": MAP[ch]}
        except Exception as e:
            return {**{k: r.get(k) for k in ("arm", "task", "k", "set", "rep")}, "hit_jev": None, "err": str(e)[:100]}
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(f, recs))
    Path(out).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in res) + "\n", encoding="utf-8")
    ok = sum(1 for x in res if x["hit_jev"] is not None)
    print(f"jev judged {ok}/{len(res)} -> {out}")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
