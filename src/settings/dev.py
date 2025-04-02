from .base import *

db_url  = urlparse(os.getenv("DATABASE_URL", 'postgresql://sonya:sonya@127.0.0.1:5432/moly'))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': db_url.path[1:],
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.hostname,
        'PORT': db_url.port or '5432',
    }
}
