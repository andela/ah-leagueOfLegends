from rest_framework import serializers

from django.db.models.signals import post_save
from notifications.signals import notify

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.authentication.models import User

from .models import Article, Comment, ArticleRatings
from django.db.models import Avg, Count


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    # SerializerMethodField - read-only field
    # gets its value by calling a method on the serializer class it is attached to.
    # method_name - The name of the method on the serializer to be called
    like = serializers.SerializerMethodField(method_name='get_like_count')
    dislike = serializers.SerializerMethodField(method_name='get_dislike_count')
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count')
    bookmarked = serializers.SerializerMethodField(method_name='get_bookmarks')
    # As for Django, serializers validate date 
    # then either save or return to the user 
    # via views.
    # We want to populate created_at and 
    # updated_at fields by calling methods
    # get_updated_at() and get_created_at() and serialize them
    created_at_date = serializers.SerializerMethodField(
        method_name='get_created_at')
    updated_at_date = serializers.SerializerMethodField(
        method_name='get_updated_at')
    average_ratings = serializers.SerializerMethodField(
        method_name="average_count")

    class Meta:
        ''' Class contains the fields to be returned by articles serializer.
            Add here any other fields you want to be serialized

        '''
    
        model = Article
        fields = (
            'author',
            'body',
            'tagList',
            'created_at_date',
            'description',
            'slug',
            'title',
            'updated_at_date',
            'like',
            'dislike',
            'favorited',
            'favoritesCount',
            'average_ratings',
            'bookmarked',
        )

    def create(self, validated_data):
        ''' Method creates an article based on validated data'''

        author = self.context.get('author', None)

        article = Article.objects.create(**validated_data)

        notify.send(author, recipient=User.objects.all(), verb="created a new article", action_object=article)
        return article

    def get_created_at(self, instance):
        # Returns the date when article was created in isoformat()
        # Example:
        # date(2002, 12, 4).isoformat() == '2002-12-04'.
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        # Returns the date when an article was updated in isoformat()
        # Example:
        # date(2002, 12, 4).isoformat() == '2002-12-04'.

        return instance.updated_at.isoformat()

    def get_like_count(self, obj):
        """Sets the value of like field to the serializer 
        by returning the length of the like object."""
        # counts the number of children the like object has
        return obj.like.count()

    def get_dislike_count(self, obj):
        """Sets the value of dislike field to the 
        serializer by returning the length of the dislike object."""
        # counts the number of children the dislike object has
        return obj.dislike.count()

    def get_favorited(self, instance):
        request = self.context.get('request', None)
        if request is None:
            return False
        if not request.user.is_authenticated:
            return False
        return request.user.profile.has_favorited(instance)

    def average_count(self, object):
        average = ArticleRatings.objects.filter(
            article=object).aggregate(Avg('rating')).get('rating__avg', 0)
        return average

    def get_bookmarks(self, instance):
        """ Sets bookmarked as True or False"""
        request = self.context.get('request', None)
        # Ensures a request exists
        if request is None:
            return False
        # Ensures user is authenticated
        if not request.user.is_authenticated:
            return False
        bookmarks = request.user.profile.bookmarks.all()
        # Checks if the instance of the article exists
        if instance in bookmarks:
            bookmarked = True
        else:
            bookmarked = False

        return bookmarked

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()


class CommentSerializer(serializers.ModelSerializer):
    '''
    mediate between comment model and python primitives
    '''
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'created_at',
            'updated_at',
            'body',
            'author',
        )

    def create(self, validated_data):
        slug = self.context.get('slug')
        author = self.context.get('author', None)
        article = Article.objects.get(slug=slug)
        comment = Comment.objects.create(article=article, author=author, **validated_data)
        return comment


class RatingSerializer(serializers.Serializer):
    """
    zserializer for rating
    """

    rating = serializers.IntegerField(required=True)

    class Meta:
        model = Article
        fields = ['rating']

    def validate(self, data):
        # Validates rating data
        # Has to be an Int and not less than 1
        # and not greater than 5
        rate = data.get('rating')

        if isinstance(rate, str) or rate is None:
            raise serializers.ValidationError(
                """Only integers allowed."""
            )

        # Rate should be >0 and < 6
        if rate > 5 or rate < 1:
            raise serializers.ValidationError(
                """Rate must be 1 and greater and not greater than 1"""
            )

        return {"rating": rate}
