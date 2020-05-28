# -*- coding: utf-8 -*-
import scrapy


class GbBlogSpider(scrapy.Spider):
    name = 'gb_blog'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['http://geekbrains.ru/']

    def parse(self, response):
        pass
