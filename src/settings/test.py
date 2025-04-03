from urllib.parse import urlparse

from .base import *

db_url = urlparse(os.getenv("DATABASE_URL", "postgresql://sonya:sonya@db:5432/moly_test"))

SECRET_KEY = "sadliyfgkuafgyligufsliafsguy"
