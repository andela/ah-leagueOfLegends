from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, ArticleSearchList

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet,
	base_name="fetch_articles")

app_name = 'articles'
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^search/articles$', ArticleSearchList.as_view(), name="search"),


]