from django.urls import include, re_path

from .views import ProfileRetrieveAPIView

app_name = 'profiles'
urlpatterns = [
  re_path(r'(?P<username>\w+)?$', ProfileRetrieveAPIView.as_view()),
] 