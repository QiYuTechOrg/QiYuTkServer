from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .. import UserTokenModel


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def user_user_token_handler(sender, instance: User, created: bool, **kwargs):
    """
    禁止用户登陆之后 需要自动删除 token 代码
    """
    if not instance.is_active:  # 禁止用户登陆
        UserTokenModel.objects.filter(user=instance).delete()
