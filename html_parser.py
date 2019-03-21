from bs4 import BeautifulSoup
import re

img_compile = re.compile(r'^https://t1.hddhhn.com/uploads/tu/\d{6}/\d*/\w*\.jpg$')
url_compile = re.compile(r'^/ent/meinvtupian/\d{4}/\d*\.html$')


class HtmlParser(object):
    def parse(self, new_url, html_content):
        if html_content is None:
            return None, None
        data = []
        urls = []
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        all_img = soup.find_all('img', src=img_compile)
        for node in all_img:
            data.append(node['src'])

        all_img = soup.find_all('a', href=url_compile)
        for node in all_img:
            urls.append('https://www.2717.com' + node['href'])
        return urls, data
