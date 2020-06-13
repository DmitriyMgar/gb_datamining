# -*- coding: utf-8 -*-
import scrapy
from gb_parse.items import AvitoItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry']
    page_num = 1

    # def __init__(self, *args, **kwargs):
    #     self.start_urls.extend([f'{self.start_urls[0]}?p={num}' for num in range(2, 101)])
    #     super().__init__(*args, **kwargs)

    def parse(self, response):
        for url in response.css('.snippet-list .item h3.snippet-title a::attr("href")'):
            yield response.follow(url, callback=self.adv_parse)

        yield response.follow(f'{self.start_urls[0]}?p={self.page_num}')
        self.page_num += 1

    def adv_parse(self, response):
        # todo парсинг объявлений
        item = AvitoItem()
        pass