# -*- coding: utf-8 -*-
import datetime
import random

from scrapy import Spider, Request
import re
from HQhair.items import Item


class HqhairSpider(Spider):
    name = 'hqhair'
    allowed_domains = ['hqhair.com']
    start_url = 'https://www.hqhair.com/health-beauty/offers/discount-code.list'
    brand_url = start_url + '?facetFilters=en_brand_content:{}&pageNumber={}'

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse_list)

    def parse_list(self, response):
        discount = response.css('.banner-title-style-1::text').re_first('(\d+)%')
        # print(discount)
        discount = 1-float(discount)*0.01
        brand_names = response.xpath('//div[@class="facets_listPanel js-facet-category js-facet-en_brand_content"]/ul//li')
        for brand in brand_names:
            brand_name = brand.xpath('.//span[@class="facets_listPanelListItemDisplayText"]/text()').get()
            en_brand_content = brand.xpath('.//input[@data-facet-category="en_brand_content"]/@value').get()
            if en_brand_content:
                en_brand_content = en_brand_content.split(':')[1]
                brand_url = self.brand_url.format(en_brand_content, 1)
                yield Request(url=brand_url, callback=self.parse_products, meta={'brand_name': brand_name, 'page': 1,
                                                                                 'en_brand_content': en_brand_content,
                                                                                 'discount': discount})

    def parse_products(self, response):
        # print(response.url)
        if "Sorry we couldn't find any results matching" in response.text:
            return
        page = response.meta['page']
        en_brand_content = response.meta['en_brand_content']
        products = response.xpath('//div[contains(@class, "item item-health-beauty")]')
        brand_name = response.meta['brand_name']
        if response.meta.get('discount'):
            discount = response.meta['discount']
        else:
            discount = 0.85
        for product in products:
            item = Item()
            pro_website = product.xpath('.//div[@data-track="product-image"]/a/@href').get()
            pro_pic = product.xpath('.//div[@data-track="product-image"]/a/img/@src').get()
            pro_price_new = product.xpath('.//div[@class="price"]/span/text()').get()
            try:
                pro_price_new = re.sub('[£,]', '', pro_price_new)
                pro_price_new = int(float(pro_price_new)*7.5)
                pro_price_old = int(pro_price_new / discount)
            except Exception as e:
                pro_price_old = int(pro_price_new)
                print('价格错误', pro_price_new, e)
            offers = pro_price_old - pro_price_new
            pro_title = product.xpath('.//p[@class="product-name"]/a/text()').get().strip()
            ran_time = random.randint(1, 1800)
            create_time = (datetime.datetime.now() + datetime.timedelta(seconds=ran_time)).strftime('%Y-%m-%d %H:%M:%S')
            update_time = create_time
            category_id = 4
            category_name = '化妆品'
            buy_source = 'HQhair'
            for file in item.fields:
                item[file] = eval(file)
            yield item

        nextNavigation = response.xpath('.//a[@data-e2e-element="nextNavigation"]/@disabled').get()
        if nextNavigation is None:
            page = page+1
            url = self.brand_url.format(en_brand_content, page)
            yield Request(url=url, callback=self.parse_products, meta={'brand_name': brand_name, 'page': page,
                                                                       'en_brand_content': en_brand_content})






