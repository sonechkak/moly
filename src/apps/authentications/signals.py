import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger("user.actions")


@receiver(user_logged_in)
def info_user_logged_in(sender, request, user, **kwargs):
    """Сигнал для добавления в лог информации о входе пользователя."""
    logging.info(
        f"Пользователь вошел в систему: {user.username}.",
        extra={
            "username": user.username,
            "email": user.email,
            "ip_address": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        },
    )


@receiver(user_logged_out)
def info_log_user_logged_out(sender, request, user, **kwargs):
    """Сигнал для добавления в лог информации о выходе пользователя."""
    logging.info(
        f"Пользователь вышел из системы: {user.username}.",
        extra={
            "username": user.username,
            "email": user.email,
            "ip_address": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        },
    )


@receiver(user_login_failed)
def info_log_user_login_failed(sender, request, credentials, **kwargs):
    """Сигнал для добавления в лог информации о неуспешном входе пользователя."""
    logging.info(
        f"Пользователь не смог войти: {credentials.get('username')}.",
        extra={
            "username": credentials.get("username"),
        },
    )
