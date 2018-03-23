# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QidianXiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fiction_name = scrapy.Field() #小说名字
    chapter_name = scrapy.Field() #章节名字
    content = scrapy.Field() #章节内容
