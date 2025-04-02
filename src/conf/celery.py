import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

celery_app = Celery(
    "conf",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.conf.beat_schedule = {
    "send_mail":{
        "task": "apps.subscribers.tasks.send_subscriber_email",
        "schedule": crontab(minute='*/1'),
    }
}

celery_app.conf.update(
    beat_schedule_filename='/tmp/celerybeat-schedule'
)

celery_app.autodiscover_tasks()
