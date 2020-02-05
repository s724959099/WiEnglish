from web.asyspider.spider import Spider, Proxy, DBProxy
import re
from pyquery import PyQuery as pq
import logging
from web.tools import log
from pprint import pprint as pp
import argparse
import time
from web.tools.functions import get_url_query_str, url_with_query_str, try_safety, timeit, url_add_params
from urllib.parse import urljoin
import os

logger = logging.getLogger('demo')
HOST = 'https://www.comicbus.com/'


class Crawler(Spider):
    status_code = (200, 301, 302)
    platform = 'desktop'
    max_tasks = 10
    sleep_time = None
    timeout = 30
    retries = 10
    check_crawled_urls = True
    update_cookies = True
    min_content_length = 1
    proxies_set = set()
    ProxyClass = Proxy
    start_urls = [
        'https://www.comicbus.com/html/14297.html'
    ]
    headers = """
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-TW,zh;q=0.9,en;q=0.8,zh-CN;q=0.7,en-US;q=0.6
    Cache-Control: max-age=0
    Connection: keep-alive
    Host: www.comicbus.com
    Sec-Fetch-Mode: navigate
    Sec-Fetch-Site: same-origin
    Sec-Fetch-User: ?1
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36
    """

    async def on_start(self):
        for url in self.start_urls:
            self.add_task(self.index_page, url)

    async def index_page(self, url):
        r = await self.async_crawl(url)
        doc = str(r.content, encoding='utf-8', errors='ignore')
        dom = pq(doc)
        _id = re.findall('\d+', url)[0]
        urls = [url_add_params(f'https://comicbus.live/online/manga_{_id}.html', ch=count) for count in
                range(1, len(dom('#div_li1 td > a')))]
        urls = list(set(urls))
        for url in urls:
            self.add_task(self.first_pages, url)

    async def save_img(self, url, fname):
        pth = os.path.join('./data/', fname)
        if os.path.exists(pth):
            return
        r = await self.async_crawl(url)
        with open(pth, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    def create_dir(self, dirname):
        pth = os.path.join('./data/', dirname)
        if not os.path.exists(pth):
            os.mkdir(pth)

    async def first_pages(self, url):
        try:
            await self.find_page(url)
        except Exception as e:
            logger.error('error: %s', url)

    async def find_page(self, url):
        r = await self.async_crawl(url)
        if not r:
            return
        doc = str(r.content, encoding='big5', errors='ignore')
        dom = pq(doc)
        dom('li > a').text()
        dirname = dom('title').text().split('-')[0].strip()
        eps = re.findall('\d+', dom('title').text().split('-')[1])[0]
        eps = int(eps)
        self.create_dir(dirname)
        page = int(dom('a.onpage').text())
        fname = '{}/{:0>3d}_{:0>2d}.jpg'.format(dirname, eps, page)
        imgs = [urljoin(url, el.attr.src) for el in dom('img').items()]
        target_img = [img for img in imgs if 'comicpic' in img][0]

        await self.save_img(target_img, fname)

        next_url = urljoin(url, dom('#sidebar-follow a').eq(-1).attr.href)
        if 'thend.asp' in next_url:
            next_url = None
        if next_url:
            await self.find_page(next_url)


if __name__ == '__main__':
    log.initlog('DEMO', level=logging.DEBUG, debug=True)
    c = Crawler()
    c.run()
