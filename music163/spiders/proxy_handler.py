# coding: utf-8
import logging
import time

import requests
class ProxyHandler():

    @staticmethod
    def random_get():
        # return "http://127.0.0.1:12759"

        db_url = "http://127.0.0.1:5010/get/"

        while True:
            rsp = requests.get(db_url)
            host = rsp.text
            if host == "":
                time.sleep(10)
                logging.error("no proxy")
                continue
            else:
                tmp_proxy = 'http://' + host
                return tmp_proxy

    @staticmethod
    def delete_proxy(proxy):
        logging.info(msg="delete proxy: {}".format(proxy))
        if proxy.startswith("http"):
            proxy = proxy[7:]
        url = "http://127.0.0.1:5010/delete/?proxy={}"
        requests.get(url.format(proxy))