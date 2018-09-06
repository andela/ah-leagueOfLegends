from rest_framework import serializers

from .models import Profile

import random

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image',)
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image
        return generate_avatar()

    def generate_avatar(self):
        random_number = random.randint(0, 99999999)
        avatar_url = 'https://api.adorable.io/avatars/100/'
        return avatar_url + str(random_number)
        
