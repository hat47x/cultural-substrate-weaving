"""Add a `signature` to each task: the distinctive element a question must probe to
count as reaching the key (merely doubting the standard explanation is not enough)."""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm  # noqa: E402

P = Path(os.environ.get("CSW_TASKS", str(Path(__file__).resolve().parents[1] / "tasks" / "tasks.json")))
tasks = json.loads(P.read_text(encoding="utf-8"))

USER = """次のケースの「鍵」に到達するには、問いが何を調べる必要があるかを書いてください。

【状況】
{material}

【鍵】
{key}

【典型的な説明】
{trap}

書くこと: signature。鍵の構造に固有の要素を、一文で書く。典型的な説明を疑うだけの問い、一般的な「原因は何か」「関係はあるか」という問いは含まない。
{null_note}
JSONのキー: signature"""

NULL_NOTE = "このケースには潜在構造がない。signature には「潜在構造を主張する問いは該当しない」と書く。\n"


def f(t):
    r = llm.call(
        "deepseek", "deepseek-v4-pro",
        [{"role": "user", "content": USER.format(
            material=t["material"], key=t["key"], trap=t["trap"],
            null_note=NULL_NOTE if t["kind"] == "null" else "")}],
        tag=f"sig-{t['id']}", max_tokens=800, temperature=0.0, json_mode=True,
    )
    obj = llm.parse_json(r["text"]) or {}
    t["signature"] = obj.get("signature")
    return t


with ThreadPoolExecutor(max_workers=8) as ex:
    out = list(ex.map(f, tasks))
P.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for t in out:
    print(t["id"], "|", t["signature"])
