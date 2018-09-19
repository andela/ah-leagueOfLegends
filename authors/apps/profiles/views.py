from rest_framework import serializers, status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Profile
from .exceptions import ProfileDoesNotExist
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    """ This Class represents GET profile endpoint"""
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile, 
                           context={'request': request} )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileList(ListAPIView):
    '''Retrives all profiles from the database'''
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(
           page,
           context=serializer_context,
           many=True
        )
        return self.get_paginated_response(serializer.data)

class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def put(self, request, username=None):
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if follower.pk is followee.pk:
            raise serializers.ValidationError('You can not follow yourself.')

        if follower.is_following(followee) is False:
            follower.follow(followee)
        else:
            follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, username):
        user = self.request.user.profile
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
    
        followers = user.get_followers(profile)
        serializer = self.serializer_class(followers,
                                    many=True,context={'request': request})
        return Response({"followers":serializer.data},
                                    status=status.HTTP_200_OK, )
     


class FollowingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, username):
        user = self.request.user.profile
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
    
        following = user.get_following(profile)
        serializer = self.serializer_class(following,many=True,
                                        context={'request': request})
        return Response({"followers":serializer.data},
                                    status=status.HTTP_200_OK, )
