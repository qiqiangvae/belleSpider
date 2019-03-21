import redis
import re

re_compile = re.compile(r'\d{6}/\d+')


class RedisClient(object):
    pool = redis.ConnectionPool(host='118.25.48.56')
    redis_client = redis.Redis(connection_pool=pool)
