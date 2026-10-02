"""Blind pointer-rubric judging: hit (reaches the planted structure), spurious
assertion, and a neutral return filter (grounding). Framework markers are scrubbed
from question text before judging so that the judge cannot infer the arm.
"""

from __future__ import annotations

import argparse
import os
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm  # noqa: E402

TASKS = Path(os.environ.get("CSW_TASKS", str(Path(__file__).resolve().parents[1] / "tasks" / "tasks.json")))

SCRUB = [
    "この系として見るなら", "この概念として見るなら", "この系として", "この概念として",
    "易経", "易", "八卦", "六十四卦", "五行", "相生", "相剋", "縁起", "ジャイナ", "多面説", "七分法",
    "アリストテレス", "四原因", "マヤ暦", "ツォルキン", "ハアブ", "ラサ", "華厳", "サーンキヤ", "四句分別",
    "発酵", "折り紙", "鍛冶", "地層", "織物", "蜂の巣", "潮汐", "渡り鳥の編隊", "渡り鳥",
]


def scrub(s: str) -> str:
    for w in sorted(SCRUB, key=len, reverse=True):
        s = s.replace(w, "【】")
    return s


JSYS = "あなたは厳密で一貫した採点者です。出力はJSONのみです。"

HIT_USER = """次の状況について、ある分析者が五つの問いを立てました。採点してください。

【状況】
{material}

【この状況に潜む構造（鍵）】
{key}

【鍵に到達する問いが調べるべき固有の要素】
{signature}

【典型的だが鍵に届かない説明】
{trap}

【分析者の問い】
{questions}

採点基準（hit）:
2 = 問いのいずれかが、上の固有の要素を直接調べる内容になっている（その要素を名指すか、明確に前提としている）。典型的な説明を疑うだけの問い、一般的な原因探しの問いは2にしない。
1 = 固有の要素の一部に触れるか、隣接する方向を向いているが、要素そのものは調べていない。
0 = 該当する問いがない。典型的な説明の範囲の問いだけである。

厳密に採点してください。表面的に近い言葉があるだけでは2にしません。

JSONのキーをこの順に出力: reason（まず、鍵に最も近い問いを挙げて二文以内で検討する）, best（最も近い問いの番号。なければnull）, hit（0,1,2のいずれか）"""

SPUR_USER = """次の状況について、ある分析者が五つの問いと根拠を挙げました。

【状況】
{material}

【分析者の問い】
{questions}

判定: 問いまたは根拠の中に、材料に書かれていない構造・関係・事実を、すでに成り立っているかのように前提としているものがあるか。
- 「かもしれない」「確かめたい」といった仮説としての表現は前提としたことに数えない。
- 材料の記述から素直に言える範囲の言い換えは数えない。

JSONのキーをこの順に出力: reason（二文以内で検討する）, asserts（該当する問いの番号の配列。なければ空配列）"""

GROUND_USER = """次の状況について、ある分析者が五つの問いと、それぞれの根拠を挙げました。

【状況】
{material}

【分析者の問いと根拠】
{questions}

各問いについて、根拠として書かれた記述が、状況の材料に実際に書かれている（または材料から素直に読み取れる）かを判定してください。
材料に書かれていない事実を根拠としている場合は false です。

JSONのキーをこの順に出力: reason（一文）, grounded（問いごとの true/false の配列。問いと同じ並び順）"""


def fmt_questions(qs: list[dict], with_basis: bool = True, subset: list[int] | None = None) -> str:
    lines = []
    for i, q in enumerate(qs, 1):
        if subset is not None and (i - 1) not in subset:
            continue
        line = f"{i}. {scrub(q['q'])}"
        if with_basis and q.get("basis"):
            line += f"\n   根拠: {scrub(q['basis'])}"
        lines.append(line)
    return "\n".join(lines)


def _call(provider, model, user, tag, thinking=False):
    return llm.call(
        provider, model,
        [{"role": "system", "content": JSYS}, {"role": "user", "content": user}],
        tag=tag, max_tokens=6000 if thinking else 800, temperature=0.0, thinking=thinking, json_mode=True,
    )


def judge_hit(task, qs, provider="deepseek", model="deepseek-v4-flash", tag="", subset=None):
    user = HIT_USER.format(
        material=task["material"], key=task["key"], signature=task.get("signature", ""), trap=task["trap"],
        questions=fmt_questions(qs, with_basis=False, subset=subset),
    )
    obj = llm.parse_json(_call(provider, model, user, f"hit-{tag}")["text"]) or {}
    h = obj.get("hit")
    return h if h in (0, 1, 2) else None


def judge_spur(task, qs, provider="deepseek", model="deepseek-v4-flash", tag="", subset=None):
    user = SPUR_USER.format(material=task["material"], questions=fmt_questions(qs, subset=subset))
    obj = llm.parse_json(_call(provider, model, user, f"spur-{tag}")["text"]) or {}
    a = obj.get("asserts")
    return len(a) if isinstance(a, list) else None


def judge_ground(task, qs, provider="deepseek", model="deepseek-v4-flash", tag=""):
    user = GROUND_USER.format(material=task["material"], questions=fmt_questions(qs))
    obj = llm.parse_json(_call(provider, model, user, f"gnd-{tag}")["text"]) or {}
    g = obj.get("grounded")
    if isinstance(g, list) and len(g) == len(qs) and all(isinstance(x, bool) for x in g):
        return g
    return None


def judge_record(rec: dict, tasks: dict, provider, model, suffix="", lite=False) -> dict:
    task = tasks[rec["task"]]
    qs = rec["questions"]
    tag = f"{rec['stage']}-{rec['arm']}-{rec['task']}-{rec['k']}-{rec['model']}{suffix}"
    out = dict(rec)
    out["judge_model"] = model
    out["hit"] = judge_hit(task, qs, provider, model, tag) if task["kind"] == "latent" else None
    out["spur"] = judge_spur(task, qs, provider, model, tag)
    if lite:
        return out
    g = judge_ground(task, qs, provider, model, tag)
    out["grounded"] = g
    if g is not None:
        keep = [i for i, x in enumerate(g) if x]
        out["survivors"] = keep
        if keep:
            out["hit_surv"] = judge_hit(task, qs, provider, model, tag + "-surv", subset=keep) if task["kind"] == "latent" else None
            out["spur_surv"] = judge_spur(task, qs, provider, model, tag + "-surv", subset=keep)
        else:
            out["hit_surv"] = 0 if task["kind"] == "latent" else None
            out["spur_surv"] = 0
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--provider", default="deepseek")
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--lite", action="store_true")
    ap.add_argument("--every", type=int, default=1, help="judge every Nth record (cross-check subsets)")
    a = ap.parse_args()
    tasks = {t["id"]: t for t in json.loads(TASKS.read_text(encoding="utf-8"))}
    recs = [json.loads(l) for l in Path(a.gen).read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [r for r in recs if r.get("ok")][:: a.every]

    def f(r):
        try:
            return judge_record(r, tasks, a.provider, a.model, a.suffix, a.lite)
        except RuntimeError as e:
            r = dict(r); r["judge_error"] = str(e)[:200]; return r

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(f, recs))
    Path(a.out).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in res) + "\n", encoding="utf-8")
    print(f"judged {len(res)} -> {a.out}; est. spend ${llm.spent():.3f}")


if __name__ == "__main__":
    main()
