from django.apps import AppConfig

__all__ = ["CoreConfig"]


class CoreConfig(AppConfig):
    name = "core"
    default_auto_field = "django.db.models.BigAutoField"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = "核心模块"
