from openpyxl import load_workbook
from requests import get, post
from functools import lru_cache

wb = load_workbook("2022年中层干部考核述职报告网盘链接统计表PDF版（20230101）.xlsx")
ac = wb.active
data = [[col.value for col in row] for row in ac.rows][2:]

all_depts = get("http://47.111.143.45:8000/depts").json()
depts = set(all_depts[0] + all_depts[1])
alias = {
    "学科建设与发展规划处": "学科建设与发展规划处（校务委员会办公室）",
    "档案馆（内设校史馆）": "档案馆（校史馆）",
    "人类命运共同体": "人类命运共同体研究院",
    "校务委员会": "校务委员会领导"
}


@lru_cache(None)
def get_members(dept):
    get_member_api = "http://47.111.143.45:8000/members?dept="

    return get(get_member_api + dept).json()


for _, dept, name, _, url in data:
    dept = dept.strip()
    dept = alias.get(dept, dept)
    name = name.strip()
    url = url.strip()
    members = get_members(dept)
    if name not in members:
        print(dept, name)
    set_work_report_api = f"http://47.111.143.45:8000/work_report?dept={dept}&member={name}"
    post(set_work_report_api, data=url)
    print(dept, name, "suc")
    # break
