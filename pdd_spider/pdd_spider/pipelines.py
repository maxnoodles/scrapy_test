# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
from datetime import datetime, timedelta

from pymongo import MongoClient
from data_clean.data_cleaning import pinduoduo_app

class PddSpiderPipeline(object):

    source = 'pinduoduo'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MOGNO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(f'mongodb://{self.mongo_uri}/')
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.source]

    def process_item(self, item, spider):
        item['buy_source'] = '拼多多'
        ran_time = random.randint(1, 1800)
        item['create_time'] = (datetime.now() + timedelta(seconds=ran_time)).strftime('%Y-%m-%d %H:%M:%S')
        item['update_time'] = (datetime.now() + timedelta(seconds=ran_time)).strftime('%Y-%m-%d %H:%M:%S')

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
        # self.collections.update_one({'pro_website': item['pro_website']}, {'$set': item}, True)

    def close_spider(self, spider):
        print('关闭管道')
        pinduoduo_app.run(self.db, self.source)
        self.client.close()
