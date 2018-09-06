from rest_framework import serializers

from .models import Profile

import random

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    is_active = serializers.CharField(source='user.is_active')
    date_joined = serializers.CharField(source='user.created_at')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image','is_active','date_joined')
        read_only_fields = ('username',)
    
    def generate_avatar(self):
        random_number = random.randint(0, 99999999)
        avatar_url = 'https://api.adorable.io/avatars/100/'
        return avatar_url + str(random_number)

    def get_image(self, obj):
        if obj.image:
            return obj.image
        return self.generate_avatar()

    
        
