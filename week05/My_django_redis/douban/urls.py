from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index),
    re_path('search/(?P<q>.+)', views.search, name='search'),
    re_path('detail/(?P<mid>\d+)/(?P<title>.+)', views.detail, name='detail')
]