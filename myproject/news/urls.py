from django.urls import path
from news import views

urlpatterns = [
    path('topics/', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.get_topic, name='get_topic'),
    path('news-id/<int:topic_id>/', views.get_news_id, name='get_news_id'),
    path('news-detail/<int:news_id>/', views.get_news_detail, name='get_news_detail'),
]
