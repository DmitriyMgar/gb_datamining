# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from gb_parse.items import GbParseItem


class GbBlogSpider(scrapy.Spider):
    name = 'gb_blog'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['http://geekbrains.ru/posts']

    xpth_str = {
        'title': '//h1[contains(@class, "blogpost-title")]/text()',
        'pub_date': '//article//time/@datetime',
        'text_content': '//article/div[contains(@class, "blogpost-content")]//text()',
        'author_url': '//article//div[@itemprop="author"]/../@href',
        'author_name': '//article//div[@itemprop="author"]/../div[@itemprop="author"]/text()',
    }

    css_str = {
        'images': ".blogpost-content img::attr('src')"
    }

    def parse(self, response):
        print(f'processing: {response.url}')
        pagination = response.xpath('//ul[contains(@class, "gb__pagination")]/li/a/@href')
        # yield response.follow_all(pagination, callback=self.parse())
        for link in pagination:
            yield response.follow(link, callback=self.parse)
        posts = response.xpath(
            '//div[@class="post-items-wrapper"]/'
            'div[contains(@class, "post-item")]//'
            'a[contains(@class, "post-item__title")]/@href'
        )
        for url in posts:
            yield response.follow(url, callback=self.post_parse)

    def post_parse(self, response):
        item = ItemLoader(GbParseItem(), response)

        item.add_value('url', response.url)

        for key, value in self.xpth_str.items():
            item.add_xpath(key, value)

        for key, value in self.css_str.items():
            item.add_css(key, value)

        yield item.load_item()


