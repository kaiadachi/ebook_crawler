# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ebook.items import EbookItem
from ebook.template import getElement, writeElement, createCsv, getPageNum
import pandas as pd

class EbookFullGirlSpider(CrawlSpider):
    name = 'ebook_full_girl'
    allowed_domains = ['www.ebookjapan.jp']
    start_urls = ['https://www.ebookjapan.jp/ebj/tag_genre/smallgenre2002/']

    def __init__(self):
        self.count = 0
        col = ['漫画タイトル', 'シリーズID', 'ISBN', '漫画家', '原作者', '出版社', '掲載雑誌', 'ジャンル', '書影URL', 'タイトルURL', '立ち読みURL','無料で読める巻数','無料キャンペーン中のタイトルなのか', '無料期限']
        self.data = pd.DataFrame(columns = col)

    def parse(self, response):
        page_num = getPageNum(response)

        total_links = []
        for i in range(page_num):
            page_links =  response.xpath("//li[@class='itemList']//a[@class = 'itemThumb ']/@href").extract()
            total_links.extend(page_links)
            target_link = "https://www.ebookjapan.jp/ebj/tag_genre/smallgenre2002/page{0}/".format(i+1)
            # if i == 1:
            #     break
            yield scrapy.Request(response.urljoin(target_link))

        for link in total_links:
            yield scrapy.Request(response.urljoin(link), self.parse_element)

    def parse_element(self, response):
        item = getElement(response)
        writeElement(self, item)
        createCsv(self, 'full', 'girl')
        self.count += 1
