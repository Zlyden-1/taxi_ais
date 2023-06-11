from .base import *

DEBUG = False

ALLOWED_HOSTS = ['80.78.244.52', '80-78-244-52.cloudvps.regruhosting.ru', '127.0.0.1']

ADMINS = [('Максим Авдошин', 'm.4vdoshin@yandex.ru')]

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