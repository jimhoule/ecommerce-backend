from os import environ
from .common import *


DEBUG = False

SECRET_KEY = environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    '',
]