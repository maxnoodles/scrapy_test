# -*- coding: utf-8 -*-

# Scrapy settings for HQhair project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os

BOT_NAME = 'HQhair'

SPIDER_MODULES = ['HQhair.spiders']
NEWSPIDER_MODULE = 'HQhair.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'HQhair (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Host': 'www.hqhair.com',
    'Cookie': 'csrf_token=12124243661416717674; JSESSIONID=7129EC4B7076910CFB68A5F646FFB427; '
              'chumewe_user=22a48946-4af4-4931-9aa9-a04bd6ffba62; chumewe_sess=395d27e6-5315-4bb0-88fc-8ba5b1bfd688; '
              'locale_V6=en_GB; NSC_mc_wtsw_efgbvmu_xfctsw_81_J=ffffffff09031f2a45525d5f4f58455e445a4a423661; '
              '_gcl_au=1.1.979795539.1554367321; gaVisitId=id5zvm7a9vaq; _ga=GA1.2.512555835.1554367322; '
              '_gid=GA1.2.644000669.1554367322; '
              'ADRUM=s=1554368318558&r=https%3A%2F%2Fwww.hqhair.com%2Fhealth-beauty%2Foffers%2Fdiscount-code.list%3F0'
              '; LPVID=A1NWZhM2YwZjhhZWM2M2Jk; LPSID-64479670=ZLANTnYeTn-qOxRCv5gv9A; _dc_gtm_UA-59323-83=1; '
              '_dc_gtm_UA-56952874-1=1 '
}
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'HQhair.middlewares.HqhairSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'HQhair.middlewares.UAMiddleware': 101,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
       'HQhair.pipelines.HqhairPipeline': 300,
    }


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGO_URI = '127.0.0.1'
MONGO_DB = 'D88'

LOG_ENABLE = True
today = datetime.date.today()
dirs = os.getcwd() + '/log/'
if not os.path.exists(dirs):
    os.makedirs(dirs)
LOG_FILE = f'{dirs}/{today}.log'
LOG_LEVEL = 'INFO'
