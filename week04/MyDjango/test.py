import pymysql
import requests
from lxml import etree
mysql_conf = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "db": "jove_class"
}

con_local = pymysql.connect(**mysql_conf)

# 实际操作都需要光标进行
cursor_local = con_local.cursor()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
}



def _crawl_movies(mid):
    url = f"https://movie.douban.com/subject/{mid}/comments"
    response = requests.get(url, headers=HEADERS).text
    htmls = etree.HTML(response).xpath('//div[@class="comment-item "]')
    for html in htmls:
        comment = html.xpath('.//p/span/text()')[0]
        time = html.xpath('.//h3/span[2]/span[3]/@title')[0]
        stars = html.xpath('.//h3/span[2]/span[2]/@title')[0]
        SQL = """insert into movies(comment, create_time, stars, mid) values ({}, {}, {})"""

        print(SQL.format( '\''+comment+'\'', time, change_stars(stars), mid))
        cursor_local.execute(SQL)
    con_local.commit()



def change_stars(star):
    if star=='力荐':
        return 5
    elif star=='推荐':
        return 4
    elif star=='还行':
        return 3
    elif star=='较差':
        return 2
    elif star=='很差':
        return 1

if __name__ == '__main__':
    _crawl_movies(1291545)