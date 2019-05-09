# -*- coding: utf-8 -*-
import json
import re

import jsonpath
from scrapy import Spider, Request
import string
from pdd_spider.items import Item


class PddSpider(Spider):
    name = 'pdd'
    allowed_domains = ['yangkeduo.com']
    # 品牌管首页
    start_url = 'https://mobile.yangkeduo.com/sjs_brand_list.html'
    # 分类的品牌url接口
    brand_url = 'https://mobile.yangkeduo.com/proxy/api/api/gentian/brand_list?' \
                'resource_type=15&brand_type=0&head_char={char}&tab_id={tab}'
    # 品牌对应的商品接口
    brand_goods = 'https://mobile.yangkeduo.com/proxy/api/api/gentian/brand_goods?' \
                  'resource_type=15&brand_id={id}&size={size}&page={page}'
    # 要抓取的字段
    field_list = ['brand_name', 'pro_title', 'pro_price_new', 'pro_price_old', 'pro_website', 'pro_pic', 'category_id',
                  'category_name', 'offers', 'discount', 'display_label']
    # 商品接口最大限制条数
    max_size = 300

    def start_requests(self):
        """起始url"""
        yield Request(url=self.start_url, callback=self.parse_table)

    def parse_table(self, response):
        """从首页获取品牌的分类ID， 根据id和品牌首字母获取品牌信息"""
        tab_ids = re.findall(r'{"tab_id":(\d+),"tab":"(.*?)"', response.text)[1:13]
        for tab_id in tab_ids:
            for i in string.ascii_uppercase:
                yield Request(url=self.brand_url.format(char=i, tab=tab_id[0]),
                              callback=self.parse_brand,
                              meta={'tab_id': tab_id})

    def parse_brand(self, response):
        """获取品牌id和品牌名，根据id获取品牌对应的商品接口"""
        tab_id = response.meta.get('tab_id')
        brands_json = json.loads(response.text)
        for brand_info in brands_json.get('list'):
            brand_id = brand_info.get('id')
            brand_name = brand_info.get('name')
            # print(brand_id, brand_name)
            yield Request(url=self.brand_goods.format(id=brand_id, size=self.max_size, page=1),
                          meta={'brand_name': brand_name, 'brand_id': brand_id, 'tab_id': tab_id},
                          callback=self.parse_goods)

    def parse_goods(self, response):
        """解析商品接口，存入item"""
        tab_id = response.meta.get('tab_id')
        brand_name = response.meta.get('brand_name')
        brand_id = response.meta.get('brand_id')
        goods_json = json.loads(response.text)
        size = goods_json.get('size')
        for goods_info in goods_json.get('list'):
            pro_price_new = goods_info.get('group').get('price')
            pro_price_old = goods_info.get('normal_price')
            if pro_price_new and pro_price_old:
                pro_price_new = round(float(pro_price_new) / 100, 1)
                pro_price_old = round(float(pro_price_old) / 100, 1)
                pro_website = 'https://mobile.yangkeduo.com/' + goods_info.get('link_url')
                pro_title = goods_info.get('goods_name')
                pro_pic = goods_info.get('hd_thumb_url')
                display_label = goods_info.get('display_label')
                offers = round(pro_price_old - pro_price_new, 1)
                discount = round(pro_price_new / pro_price_old, 2)
                category_id = tab_id[0]
                category_name = tab_id[1]
                item = Item()
                for field in self.field_list:
                    item[field] = eval(field)
                yield item

        # 判断品牌商品是否大于300，如果大于则翻页
        page = int(re.search(r'page=(\d+)', response.url).group(1))
        if int(size) > page*300:
            page += 1
            url = self.brand_goods.format(id=brand_id, size=self.max_size, page=page)
            yield Request(url=url,
                          meta={'brand_name': brand_name, 'brand_id': brand_id, 'tab_id': tab_id},
                          callback=self.parse_goods)
