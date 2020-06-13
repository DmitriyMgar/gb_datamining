# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy_config import CLIENT_DB


class GbParsePipeline:
    def process_item(self, item, spider):
        collection = CLIENT_DB[spider.name]
        collection.insert(item)
        return item


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get('images', []):
            try:
                yield Request(url)
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results]
        return item


class GbParse2Pipeline:
    def process_item(self, item, spider):
        print(1)
        return item