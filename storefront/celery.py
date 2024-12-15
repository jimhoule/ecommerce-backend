from os import environ
from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

celery = Celery()
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()