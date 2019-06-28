# coding: utf-8
import logging

import requests
from music163.spiders.Proxy_handler import ProxyHandler

class MyProxyMiddleware(object):
    db_url = "http://127.0.0.1:5010/get/"
    delete_url = "http://127.0.0.1:5010/delete/?proxy={}"

    def process_request(self, request, spider):
        # rep = requests.get(self.db_url)
        # tmp_proxy = 'http://' + rep.text
        # print('get proxy:', tmp_proxy)
        # tmp_proxy = ProxyHandler.random_get()
        tmp_proxy = "http://127.0.0.1:12759"
        request.meta['proxy'] = tmp_proxy

    # def process_response(self, request, response, spider):
    #     if response.status != 200:
    #         tmp_proxy = ProxyHandler.random_get()
    #         request.meta['proxy'] = tmp_proxy
    #         return request
    #
    #     return response
    #
    # def process_exception(self, request, exception, spider):
    #     logging.info("download {} exception, retry...: {}, proxy: {}".format(request.url, repr(exception), request.meta['proxy']))
    #     ProxyHandler.delete_proxy(request.meta['proxy'])
    #     tmp_proxy = ProxyHandler.random_get()
    #     request.meta['proxy'] = tmp_proxy
    #     return request




if __name__ == "__main__":
    db_url = "http://127.0.0.1:5010/get/"
    rep = requests.get(db_url)
    print(rep.text)
    proxy = 'http://' + rep.text
    print(proxy)