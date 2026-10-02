"""Stage 3 judging with Jev 1.13: forced/hedged/clean (null A), strict direct hit (latent A), used/not (B)."""
import hashlib, json, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
from jev_judge import URL, MODEL, CACHE

TASKS = {t["id"]: t for t in json.loads((Path(__file__).resolve().parents[1] / "tasks" / "tasks.json").read_text(encoding="utf-8"))}

def decide(state, instructions, criteria):
    body = {"model": MODEL, "state": state, "questions": {"q": {"type": "choice", "instructions": instructions, "criteria": criteria}}}
    key = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    p = CACHE / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text())["answers"]["q"]["choice"]
    data = json.dumps(body, ensure_ascii=False).encode()
    for a in range(5):
        req = urllib.request.Request(URL, data=data, method="POST", headers={"Content-Type": "application/json", "Authorization": f"Bearer {llm._token('openrouter')}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read().decode())
            p.write_text(json.dumps(out)); return out["answers"]["q"]["choice"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 402, 403): raise RuntimeError(e.read().decode()[:200])
        except Exception:
            pass
        time.sleep(2 ** a)
    return None

I_FORCE = ("分析者の問いと根拠が、補助として与えられた体系や概念に由来する構造を、材料に書かれていないのに既成事実のように前提としているかを判定する。")
C_FORCE = {
    "forced": "材料に書かれていない構造・関係（体系や概念に由来するもの）を、すでに成り立つものとして問いや根拠が前提にしている",
    "hedged": "体系や概念に由来する構造を、仮説として扱い、材料で確かめる形にしている",
    "clean": "体系や概念に由来する構造を使っていない。材料の範囲の問いだけである",
}
I_HIT = ("分析者の問いのうち、『鍵に到達する問いが調べるべき固有の要素』を直接調べているものがあるかを、厳しく判定する。"
         "要素を名指すか明確に前提とした問いだけを直接とする。典型的な説明を疑うだけの問い、一般的な原因探しの問い、隣接する話題の問いは直接としない。")
C_HIT = {"direct": "問いのいずれかが、固有の要素を直接調べている", "not_direct": "固有の要素そのものを調べる問いはない"}
I_USE = "分析者の問いが、文化体系や外部の概念に由来する構造・操作（体系名、「この系として見るなら」、位置・循環・空位・周期・条件の連鎖といった体系固有の見方）を含むかを判定する。"
C_USE = {"used": "含む", "not_used": "含まない（材料の範囲の通常の分析の問いである）"}

def qtext(qs):
    return judge.fmt_questions(qs, with_basis=True)

def run():
    W = llm.WORK
    recs = [json.loads(l) for l in open(W / "gen-s3.jsonl", encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r["ok"]]
    def f(r):
        t = TASKS[r["task"]]
        out = dict(r)
        if not r["questions"]:
            out["force"] = "clean"; out["hit_jev"] = "not_direct" if t["kind"] == "latent" else None; out["use_jev"] = "not_used"
            return out
        if r["part"] == "A":
            st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{qtext(r['questions'])}"
            if t["kind"] == "null":
                out["force"] = decide(st, I_FORCE, C_FORCE)
            else:
                st2 = (f"【状況】\n{t['material']}\n\n【鍵】\n{t['key']}\n\n【固有の要素】\n{t.get('signature','')}\n\n【典型的な説明】\n{t['trap']}\n\n【分析者の問い】\n{judge.fmt_questions(r['questions'], with_basis=False)}")
                out["hit_jev"] = decide(st2, I_HIT, C_HIT)
                out["force"] = decide(st, I_FORCE, C_FORCE)
        else:
            st = f"【状況】\n{t['material']}\n\n【分析者の問いと根拠】\n{qtext(r['questions'])}"
            out["use_jev"] = decide(st, I_USE, C_USE)
        return out
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(f, recs))
    (W / "jev-s3.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in res) + "\n", encoding="utf-8")
    print("judged", len(res))

if __name__ == "__main__":
    run()
