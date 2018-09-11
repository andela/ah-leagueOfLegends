from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    date_joined = serializers.CharField(source='user.created_at')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.URLField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image','date_joined')
        read_only_fields = ('username',)
    

    
        
