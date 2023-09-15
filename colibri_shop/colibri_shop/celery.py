import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colibri_shop.settings')

app = Celery('colibri_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
