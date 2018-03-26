# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SytrackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tracking_number = scrapy.Field()
    info_content = scrapy.Field()
    info_date = scrapy.Field()
    j = scrapy.Field()

