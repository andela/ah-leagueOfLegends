from django.db import models
from authors.apps.core.models import TimestampedModel


class Profile(TimestampedModel):
    """ This class represents the user Profile model """
    # There is one-to-one relationship between the user an profile model
    # A user will only have one related Profile model
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    # Many-To-Many relationship where both sides of the same model (Profile)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )
    
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    bookmarks = models.ManyToManyField('articles.Article', blank=True, related_name='bookmark')
    favorites = models.ManyToManyField('articles.Article',
                                       related_name='favorited_by'
                                       )

    get_notifications = models.BooleanField(default=True)

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
    
    def follow(self, profile):
       """Follow profile"""
       self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow profile."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we are following user"""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if profile is following us"""
        return self.followed_by.filter(pk=profile.pk).exists()
    
    def get_followers(self, profile):
        """Returns all users following us"""
        return profile.followed_by.all()

    def get_following(self, profile):
        """Returns all users we are following"""
        return profile.follows.all()
