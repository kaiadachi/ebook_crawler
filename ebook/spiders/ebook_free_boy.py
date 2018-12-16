# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ebook.items import EbookItem
import re
import pandas as pd

class EbookFreeBoySpider(CrawlSpider):
    name = 'ebook_free_boy'
    allowed_domains = ['www.ebookjapan.jp']
    start_urls = ['https://www.ebookjapan.jp/ebj/free/keyword-books/?uniGenres=10%2C11&genreLabel=人気の無料少年・青年まんが&sort=1']

    def __init__(self):
        self.count = 0
        col = ['漫画タイトル', 'シリーズID', 'ISBN', '漫画家', '原作者', '出版社', '掲載雑誌', 'ジャンル', '書影URL', 'タイトルURL', '立ち読みURL','無料で読める巻数','無料キャンペーン中のタイトルなのか', '無料期限']
        self.data = pd.DataFrame(columns = col)

    def createCsv(self):
        try:
            self.data.to_csv('csv/ebook_free_boy.csv', encoding="Shift_jis")
        except:
            self.data.to_csv('csv/ebook_free_boy.csv', encoding="cp932")

    def writeElement(self, item):
        self.data.at[self.count, '漫画タイトル'] = item['title']
        self.data.at[self.count, 'シリーズID'] = item['id']
        self.data.at[self.count, 'ISBN'] = item['isbn']
        self.data.at[self.count, '漫画家'] = item['author']
        self.data.at[self.count, '原作者'] = item['original']
        self.data.at[self.count, '出版社'] = item['company']
        self.data.at[self.count, '掲載雑誌'] = item['book']
        self.data.at[self.count, 'ジャンル'] = item['genru']
        self.data.at[self.count, '書影URL'] = "https://" + item['urlS']
        self.data.at[self.count, 'タイトルURL'] = item['urlC']
        self.data.at[self.count, '立ち読みURL'] = item['urlT']
        self.data.at[self.count, '無料で読める巻数'] = item['size']
        self.data.at[self.count, '無料キャンペーン中のタイトルなのか'] = item['free']
        self.data.at[self.count, '無料期限'] = item['expire']

    def getPageNum(self, response):
        p = response.xpath("//div[@class='sectionContent']/p").xpath('string()').extract_first()
        p = p.split("/")
        total_element = int(re.sub(r'\D', '', p[1]))
        q, mod = divmod(total_element, 25)
        if mod == 0:
            page_num = q
        else:
            page_num = q + 1

        return page_num

    def parse(self, response):
        page_num = self.getPageNum(response)

        total_links = []
        for i in range(page_num):
            page_links = response.xpath("//p[@class='itemThumb']/a/@href").extract()
            total_links.extend(page_links)
            target_link = "https://www.ebookjapan.jp/ebj/free/keyword-books/page{0}/?uniGenres=10%2C11&genreLabel=人気の無料少年・青年まんが&sort=1".format(i+1)
            if i == 3:
                break
            yield scrapy.Request(response.urljoin(target_link))

        for link in total_links:
            yield scrapy.Request(response.urljoin(link), self.parse_element)

    def parse_element(self, response):
        item = EbookItem()
        item['title'] = response.xpath("//*[@id='volumeTitle']/span").xpath('string()').extract_first()
        item['id'] = response.url.split("/")[4]
        isbn = response.xpath("//span[@class = 'subCatch1']").xpath('string()').extract_first()
        if isbn != None:
            isbn = isbn.replace("冊を配信中", "")
            item['isbn'] = isbn
        else:
            item['isbn'] = 'None'

        author_info = response.xpath("//p[@class = 'bookAuthor']").xpath('string()').extract_first()
        if "原作：" in author_info:
            author_info = author_info.replace("原作：", "/")
            author_infos = author_info.split("/")
            item['author'] = author_infos[0]
            item['original'] = author_infos[1]
        else:
            item['author'] = author_info
            item['original'] = ''

        item['company'] = response.xpath("//p[@class = 'bookPublisher']").xpath('string()').extract_first()
        item['book'] = response.xpath("//div[@class = 'detailTable']//li[5]//a").xpath('string()').extract_first()
        item['genru'] = response.xpath("//p[@class = 'bookGenre']").xpath('string()').extract_first().replace('ジャンル：', '')
        item['urlS'] = response.xpath("//div[@class = 'bookThumbArea']/figure/a/@href").extract_first()
        item['urlC'] = response.url
        item['urlT'] = response.xpath("//ul[@class = 'bookBtns']/li/a/@href").extract_first()
        book_list = response.xpath("//ul[@class = 'bookList']/li").extract()
        item['size'] = len(book_list)
        free = response.xpath("//div[@class = 'sectionHeader clearfix']/h2").xpath('string()').extract_first()
        if '無料で読める' in free:
            item['free'] = '無料'
        else:
            item['free'] = '有料'

        kikan = response.xpath("//p[@class = 'kikan']").xpath('string()').extract_first()
        if kikan != None:
            item['expire'] = kikan.replace("まで", "")
        else:
            item['expire'] = ""


        self.writeElement(item)
        self.createCsv()
        self.count += 1
