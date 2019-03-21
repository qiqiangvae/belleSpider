import redis


class RedisClient(object):
    pool = redis.ConnectionPool(host='118.25.48.56')
    redis_client = redis.Redis(connection_pool=pool)
