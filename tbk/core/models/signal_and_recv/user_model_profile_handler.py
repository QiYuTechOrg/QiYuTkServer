import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from structlog.stdlib import get_logger

from tbk.s_config import SConfig
from .. import Profile

__all__ = ["user_model_handler"]


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def user_model_handler(sender, instance: User, created: bool, **kwargs):
    """
    Python 的 signal and slot 函数
    比在 admin 中 保存其他的 StackInline 之前执行
    """
    if created:
        Profile.objects.create(mobile=instance.username, user=instance, nickname="奇遇淘客")
        logger = get_logger("webhook")
        try:
            new_user_webhook = SConfig.WEBHOOK_NEW_USER
            if new_user_webhook is None or new_user_webhook == "":
                return

            user = instance
            # send request to webhook
            resp = requests.post(new_user_webhook, json={"username": user.username}, timeout=(5.0, 5.0))
            if resp.ok:
                return
            logger.warning(f"{new_user_webhook=} {resp=}")
        except Exception as e:
            logger.error(f"new user webhook error: {e=}")
