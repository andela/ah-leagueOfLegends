from django.db.models.signals import post_save
from django.dispatch import receiver

from authors.apps.profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
