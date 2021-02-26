# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from scrapy.core.downloader.handlers.http11 import TunnelError


class RandomUaMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['user-agent'] = self.ua.random


class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta['proxy'] = '183.220.145.3:801'
        raise TunnelError('a')

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TunnelError):
            request.meta['proxy'] = '183.220.145.3:80'
            return request
