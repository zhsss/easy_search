from requests import get
import json
from collections import Counter

time_string="2023-01-04_200619"
tokens=get("http://47.111.143.45:8000/tokens?time_string="+time_string).json()
c=Counter()
for token in tokens:
    progress=get(f"http://47.111.143.45:8000/progress?time_string={time_string}&token={token}").json()
    for p in progress["progress"]:
        for s in p["score"]:
            c[s]+=1
        for i in p["members"].values():
            c[i]+=1
    # break
print(c.most_common())