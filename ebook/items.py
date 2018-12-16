# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbookItem(scrapy.Item):
    # 漫画タイトル※必須
    title = scrapy.Field()

    # シリーズID※必須
    id = scrapy.Field()

    # ISBN
    isbn = scrapy.Field()

    # 漫画家
    author = scrapy.Field()

    # 原作者
    original= scrapy.Field()

    # 出版社
    company= scrapy.Field()

    # 掲載雑誌
    book= scrapy.Field()

    # ジャンル
    genru = scrapy.Field()

    # 書影URL
    urlS = scrapy.Field()

    # タイトルURL※必須
    urlC = scrapy.Field()

    # 立ち読みURL※必須
    urlT = scrapy.Field()

    # 無料で読める巻数※必須
    size = scrapy.Field()

    # 無料キャンペーン中のタイトルなのか※必須
    free = scrapy.Field()

    # 無料期限
    expire = scrapy.Field()
