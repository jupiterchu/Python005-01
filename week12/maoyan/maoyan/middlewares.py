# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent


class RandomUaMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['user-agent'] = self.ua.random


class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta['proxy'] = '58.220.95.86:9401'
