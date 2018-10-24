#-*-coding:utf-8-*-
import logging
import socket
from json import JSONDecodeError

import scrapy
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, ChunkedEncodingError, ConnectionError
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors  import LinkExtractor
from wangyiyun.items import WangyiyunItem
from wangyiyun.spiders.Proxy_handler import ProxyHandler
import requests

class MusicSpider(scrapy.Spider):
    name = 'wangyiyun'
    allowed_domains=["music.163.com"]

    start_urls=[
                "http://music.163.com/discover/artist",
                "http://music.163.com/artist?id=91725",
                "http://music.163.com/song?id=411214279",
                "http://music.163.com/song?id=186016",
    ]

    rules = [Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+')), follow=True),
             Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+&initial=\d+')), follow=True),
             Rule(LinkExtractor(allow=(r'/artist\?id=\d+')), follow=True),
             Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+')), follow=True),
             Rule(LinkExtractor(allow=(r'/artist/album\?id=\d+&limit=\d+&offset=\d+')), follow=True),
             Rule(LinkExtractor(allow=(r'/album\?id=\d+')), callback='pare_song'),
             ]

    def parse_song(self,response):
        # inspect shell
        # inspect_response(response, self)

        sel=Selector(response)
        # 部分网页正文为空（禁止js的时候，如 http://music.163.com/#/song?id=32548815）
        songs = sel.xpath("//")

        item=WangyiyunItem()
        item['music_name']=sel.xpath('//div[@class="n-songtab"]//text()').extract()[0]
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



