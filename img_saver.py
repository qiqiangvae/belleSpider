import requests
import re
import os

from bellespider.redis_client import RedisClient

HAS_IMG_KEY_SAVED = 'belle:img:url:saved'
HAS_IMG_KEY_FAILED = 'belle:img:url:failed'


class ImgSaver(object):
    cnt = 0

    def __init__(self):
        self.redis = RedisClient.redis_client

    def save(self, img_data):
        if img_data is None or len(img_data) == 0:
            return
        for img_url in img_data:
            if self.had_downloaded(img_url):
                print('img %s had downloaded already' % img_url)
            try:
                response = requests.get(img_url)
                if response.status_code != 200:
                    continue
                else:
                    img = response.content
                    dir_name = '/Users/qiqiang/Desktop/belle/' + re.compile(r'\d{6}/\d+').search(
                        img_url).group().replace(
                        '/', '')
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                    img_name = dir_name + '/' + re.compile(r'\w*\.jpg').search(img_url).group()
                    with open(img_name, 'wb') as f:
                        f.write(img)
                        self.downloaded(img_url)
                        print('save belle img %d : %s successful' % (ImgSaver.cnt, img_url))
                        ImgSaver.cnt += 1


            except Exception as ex:
                print('save belle img %d : %s  failed' % (ImgSaver.cnt, img_url))
                self.failed(img_url)

    def had_downloaded(self, url):
        return self.redis.sismember(HAS_IMG_KEY_SAVED, url)

    def downloaded(self, url):
        return self.redis.sadd(HAS_IMG_KEY_SAVED, url)

    def failed(self, url):
        return self.redis.sadd(HAS_IMG_KEY_FAILED, url)

    def retry(self):
        lst = self.redis.smembers(HAS_IMG_KEY_FAILED)
        self.save(lst)
