from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taxi_ais',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': '',
    }
}