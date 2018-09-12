
release: python manage.py migrate
web: gunicorn authors.wsgi --log-file -
worker: celery -A authors  worker -l info