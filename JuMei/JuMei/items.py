# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):

    category_id = scrapy.Field()
    category_name = scrapy.Field()
    brand_name = scrapy.Field()
    pro_title = scrapy.Field()
    pro_website = scrapy.Field()
    pro_price_new = scrapy.Field()
    pro_price_old = scrapy.Field()
    offers = scrapy.Field()
    discount = scrapy.Field()
    pro_pic = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    buy_source = scrapy.Field()
