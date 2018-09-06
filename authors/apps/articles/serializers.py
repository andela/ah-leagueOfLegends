from rest_framework import serializers
from authors.apps.authentication.serializers import UserSerializer

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    # As for Django, serializers validate date then either save or return to the user 
    # via views.
    # We want to populate created_at and updated_at fields by calling methods
    # get_updated_at() and get_created_at() and serialize them

    created_at_date = serializers.SerializerMethodField(method_name='get_created_at')

    updated_at_date = serializers.SerializerMethodField(method_name='get_updated_at')

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
        )

    def create(self, validated_data):

        ''' Method creates an article based on validated data'''

        author = self.context.get('author', None)


        article = Article.objects.create(**validated_data)


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