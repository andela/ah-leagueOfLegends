from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
<<<<<<< HEAD
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
=======
>>>>>>> [Feature #159965488]Upate models to enable users recieve email notifications


from authors.apps.authentication.models import User
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
class ArticleRatings(models.Model):
    """
    Defines the ratings fields for a rater
    """
    rater = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, 
        related_name='articlesrating'
    )
    article = models.ForeignKey(
        Article,  on_delete=models.CASCADE, related_name="articlerating")
    rating = models.IntegerField()



<<<<<<< HEAD
<<<<<<< HEAD
class Report(TimestampedModel):
    """Reporting an article model"""
    body = models.TextField()
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
=======
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
        receivers = list(User.objects.all())
        link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{instance.slug}'
        subscription = f'https://ah-leagueoflegends-staging.herokuapp.com/api/users/subscription/'
        SendEmail(
            template="create_article.html",
            context={
                "article": instance,
                "author": instance.author,
                "url_link": link,
                "subscription": subscription
            },
            subject=" has published a new article",
            e_to=[u.email for u in receivers],
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
        # import pdb; pdb.set_trace()
        receivers = list(User.objects.all())
        print(receivers)
        author = User.objects.get(email=instance.author)
<<<<<<< HEAD
        article = Article.objects.get(author=author, id=instance.id)
        link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{article.slug}/comments/{instance.id}'
        SendEmail(
            template="comment_notification.html",
            context={
                "article": instance,
                "url_link": link
=======
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
        receivers = list(User.objects.all())
        link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{instance.slug}'
        SendEmail(
            template="create_article.html",
            context={
                "article": instance,
                "author": instance.author,
                "url_link": link
            },
            subject=" has published a new article",
            e_to=[u.email for u in receivers],
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
        receivers = list(User.objects.all())
        author = User.objects.get(email=instance.author)
<<<<<<< HEAD
        article = Article.objects.get(author=author, id=instance.id)
        link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{article.slug}/comments/{instance.id}'
        SendEmail(
            template="comment_notification.html",
            context={
<<<<<<< HEAD
                "article": instance
>>>>>>> [Feature #159965488]Upate models to enable users recieve email notifications
=======
                "article": instance,
                "url_link": link
>>>>>>> [Feature #159965488] Add templates that links the user to the actual comment written.
            },
            subject=" has published a new article",
            e_to=[u.email for u in receivers],
        ).send()
<<<<<<< HEAD
>>>>>>> [Feature #159965488]Upate models to enable users recieve email notifications
=======
        if author:
            # article = Article.objects.get(author=author, id=instance.id)
            comment = Comment.objects.get(id=instance.id)
            link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{comment.article.slug}/comments/{instance.id}'
            uuid = urlsafe_base64_encode(force_bytes(author.id)
                                         ).decode("utf-8")
            subscription = f'http://127.0.0.1:8000/api/users/subscription/{uuid}'
            SendEmail(
                template="comment_notification.html",
                context={
                    "article": instance.article,
                    "comment": instance,
                    "url_link": link,
                    "subscription": subscription
=======
        if author:
            # article = Article.objects.get(author=author, id=instance.id)
            # link = f'https://ah-leagueoflegends-staging.herokuapp.com/api/articles/{article.slug}/comments/{instance.id}'
            SendEmail(
                template="comment_notification.html",
                context={
                    "article": instance,
                    # "url_link": link
>>>>>>> [Feature #159965488] Update model to make travis build pass
                },
                subject=" has published a new article",
                e_to=[u.email for u in receivers],
            ).send()
<<<<<<< HEAD
>>>>>>> [Feature #159965488] Update model to make travis build pass
=======
>>>>>>> [Feature #159965488]Upate models to enable users recieve email notifications
=======
>>>>>>> [Feature #159965488] Update model to make travis build pass
