# coding: utf-8
import logging
import os
import random

import redis as redis
import requests

conn = redis.Redis(host='localhost', port=6379, decode_responses=True)

def random_proxy():
    ps = conn.hkeys("useful_proxy")
    if len(ps) == 0:
        logging.error("no proxy")
        return ""
    else:
        return random.choice(ps)

def delete_proxy(hostport):
    conn.hdel("useful_proxy", hostport)
    logging.info("delete proxy:{}".format(hostport))

def xdl_fetch():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    url = "http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20197305829EowQb5/74330bc2fcdd11e6942200163e1a31c0?returnType=1"
    rsp = requests.get(url)
    if rsp.status_code == 200:
        txt = rsp.text
        ps = txt.splitlines()
        if ps.find("ERRORCODE") != -1:
            return ""
        print("ps: {}".format(ps))
        for i in ps:
            r.hset("useful_proxy", i, 1)
            return i