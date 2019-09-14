# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class artist_item(Item):
    artist_id = Field()
    artist_name = Field()
    artist_alias = Field()
    album_size = Field()  # 专辑数量
    music_size = Field()  # 似乎是歌曲总数量

class albums_item(Item):
    artist_id = Field()
    artist_name = Field()
    album_id = Field()
    album_name = Field()
    album_comments_id = Field()
    album_publishTS = Field()
    album_company = Field()
    album_size = Field() # 包含歌曲数量






