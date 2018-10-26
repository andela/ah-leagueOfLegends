from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count

from .models import Article, ArticleRating
from .renderers import ArticleJSONRenderer, RatingJSONRenderer
from .serializers import ArticleSerializer, RatingSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.filters import SearchFilter
from django.views.generic import ListView
import django_filters
from django_filters import rest_framework as filters
from django.contrib.postgres.fields import ArrayField
from .models import Article, Comment, Report, ArticleRating
from .renderers import ArticleJSONRenderer, CommentJSONRenderer, ReportJSONRenderer
from .serializers import ArticleSerializer, CommentSerializer, ReportSerializer


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

        return Response(serializer.data,
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

        serializer = self.serializer_class(
            article,
            context=serializer_context
        )

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


class ArticleFilter(filters.FilterSet):
    """
    Class creates a custom filter class for articles,
    for getting dynamic queries from the url
    """
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains')
    body = filters.CharFilter(field_name='body', lookup_expr='icontains')
    author__username = filters.CharFilter(
        field_name='author__username', lookup_expr='icontains')

    class Meta:
        """
        This class describes the fields to be used in the search.
        The ArrayField has also been over-ridden
        """
        model = Article
        fields = [
            'title', 'description', 'body', 'author__username', 'tagList'
        ]
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains', },
            },
        }


class ArticleSearchList(generics.ListAPIView):
    """
    Implements class to enable searching and filtering
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_list = ['title', 'body',
                   'description', 'author__username', 'tagList']
    filter_list = ['title', 'author__username', 'tagList', ]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = filter_list
    search_fields = search_list
    filterset_class = ArticleFilter


class ArticlesFavoriteAPIView(APIView):
    """
    This View allows users to Favorite and Unfavorite articles, an exception is
    thrown if the article doesn’t
    exist.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def delete(self, request, article_slug=None):
        """
        Unfavorites an existing article with the profile unfavorite method
        """
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.unfavorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_slug=None):
        """
        unfavorites an existing article with the profile favorite method
        """
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.favorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    '''
    View to create and list comments
    '''

    lookup_field = 'article__slug'
    lookup_url_kwarg = 'slug'

    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def filter_queryset(self, queryset):
        """Handle getting comments on an article."""
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def get(self, request, **kwargs):
        '''
        Get all comments to an article
        '''
        slug = self.kwargs['slug']
        try:
            article = Article.objects.get(slug=slug)
            comments = Comment.objects.all().filter(article=article.id)
            serializer = self.serializer_class(comments, many=True)

            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')

    def create(self, request, **kwargs):
        '''
        Add comment to an article
        '''
        slug = self.kwargs['slug']
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with that slug does not exist")
        serializer_context = {"author": request.user, "slug": slug}
        serializer_data = request.data.get('comment', {})
        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''
    View to retreive, update and delete a single comment
    '''
    lookup_url_kwarg = 'pk'
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def retrieve(self, request, **kwargs):
        '''
        Get single comment
        '''
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')
        try:
            comment = Comment.objects.get(pk=pk)
        except:
            raise NotFound('The comment with that id does not exist')

        serializer = self.serializer_class(comment)

        return Response({"comment": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, **kwargs):
        '''
        Delete comment
        '''
        pk = self.kwargs['pk']
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        if comment.author.id != request.user.id:
            return Response({
                "error": "you can not delete a comment that does not belong to you"},
                status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()

        return Response({
            "message": "Your comment has been successfully deleted"},
            status=status.HTTP_200_OK)


class LikeComment(APIView):
    '''
    Like a comment
    '''
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentJSONRenderer,)

    def put(self, request, **kwargs):
        '''
        update like field in comment model
        '''
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.dislikes.remove(request.user)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"message": "You unliked this article."},
                            status=status.HTTP_200_OK)

        comment.likes.add(request.user)
        return Response({"message": "You liked this comment"},
                        status=status.HTTP_200_OK)


class DislikeComment(APIView):
    '''
    dislike a comment
    '''
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentJSONRenderer,)

    def put(self, request, **kwargs):
        '''
        update dislike field in comment model
        '''
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.likes.remove(request.user)

        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
            return Response({"message": "You undisliked this article."},
                            status=status.HTTP_200_OK)

        comment.dislikes.add(request.user)
        return Response({"message": "You disliked this comment"},
                        status=status.HTTP_200_OK)

class RateArticlesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (RatingJSONRenderer,)
    serializer_class = RatingSerializer

    def post(self, request, slug):
        """
        Method that posts users article ratings
        """
        ratingData = request.data.get("rate", {})

        rating = ratingData.get('rating', None)
        note = ratingData.get('note', None)

        if not isinstance(rating, int):
            return Response(
                {'message': 'Rating should be an integer'},
                status=status.HTTP_401_UNAUTHORIZED)
        if rating <1 or rating > 5:
            return Response(
                {'error': 'Rating should be between 1 and 5'},
                status=status.HTTP_401_UNAUTHORIZED)
        # Try to get an article using slug, raise an exception if not found
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")
        # User should not rate own article, raise unauthorised status
        if request.user ==  article.author:
            return Response(
                {'message': 'You cannot rate your article'},

                status=status.HTTP_401_UNAUTHORIZED)
        # No previous ratings, so just take the rating and save to the db
        # after aggregating
        # Check the existing number or rating
        # SELECT count(ID) FROM RATINGS WHERE ARTICLE = article and Rater = user
        user = request.user
        try:
            # Get a user rating if there is previous record
            currentRating = ArticleRating.objects.get(rater=user, article=article);
        except:
            currentRating = None

         # Save the rating
        if currentRating is None:
            article_rating = ArticleRating(article=article,
            rating=rating, rater=user, note=note)
            article_rating.save()
        ## update the rating
        else:
            #Upadte previous rating with current rating
            currentRating.rating=rating
            currentRating.save()

        # Get the ratings avarage
        average = ArticleRating.objects.filter(
            article=article).aggregate(Avg('rating')).get('rating__avg', 0)
        return Response(
            {"average_rating": average, "Note": note},
            status=status.HTTP_201_CREATED)

                    # Get the ratings avarage
        average = ArticleRating.objects.filter(
            article=article).aggregate(Avg('rating')).get('rating__avg', 0)
        return Response(
            {"average_rating": average, "Note": note},
            status=status.HTTP_201_CREATED)
    # End pints returns an initial rating of the user if exists
    def get(self, request, slug):
        """
        Method that posts users article ratings
        """

        # Try to get an article using slug, raise an exception if not found
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")
        # after aggregating
        # Check the existing number or rating
        # SELECT count(ID) FROM RATINGS WHERE ARTICLE = article and Rater = user
        user = request.user
        try:
            # Get a user rating if there is previous record
            currentRating = ArticleRating.objects.get(
                rater=user, article=article)
        except:
            currentRating = None
            return Response("You have not rated before")

         # Return the rating
        if currentRating:
            return Response(
                {"rating": currentRating.rating},
                status=status.HTTP_200_OK)


class BookmarkAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    lookup_field = 'slug'

    def update(self, request, slug):
        """Update the bookmark status on a particular article."""
        user = request.user
        profile = user.profile

        # Checks if the article exists
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        bookmarks = user.profile.bookmarks.all()
        # Bookmarks article, if article is not bookmarked
        if article not in bookmarks:
            user.profile.bookmarks.add(article)
            response = 'Added to Bookmarks'
        # Remove bookmark, if one exists
        else:
            user.profile.bookmarks.remove(article)
            response = 'Removed from Bookmarks'
        return Response(response, status=status.HTTP_200_OK)

class ReportCreateAPIView(generics.CreateAPIView):
    """Facilitate create reports"""

    lookup_field = 'article__slug'
    lookup_url_kwarg = 'slug'

    queryset = Report.objects.select_related()
    serializer_class = ReportSerializer
    renderer_classes = (ReportJSONRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def filter_queryset(self, queryset):
        """Handle getting reports on an article."""
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def create(self, request, **kwargs):
        """Create reports to an article"""
        slug = self.kwargs['slug']
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with that slug does not exist")
        serializer_context = {"author": request.user, "slug": slug}
        serializer_data = request.data.get('report', {})
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportListAPIView(generics.ListAPIView):
    """Facilitate list reports"""

    lookup_field = 'article__slug'
    lookup_url_kwarg = 'slug'

    queryset = Report.objects.select_related()
    serializer_class = ReportSerializer
    renderer_classes = (ReportJSONRenderer,)
    permission_classes = (IsAdminUser,)

    def filter_queryset(self, queryset):
        """Handle getting reports on an article."""
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def get(self, request, **kwargs):
        """Get all reports to an article"""
        slug = self.kwargs['slug']
        try:
            article = Article.objects.get(slug=slug)
            reports = Report.objects.all().filter(article=article.id)
            serializer = self.serializer_class(reports, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:

            raise NotFound('An article with this slug does not exist.')
