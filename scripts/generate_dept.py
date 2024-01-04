import json
from collections import defaultdict
import time
from openpyxl import Workbook, load_workbook
from requests import get, post

path_text = '''校长助理
校务委员会领导
学部领导
本科生院
研究生院
招生处
法治与内控管理办公室
科学研究处
学科建设与发展规划处（校务委员会办公室）
教育质量评估与督导处
人事处
财务处
审计处
国际交流与合作处（港澳台事务办公室）
国内交流与合作处（校友工作办公室）
信息化处
实验室与设备管理处
培训教育管理处
校园建设处
国有资产管理处
后勤保障处
校教育基金会秘书处
党政办公室
纪委办公室（监察处）
党委巡察工作办公室
党委组织部
党委宣传部
党委统战部
党委教师工作部
学生工作部（处）（武装部）
保卫部（处）
离退休工作处
机关党委
工会
团委
继续教育学院（高等职业技术学院）
人类命运共同体研究院
图书馆
档案馆（校史馆）
传媒博物馆
融媒体中心
校医院 
教育服务中心
教育发展中心
出版社
信息与通信工程学院
计算机与网络空间安全学院
数据科学与智能媒体学院
媒体融合与传播国家重点实验室
政府与公共事务学院
新闻学院
电视学院
传播研究院
人文学院
外国语言文化学院
戏剧影视学院
播音主持艺术学院
动画与数字艺术学院
音乐与录音艺术学院
艺术研究院
经济与管理学院
广告学院
文化产业管理学院
马克思主义学院
体育部
国际传媒教育学院（海南国际学院）（境外学生教育中心）'''

all_depts = [i.strip() for i in path_text.split('\n')]

data = load_workbook("2022年中层干部考核人员名单.xlsx")
ac = data.active
lines = [[col.value for col in line] for line in ac.rows]
lines.pop(0)
lines.pop(0)

depts = [[], []]

dept_cor = {}
members = defaultdict(list)

for line in lines:
    dept = line[1].strip()
    member = line[2].strip()
    origin = line[3].strip()
    dept_cor[dept] = origin
    members[dept].append(member)

for dept in all_depts:
    if dept_cor[dept] == "教学科研单位":
        depts[0].append(dept)
    elif dept_cor[dept] == "党群行政职能部门":
        depts[1].append(dept)
    elif dept_cor[dept] == "两个部门兼有":
        depts[0].append(dept)
        depts[1].append(dept)
    else:
        raise Exception(dept + " " + dept_cor[dept])

# set_depts_api = "http://47.111.143.45:8000/depts"
set_depts_api = "http://127.0.0.1:8000/depts"

post(set_depts_api, data=json.dumps(depts, ensure_ascii=False).encode())
# set_member_api = "http://47.111.143.45:8000/members?dept="
set_member_api = "http://127.0.0.1:8000/members?dept="
for dept in all_depts:
    post(set_member_api + dept, data=json.dumps(members[dept], ensure_ascii=False).encode())
