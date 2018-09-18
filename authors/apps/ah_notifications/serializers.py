from rest_framework import serializers

from authors.apps.authentication.models import User
from notifications.models import Notification
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.articles.serializers import ArticleSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor =  UserSerializer('actor_object_id')
    action_object = ArticleSerializer('action_object_object_id')

    class Meta:
        '''
        Notification fields to be returned to users
        '''
        model = Notification
        fields = ('actor', 'verb', 'action_object', 'target')