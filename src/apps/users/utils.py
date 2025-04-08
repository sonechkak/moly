from pathlib import Path

from django.utils.text import slugify


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
