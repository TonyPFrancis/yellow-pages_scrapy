# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class YellowpagesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    business_name1 = Field()
    business_name2 = Field()
    address = Field()
    city = Field()
    zip = Field()
    phone = Field()
    url = Field()
