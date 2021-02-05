import scrapy
from scrapy.selector import Selector

from maoyan.items import MaoyanItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        movies_array = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies_array:
            title = Selector(movie).xpath('./div/@title').extract_first()
            tag = Selector(movie).xpath('./div[2]/text()[2]').extract_first().replace('\n', '').strip()
            release_time = Selector(movie).xpath('./div[4]/text()[2]').extract_first().replace('\n', '').strip()

            item = MaoyanItem()
            item['title'] = title
            item['tag'] = tag if tag else '未知'
            item['release_time'] = release_time if release_time else '待定'
            yield item
