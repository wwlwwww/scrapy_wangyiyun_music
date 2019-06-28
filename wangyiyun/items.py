# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class song_item(Item):
    song_id = Field()
    song_name = Field()
    author = Field()
    comment_cnt = Field()

class comment_item(Item):
    comment_id = Field()
    user_nick = Field()
    user_id = Field()
    liked_count = Field()
    content = Field()
    replied_content = Field()

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






