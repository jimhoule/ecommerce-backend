from os import environ
from .common import *


DEBUG = False

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    '',
]

# CORS
CORS_ALLOWED_ORIGINS = [
    '',
]

# EMAIL
EMAIL_HOST = environ.get('EMAIL_HOST')
EMAIL_HOST_USER = environ.get('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_PASSWORD')
EMAIL_PORT = environ.get('EMAIL_PORT')

ADMINS = [
    ('Admin', environ.get('EMAIL_ADMIN_SENDER')),
]

# DB
DATABASES['default']['NAME'] = environ.get('DB_NAME')
DATABASES['default']['USER'] = environ.get('DB_USERNAME')
DATABASES['default']['PASSWORD'] = environ.get('DB_PASSWORD')
DATABASES['default']['HOST'] = environ.get('DB_HOST')
DATABASES['default']['PORT'] = environ.get('DB_PORT')

# CELERY
CELERY_BROKER_URL = environ.get('BROKER_URL')

# CACHE
CACHES['default']['LOCATION'] = environ.get('CACHE_URL')

# LOGGING
LOGGING['loggers']['']['level'] = environ.get('DJANGO_LOG_LEVEL')