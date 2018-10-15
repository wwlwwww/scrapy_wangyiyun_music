# -*- coding: utf-8 -*-
import wangyiyun
# Scrapy settings for wangyiyun project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wangyiyun'

SPIDER_MODULES = ['wangyiyun.spiders']
NEWSPIDER_MODULE = 'wangyiyun.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wangyiyun (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wangyiyun.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wangyiyun.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wangyiyun.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'wangyiyun.spiders.rotate_useragent.RotateUserAgentMiddleware': 400,
    'wangyiyun.spiders.MyProxyMiddleware.MyProxyMiddleware': 700
}

ITEM_PIPELINES={
    'wangyiyun.pipelines.WangyiyunPipeline':300,
}

# 延时，0.5~1.5 * delay_value
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY=0.5

COOKIES_ENABLED = False

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'wangyiyun'
MONGODB_COLLECTION = 'hot_comments_new3'

CONCURRENT_REQUESTS = 800
CONCURRENT_REQUESTS_PER_DOMAIN = 800


DOWNLOAD_TIMEOUT = 8

FEED_EXPORT_ENCODING = "utf-8"
DUPEFILTER_DEBUG = True
DUPEFILTER_CLASS = "wangyiyun.spiders.MyURLFilter.MyURLFilter"
# LOG_FORMATTER = 'wangyiyun.spiders.PoliteLogFormatter'
