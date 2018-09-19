from django.urls import include, path

from .views import ProfileRetrieveAPIView, ProfileFollowAPIView, \
                  FollowersAPIView, FollowingAPIView, ProfileList

app_name = 'profiles'
urlpatterns = [
  path('<str:username>', ProfileRetrieveAPIView.as_view()),
  path('', ProfileList.as_view()),
  path('<str:username>/follow', ProfileFollowAPIView.as_view()),
  path('<str:username>/following', FollowingAPIView.as_view()),
  path('<str:username>/followers', FollowersAPIView.as_view()),
] 