# -*- coding: utf-8 -*-
import datetime

from scrapy import Spider, Request
from JuMei.items import Item


class JumeiSpider(Spider):
    name = 'jumei'
    keywords = {'化妆品': 4, '食品保健': 8, '母婴健康': 7}
    # keywords = {'化妆品': 4}
    allowed_domains = ['jumei.com']
    # 搜索页url
    start_url = 'http://search.jumei.com/?filter=0-11-1&search={key}'

    cookies = {
        'default_site_25': 'gz',
        'first_visit': '1',
        'first_visit_time': '1554889982',
        'jml14': '2',
        'jmdl14': '2',
        '__utmz': '1.1554889985.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'jumei_index_tab': '1554889983',
        'user_history': 'eNptUMFugzAM%2FZccpwpiQqHwK82E0sRq2RqIQnLoEP8%2BW%2BsBaVys5%2FdsP9ur%2BMbXIvpVOOhkDTLUqpYA1Y8V%2FQG3nYQzyYj%2BunLnYc1JpFdAltA8KbMm4X2OXBzi7LJNRL7RMDqi371E5%2Fik%2FJFS6HWpyzGhL76yx7Gws9flP7PikTx7LI85pmEynn11vlRdp3ONyjG%2BKcZA%2BAxW6tw403CEVueubSqOYEHK%2Bwfv4MbFznlK6IYQR8sT4dLtBCKaQu2OiBjIfhmm7G8YSZZcTdcPtLXHaS%2BBOrdi%2B6S3%2FI06%2FLzatl%2BX13x3',
        'device_platform': 'other',
        'guide_download_show': '1',
        'has_download': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2216a071e26bf2b0-0eb8863b13c0cd-7a1437-2073600-16a071e26c016c%22%7D',
        'from_source': 'browser',
        'abt52': 'new',
        'abt62': 'old',
        'PHPSESSID': 'c7519inkbgfsla6cre4ht1cp93',
        'cookie_uid': '15549700983420596791',
        'referer_site': 'www.jumeiglobal.com',
        '_adwc': '265569940',
        'route': '4203da21044efb29d11daf69d8eac8ff',
        '_adwp': '265569940.0355875440.1554889984.1554896545.1554970098.3',
        '__utma': '1.2012326795.1554889985.1554896545.1554970098.3',
        '__utmc': '1',
        'session_id': '5caef5f52494f4545',
        'account': 'tMJozwGHi0Jzz7u25MswQj3Rj%2FTw1UZneODU0mSbZU4LUl7S8M2pIm9vFTbc%2FTIoVPebMKGILHQ%2FNwmCiMMGdApMERhxfL3DVBfaKYO3EWmiXO%2Fz0zPkqVDHxTY6YzX74kv5T7zAy5%2BxL%2FKLT3xdgiyRiVKNzbLoV5ISZLYLhFRBw5S%2Fbny3g5jb5uz%2BGqBbTRe4PPfNZDELa9Ta3v2UUg%3D%3D',
        'tk': '00d6251f01b7752aaf6f7dc3128985a1755a5a16',
        'uid': '496047126',
        'v_uid': '496047126',
        'nickname': 'JM1kRCuOaVUA0',
        'token': 'g3SZqnMUYf0sre8jTX90efh1thksmNn2CMazYGx8Ppqjic4bQ5vyVtpiQm741HSTRuFxXRv65ZNPDwdAzEgOclIkC273BHb9WloDWdJKBoVFI6EwKJaGyuULLAKwPNOD',
        'session': 'VSjYqQbu1rgwBhc9lPXvnx6oaBMVKDZA',
        'privilege_group': '0',
        'register_time': '1554970337',
        'cookie_ver': '1',
        'login_mode': 'pc_register_login',
        'new_signup': 'null',
        'm_vid': '496047126',
        '__xsptplus428': '428.4.1554970098.1554970365.2%233%7Cwww.jumeiglobal.com%7C%7C%7C%7C%23%23yjmz3bveGK2rYtuY2dOFQsvp_nTbXJXh%23',
        'Hm_lvt_884477732c15fb2f2416fb892282394b': '1554889985,1554897394,1554970099,1554970366',
        '_adwb': '251407876',
        '_adwr': '251407876%23http%253A%252F%252Fmall.jumei.com%252F%253Ffrom%253DGlobal_top_nav_fresh_mall_tab',
        'cs_logined_uid': '496047126',
        'search_user_status': '1',
        'b5164fbdf0a4526876438e688f5e4130': '1',
        'isSellCheck': '0',
        'search_start_time': '1554970421525',
        '__utmb': '1.9.9.1554970337632',
        'Hm_lpvt_884477732c15fb2f2416fb892282394b': '1554970422',
    }
    # 分类ID
    category = {
        "服装": 3, "美妆": 4, "电子": 5, "家居": 6, "母婴": 7, "食物": 8, "运动": 9,
        "个户": 10, "旅游": 11, "汽车": 12, "其他": 13
    }
    # 分类字典键值翻转
    rever_category = {v: k for k, v in category.items()}

    # 抓取字段
    field_list = ['brand_name', 'pro_title', 'pro_price_new', 'pro_price_old', 'pro_website', 'pro_pic', 'category_id',
                  'category_name', 'offers', 'discount']

    def start_requests(self):
        """商城搜索url拼接搜索关键字"""
        for key in self.keywords.keys():
            url = self.start_url.format(key=key)
            yield Request(url=url, callback=self.parse_index, cookies=self.cookies, meta={'key': self.keywords[key]})

    def parse_index(self, response):
        """解析搜索页，根据品牌url细分"""
        key = response.meta['key']
        contents = response.css('#filter_brand>ul>li')
        for content in contents:
            # 获取品牌名
            brand_name = content.attrib['title']
            # 获取品牌url
            url = content.css('a').attrib['href']
            yield Request(url=url, callback=self.parse_detail, cookies=self.cookies,
                          meta={'key': key, 'brand_name': brand_name})

    def parse_detail(self, response):
        """解析品牌搜索页"""
        meta = response.meta
        category_id = meta.get('key')
        # 根据分类id获取分类名
        category_name = self.rever_category.get(category_id)
        brand_name = meta.get('brand_name')

        commoditys = response.css('.hai')
        for commodity in commoditys:
            # 判断是否抢光
            qg = commodity.css('.qiang_guang')
            qg2 = commodity.css('.search_pl::text').get()
            if qg == [] and qg2 != '已抢光':
                # 若没抢光，判断是否自营
                if '非自营' not in commodity.css('strong::text').get():
                    # 商品折扣价
                    pro_price_new = commodity.css('.search_list_price span::text').get()
                    # 商品原价
                    pro_price_old = commodity.css('.search_list_price del::text').re_first('¥(\d+)', default=0)
                    # 原价为0代表抢光
                    if float(pro_price_new) != 0 and float(pro_price_old) != 0:
                        # 取折扣前2位
                        discount = '%.2f' % (float(pro_price_new) / float(pro_price_old))
                        item = Item()
                        # 商品标题
                        pro_title = commodity.css('.s_l_name a::text').get().strip()
                        # 商品url
                        pro_website = commodity.css('a::attr(href)').get()
                        # 折扣差价
                        offers = int(float(pro_price_old) - float(pro_price_new))
                        # 首图url
                        pro_pic = commodity.css('.s_l_pic img::attr(src)').get()
                        # item字段赋值
                        for field in self.field_list:
                            try:
                                item[field] = eval(field)
                            except:
                                print('字段不存在:', field)
                        yield item
        # 判断下一页
        next = response.css('a.enable.next::attr(href)').get()
        if next is not None:
            yield Request(url=next, callback=self.parse_detail, cookies=self.cookies, meta=meta)
