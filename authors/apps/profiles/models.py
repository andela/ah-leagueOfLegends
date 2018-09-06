from django.db import models


class Profile(models.Model):
    """ This class represents the user Profile model """
    # There is one-to-one relationship between the user an profile model
    # A user will only have one related Profile model
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
