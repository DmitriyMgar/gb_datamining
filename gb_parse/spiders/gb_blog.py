# -*- coding: utf-8 -*-
import scrapy


class GbBlogSpider(scrapy.Spider):
    name = 'gb_blog'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['http://geekbrains.ru/posts']

    def parse(self, response):
        print(1)
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
        print(1)

    def post_parse(self, response):
        title = response.xpath('//h1[contains(@class, "blogpost-title")]/text()').extract_first()
        pub_date = response.xpath('//article//time/@datetime').extract_first()
        text_content = response.xpath('//article/div[contains(@class, "blogpost-content")]//text()').extract()
        author_selector = response.xpath('//article//div[@itemprop="author"]/..')[0]
        author_url = author_selector.xpath('@href').extract_first()
        author_name = author_selector.xpath('div[@itemprop="author"]/text()').extract_first()
        print(1)


