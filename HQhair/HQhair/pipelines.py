# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymongo
from datetime import datetime
from data_clean.data_cleaning import HQhair_app


class HqhairPipeline(object):

    source = 'HQhair'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.source]

    def process_item(self, item, spider):
        url_find = {'pro_website': item['pro_website']}
        data = self.collection.find_one(url_find)
        if data:
            old_offers = data.get('offers')
            if item['offers'] != old_offers:
                print("***************旧数据，价格有所变动，直接删除后插入最新数据***************\n{}".format(item))
                self.collection.delete_one(url_find)
                self.collection.insert(dict(item))
        else:
            print("***************新数据，直接插入***************\n{}".format(item))
            self.collection.insert(dict(item))

    def close_spider(self, spider):
        print('关闭管道')
        HQhair_app.run(self.db, self.source)
        self.client.close()

