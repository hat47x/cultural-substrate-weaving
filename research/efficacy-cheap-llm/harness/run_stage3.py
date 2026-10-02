"""Stage 3: 3A calibrated use/restraint (declinable output) and 3B delegation compliance."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import arms, llm

TASKS = Path(__file__).resolve().parents[1] / "tasks" / "tasks.json"
tasks = {t["id"]: t for t in json.loads(TASKS.read_text(encoding="utf-8"))}
PRIMARY = ["T1_vacancy-3","T3_chain_cut-1","T3_chain_cut-3","T4_standpoint-1","T5_four_whys-1","T5_four_whys-2","T6_two_cycles-2","T8_part_whole-2"]
NULLS = [f"N-{i}" for i in range(1, 9)]
IDS = NULLS + PRIMARY

REQUEST_A = (
    "【依頼】この状況について、まだ調べられていない、または確かめる価値のある問いを、最大五つ挙げてください。"
    "材料に支えのある問いが少なければ、五つ未満でかまいません。補助が状況に合わないと判断したら、合わないと述べて、補助を使わずに答えてかまいません。\n"
    "各問いには、材料のどの記述に基づくかを一文で添えてください。\n"
    'fitは、与えられた補助の適合度です（good, partial, poor, none。補助がなければnone）。\n'
    '出力はJSONのみ: {"fit":"good|partial|poor|none","fit_note":"一文","questions":[{"q":"問い","basis":"根拠となる材料内の記述"}]}'
)

def build_A(arm, task):
    msgs = arms.build(arm, task)
    u = msgs[0]["content"].replace(arms.REQUEST, REQUEST_A)
    return [{"role": "user", "content": u}]

DELEG = {
    "ON": "【著者の指示】文化体系を使って答えてください。",
    "OFF": "【著者の指示】文化体系は使わず、通常の分析で答えてください。",
    "AUTO": "",
}
REQUEST_B = (
    "【依頼】この状況について、まだ調べられていない、または確かめる価値のある問いを五つ挙げてください。"
    "各問いには、材料のどの記述に基づくかを一文で添えてください。\n"
    '出力はJSONのみ: {"used_framework":true または false,"framework":["使った体系のid"],"questions":[{"q":"問い","basis":"根拠"}]}'
)

def parse(text):
    o = llm.parse_json(text)
    if not isinstance(o, dict): return None
    qs = [q for q in (o.get("questions") or []) if isinstance(q, dict) and isinstance(q.get("q"), str)]
    o["questions"] = [{"q": q["q"], "basis": str(q.get("basis", ""))} for q in qs][:5]
    return o

def jobA(arm, tid, k):
    t = tasks[tid]
    for a in range(3):
        r = llm.call("deepseek", "deepseek-v4-flash", build_A(arm, t), tag=f"s3A-{arm}-{tid}-{k}-{a}", max_tokens=2000, temperature=1.0)
        o = parse(r["text"])
        if o is not None:
            return {"part": "A", "arm": arm, "task": tid, "k": k, "ok": True, "fit": o.get("fit"), "fit_note": o.get("fit_note"), "questions": o["questions"], "model": "deepseek-v4-flash", "stage": "s3"}
    return {"part": "A", "arm": arm, "task": tid, "k": k, "ok": False}

def jobB(arm, tid, k):
    t = tasks[tid]
    user = arms.task_block(t) + DELEG[arm] + ("\n\n" if DELEG[arm] else "") + REQUEST_B
    msgs = [{"role": "system", "content": arms.runtime_system()}, {"role": "user", "content": user}]
    for a in range(3):
        r = llm.call("deepseek", "deepseek-v4-flash", msgs, tag=f"s3B-{arm}-{tid}-{k}-{a}", max_tokens=2000, temperature=1.0)
        o = parse(r["text"])
        if o is not None:
            return {"part": "B", "arm": arm, "task": tid, "k": k, "ok": True, "used_self": o.get("used_framework"), "framework": o.get("framework"), "questions": o["questions"], "model": "deepseek-v4-flash", "stage": "s3"}
    return {"part": "B", "arm": arm, "task": tid, "k": k, "ok": False}

if __name__ == "__main__":
    jobs = []
    for tid in IDS:
        for arm in ["B0", "G", "R", "N", "Fx", "Fm"]:
            for k in range(6):
                jobs.append((jobA, arm, tid, k))
        for arm in ["ON", "OFF", "AUTO"]:
            for k in range(4):
                jobs.append((jobB, arm, tid, k))
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(lambda j: j[0](*j[1:]), jobs))
    out = llm.WORK / "gen-s3.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in res) + "\n", encoding="utf-8")
    print(sum(1 for r in res if r["ok"]), "/", len(res), "ok", f"est ${llm.spent():.3f}")
