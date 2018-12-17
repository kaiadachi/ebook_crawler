import re
from ebook.items import EbookItem
import pandas as pd

def getElement(response):
    item = EbookItem()
    title = response.xpath("//*[@id='volumeTitle']/span").xpath('string()').extract_first()
    if title:
        item['title'] = title
    else:
        item['title'] = response.xpath("//section[3][@class='LV2']/div[@class='sectionHeader clearfix']/h2").xpath('string()').extract_first()
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
    genru = response.xpath("//span[@itemprop = 'genre']").xpath('string()').extract()
    genru = ("/").join(genru)
    item['genru'] = response.xpath("//p[@class = 'bookGenre']").xpath('string()').extract_first().replace('ジャンル：', '') + genru
    item['urlS'] = response.xpath("//div[@class = 'bookThumbArea']/figure/a/@href").extract_first()
    item['urlC'] = response.url
    item['urlT'] = response.xpath("//ul[@class = 'bookBtns']/li/a/@href").extract_first()
    book_list = response.xpath("//ul[@class = 'bookList']/li").extract()
    item['size'] = len(book_list)
    free = response.xpath("//p[@class = 'campInfo']/strong").xpath('string()').extract_first()
    if free:
        if '無料で読める' in free:
            item['free'] = '無料'
        else:
            item['free'] = '有料'
    else:
        item['free'] = '有料'

    kikan = response.xpath("//p[@class = 'kikan']").xpath('string()').extract_first()
    if kikan != None:
        item['expire'] = kikan.replace("まで", "")
    else:
        item['expire'] = ""

    return item

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

def createCsv(self, free, type):
    try:
        self.data.to_csv('csv/ebook_{0}_{1}.csv'.format(free, type), encoding="Shift_jis")
    except:
        self.data.to_csv('csv/ebook_{0}_{1}.csv'.format(free, type), encoding="cp932")

def getPageNum(response):
    p = response.xpath("//div[@class='sectionContent']/p").xpath('string()').extract_first()
    p = p.split("/")
    total_element = int(re.sub(r'\D', '', p[1]))
    q, mod = divmod(total_element, 25)
    if mod == 0:
        page_num = q
    else:
        page_num = q + 1

    return page_num
