from django.apps import AppConfig

__all__ = ["WebConfig"]


class WebConfig(AppConfig):
    name = "web"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = "Web应用"
