# coding: utf-8

import logging
from scrapy import logformatter


class PoliteLogFormatter(logformatter.LogFormatter):

    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.INFO,
            'msg': logformatter.DROPPEDMSG,
            'args': {
                'exception': exception,
                'item': item,
            }
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
