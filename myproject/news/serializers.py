
from rest_framework import serializers
from rest_framework import viewsets
from .models import Category, News, Comment, NewsRecommend, User, NewsTopic


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTopic
        fields = '__all__'

class RecommendSerializer(serializers.ModelSerializer):

    news = NewsSerializer(read_only=True) 
    class Meta:
        model = NewsRecommend
        fields = '__all__'