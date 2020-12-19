from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from . import models

def index(request):
    return HttpResponse('Hello Django!')

def year(request, year):
    return HttpResponse(year)

def name(request, **kwargs):
    return HttpResponse(kwargs['name'])

def myyear(request, year):
    return render(request, 'yearview.html')


def books(request):
    n = models.Name.objects.all()
    # 将本地变量都传给模板
    return render(request, 'booklist.html', locals())