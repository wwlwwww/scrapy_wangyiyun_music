#-*-coding:utf-8-*-
import json
import logging
import socket
from json import JSONDecodeError
from urllib.parse import urlencode

import scrapy
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, ChunkedEncodingError, ConnectionError
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors  import LinkExtractor

import wangyiyun.api.api as api
from wangyiyun import items
from wangyiyun.spiders.Proxy_handler import ProxyHandler
import requests

BASE_URL = "http://music.163.com"

# 遍历artist，获取albums
class Artist_spider(scrapy.Spider):
    # 不可重复，spider的名字
    name = 'artist_spider'
    allowed_domains=["music.163.com"]

    # start_urls=[
    #             "http://music.163.com/discover/artist",
    #             "http://music.163.com/artist?id=91725",
    #             "http://music.163.com/artist?id=1012032",
    # ]

    # rules = [Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+')), follow=True),
    #          Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+&initial=\d+')), follow=True),
    #          Rule(LinkExtractor(allow=(r'/artist\?id=\d+')), follow=True),
    #          Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+')), follow=True),
    #          Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+&limit=\d+&offset=\d+')), follow=True),
    #          Rule(LinkExtractor(allow=(r'/album\?id=\d+')), callback='pare_song'),
    #          ]
    # 遍历歌手，获取album
    def start_requests(self):
        i = 2116
        yield self.get_request_albums_by_artist(i)

        # while i < 20000000:
            # yield self.get_request_albums_by_artist(i)
            # i = i + 1

    def get_request_albums_by_artist(self, artist_id):
        relative_path, params = api.get_artist_album(artist_id)
        url = api.BASE_URL + relative_path

        csrf_token = ""
        params.update({"csrf_token": csrf_token})
        params = api.encrypted_request(params)
        params = urlencode(params)
        cookies = {'os': 'android'}
        yield scrapy.Request(url, callback=self.parse_albums_by_artist, method="POST", headers=api.HEADERS, body=params,
                             cookies=cookies, dont_filter=True)

    def parse_albums_by_artist(self, response):
        if response.status == 404:
            return

        if response.status == 200:
            inspect_response(response, self)
            res_json = json.loads(response.body)
            artist_res = items.artist_item
            artist_res.artist_id = artist_res.get('artist', {'id': -1}).get('id')
            artist_res.artist_name = artist_res.get('artist', {'name': '_yiming'}).get('name')
            artist_res.artist_alias = '|'.join(artist_res.get('artist', {'alias': ['']}).get('alias'))
            artist_res.album_size = artist_res.get('artist', {'albumSize': -1}).get('albumSize')
            artist_res.music_size = artist_res.get('artist', {'musicSize': -1}).get('musicSize')

            for i in range(len(res_json.get('hotAlbums', {}))):
                album_res = items.albums_item
                album_res.artist_id = artist_res.artist_id
                album_res.artist_name = artist_res.artist_name
                album_res.album_id = res_json['hotAlbums'][i].get('id', -1)
                album_res.album_name = res_json['hotAlbums'][i].get('name', '_yiming')
                album_res.album_comments_id = res_json['hotAlbums'][i].get('commentThreadId', '')
                album_res.album_publishTS = res_json['hotAlbums'][i].get('publishTime', -1000) / 1000
                album_res.album_company = res_json['hotAlbums'][i].get('company', '')
                album_res.album_size = res_json['hotAlbums'][i].get('size', -1)
                yield album_res

            # 最后yield artist的
            yield artist_res

        logging.ERROR("status:{}, url:{}, rsp:{}".format(response.status, response.url, response.body.decode('utf-8')))





