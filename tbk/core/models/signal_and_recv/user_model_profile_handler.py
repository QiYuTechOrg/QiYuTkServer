from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from structlog.stdlib import get_logger

from core.webhook import send_webhook_request
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

        json_data = {"username": instance.username}
        send_webhook_request(SConfig.WEBHOOK_NEW_USER, json_data=json_data)
