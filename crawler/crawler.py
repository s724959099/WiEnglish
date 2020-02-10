from asyspider.spider import Spider, Proxy
import re
from pyquery import PyQuery as pq
import logging
from tools import log
from tools.functions import url_add_params
from urllib.parse import urljoin

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
    start_urls = (
        'https://www.comicbus.com/html/14297.html',
    )
    words = ['invest']

    def __init__(self, models):
        super().__init__()
        self.models = models

    def to_url(self, word):
        return f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{word}'

    async def on_start(self):
        for word in self.words:
            self.add_task(self.index_page, word)

    async def find_synonyms_and_antonyms(self, word):
        url = f'https://www.thesaurus.com/browse/{word}'
        return await self.async_crawl(url)

    async def index_page(self, word):
        """
        todo 不做任何的確認 應該要在之前就先確認
        """
        url = self.to_url(word)
        r = await self.async_crawl(url)
        doc = str(r.content, encoding='utf-8', errors='ignore')
        dom = pq(doc)
        if self.models.Word.objects.filter(english=word).count():
            instance = self.models.Word.objects.filter(english=word).first()
        else:
            instance = self.models.Word.objects.create(
                english=word,
                chinese=dom('.def-body > .trans').text(),
                word_type=dom('span.pos').text(),
            )
        r = await self.find_synonyms_and_antonyms(word)
        dom = pq(r.text)
        # synonyms
        for el in dom('.css-1lc0dpe').eq(0)('li').items():
            sub_word = el.text()
            if self.models.Word.objects.filter(english=sub_word).count():
                sub_instance = self.models.Word.objects.filter(english=sub_word).first()
            else:
                sub_instance = self.models.Word.objects.create(
                    english=sub_word,
                )
            instance.synonyms.add(sub_instance)
            sub_instance.synonyms.add(instance)
            sub_instance.save()
        # antonym
        for el in dom('.css-1lc0dpe').eq(1)('li').items():
            sub_word = el.text()
            if self.models.Word.objects.filter(english=sub_word).count():
                sub_instance = self.models.Word.objects.filter(english=sub_word).first()
            else:
                sub_instance = self.models.Word.objects.create(
                    english=sub_word,
                )
            instance.antonym.add(sub_instance)
            sub_instance.antonym.add(instance)
            sub_instance.save()
        instance.save()
        for el in dom('div.examp').items():
            self.models.Sentence.objects.create(
                word=instance,
                english=el('span.deg').text(),
                chinese=el('span.trans.hdb').text()
            )
