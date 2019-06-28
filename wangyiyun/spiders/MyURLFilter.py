# coding: utf-8
import os
from urllib.parse import parse_qs, urlparse

from scrapy.dupefilters import RFPDupeFilter, BaseDupeFilter


class MyURLFilter(BaseDupeFilter):
    def regular_url(self, request):
        pass

    def request_seen(self, request):
        fp = request.url[41:]

        if fp in self.fingerprints:
            return True

        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
            # self.file.close()


