from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    date_joined = serializers.CharField(source='user.created_at')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.URLField()
    get_notifications = serializers.BooleanField()
    bookmarks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    following = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image','date_joined','following','bookmarks', 'get_notifications')
        read_only_fields = ('username',)
        
    def get_following(self, instance):
        request = self.context.get('request', None)
                
        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followee = instance
        return follower.is_following(followee)
