# coding: utf-8
import logging
import random

import requests
import twisted
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from twisted.internet.error import T

from music163.spiders.proxy_handler import ProxyHandler


class proxy_mid(object):
    # qc_proxy = "http://118.24.154.108:8899"
    db_url = "http://127.0.0.1:5010/get/"
    delete_url = "http://127.0.0.1:5010/delete/?proxy={}"

    def process_request(self, request, spider):
        rd = random.randint(1,50)
        if rd < 10:
            return

        tmp_proxy = ProxyHandler.random_get()
        request.meta['proxy'] = tmp_proxy

    # def process_response(self, request, response, spider):
    #     if response.status != 200:
    #         tmp_proxy = ProxyHandler.random_get()
    #         request.meta['proxy'] = tmp_proxy
    #         return request
    #
    #     return response
    #
    def process_exception(self, request, exception, spider):

        if isinstance(exception, twisted.internet.error.ConnectError) or \
                isinstance(exception, twisted.internet.error.TCPTimedOutError) or \
                isinstance(exception, twisted.internet.error.TimeoutError) or \
                isinstance(exception, twisted.internet.error.ConnectionDone) or \
                isinstance(exception, twisted.internet.error.ConnectionRefusedError) or \
                isinstance(exception, twisted.internet.error.ConnectionLost) or \
                isinstance(exception, twisted.internet.error.ConnectionClosed) or \
                isinstance(exception, twisted.internet.error.ConnectionAborted) or \
                isinstance(exception, twisted.web._newclient.ResponseNeverReceived):

            logging.error("download_mids, exception: ")
            print(exception)
            request.meta['proxy'] = ""
            request.dont_filter = True
            return request
        else:
            logging.error("download_mids, uncatched exception: ")
            print(exception)
            request.meta['proxy'] = ""
            request.dont_filter = True
            return request


class ua_mid(object):

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            # print "********Current UserAgent:%s************" % UA
            request.headers['User-Agent'] = ua

    user_agent_list = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)',
        'Mozilla/5.0 (Linux; Android 8.1; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.143 Crosswalk/24.53.595.0 XWEB/358 MMWEBSDK/23 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/4G Language/zh_CN',
        'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
        'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Redmi 6 Pro Build/OPM1.171019.019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.8.7',
        'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Redmi Note 4X Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 7.1.2; zh-CN; Redmi 5 Plus Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; Redmi Note 4X Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1',
        'Mozilla/5.0 (Linux; Android 8.1.0; Redmi 6 Pro Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.12 baiduboxapp/10.12.0.12 (Baidu; P1 8.1.0)',
        'Mozilla/5.0 (Linux; Android 8.1; Redmi Note 5 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.10 baiduboxapp/10.10.0.12 (Baidu; P1 8.1.0)',
        'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Redmi 6 Pro Build/OPM1.171019.019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.2',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iPhone 6s; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.3.0 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 wxwork/2.5.8 MicroMessenger/6.3.22 Language/zh',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B100 Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1',
    ]


if __name__ == "__main__":
    db_url = "http://127.0.0.1:5010/get/"
    rep = requests.get(db_url)
    print(rep.text)
    proxy = 'http://' + rep.text
    print(proxy)
