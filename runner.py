from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse import settings
from gb_parse.spiders.gb_blog import GbBlogSpider
from gb_parse.spiders.avito import AvitoSpider
from gb_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(
        InstagramSpider,
        'scrapyman6',
        '#PWD_INSTAGRAM_BROWSER:10:1592066895:AZJQAH5RcrX1fbgDcEPXc4OL1OjaB5HtMhJZ7/WFu97eRM82p287QjhEYfzlsE/sc9DmAPZ'
        '04nkhPCbVou0rE0BUIDEfFzLr22eceh+ddsf/8IHXOf45qgYs4dc1/4Rlq+CjWITnBdPK8+mN/kgXd/zi',
        ['realdonaldtrump', ]
    )
    crawl_proc.start()
