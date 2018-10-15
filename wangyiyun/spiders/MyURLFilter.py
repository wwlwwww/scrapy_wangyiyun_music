# coding: utf-8
import os
from scrapy.dupefilters import RFPDupeFilter

class MyURLFilter(RFPDupeFilter):
    def regular_url(self, request):
        pass

    def request_seen(self, request):
        fp = request.url
        if fp in self.fingerprints:
            return True
        # print("url filter: {}".format(fp))
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
            # self.file.close()


