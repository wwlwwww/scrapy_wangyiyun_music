# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import threading
from os import path

from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
import logging

from music163 import items, settings


# artist_queue = queue.Queue(maxsize=10000)
# album_queue = queue.Queue(maxsize=10000)
from music163.spiders import db


class my_pipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        logging.debug("item: %s", item)
        conn = db.pool.connection()
        cursor = conn.cursor()
        try:
            if isinstance(item, items.artist_item):
                row = [item['artist_id'], item['artist_name'], item['artist_alias'],
                    item['album_size'], item['music_size']]
                cursor.execute(r'insert into t_artists values (?, ?, ?, ?, ?) on duplicate key update f_name={}, f_alias={}, '
                               r'f_album_size={}, f_music_size={}'.format(
                                 item['artist_name'], item['artist_alias'], item['album_size'], item['music_size']), row)

            elif isinstance(item, items.albums_item):
                # print("item: ", item)
                row = [item['artist_id'], item['artist_name'], item['album_id'], item['album_name'],
                               item['album_comments_id'], item['album_publishTS'], item['album_company'], item['album_size']]
                cursor.execute(r'insert into t_albums values (?, ?, ?, ?, ?, ?, ?, ?) on duplicate key update '
                               r'f_artist_id={}, f_artist_name={}, f_album_name={}, f_album_comment_id={}, f_album_ts={},'
                               r'f_album_company={}, f_album_size={}'.format(item['artist_id'], item['artist_name'], item['album_name'],
                               item['album_comments_id'], item['album_publishTS'], item['album_company'], item['album_size']), row)
        except sqlite3.IntegrityError as e:
            pass
        except Exception as e:
            print("item: ", item)
            print('exception: ', e)

        cursor.close()
        self.conn.commit()

    def open_spider(self, spider):
        logging.info("open spider in pipline")

    def close_spider(self, spider):
        logging.info("close spider in pipline")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
