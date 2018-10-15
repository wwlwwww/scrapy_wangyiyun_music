# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
from scrapy.conf import settings
import logging
from scrapy.exceptions import CloseSpider
import sys
import time
import os

class WangyiyunPipeline(object):

    def __init__(self):
        client=MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        db=client[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid=True
        for data in item:
            if data is None:
                valid=False
        if valid:
            # song_key = {'_id': item['song_url']}
            # song_info={
            #     "music_name":item['music_name'],
            #     "artist":item['artist'],
            #     "album":item['album'],
            #     "hot_comments":item['hot_comments'],
            #     "total_comments_cnt" : item['total_comments_cnt'],
            # }
            song_info = {
                '_id': item['song_url'],
                "music_name": item['music_name'],
                "artist": item['artist'],
                "album": item['album'],
                "hot_comments": item['hot_comments'],
                "total_comments_cnt": item['total_comments_cnt'],
            }
            try:
                # self.collection.update_one(song_key, {"$set": song_info}, upsert=True)
                self.collection.insert_one(song_info)
            except DuplicateKeyError as e:
                pass
            except Exception as e:
                print('Pipline Exception: ', e)
                logging.info("Item wrote to MongoDB database %s/%s" %
                        (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                        level=logging.DEBUG, spider=spider)
            # cnt = self.collection.find().count()
            # if self.collection.find().count() > 2 :
            #     # spider.close_down = True
            #     # sys.exit("shut down" + time.asctime(time.localtime(time.time())))
            #     # raise CloseSpider('items is enough')
            #     # os.abort()
            #     pass
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
