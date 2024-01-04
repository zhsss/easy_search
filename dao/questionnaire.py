import datetime
import json
from collections import defaultdict

from .member import m
from .departments import d
from util import r, random_str

'''
核心是2种结构：
    key:
        qs 所有问卷时间
        qs:{time_key} 该问卷所有有效token
        qs:{time_key}:{token} 该token所有分数  
'''


class Questionnaire:
    q_key = "qs"

    def getall(self):
        return sorted(r.smembers(self.q_key), reverse=True)

    def get_tokens(self, time_string):
        return list(r.smembers(f"{self.q_key}:{time_string}"))

    def is_valid_token(self, time_string, token):
        return r.sismember(f"{self.q_key}:{time_string}", token)

    def generate_a_qs(self, online_num, offline_num, leader_num):
        def match_only_member_dept(target):
            no_tot_rank_depts = {"校长助理", "学部领导", "校务委员会领导"}
            for dept in no_tot_rank_depts:
                if target.startswith(dept):
                    return True
            return False

        now = datetime.datetime.now()
        time_string = str(now.strftime("%Y-%m-%d_%H%M%S"))

        time_key = f"{self.q_key}:{time_string}"
        token_num = (online_num + offline_num) * 2 + leader_num
        tokens = set()
        while len(tokens) < token_num:
            tokens.add(random_str(6))
        tokens = list(tokens)

        depts = json.loads(d.getall())

        tokens_copy = tokens[:]
        online_type0_tokens = [tokens_copy.pop() for _ in range(online_num)]
        online_type1_tokens = [tokens_copy.pop() for _ in range(online_num)]
        offline_type0_tokens = [tokens_copy.pop() for _ in range(offline_num)]
        offline_type1_tokens = [tokens_copy.pop() for _ in range(offline_num)]
        leader_tokens = [tokens_copy.pop() for _ in range(leader_num)]

        type0_depts, type1_depts = depts

        token_to_progress = {}

        # token_to_result中的type说明
        # 第一个数字代表是否为在线，0代表online， 1代表offline
        # 第二个数字代表dept类型，0代表教学教研， 1代表党群行政职能部门
        for token in online_type0_tokens:
            token_to_progress[token] = json.dumps({
                'type': f"00",
                'progress': [
                    {'id': i, 'name': dept, "score": [0] * 4, "members": {}}
                    for i, dept in enumerate([dept for dept in type0_depts if not match_only_member_dept(dept)])]
            }, ensure_ascii=False)
        for token in online_type1_tokens:
            token_to_progress[token] = json.dumps({
                'type': f"01",
                'progress': [
                    {'id': i, 'name': dept, 'score': [0] * 2, "members": {}}
                    for i, dept in enumerate([dept for dept in type1_depts if not match_only_member_dept(dept)])]
            }, ensure_ascii=False)
        for token in offline_type0_tokens:
            token_to_progress[token] = json.dumps({
                'type': f"10",
                'progress': [
                    {'id': i, 'name': dept, 'score': [0] * 4, "members": {name: 0 for name in json.loads(m.get(dept))}}
                    for i, dept in enumerate(type0_depts)]
            }, ensure_ascii=False)
        for token in offline_type1_tokens:
            token_to_progress[token] = json.dumps({
                'type': f"11",
                'progress': [
                    {'id': i, 'name': dept, 'score': [0] * 2, "members": {name: 0 for name in json.loads(m.get(dept))}}
                    for i, dept in enumerate(type1_depts)]
            }, ensure_ascii=False)
        for token in leader_tokens:
            leader_progress = {
                'type': '2',
                'progress': []
            }

            for i, dept in enumerate(type1_depts):
                leader_progress['progress'].append({
                    'id': i, 'name': dept, 'score': [0] * 2, 'members': {name: 0 for name in json.loads(m.get(dept))}
                })
            for i, dept in enumerate([dept for dept in type0_depts if not match_only_member_dept(dept)],
                                     start=len(type1_depts)):
                leader_progress['progress'].append({
                    'id': i, 'name': dept, 'score': [0] * 4, 'members': {name: 0 for name in json.loads(m.get(dept))}
                })
            token_to_progress[token] = json.dumps(leader_progress, ensure_ascii=False)
            # token_to_progress[token] = json.dumps({
            #     'type': f"2",
            #     'progress': [
            #         {'id': i, 'name': dept, 'score': [0] * 2, "members": {name: 0 for name in json.loads(m.get(dept))}}
            #         for i, dept in enumerate(type0_depts + type1_depts)]
            # }, ensure_ascii=False)

        for token, progress_string in token_to_progress.items():
            progress = json.loads(progress_string)
            for target in progress["progress"]:
                if match_only_member_dept(target["name"]):
                    # if any(target["name"].startswith(dept) for dept in no_tot_rank_depts):
                    target["score"] = [99] * len(target["score"])
            token_to_progress[token] = json.dumps(progress, ensure_ascii=False)

        r.sadd(self.q_key, time_string)
        [r.sadd(time_key, token) for token in tokens]
        [r.set(f"{time_key}:{token}", progress_string) for token, progress_string in token_to_progress.items()]

        return time_string

    def get_progress(self, time_string, token):
        return r.get(f"{self.q_key}:{time_string}:{token}")

    def update_score(self, time_string, token, did, score, no):
        token_key = f"{self.q_key}:{time_string}:{token}"
        progress = json.loads(self.get_progress(time_string, token))
        progress['progress'][did]['score'][no] = score
        r.set(token_key, json.dumps(progress, ensure_ascii=False))

    def update_member_score(self, time_string, token, did, score, name):
        token_key = f"{self.q_key}:{time_string}:{token}"
        progress = json.loads(self.get_progress(time_string, token))
        progress['progress'][did]['members'][name] = score
        r.set(token_key, json.dumps(progress, ensure_ascii=False))

    def get_a_qs_result(self, time_string):
        # 导出某份试卷所有
        tokens = self.get_tokens(time_string)
        scores = defaultdict(list)
        for token in tokens:
            progress = json.loads(self.get_progress(time_string, token))
            for p in progress['progress']:
                scores[p['name']].append(p['score'])
        return scores

    def get_status(self, time_string, token):
        return r.get(f"{self.q_key}:{time_string}:{token}_status")

    def set_status(self, time_string, token, status):
        return r.set(f"{self.q_key}:{time_string}:{token}_status", status)


q = Questionnaire()
