from django.urls import path

from .views import (
    save_subscribers,
    send_mail_to_customers,
)


app_name = "subscribers"


urlpatterns = [
    path("subscribe/", save_subscribers, name="subscribe"),
    path("send_mail/", send_mail_to_customers, name="send_mail"),
]