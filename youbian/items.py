# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoubianItem(scrapy.Item):
    code = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()




