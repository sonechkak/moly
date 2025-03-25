from django.contrib.auth import get_user_model

from .models import Subscribe


User = get_user_model()


class SubscribeService:
    def __init__(self, subscribe: Subscribe):
        self.subscribe = subscribe

    def send_template_mail(self):
        pass

    def send_notification_mail(self):
        pass

    def _send_mail(self, to, subject):
        pass

