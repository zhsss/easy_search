from flask import Blueprint, request
import json
from dao.departments import d

depts_view = Blueprint("depts", __name__)


@depts_view.route('/depts', methods=['GET', 'POST', 'DELETE'])
def depts_api():
    if request.method == "GET":
        return d.getall()
    elif request.method == "POST":
        # type=0为教学教研单位  type=1为党群行政职能部门

        depts = json.loads(request.data.decode())
        d.set(json.dumps(depts, ensure_ascii=False))
        return ""



