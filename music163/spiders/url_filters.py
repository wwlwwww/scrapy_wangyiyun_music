# coding: utf-8
import logging
import os
import sqlite3
from os import path
from urllib.parse import parse_qs, urlparse

from bitmap.bitmap import BitMap
from scrapy.dupefilters import RFPDupeFilter, BaseDupeFilter

from music163 import settings


class artist_id_fileter(BaseDupeFilter):
    def __init__(self):
        self.seen_artist = BitMap(13000000)

        db_path = path.join(settings.DB_PATH, 'music163.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('select f_id from t_artists')
        for row in cursor:
            self.seen_artist.set(row[0])
        cursor.close()
        conn.close()

        logging.info("seenid, cnt: {}".format(self.seen_artist.count()))

    def request_seen(self, request):
        artist_id = int(request.url[41:])
        if self.seen_artist.test(artist_id):
            logging.info("url:{}, seen".format(request.url))
            return True
        else:
            self.seen_artist.set(artist_id)
            if artist_id % 20 == 0:
                logging.info("url:{}, add seen id: [{}]".format(request.url, artist_id))
            return False



