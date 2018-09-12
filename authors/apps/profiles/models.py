from django.db import models
from authors.apps.core.models import TimestampedModel

class Profile(TimestampedModel):
    """ This class represents the user Profile model """
    # There is one-to-one relationship between the user an profile model
    # A user will only have one related Profile model
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    favorites = models.ManyToManyField('articles.Article',
                                       related_name='favorited_by'
                                       )

    def __str__(self):
        return self.user.username

    def favorite(self, article):
        """Favorites an article if we favorited it."""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Unfavorites an article if we've already favorited it."""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Returns True if we have favorited an article; else False."""
        return self.favorites.filter(pk=article.pk).exists()