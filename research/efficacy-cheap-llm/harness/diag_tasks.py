"""Diagnose why task-bank candidates are rejected (reads cached writer/check calls)."""
import collections
import sys

sys.path.insert(0, ".")
import build_tasks as b  # noqa: E402
import llm  # noqa: E402

specs = []
for tname, t in b.TYPES.items():
    for i, dom in enumerate(t["domains"]):
        specs.append(dict(id=f"{tname}-{i+1}", kind="latent", type=tname, domain=dom, plant=t["plant"], banned=t["banned"]))
for i, (e, tr) in enumerate(b.NULL_DOMAINS):
    specs.append(dict(id=f"N-{i+1}", kind="null", type="null", domain=e, event=e, truth=tr))

reasons = collections.Counter()
per = collections.defaultdict(list)
for spec in specs:
    for attempt in range(4):
        if spec["kind"] == "latent":
            user = b.WRITER_USER.format(domain=spec["domain"], plant=spec["plant"], banned="、".join(spec["banned"]))
        else:
            user = b.NULL_USER.format(event=spec["event"], truth=spec["truth"])
        sid = spec["id"]
        r = llm.call(
            "deepseek", "deepseek-v4-pro",
            [{"role": "system", "content": b.WRITER_SYS}, {"role": "user", "content": user}],
            tag=f"writer-{sid}-{attempt}", max_tokens=2500, temperature=0.8, json_mode=True,
        )
        o = llm.parse_json(r["text"])
        if not isinstance(o, dict) or not all(k in o for k in ("material", "trap", "key", "evidence")):
            reasons["json"] += 1; per[sid].append("json"); continue
        m = o["material"]
        if not isinstance(m, str) or not (350 <= len(m) <= 1000):
            tag = "len:%d" % (len(m) if isinstance(m, str) else -1)
            reasons["len"] += 1; per[sid].append(tag); continue
        hit = [x for x in spec.get("banned", []) if x in m]
        if spec["kind"] == "latent" and hit:
            reasons["banned"] += 1; per[sid].append("banned:" + ",".join(hit)); continue
        ev = o["evidence"]
        if not isinstance(ev, list) or not all(isinstance(e, str) and e in m for e in ev):
            reasons["evidence-not-verbatim"] += 1; per[sid].append("evidence"); continue
        c = llm.call(
            "deepseek", "deepseek-v4-flash",
            [{"role": "system", "content": b.CHECK_SYS}, {"role": "user", "content": b.CHECK_USER.format(material=m, key=o["key"])}],
            tag=f"check-{sid}-{attempt}", max_tokens=600, temperature=0.0, thinking=True, json_mode=True,
        )
        chk = llm.parse_json(c["text"]) or {}
        reasons["check:%s/%s" % (chk.get("derivable"), chk.get("leaks"))] += 1
        per[sid].append("check:%s/%s %s" % (chk.get("derivable"), chk.get("leaks"), str(chk.get("note"))[:70]))
print(reasons)
for k, v in per.items():
    print(k, v)
