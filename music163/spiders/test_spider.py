import scrapy


class MySpider(scrapy.Spider):
    name = 'test_spider'

    def start_requests(self):
        return [scrapy.FormRequest("http://www.baidu.com/", callback=self.logged_in)]

    def logged_in(self, response):
        print("hello baidu")
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass