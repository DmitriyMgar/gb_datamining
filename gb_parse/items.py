# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def gb_text_to_str(item):
    return ''.join(item)


class GbParseItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    pub_date = scrapy.Field(output_processor=TakeFirst())
    text_content = scrapy.Field(input_processor=gb_text_to_str, output_processor=TakeFirst())
    author_url = scrapy.Field(output_processor=TakeFirst())
    author_name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()


class AvitoItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
