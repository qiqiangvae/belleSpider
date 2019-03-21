from bellespider.redis_client import RedisClient

NEW_SPECIAL_KEY = 'belle:special:url:new'
OLD_SPECIAL_KEY = 'belle:special:url:old'


class UrlManager(object):

    def __init__(self):
        self.redis = RedisClient.redis_client
        pass

    def add_new_special(self, url):
        if url is None:
            return
        if not self.redis.sismember(NEW_SPECIAL_KEY, url) \
                and not self.redis.sismember(OLD_SPECIAL_KEY, url):
            self.redis.sadd(NEW_SPECIAL_KEY, url)

    def add_new_specials(self, new_urls):
        if new_urls is None or len(new_urls) == 0:
            return
        for url in new_urls:
            self.add_new_special(url)

    def has_new_special(self):
        return self.redis.scard(NEW_SPECIAL_KEY) > 0

    def get_new_special(self):
        pop = self.redis.spop(NEW_SPECIAL_KEY)
        self.redis.sadd(OLD_SPECIAL_KEY, pop)
        return str(pop, encoding="utf8")

    def start(self):
        start = self.redis.spop(NEW_SPECIAL_KEY)
        if start is None:
            return None
        return str(start, encoding="utf8")
