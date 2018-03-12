# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    birthday = scrapy.Field()


class PlayerDataItem(scrapy.Item):
    name = scrapy.Field()
    g = scrapy.Field()
    pts = scrapy.Field()
    trb = scrapy.Field()
    ast = scrapy.Field()
    fg = scrapy.Field()
    fg3 = scrapy.Field()
    ft = scrapy.Field()
    efg = scrapy.Field()
    per = scrapy.Field()
    ws = scrapy.Field()