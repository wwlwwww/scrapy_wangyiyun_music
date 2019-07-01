# -*-coding:utf-8-*-
import json
import logging
import socket
from json import JSONDecodeError
from urllib.parse import urlencode

import scrapy
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, ChunkedEncodingError, ConnectionError
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import music163.api.api as api
from music163 import items
from music163.spiders.proxy_handler import ProxyHandler
import requests

BASE_URL = "http://music.163.com"


# 遍历artist，获取albums
class artist_spider(scrapy.Spider):
    # 不可重复，spider的名字
    name = 'artist_spider'

    # allowed_domains=["music.163.com"]

    # 遍历歌手，获取album
    def start_requests(self):
        # yield scrapy.Request("http://www.baidu.com", callback=self.parse_baidu)

        # yield self.get_request_albums_by_artist(123)
        # return

        i = 481000
        while i < 1000000:
            yield self.get_request_albums_by_artist(i)
            i = i + 1

    def get_request_albums_by_artist(self, artist_id):
        relative_path, params = api.get_artist_album(artist_id)
        url = api.BASE_URL + relative_path

        csrf_token = ""
        params.update({"csrf_token": csrf_token})
        params = api.encrypted_request(params)
        params = urlencode(params)
        # cookies = {'os': 'android'}
        cookies = {}
        # url = "http://music.163.com/weapi/artist/albums/43650"
        return scrapy.Request(url, callback=self.parse_albums_by_artist, method="POST", headers=api.HEADERS,
                              body=params,
                              cookies=cookies, dont_filter=False)


    def parse_albums_by_artist(self, response):
        # inspect_response(response, self)
        req = response.request
        req.dont_filter = True
        if response.status != 200:
            logging.error("code:{}, url: {}, proxy:{}".format(response.status, response.url, req.meta['proxy']))
            return
        elif response.status == 200:
            if response.body is None or len(response.body) == 0:
                return req
            try:
                res_json = json.loads(response.body)
            except JSONDecodeError as e:
                # print("response.body:[{}]".format(response.body))
                print("response.url:[{}]".format(response.url))
                print("proxy:{}".format(req.meta['proxy']))
                return req
            if res_json.get('code', 404) != 200:
                # invalid id
                # logging.error("error get {}".format(response.url))
                return

            artist_res = items.artist_item()
            artist_res['artist_id'] = res_json.get('artist', {'id': -1}).get('id')
            artist_res['artist_name'] = res_json.get('artist', {'name': '_yiming'}).get('name')
            artist_res['artist_alias'] = '|'.join(res_json.get('artist', {'alias': ['']}).get('alias'))
            artist_res['album_size'] = res_json.get('artist', {'albumSize': -1}).get('albumSize')
            artist_res['music_size'] = res_json.get('artist', {'musicSize': -1}).get('musicSize')

            for i in range(len(res_json.get('hotAlbums', {}))):
                album_res = items.albums_item()
                album_res['artist_id'] = artist_res['artist_id']
                album_res['artist_name'] = artist_res['artist_name']
                album_res['album_id'] = res_json['hotAlbums'][i].get('id', -1)
                album_res['album_name'] = res_json['hotAlbums'][i].get('name', '_yiming')
                album_res['album_comments_id'] = res_json['hotAlbums'][i].get('commentThreadId', '')
                album_res['album_publishTS'] = res_json['hotAlbums'][i].get('publishTime', -1000) // 1000
                album_res['album_company'] = res_json['hotAlbums'][i].get('company', '')
                album_res['album_size'] = res_json['hotAlbums'][i].get('size', -1)
                yield album_res

            # 最后yield artist的
            yield artist_res
        else:
            logging.error(
                "status:{}, url:{}, rsp:{}".format(response.status, response.url, response.body.decode('utf-8')))

    def parse_baidu(self, response):
        print("hello baidu")
