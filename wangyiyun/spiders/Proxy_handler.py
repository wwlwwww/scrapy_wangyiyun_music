# coding: utf-8
import logging

import requests
class ProxyHandler():

    @staticmethod
    def random_get():
        db_url = "http://127.0.0.1:5010/get/"
        rep = requests.get(db_url)
        tmp_proxy = 'http://' + rep.text
        logging.info(msg="get proxy: {}".format(tmp_proxy))
        return tmp_proxy

    @staticmethod
    def delete_proxy(proxy):
        logging.info(msg="delete proxy: {}".format(proxy))
        url = "http://127.0.0.1:5010/delete/?proxy={}"
        rep = requests.get(url.format(proxy[7:]))