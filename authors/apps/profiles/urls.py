from django.urls import include, re_path,path

from .views import ProfileRetrieveAPIView, ProfileList

app_name = 'profiles'
urlpatterns = [
  path('', ProfileList.as_view()),
  re_path(r'(?P<username>\w+)?$', ProfileRetrieveAPIView.as_view()),
] 