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
from music163.spiders import proxy_handler
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

        i = 1
        while i < 2000000:
            yield self.get_request_albums_by_artist(i)
            i = i + 1
            if i % 10000 == 0:
                print("done i: {}".format(i))

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
            proxy_handler.delete_proxy(req.meta['proxy'][7:])
            return req
        else:
            # 请求成功
            if response.body is None or len(response.body) == 0:
                proxy_handler.delete_proxy(req.meta['proxy'][7:])
                return req
            try:
                res_json = json.loads(response.body)
            except JSONDecodeError as e:
                # print("response.body:[{}]".format(response.body))
                print("response.url:[{}]".format(response.url))
                print("proxy:{}".format(req.meta['proxy']))
                proxy_handler.delete_proxy(req.meta['proxy'][7:])
                return req

            artist_res = items.artist_item()
            content_code = res_json.get('code', -1)
            if content_code == 404:
                artist_res['artist_id'] = self.get_artistID_fromURL(response.url)
                artist_res['artist_name'] = ""
                artist_res['artist_alias'] = ""
                artist_res['album_size'] = -1
                artist_res['music_size'] = -1
                return artist_res

            if content_code == -460:
                proxy = req.meta['proxy']
                proxy_handler.delete_proxy(req.meta['proxy'][7:])
                return req

            if content_code != 200:
                # invalid id
                logging.error("error code: {}, url: {}".format(content_code, response.url))
                logging.error("error get {}".format(response.url))
                return req
            else:
                # 成功
                artist_res['artist_id'] = res_json.get('artist', {'id': -1}).get('id')
                artist_res['artist_name'] = res_json.get('artist', {'name': '_yiming'}).get('name')
                artist_res['artist_alias'] = '|'.join(res_json.get('artist', {'alias': ['']}).get('alias'))
                artist_res['album_size'] = res_json.get('artist', {'albumSize': -1}).get('albumSize')
                artist_res['music_size'] = res_json.get('artist', {'musicSize': -1}).get('musicSize')
                yield artist_res

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

    # http://music.163.com/weapi/v1/album/
    # http://music.163.com/weapi/artist/albums/
    def get_artistID_fromURL(self, url):
        ws = url.split('/')
        logging.info("url:{}, uid:{}".format(url, ws[-1]))
        uid = int(ws[-1])
        logging.info("url:{}, uid:{}".format(url, uid))
        return uid


