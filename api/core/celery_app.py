import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("drm")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add the periodic task to the beat schedule
app.conf.beat_schedule = {
    'periodically-kick-expired-users': {
        'task': 'orders.tasks.periodically_kick_expired_users',
        'schedule': crontab(hour=1, minute=0),  # Run every 10 minutes (in seconds)
    },
    'sending-notify-for-expiration-users': {
            'task': 'orders.tasks.sending_notify_for_expiration_users',
            'schedule': crontab(hour=7, minute=0),  # Run every 10 minutes (in seconds)
    },
}
