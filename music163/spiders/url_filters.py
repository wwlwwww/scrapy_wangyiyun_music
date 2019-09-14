# coding: utf-8
import logging
import os
from os import path
from urllib.parse import parse_qs, urlparse

from bitmap.bitmap import BitMap
from scrapy.dupefilters import RFPDupeFilter, BaseDupeFilter

from music163.spiders import db_pool


class artist_id_fileter(BaseDupeFilter):
    def __init__(self):
        self.seen_artist = BitMap(20000000)
        conn = db_pool.pool.connection()
        cursor = conn.cursor()

        cursor.execute('select f_id, f_music_size from t_artists')
        for row in cursor.fetchone():
            if int(row[0]) > 0 or int(row[0]) < 0:
                self.seen_artist.set(row[0])

        cursor.close()
        conn.close()

        logging.info("seenid, cnt: {}".format(self.seen_artist.count()))

    def request_seen(self, request):
        ws = request.url.split('/')
        artist_id = int(ws[-1])
        if self.seen_artist.test(artist_id):
            logging.info("url:{}, seen".format(request.url))
            return True
        else:
            self.seen_artist.set(artist_id)
            if artist_id % 200 == 0:
                logging.info("url:{}, add seen id: [{}]".format(request.url, artist_id))
            return False



