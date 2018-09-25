'''
ah_notifications urls
'''
from django.conf.urls import include, url
from django.urls import path

from .views import NotificationViewList, NotificationRetrieveView

urlpatterns = [
    path('notifications', NotificationViewList.as_view()),
    path('notifications/<pk>', NotificationRetrieveView.as_view()),

]