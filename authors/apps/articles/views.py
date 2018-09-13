from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer
from rest_framework.pagination import LimitOffsetPagination


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    ''' By subclassing create, list, retrieve and destroy
    we can define create, list, retrieve and destroy
    endpoints in one class '''

    lookup_field = 'slug'
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = self.queryset

        return queryset

    def create(self, request):

        ''' Creates a new article in the database
        Method takes user data, validates and commits in the db
        '''

        serializer_context = {
            'author': request.user,
            'request': request
        }
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, \
 \
                        status=status.HTTP_201_CREATED)

    def list(self, request):

        ''' Retrives all articles from the database
        with the latest to be created first
        (chronologically)
        '''

        serializer_context = {'request': request}
        page = self.paginate_queryset(self.queryset)

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):

        ''' Method returns a single article 
        Takes a slug as unique identifier, searches the db
        and returns an article with matching slug.
        Returns NotFound if an article does not exist '''

        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(article)

        return Response(
            {'article': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, slug):

        ''' Method updates partially a single article 
        Takes a slug as unique identifier, searches the db
        and updates an article with matching slug.
        Returns NotFound if an article does not exist '''

        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        article = Article.objects.get(slug=slug);

        if request.user != article.author:
            return Response(
                {'message': 'You can only update your article'},

                status=status.HTTP_401_UNAUTHORIZED)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, slug):

        ''' Method deletes a single article 
        Takes a slug as unique identifier, searches the db
        and deletes an article with matching slug.
        Returns NotFound if an article does not exist '''

        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)

        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        article = Article.objects.get(slug=slug);

        if request.user != article.author:
            return Response({'message': 'You can only delete your article'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if article.delete():
            return Response(
                {'message': 'You have successfully deleted the article'},
                status=status.HTTP_200_OK)


class LikeAPIView(UpdateAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    lookup_field = 'slug'

    def update(self, request, slug):
        """Update the user's liking status on a particular article."""
        # if not auth Sign in to make your opinion count.
        user = request.user

        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            return Response({"message": "The article does not exist."}, status=status.HTTP_404_NOT_FOUND)
            # raise NotFound('The article does not exist.')

        if user in article.like.all():
            # If like exists, remove like
            article.like.remove(user.id)
            return Response({"message": "You no longer like this article"}, status=status.HTTP_200_OK)
        if user in article.dislike.all():
            # If user had disliked the article, removes the dislike and adds the like
            article.dislike.remove(user.id)
            article.like.add(user.id)
            return Response({"message": "Removed from dislike and Added to Liked articles"}, status=status.HTTP_200_OK)
        else:
            # If like does not exist, add like
            article.like.add(user.id)
            return Response({"message": "Added to Liked articles"}, status=status.HTTP_200_OK)


class DisLikeAPIView(UpdateAPIView):
    queryset = Article.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    lookup_field = 'slug'

    def update(self, request, slug):
        """Update the user's liking status on a particular article."""
        # if not auth Sign in to make your opinion count.
        user = request.user

        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            return Response({"message": "The article does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if user in article.dislike.all():
            # If dislike exists, remove dislike
            article.dislike.remove(user.id)
            return Response({"message": "You no longer dislike this article"}, status=status.HTTP_200_OK)
        if user in article.like.all():
            article.like.remove(user.id)
            article.dislike.add(user.id)
            return Response({"message": "Removed from Liked Articles and Added to Disliked articles"},
                            status=status.HTTP_200_OK)
        else:
            # If dislike does not exist, add dislike
            article.dislike.add(user.id)
            return Response({"message": "You Dislike this Article"}, status=status.HTTP_200_OK)
