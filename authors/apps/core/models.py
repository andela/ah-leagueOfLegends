from django.db import models


class TimestampedModel(models.Model):
    """ 
    This model reprsesnts the Timestamp model it shows when an object was 
    created.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']