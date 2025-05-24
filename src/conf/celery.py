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
    "send_mail": {
        "task": "apps.subscribers.tasks.send_subscriber_email",
        "schedule": crontab(minute="*/1"),
    },
    "send_referral_coupon_email": {
        "task": "apps.subscribers.tasks.send_referral_coupon_email",
        "schedule": crontab(minute="*/1"),
    },
    "check_expired_cashback": {
        "task": "apps.cashback.tasks.check_expiring_cashback",
        "schedule": crontab(minute="*/1"),
    },
}

celery_app.autodiscover_tasks()
