# from django.test import TestCase

# Create your tests here.
from pprint import pprint

import requests

from test import HEADERS


def _crawl_api(q):

    q = "大鱼"
    url = f"https://movie.douban.com/j/subject_suggest?q={q}"
    response = requests.get(url=url, headers=HEADERS)
    return response.json()

pprint(_crawl_api('大鱼'))