import json, sys, time
sys.path.insert(0, ".")
import local_judge as lj
t = {"material": "A社の会議は毎週月曜に開かれ、議事録は担当者が書く。" * 5, "key": "議事録の担当が決まっていない。", "signature": "議事録を書く担当の不在", "trap": "担当者の怠慢。"}
qs = [{"q": "議事録を書く担当は誰か。", "basis": "x"}, {"q": "会議は何曜日か。", "basis": "y"}]
for i in range(3):
    r = lj.ask("qwen3.5:4b", t, qs)
    print(i, json.dumps(r, ensure_ascii=False))
