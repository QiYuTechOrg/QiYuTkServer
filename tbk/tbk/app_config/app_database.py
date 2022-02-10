import os

from django_qiyu_utils import EnvHelper

__all__ = ["DATABASES"]


def _get_databases_config() -> dict:
    """
    获取 数据库配置 增加 DB_USE_SQLITE 环境变量，表示是否使用 SQLite 数据库
    """
    if EnvHelper.in_prod() and os.getenv("DB_USE_SQLITE", "") == "":  # production env
        db_name = EnvHelper.get_from_env("DB_NAME")

        return {
            "default": {
                "ENGINE": EnvHelper.get_from_env("DB_ENGINE"),
                "NAME": db_name,
                "USER": EnvHelper.get_from_env("DB_USER"),
                "PASSWORD": EnvHelper.get_from_env("DB_PASSWORD"),
                "HOST": EnvHelper.get_from_env("DB_HOST"),
                "PORT": int(EnvHelper.get_from_env("DB_PORT")),
                "DBNAME": db_name,
            }
        }

    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(
                os.path.dirname(__file__), "../../../sqlite/db.sqlite3"
            ),
        }
    }


DATABASES = _get_databases_config()
