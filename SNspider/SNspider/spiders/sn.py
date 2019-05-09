# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request
from SNspider.settings import KEYWORDS
import json
from SNspider.items import Item


class SnSpider(Spider):
    name = 'sn'
    # 商品详细信息的域名在'suning.cn'
    allowed_domains = ['suning.com', 'suning.cn']
    # 商城关键词搜索页
    start_url = 'https://search.suning.com/{kw}/'
    # 对应关键词的品牌页（参数ct=1表示苏宁自营产品）
    brand_url = 'https://search.suning.com/{kw}/&hf=brand_Name_FacetAll:{brand}&iy=-1&ct=1'
    # 对应品牌的商品列表页
    detail_url = 'https://search.suning.com/emall/searchV1Product.do?keyword={kw}' \
                 '&pg=01&iy=-1&hf=brand_Name_FacetAll:{name}&ct=1' \
                 '&n=1&id=IDENTIFYING&cc=755&paging={pg}&sub=1'

    headers = {
        'authority': 'ds.suning.cn',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }


    def start_requests(self):
        """遍历关键词，请求商城搜索页"""
        for keyword in KEYWORDS:
            yield Request(url=self.start_url.format(kw=keyword), callback=self.parse_brand, meta={'kw': keyword})

    def parse_brand(self, response):
        """遍历关键词的所有品牌，进入品牌页页"""
        kw = response.meta['kw']
        for brand in response.xpath('//li[contains(@class, "s-brand")]')[:10]:
            # 获取品牌名
            name = brand.xpath('./@filter_value').get()
            url = self.brand_url.format(kw=kw, brand=name)
            yield Request(url=url, callback=self.parse_page, meta={'kw': kw, 'brand_name':name})

    def parse_page(self, response):
        """根据品牌商品的数量计算商品列表的页数，进入商品列表页"""
        meta = response.meta
        # 获取商品数量
        totalCount = response.xpath('//input[@id="totalCount"]/@value').get()
        # 计算页数
        totalCount = int(int(totalCount) / 30) + 1
        for page in range(totalCount):
            url = self.detail_url.format(kw=meta['kw'], name=meta['brand_name'], pg=page)
            yield Request(url=url, callback=self.parse_commodity, meta=meta)

    def parse_commodity(self, response):
        """解析商品信息，并构造url获取商品详细的接口"""
        # 接收调用函数传入的参数
        meta = response.meta
        # url_params存放拼接的参数用于请求详情页url
        url_params = []
        # commodities存放商品封面信息,用于传递给详情页
        commodities = []
        # 循环解析商品概要信息
        for commodity in response.xpath('//li[contains(@id, "00")]'):
            # 商品id分为两部分，格式类似与xxx-xxx, '-'前的为活动id,'-'后的为商品id
            temp = commodity.xpath('./@id').get().split('-')
            # 获取店铺名，可用来判断是否是自营
            # shop = commodity.xpath('.//div[@class="store-stock"]/a/text()').get()

            # '0088888888'表示该商品是节日广告
            if temp[0] != '0088888888':
                dic = dict()
                # 商品id
                c_id = temp[1]
                dic['c_id'] = c_id
                # 活动id起始为'0070'的商品用于请求详情页url的参数的拼接格式不同
                if temp[0][:4] == '0070':
                    url_param = str('0' * (18 - len(str(c_id)))) + str(c_id) + '__2_' + temp[0]
                else:
                    url_param = str('0' * (18 - len(str(c_id)))) + str(c_id) + '_'
                # 抓取商品url，标题，评论数，首图url，商店
                dic['pro_website'] = 'http://product.suning.com/{}/{}.html'.format(temp[0], temp[1])
                dic['pro_title'] = ','.join(commodity.xpath('.//div[@class="title-selling-point"]/a/text()').getall()).strip()
                dic['comment'] = commodity.xpath('.//div[@class="info-evaluate"]//i/text()').get(default='新品')
                dic['pro_pic'] = 'http:'+commodity.xpath('.//div[@class="img-block"]//img/@src').get()
                # dic['shop'] = shop
                dic['url2'] = response.url
                url_params.append(url_param)
                commodities.append(dic)

        # 苏宁详情信息api只支持最多拼接20个id的信息，平均每一页有大约30条信息，所以分2次查询详情页消息。
        list_half = ','.join(url_params[:20])
        url1 = 'https://ds.suning.cn/ds/generalForTile/{}-755-2-0000000000-1--'.format(list_half)
        meta['commodities'] = commodities[:20]
        yield Request(url=url1, callback=self.parse_detail, meta=meta, headers=self.headers, dont_filter=False)
        # 一页中符合要求的商品超过20个商品才进行第二次请求详情
        if len(url_params) > 20:
            meta['commodities'] = commodities[20:]
            list_other = ','.join(url_params[20:])
            url2 = 'https://ds.suning.cn/ds/generalForTile/{}-755-2-0000000000-1--'.format(list_other)
            yield Request(url=url2, callback=self.parse_detail, meta=meta, headers=self.headers, dont_filter=False)

    def parse_detail(self, response):
        keyword = response.meta['kw']
        commodities = response.meta['commodities']
        # 商品详情列表，用于和商品封面信息合并
        commodities_detail = []
        # 商品信息合并列表
        totals = []
        item = Item()
        res = json.loads(response.text)
        details = res.get('rs')

        # 获取商品的现价，原价，优惠，折扣金额，折扣百分比
        for detail in details:
            dic = dict()
            price = detail.get('price')
            # refprice = detail.get('refPrice')
            snPrice = detail.get('snPrice')
            if snPrice != "":
                dic['pro_price_old'] = snPrice
            else:
                snPrice = price
            # dic['promotions'] = ','.join(i['simple'] for i in detail.get('promotionList'))
            promotions = detail.get('promotionList')
            if promotions:
                dic['promotions'] = promotions[0].get('simple')
            else:
                dic['promotions'] = ''
            if price == '' or price == '待发布' or '?' in price:
                dic['pro_price_new'] = 0
                dic['offers'] = 0
                dic['discount'] = 1
            else:
                dic['pro_price_new'] = price
                dic['offers'] = round(float(snPrice) - float(price), 2)
                dic['discount'] = round((float(price) / float(snPrice)), 2)
            commodities_detail.append(dic)

        # 合并商品信息
        for i, j in zip(commodities, commodities_detail):
            totals.append(dict(i, **j))

        for total in totals:
            if total['pro_price_new'] != 0 and total['discount'] < 1:
                total['brand_name'] = response.meta['brand_name']
                total.pop('c_id')
                total.pop('comment')
                total.pop('url2')
                for key, value in total.items():
                    item[key] = value
                yield item





