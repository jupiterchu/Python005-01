## 第四周作业

### 使用 Django 展示豆瓣电影中某个电影的短评和星级等相关信息：

设计思路：

```
1. 将主页定义为搜索页面
2. 将搜索结果展示
	1> 直接将搜索结果的所有电影爬取。
	2> 只爬取点击的电影。
3. 点击对应电影名进入详情页
	这里采用第二种方法。对电影名称进行判断，在数据库直接返回；没有通过爬虫爬取，再返回。
```

```python
# Douban/urls.py
urlpatterns = [
    path('', views.index),
    re_path('search/(?P<q>.+)', views.search, name='search'),
    re_path('detail/(?P<mid>\d+)/(?P<title>.+)', views.detail, name='detail')
]

# MyDjango/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Douban.urls')),
    path('movies/', include('Douban.urls') ),
]
```

#### 1. 要求使用 MySQL 存储短评内容（至少 20 条）以及短评所对应的星级；

![image-20201219220934284](https://github.com/jupiterchu/Python005-01/blob/main/week04/%E5%9B%BE%E7%89%87/mysql.png)


实现代码：
```python
# Douban/models.py
class Movies(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    mid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'

# Douban/views.py
def _crawl_movies(mid, title):
    '''爬取豆瓣电影详情页'''
    url = f"https://movie.douban.com/subject/{mid}/comments"
    response = requests.get(url, headers=HEADERS).text
    htmls = etree.HTML(response).xpath('//div[@class="comment-item "]')
    for html in htmls:
        comment = html.xpath('.//p/span/text()')[0]
        time = html.xpath('.//h3/span[2]/span[3]/@title')[0]
        stars = html.xpath('.//h3/span[2]/span[2]/@title')[0]
        
        # 保存到 MySQL
        _insert(name=title, comment=comment, create_time=time, stars=change_stars(stars), mid=mid)

def _insert(**kwargs):
    Movies.objects.create(**kwargs)

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
```



#### 2. 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；

![image-20201219221149940](https://github.com/jupiterchu/Python005-01/blob/main/week04/%E5%9B%BE%E7%89%87/detail.jpg)

实现代码：

```python
# Douban/views.py
def detail(request, mid, title):
    movie = Movies.objects.filter(stars__gte=3, name=title).all()
    if len(movie):
        data = movie
    else:
        _crawl_movies(mid, title)
        data = Movies.objects.filter(stars__gte=3, name=title).all()
    return render(request, 'detail.html', locals())
```

#### 3. （选做）在 Web 界面增加搜索框，根据搜索的关键字展示相关的短评。

![image-20201219214848207](https://github.com/jupiterchu/Python005-01/blob/main/week04/%E5%9B%BE%E7%89%87/search.jpg)

![Inkedimage-20201219215624940_LI](https://github.com/jupiterchu/Python005-01/blob/main/week04/%E5%9B%BE%E7%89%87/result.jpg)

```python
# # Douban/views.py
def index(request):
    return render(request, 'index.html')

def search(request, q):
    data = _crawl_api(q)
    return render(request, 'search.html', locals())

def _crawl_api(q):
    url = f"https://movie.douban.com/j/subject_suggest?q={q}"
    response = requests.get(url=url, headers=HEADERS)
    return response.json()
```

