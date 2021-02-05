from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .. import Profile

__all__ = ["user_profile_handler"]


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def user_profile_handler(sender, instance: User, created: bool, **kwargs):
    """
    Python 的 signal and slot 函数
    比在 admin 中 保存其他的 StackInline 之前执行
    """
    if created:
        Profile.objects.create(mobile=instance.username, user=instance, nickname="奇遇淘客")
