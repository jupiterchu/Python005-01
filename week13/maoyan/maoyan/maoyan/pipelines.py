# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

import pymysql

from maoyan.settings import MYSQL_CONF


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


class StoreMySQLPipeline:

    def __init__(self):
        self.db = pymysql.connect(**MYSQL_CONF)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        SQL = """INSERT INTO `maoyan` (`title`, `tag`, `release_time`) VALUES (%s, %s, %s)"""
        self.cursor.execute(SQL, [item['title'],
                                  item['tag'],
                                  item['release_time']])
        self.db.commit()
