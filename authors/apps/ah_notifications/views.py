'''
Notifications view
'''
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView	
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer

from notifications.models import Notification
from .renderers import NotificationJSONRenderer

class NotificationViewList(APIView):
    '''
    get all notifications where the receiver was the current user
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (NotificationJSONRenderer,)
    serializer_class = NotificationSerializer
    

    def get(self, request):
        queryset = self.request.user.notifications.unread()
        for notification in queryset:
            notification.mark_as_read()

        serializer = self.serializer_class(
            queryset,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

