from requests import get
import json
import requests

url = "http://47.111.143.45:8000/tokens?time_string=2022-12-28_210923"

tokens = json.loads(requests.request("GET", url).content)
for token in tokens:
    progress = json.loads(get(f"http://47.111.143.45:8000/progress?time_string=2022-12-28_210923&token={token}").content)
    if progress["type"][0]=="2":
        print(progress)
