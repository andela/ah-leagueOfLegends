
from .celery import app as celery_app
# this will make sure that our app is Important every time django starts
__all__ = ['celery_app']