#-*-coding:utf-8-*-
import logging
import socket
from json import JSONDecodeError

from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, ChunkedEncodingError, ConnectionError
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors  import LinkExtractor
from wangyiyun.items import WangyiyunItem
from scrapy.http import FormRequest
from scrapy.exceptions import DropItem
from scrapy.shell import inspect_response
from wangyiyun.spiders.Proxy_handler import ProxyHandler
import binascii

import requests
import json
import os
import base64
from Crypto.Cipher import AES


class MusicSpider(CrawlSpider):
    name = 'wangyiyun'
    allowed_domains=["music.163.com"]
    start_urls=[
                "http://music.163.com/discover/artist",
                "http://music.163.com/artist?id=91725",
                "http://music.163.com/song?id=411214279",
                "http://music.163.com/song?id=186016",
    ]
                # 'http://music.163.com/artist?id=5770']
    # start_urls = ['http://music.163.com/artist?id=5770']

    rules = [Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+'))),
             Rule(LinkExtractor(allow=(r'/artist\?id=\d+'))),
             Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+&initial=\d+'))),
             Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+'))),
             Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+&limit=\d+&offset=\d+'))),
             Rule(LinkExtractor(allow=(r'/album\?id=\d+'))),
             Rule(LinkExtractor(allow=(r'/song\?id=\d+')),callback="parse_song")]

    def parse_song(self,response):
        # inspect shell
        # inspect_response(response, self)

        sel=Selector(response)
        # 部分网页正文为空（禁止js的时候，如 http://music.163.com/#/song?id=32548815）
        nodes = sel.xpath("//div[@class='g-mn4']")
        if len(nodes) < 1:
            return

        item=WangyiyunItem()
        item['music_name']=sel.xpath('//em[@class="f-ff2"]/text()').extract()[0]
        artist_nodes = sel.xpath('//p[@class="des s-fc4"]/span/a/text()')
        if len(artist_nodes)>0:
            item['artist'] = artist_nodes.extract()[0]
        else:
            item['artist'] = sel.xpath('//p[@class="des s-fc4"]/span/span/text()').extract()[0]
        item['album']=sel.xpath('//p[@class="des s-fc4"]/a/text()').extract()[0]

        # comments_api='http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+response.url[29:]+'/?csrf_token='
        song_id = response.url[29:]
        retry_time = 0
        while True:
            try:
                cur_proxy = ProxyHandler.random_get()
                rep = self.get_comments_response(song_id, cur_proxy)
                item['hot_comments']=self.get_hot_comments(rep)
                item['total_comments_cnt'] = self.get_comments_cnt(rep)
                item['song_url']=response.url

                if item['total_comments_cnt'] > 200 and len(item['hot_comments'])>0:
                    return item
                else:
                    return
                # raise DropItem("not hot song")
            # except (requests.Timeout, json.JSONDecodeError, requests.ConnectTimeout, socket.timeout, ProxyError, ConnectionError, requests.ReadTimeout, ) as e:
            #     ProxyHandler.delete_proxy(cur_proxy)
            #     logging.warning("comments get exception: {}".format(retry_time))
            #     retry_time += 1
            #     if retry_time>3:
            #         return
            except (ConnectTimeout, ReadTimeout, ProxyError, ChunkedEncodingError, ConnectionError) as e:
                ProxyHandler.delete_proxy(cur_proxy)

            except (JSONDecodeError, ) as e:
                return
            except (Exception) as e:
                logging.warning("comments get exception: {}, song url: {}".format(retry_time, response.url))
                logging.warning("exception detail: {}".format(repr(e)))
                retry_time += 1
                if retry_time > 3:
                    return


    #以下为评论区API，来自知乎
    #知乎链接：http://www.zhihu.com/question/36081767/answer/65820705
    def aesEncrypt(self,text, secKey):
        pad = 16 - len(text) % 16
        if not isinstance(text, str):
            text = text.decode("utf8")
        text = text + (pad * chr(pad))
        secKey = bytes(secKey, encoding="utf8")
        encryptor = AES.new(secKey, 2, b'0102030405060708')
        text = bytes(text, encoding="utf8")
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext


    def rsaEncrypt(self,text, pubKey, modulus):
        text = text[::-1]
        text = bytes(text, encoding="utf8")
        tmp = int(binascii.b2a_hex(text), 16)
        rs = tmp ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(xx)[2:]), os.urandom(size))))[0:16]

    def get_req(self,url):
        headers = {
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36'
        }
        text = {
            'username': '1223292709@qq.com',
            'password': 'WML13938182619',
            'rememberLogin': 'true'
        }
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(self.aesEncrypt(text, nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        try:
            req = requests.post(url, headers=headers, data=data,timeout=1)
            print('API获取成功')
            return req
        except Exception as e:
            print('API获取失败')
            print(e)
            return -1

    def get_comments_response(self, music_id, tmp_proxy, offset=0, total='false', limit=100):
        action = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}/?rid=R_SO_4_{}&\
                            offset={}&total={}&limit={}'.format(music_id, music_id, offset, total, limit)
        headers = {
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36'
        }

        # Proxy
        proxy = {"http": tmp_proxy}
        rep = requests.get(action, headers=headers, timeout=(2, 8), proxies=proxy)
        # rep = requests.get(action, headers=headers)
        return rep

    def get_hot_comments(self, rep):
        comments_list = []
        comments = rep.json()['hotComments']
        for comment in comments:
            tmp_dict = {}
            tmp_dict['nickname'] = comment['user']['nickname']
            tmp_dict['star_cnt'] = comment['likedCount']
            tmp_dict['content'] = comment['content']
            if len(comment['beReplied'])>0:
                tmp_dict['quote'] = comment['beReplied'][0]['content']
            # log.msg(tmp_dict, _level=log.INFO)
            comments_list.append(tmp_dict)

        return comments_list

    def get_comments_cnt(self, req):
        return req.json()['total']

if __name__=="__main__":
    pass



