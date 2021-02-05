import secrets
from typing import Optional, Awaitable

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

__all__ = ["UserTokenModel"]


class UserTokenModel(models.Model):
    """
    用户 认证令牌 模块

    每一个用户可以有一个令牌 用来访问 fastAPI 的接口
    """

    class Meta(object):
        verbose_name = "令牌"
        verbose_name_plural = "令牌"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户"
    )

    token = models.TextField(
        max_length=256, verbose_name="token", help_text="用户的 token"
    )

    ctime = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间", help_text="用户第一个创建 token 的时间"
    )

    mtime = models.DateTimeField(
        auto_now=True, verbose_name="修改时间", help_text="用户最近修改 token 的时间"
    )

    @staticmethod
    @sync_to_async
    def get_user_by_token_async(token: str) -> Awaitable[Optional[User]]:
        # noinspection PyTypeChecker
        return UserTokenModel.get_user_by_token(token)

    @staticmethod
    def create_or_update(user: User) -> str:
        token = secrets.token_hex(32)
        UserTokenModel.objects.update_or_create(
            user=user, defaults={"token": token, "user": user}
        )
        return token

    @staticmethod
    def get_user_by_token(token: str) -> Optional[User]:
        ret: Optional[UserTokenModel] = UserTokenModel.objects.filter(
            token=token
        ).first()
        if ret is None:
            return None
        return ret.user

    def __str__(self) -> str:
        return f"{self.user}({self.mtime})"
