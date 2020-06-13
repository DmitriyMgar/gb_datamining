from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse import settings
from gb_parse.spiders.gb_blog import GbBlogSpider
from gb_parse.spiders.avito import AvitoSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(GbBlogSpider)
    crawl_proc.start()
