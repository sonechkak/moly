from pathlib import Path

import pyotp
from django.utils.text import slugify


def generate_totp_uri(user, secret_key):
    return pyotp.totp.TOTP(secret_key).provisioning_uri(name=user.username or user.email, issuer_name="moly")


def get_avatar_upload_path(instance, filename):
    """Для загрузки изображений в папку avatars."""
    try:
        path = Path(filename)
        # path.stem - имя файла без расширения
        # path.suffix - расширение с точкой
        safe_name = f"{slugify(path.stem)}{path.suffix.lower()}"
    except ValueError:
        safe_name = filename

    return f"upload/avatars/{instance.pk}/{safe_name}"
