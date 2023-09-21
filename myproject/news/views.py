from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from news.models import News, NewsTopic, NewsRecommend
from news.serializers import NewsSerializer, TopicSerializer, RecommendSerializer
from django.http import JsonResponse

#topic list 보여주기
@api_view(['GET'])
def topic_list(request):
    json_dumps_params = {'ensure_ascii': False}
    topics = NewsTopic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return JsonResponse(serializer.data, json_dumps_params=json_dumps_params, safe=False)

#topic_id, topic_name가져오기
@api_view(['GET'])
def get_topic(request, topic_id):
    json_dumps_params = {'ensure_ascii': False}
    try:
        topic = NewsTopic.objects.get(topic_id=topic_id)
        serializer = TopicSerializer(topic)
        return JsonResponse(serializer.data, json_dumps_params=json_dumps_params, safe=False)

    except NewsTopic.DoesNotExist:
        return Response({"message": "No content"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#topic_id에 따른 news_id가져오기
@api_view(['GET'])
def get_news_id(request, topic_id):
    json_dumps_params = {'ensure_ascii': False}
    try:
        recommends = NewsRecommend.objects.filter(topic__topic_id=topic_id)
        serializer = RecommendSerializer(recommends, many=True)
        news_ids = [recommend_data['news']['id'] for recommend_data in serializer.data]
        return JsonResponse(news_ids, json_dumps_params=json_dumps_params, safe=False)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#news_id에 따른 news 상세 모두 가져오기
@api_view(['GET'])
def get_news_detail(request, news_id):
    json_dumps_params = {'ensure_ascii': False}
    try:
        news_instance = News.objects.get(id=news_id)
        serializer = NewsSerializer(news_instance)
        return JsonResponse(serializer.data, json_dumps_params=json_dumps_params, safe=False)

    except News.DoesNotExist:
        return Response({"message": "No content"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

