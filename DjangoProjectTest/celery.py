import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectTest.settings')

app = Celery('DjangoProjectTest')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
