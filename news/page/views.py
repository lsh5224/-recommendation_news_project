from django.shortcuts import render
from .models import Category1, Category2, News, Platform, User
from django.views.generic import ListView

def news(request):

    topic_list = ["환율", "코스피", "미국"]
    topic_news = {}

    for topic in topic_list:
        # 뉴스 검색 (title 필드 기반)
        news_items = News.objects.filter(title__icontains=topic).order_by('-date_upload')[:5]

        topic_news[topic] = news_items

    context = { 
        'topics': topic_list,
        'topic_news': topic_news
    }

    return render(request, 'page/news.html', context)


