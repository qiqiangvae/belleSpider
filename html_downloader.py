import requests
import re

re_compile = re.compile(r'^https://www.2717.com/ent/meinvtupian/\d{4}/\d*\.html$')


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        if not re_compile.match(url):
            return None
        response = requests.get(url)
        if response.status_code != 200:
            return None
        else:
            return response.content
