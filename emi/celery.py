from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

# from tbm.views import glo_subject,glo_message,glo_recipient
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emi.settings')

app = Celery('emi')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'tbm.tasks.delete_one_time_crontab',
        'schedule': crontab(hour=21,minute=27),
    },
}

    