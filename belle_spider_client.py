from bellespider import url_manager, html_downloader, html_parser, img_saver, redis_client


class SpiderMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.saver = img_saver.ImgSaver()

    def craw(self, url):
        cnt = 1
        start = self.urls.start()
        if start is None or len(start) == 0:
            start = url
        self.urls.add_new_special(start)
        while self.urls.has_new_special():
            new_url = self.urls.get_new_special()
            print('craw special %d : %s' % (cnt, new_url))
            html_content = self.downloader.download(new_url)
            new_urls, img_data = self.parser.parse(new_url, html_content)
            self.urls.add_new_specials(new_urls)
            self.saver.save(img_data)
            cnt += 1
            if cnt == 1000:
                break


if __name__ == '__main__':
    root_url = 'https://www.2717.com/ent/meinvtupian/2019/314371.html'
    main = SpiderMain()
    main.craw(root_url)
