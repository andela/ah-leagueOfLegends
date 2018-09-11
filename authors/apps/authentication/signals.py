import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.image = generate_avatar()
        profile.save()
        
def generate_avatar():
    """Genarates an avatar and saves to the user model upon instantiation"""
    random_number = random.randint(0, 99999999)
    avatar_url = 'https://api.adorable.io/avatars/500/'
    image = avatar_url + str(random_number)
    return image 
