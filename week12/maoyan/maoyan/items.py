# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    title = scrapy.Field()
    tag = scrapy.Field()
    release_time = scrapy.Field()
