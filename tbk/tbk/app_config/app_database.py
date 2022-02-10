import os

from django_qiyu_utils import EnvHelper

__all__ = ["DATABASES"]

if EnvHelper.in_prod():  # production env
    DB_NAME = EnvHelper.get_from_env("DB_NAME")

    DATABASES = {
        "default": {
            "ENGINE": EnvHelper.get_from_env("DB_ENGINE"),
            "NAME": DB_NAME,
            "USER": EnvHelper.get_from_env("DB_USER"),
            "PASSWORD": EnvHelper.get_from_env("DB_PASSWORD"),
            "HOST": EnvHelper.get_from_env("DB_HOST"),
            "PORT": int(EnvHelper.get_from_env("DB_PORT")),
            "DBNAME": DB_NAME,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(os.path.dirname(__file__), "../../../sqlite/db.sqlite3"),
        }
    }
