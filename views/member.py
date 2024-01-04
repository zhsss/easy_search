import json

from flask import request, Blueprint
from dao.questionnaire import q
from dao.member import m

member_view = Blueprint("member", __name__)


@member_view.route('/rate_member', methods=["POST"])
def rate_member():
    # 打分
    time_string = request.args.get('time_string')
    token = request.args.get('token')
    did = int(request.args.get('id'))
    name = request.args.get('name')
    score = int(request.args.get('score'))
    q.update_member_score(time_string, token, did, score, name)
    return ""


@member_view.route('/members', methods=['GET', 'POST'])
def members_api():
    dept = request.args.get('dept')
    if request.method == "GET":
        return m.get(dept)
    elif request.method == "POST":
        m.set(dept, request.data.decode())
        return ""


@member_view.route('/work_report', methods=['GET', 'POST'])
def get_work_report():
    dept = request.args.get('dept')
    if '-' in dept:
        dept = dept.split('-')[0]
    member = request.args.get('member')

    if request.method == "GET":
        return m.get_work_report(dept, member)
    elif request.method == "POST":
        url = request.data.decode()
        m.set_work_report(dept, member, url)
        return ""
