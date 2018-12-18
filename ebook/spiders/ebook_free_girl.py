# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ebook.items import EbookItem
from ebook.template import getElement, writeElement, createCsv, getPageNum
import pandas as pd
from scrapy import signals

class EbookFreeGirlSpider(CrawlSpider):
    name = 'ebook_free_girl'
    allowed_domains = ['www.ebookjapan.jp']
    start_urls = ['https://www.ebookjapan.jp/ebj/free/keyword-books/?uniGenres=12&genreLabel=人気の無料少女・女性まんが&sort=1']

    def __init__(self):
        self.count = 0
        col = ['漫画タイトル', 'シリーズID', 'ISBN', '漫画家', '原作者', '出版社', '掲載雑誌', 'ジャンル', '書影URL', 'タイトルURL', '立ち読みURL','無料で読める巻数','無料キャンペーン中のタイトルなのか', '無料期限']
        self.data = pd.DataFrame(columns = col)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(EbookFreeGirlSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print("done!!!!!!")
        createCsv(self, 'free', 'girl')

    def parse(self, response):
        page_num = getPageNum(response)

        total_links = []
        for i in range(page_num):
            page_links = response.xpath("//p[@class='itemThumb']/a/@href").extract()
            total_links.extend(page_links)
            target_link = "https://www.ebookjapan.jp/ebj/free/keyword-books/page{0}/?uniGenres=12&genreLabel=人気の無料少女・女性まんが&sort=1".format(i+1)
            # if i == 2:
            #     break
            yield scrapy.Request(response.urljoin(target_link))

        for link in total_links:
            yield scrapy.Request(response.urljoin(link), self.parse_element)

    def parse_element(self, response):
        item = getElement(response)
        writeElement(self, item)
        self.count += 1
