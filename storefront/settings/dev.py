from mimetypes import add_type

from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-qfw-t8pkc+=uoiil_r@!g!p!xc7fvc+ps0u$*yk#d)tpm*t8(0'

# MIDDLEWARES
MIDDLEWARE = (
	['debug_toolbar.middleware.DebugToolbarMiddleware']
	+ MIDDLEWARE
	+ ['silk.middleware.SilkyMiddleware']
)

# DEBUG TOOLBARD
INTERNAL_IPS = [
	# ...
	'127.0.0.1',
	# ...
]

# NOTE: Solves a display bug in Django Toolbar
add_type('application/javascript', '.js', True)
DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# CORS
CORS_ALLOWED_ORIGINS = [
	'http://localhost:5001',
]

# EMAIL
EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

ADMINS = [
	('Admin', 'admin@test.com'),
]

# DB
DATABASES['default']['NAME'] = 'storefront'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = 'postgres'
DATABASES['default']['PORT'] = 5432

# CELERY
CELERY_BROKER_URL = 'redis://redis:6379/1'

# CACHE
CACHES['default']['LOCATION'] = 'redis://redis:6379/2'

# LOGGING
LOGGING['loggers']['']['level'] = 'INFO'
