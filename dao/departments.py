import json

from util import r


class Departments:
    d_key = "depts"

    def getall(self):
        return r.get(self.d_key) or "[[],[]]"

    def set(self, depts):
        r.set(self.d_key, depts)

    # def add(self, dept, typ):
    # r.hset(self.d_key, dept, typ)
    #
    # def remove(self, dept):
    #     r.hdel(self.d_key, dept)


d = Departments()
