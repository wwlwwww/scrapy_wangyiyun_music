# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import threading

from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
from scrapy.conf import settings
import logging
from scrapy.exceptions import CloseSpider
import sys
import time
import os
import queue

from wangyiyun import items

# artist_queue = queue.Queue(maxsize=10000)
# album_queue = queue.Queue(maxsize=10000)

class WangyiyunPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        if isinstance(item, items.artist_item):
            # cursor.execute(r'insert into t_artists values ({id}, "{name}", "{alias}", {album_size}, {music_size})'.format(id=item.artist_id, name=item.artist_name, alias=item.artist_alias, album_size=item.album_size, music_size=item.music_size))
            print("item: ", item)
        elif isinstance(item, items.albums_item):
            print("item: ", item)
            # cursor.execute(r'insert into t_albums values ({artist_id}, "{artist_name}", {id}, "{name}", "{comment_id}", {ts}, "{company}", {size})'.format(artist_id=item.artist_id, artist_name=item.artist_name, id=item.album_id, name=item.album_name,comment_id=item.album_comments_id, ts=item.album_publishTS, company=item.album_company, size=item.album_size))
        # cursor.close()
        # self.conn.commit()

    def open_spider(self, spider):
        db_path = '/home/wml/db/music163.db'
        db_path = 'C:/SQLite/DB/music163.db'
        self.conn = sqlite3.connect()
        logging.info("open spider in pipline")

    def close_spider(self, spider):
        # self.conn.close()
        logging.info("close spider in pipline")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

class artist_intodb_thread(threading.Thread):
    def run(self) -> None:
        # conn = sqlite3.connect("/home/wml/db/music163.db")

        pass

class album_intodb_thread(threading.Thread):
    def run(self) -> None:
        # conn = sqlite3.connect('/home/wml/db/music163.db')

        pass
