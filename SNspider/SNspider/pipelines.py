# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
from datetime import datetime, timedelta
import pymongo
from SNspider.settings import KEYWORDS, MONGO_URI, MONGO_DB
from data_clean.data_cleaning import SN_app

class MongoPipeline(object):

    source = '苏宁自营_电子'

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[self.source]

    def process_item(self, item, spider):
        ran_time = random.randint(1, 1800)
        item['create_time'] = (datetime.now() + timedelta(seconds=ran_time)).strftime('%Y-%m-%d %H:%M:%S')
        item['update_time'] = (datetime.now() + timedelta(seconds=ran_time)).strftime('%Y-%m-%d %H:%M:%S')
        item['category_id'] = 5
        item['category_name'] = '电子'
        item['buy_source'] = '苏宁自营'
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
        SN_app.run(self.db, self.source)
        self.client.close()



