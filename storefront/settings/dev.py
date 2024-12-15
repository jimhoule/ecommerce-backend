from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-qfw-t8pkc+=uoiil_r@!g!p!xc7fvc+ps0u$*yk#d)tpm*t8(0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'storefront', 
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost', 
        'PORT': 5435,
    }
}