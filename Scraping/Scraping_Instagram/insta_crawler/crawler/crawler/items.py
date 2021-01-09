# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CrawlerItem(Item):
    # the model item for general infos
    name = Field()
    profile_pic = Field()
    biography = Field()
    followed = Field()
    follow = Field()
    pass

class Post(Item):
    # the model item for a post in the profil
    shortcode = Field()
    likes = Field()
    text = Field()
    location =  Field()
    taken_at_timestamp = Field()
    comments = Field()
    pass