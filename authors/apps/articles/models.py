from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


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

    # An author is the creator of the article, usually the current logged in user.
    # I create a foreign key r/ship.
    # This r/ship can help returns all articles of a particular author.
    author = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, 
        related_name='articles'
    )

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

    def __str__(self):

        ''' Returns a title of the article as object representation'''

        return self.title





