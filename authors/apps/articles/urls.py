from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, LikeAPIView, DisLikeAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet, base_name="fetch_articles")

app_name = 'articles'

urlpatterns = [
    url(r'^', include(router.urls)),
    path('articles/<str:slug>/like/', LikeAPIView.as_view(), name='like_article'),
    path('articles/<str:slug>/dislike/', DisLikeAPIView.as_view(), name='dislike_article'),

]
