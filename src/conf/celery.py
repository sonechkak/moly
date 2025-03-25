from celery import Celery
from celery.schedules import crontab

celery_app = Celery()

celery_app.conf.beat_schedule = {
    "send_mail":{
        "task": "apps.subscribers.tasks.send_subscriber_email",
        "schedule": crontab(hour="1"),
    }
}
