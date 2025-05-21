def get_loyalty_level_icon_path(instance, filename):
    """Генерирует путь для сохранения изображения уровня лояльности."""
    return f"loyalty/levels/{instance.slug}/{filename}"
