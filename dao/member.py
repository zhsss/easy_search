import json

from util import r

DEFAULT_WORK_REPORT_URL = "https://kod.cuc.edu.cn/#s/81CphtQA"


class Member:
    m_key = "members"

    def get(self, dept):
        return r.get(f"{self.m_key}_{dept}") or "[]"

    def set(self, dept, members):
        r.set(f"{self.m_key}_{dept}", members)

    def get_work_report(self, dept, member):
        return r.get(f"work_{dept}_{member}") or DEFAULT_WORK_REPORT_URL

    def set_work_report(self, dept, member, url):
        r.set(f"work_{dept}_{member}", url)


m = Member()
