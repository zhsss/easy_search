import random
import string

import os
import redis


def random_str(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


redis_info = {
    "host": os.environ.get("db", "localhost"),
    "password": "1358282318",
    "port": 6379,
    "db": 0
}

r = redis.Redis(**redis_info, decode_responses=True)
