import os

from django.apps import AppConfig
from django.dispatch import receiver

__all__ = ["WebConfig"]


def auto_update_ztk_app_key_env():
    """
    this is ugly hack (todo removed)

    auto update ZTK_APP_KEY environment ()
    """
    from constance.signals import config_updated
    from tbk.s_config import SConfig

    key_ztk_app_key = "ZTK_APP_KEY"

    env_app_key = os.getenv(key_ztk_app_key, "").strip()
    # 我们优先使用 constance 配置的值
    config_app_key = SConfig.ZTKAppKey
    if config_app_key and env_app_key == "":
        os.environ[key_ztk_app_key] = config_app_key

    @receiver(config_updated)
    def constance_updated(sender, key, old_value, new_value, **kwargs):
        """当 constance 更新时候，我们也需要更新环境变量"""
        if key == key_ztk_app_key:  # ignore other key update
            os.environ[key_ztk_app_key] = new_value


class WebConfig(AppConfig):
    name = "web"
    default_auto_field = "django.db.models.BigAutoField"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.verbose_name = "Web应用"

    def ready(self):
        """
        环境变量 HOOK

        :doc https://django-constance.readthedocs.io/en/latest/#signals
        """
        auto_update_ztk_app_key_env()
