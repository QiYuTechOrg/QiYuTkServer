from django_qiyu_utils import EnvHelper

__all__ = ["DB_ENGINE", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]

DB_ENGINE = EnvHelper.get_from_env("DB_ENGINE")
DB_NAME = EnvHelper.get_from_env("DB_NAME")
DB_USER = EnvHelper.get_from_env("DB_USER")
DB_PASSWORD = EnvHelper.get_from_env("DB_PASSWORD")
DB_HOST = EnvHelper.get_from_env("DB_HOST")
DB_PORT = int(EnvHelper.get_from_env("DB_PORT"))
