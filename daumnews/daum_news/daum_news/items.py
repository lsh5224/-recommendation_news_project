# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DaumNewsItem(scrapy.Item):
    URL = scrapy.Field()
    TITLE = scrapy.Field()
    CAT_BIG = scrapy.Field()
    CAT_SMALL = scrapy.Field()
    PRESS = scrapy.Field()
    DATE = scrapy.Field()
    NUM_EMOTIONS = scrapy.Field()
    NUM_COMM = scrapy.Field()
    CONTENTS = scrapy.Field()

    LIKE = scrapy.Field()
    DISLIKE = scrapy.Field()
    GREAT = scrapy.Field()
    SAD = scrapy.Field()
    ABSURD = scrapy.Field()
    ANGRY = scrapy.Field()
    RECOMMEND = scrapy.Field()
    IMPRESS = scrapy.Field()