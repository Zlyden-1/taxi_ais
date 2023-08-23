import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxi_ais.settings')
app = Celery('taxi_ais')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
