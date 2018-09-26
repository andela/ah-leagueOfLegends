'''
ah_notifications urls
'''
from django.conf.urls import include, url
from django.urls import path

from .views import NotificationViewList, NotificationRetrieveView
from authors.apps.profiles.views import SubscribeNotificationAPIView, UnsubscribeNotificationAPIView

urlpatterns = [
    path('notifications', NotificationViewList.as_view()),
    path('notifications/subscribe', SubscribeNotificationAPIView.as_view()),
    path('notifications/unsubscribe', UnsubscribeNotificationAPIView.as_view()),
    path('notifications/<pk>', NotificationRetrieveView.as_view()),

]