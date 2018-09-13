from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import (ArticleViewSet, LikeAPIView, DisLikeAPIView,
                    ArticleSearchList, ArticlesFavoriteAPIView, CommentsListCreateAPIView,
                      CommentRetrieveUpdateDestroy)
=======
from .views import LikeAPIView, DisLikeAPIView, ArticleSearchList
from .views import (ArticleViewSet, CommentsListCreateAPIView, 
                    CommentRetrieveUpdateDestroy, LikeComment, DislikeComment)
>>>>>>> [Feature #159965503] Add like,dislike comments and tests

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet, base_name="fetch_articles")

app_name = 'articles'

urlpatterns = [
    url(r'^', include(router.urls)),
    path('articles/<str:slug>/like/', LikeAPIView.as_view(), name='like_article'),
    path('articles/<str:slug>/dislike/', DisLikeAPIView.as_view(), name='dislike_article'),
    url(r'^search/articles$', ArticleSearchList.as_view(), name="search"),
    url(r'^articles/(?P<article_slug>[-\w]+)/favorite/?$',
     ArticlesFavoriteAPIView.as_view()),

    path('articles/<slug>/comments', CommentsListCreateAPIView.as_view()),
    path('articles/<slug>/comments/<pk>', CommentRetrieveUpdateDestroy.as_view()),
    path('articles/<slug>/comments/<pk>/like', LikeComment.as_view()),
    path('articles/<slug>/comments/<pk>/dislike', DislikeComment.as_view())

]
