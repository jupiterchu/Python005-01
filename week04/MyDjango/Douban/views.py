import requests
from django.shortcuts import render

# Create your views here.
from lxml import etree

from Douban.models import Movies

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
}

def search(request, q):
    data = _crawl_api(q)
    return render(request, 'search.html', locals())


def detail(request, mid, title):

    movie = Movies.objects.filter(stars__gte=3, name=title).all()
    if len(movie):
        data = movie
    else:
        _crawl_movies(mid, title)
        data =  Movies.objects.filter(stars__gte=3, name=title).all()
    return render(request, 'detail.html', locals())


def _detail(request, mid):
    if request.GET:
        name = request.GET.get('suggest', '')
        print(name)
    data = Movies.objects.filter(mid__gte=3, mid=1291545).all()
    return render(request, 'detail.html', locals())

def index(request):
    return render(request, 'index.html')


def _crawl_movies(mid, title):
    url = f"https://movie.douban.com/subject/{mid}/comments"
    response = requests.get(url, headers=HEADERS).text
    htmls = etree.HTML(response).xpath('//div[@class="comment-item "]')
    for html in htmls:
        comment = html.xpath('.//p/span/text()')[0]
        time = html.xpath('.//h3/span[2]/span[3]/@title')[0]
        stars = html.xpath('.//h3/span[2]/span[2]/@title')[0]

        print(comment, time, stars, mid)

        _insert(name=title, comment=comment, create_time=time, stars=change_stars(stars), mid=mid)

def _insert(**kwargs):
    Movies.objects.create(**kwargs)


def _crawl_api(q):
    url = f"https://movie.douban.com/j/subject_suggest?q={q}"
    response = requests.get(url=url, headers=HEADERS)
    return  response.json()


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
