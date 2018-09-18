from django.conf.urls import include, url
from django.urls import path

from .views import NotificationViewList

urlpatterns = [
    path('notifications', NotificationViewList.as_view()),
   

]