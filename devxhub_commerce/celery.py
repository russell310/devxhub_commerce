from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devxhub_commerce.settings')

app = Celery('devxhub_commerce')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'send_order_confirmation': {
        'task': 'send_confirmation_email',
        'schedule': crontab(minute='*/1'),
        'options': {
            'expires': 2 * 60,
        },
    },
}

app.autodiscover_tasks()

# celery -A devxhub_commerce worker --pool=solo -l info
# celery -A devxhub_commerce beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

