import os
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.core.email_with_celery import SendEmail


class TimestampedModel(models.Model):
    ''' Model to take care of when an instance occurs in the database
    Appends created at and updated at fields using datetime.now()'''

    # Timestamp shows when an object was first created in the database
    created_at = models.DateTimeField(auto_now_add=True)

    # represents when an object was last changed

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # It is a good practice to have ordering in reverse chronology.
        # 
        ordering = ['-created_at', '-updated_at']


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    tagList = ArrayField(models.CharField(
        max_length=255), default=None, null=True, blank=True)
    image = models.ImageField(
        upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
    # blank = True
    # a many-to-many field will map to a serializer field that
    # requires at least one input, unless the model field has blank=True
    like = models.ManyToManyField(User, blank=True, related_name='like')
    # define related_name argument for 'Article.like' or 'Article.dislike'.
    # to ensure that the fields were not conflicting with each other,
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike')
    # Bookmarked is set as False
    bookmarked = models.BooleanField(default=False)
    # An author is the creator of the article, usually the current logged in user.
    # I create a foreign key r/ship.
    # This r/ship can help returns all articles of a particular author.
    author = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE,
        related_name='articles'
    )
    ratings_counter = models.IntegerField(default=0)

    prepopulated_fields = {"slug": ("title",)}

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        ''' Creates a slug based on Article title
        Example:
        Title: ArticleOne
        Slug: ArticleOne-1
        '''
        self.slug = self._get_unique_slug()
        super(Article, self).save(*args, **kwargs)

    def updaterate(self, rating):
        ''' 
        '''
        self.ratings_counter = rating
        

    def __str__(self):
        ''' Returns a title of the article as object representation'''

        return self.title


class Comment(TimestampedModel):
    '''
    Comment class implementation
    '''
    body = models.TextField()
    author = models.ForeignKey('authentication.User',
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes = models.ManyToManyField('authentication.User',
                                   related_name='likes', blank=True)
    dislikes = models.ManyToManyField('authentication.User',
                                      related_name='dislikes', blank=True)

    def __str__(self):
        return self.body
class ArticleRating(models.Model):
    """
    Defines the ratings fields for a rater
    """
    rater = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, 
        related_name='articlesrating'
    )
    note =models.TextField()
    article = models.ForeignKey(
        Article,  on_delete=models.CASCADE, related_name="articlerating")
    rating = models.IntegerField()
 
    def __str__(self):
        return self.note



class Report(TimestampedModel):
    """Reporting an article model"""
    body = models.TextField()
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

@receiver(post_save, sender=Article)
def send_notifications_to_all_users(sender,
                                    instance,
                                    created, *args, **kwargs):
    """Create a Signal that sends email to all users that follow the author.

    Arguments:
        sender {[type]} -- [Instance of ]
        created {[type]} -- [If the article is posted.]
    """

    if instance and created:
        users_following = instance.author.profile.get_followers(
                                                    instance.author.profile)
        users_follow = [u.user for u in users_following if u.get_notifications]
        link = f'{os.getenv("HEROKU_BACKEND_URL")}/api/articles/{instance.slug}'
        users_foll = [u.user.id for u in users_following]
        if users_foll:
            uuid = urlsafe_base64_encode(force_bytes(users_foll[0])
                                         ).decode("utf-8")
            subscription = f'{os.getenv("HEROKU_BACKEND_URL")}/api/users/subscription/{uuid}/'
            SendEmail(
                template="create_article.html",
                context={
                    "article": instance,
                    "author": instance.author,
                    "url_link": link,
                    "subscription": subscription
                },
                subject="New Article",
                e_to=[u.email for u in users_follow],
            ).send()


@receiver(post_save, sender=Comment)
def send_notifications_to_all_users_on_comments(sender,
                                                instance,
                                                created,
                                                *args, **kwargs):
    """Create a Signal that sends email to all users that follow the author.

    Arguments:
        sender {[type]} -- [Instance of ]
        created {[type]} -- [If the article is posted.]
    """

    if instance and created:
        user_following = Profile.objects.all()
        user_follow = [u.user for u in user_following if \
                  u.has_favorited(instance.article) and u.get_notifications]
        author = User.objects.get(email=instance.author)
        if author:
            comment = Comment.objects.get(id=instance.id)
            link = f'{os.getenv("HEROKU_BACKEND_URL")}/api/articles/{comment.article.slug}/comments/{instance.id}'
            uuid = urlsafe_base64_encode(force_bytes(author.id)
                                         ).decode("utf-8")
            subscription = f'{os.getenv("HEROKU_BACKEND_URL")}/api/users/subscription/{uuid}/'
            SendEmail(
                template="comment_notification.html",
                context={
                    "article": instance.article,
                    "comment": instance,
                    "url_link": link,
                    "subscription": subscription
                },
                subject=" New Comment.",
                e_to=[u.email for u in user_follow],
            ).send()
