# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authors.settings')

# Creating an instance of celery
# app = Celery('authors', broker_connection_max_retries='1')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
from __future__ import absolute_import

import os

from celery import Celery, shared_task
from django.core.mail import EmailMessage

# set the default Django settings module for the 'celery' program.
os.environ['DJANGO_SETTINGS_MODULE'] = 'authors.settings'

app = Celery('authors')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # does nothing
app.autodiscover_tasks()  # also does nothing

print('Registering debug task...')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def task(data_to_queue):
    ''' Gets payload from the user and sends it to mail '''
    mail = EmailMessage(
                subject=data_to_queue['subject'],
                body=data_to_queue['message'],
                to=data_to_queue['to'],
                from_email=data_to_queue['from_email']

            )
    mail.content_subtype = "html"
    mail.send()