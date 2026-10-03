import json, sys, time, urllib.request
sys.path.insert(0, ".")
import local_judge as lj, validate_local as vl

def gen(prompt, n=1):
    body = {"model": "qwen3.5:4b", "prompt": prompt, "raw": True, "stream": False, "think": False,
            "logprobs": True, "top_logprobs": 12, "keep_alive": "60m",
            "options": {"temperature": 0, "num_predict": n, "num_ctx": 6144}}
    t = time.time()
    r = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(r, timeout=900).read().decode())
    return out, time.time() - t

recs = vl.build_records()
tid = recs[0]["key"][1]
same = [r for r in recs if r["key"][1] == tid][:4]
task = vl.TASKS[tid]
head = "<|im_start|>system\n" + lj.SYSTEM + "<|im_end|>\n<|im_start|>user\n" + lj.prefix(task)
tail = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
o, s = gen(head)
print("prefill", round(s, 1), "s; eval_count", o.get("prompt_eval_count"), "keys", [k for k in o if k != "response"][:12])
for r in same:
    o, s = gen(head + lj.suffix(r["questions"]) + tail)
    lp = (o.get("logprobs") or [{}])[0].get("top_logprobs", [])[:3]
    print(round(s, 1), "s", "prompt_eval_count", o.get("prompt_eval_count"), "resp", repr(o.get("response")), [(x["token"], round(x["logprob"], 2)) for x in lp])
