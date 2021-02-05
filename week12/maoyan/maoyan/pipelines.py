# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from itemadapter import ItemAdapter


class MaoyanPipeline:

    def __init__(self):
        with open('movies1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'tag', 'release_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def process_item(self, item, spider):
        with open('movies1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'tag', 'release_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(item)
        return item
