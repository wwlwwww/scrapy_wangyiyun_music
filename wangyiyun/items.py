# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WangyiyunItem(Item):
    music_name=Field()
    artist=Field()
    album=Field()
    hot_comments=Field()
    total_comments_cnt = Field()
    song_url=Field()

