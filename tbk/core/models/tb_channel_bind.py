from typing import Optional

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

__all__ = ["TBChannelBindModel"]


class TBChannelBindModel(models.Model):
    """
    淘宝渠道 ID 绑定表

    这个表里面存储的都是 准备绑定渠道 ID 的信息
    """

    class Meta(object):
        verbose_name = "渠道ID绑定"
        verbose_name_plural = "渠道ID绑定"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="哪个用户尝试绑定渠道ID的"
    )

    state = models.CharField(
        unique=True, max_length=128, verbose_name="随机状态", help_text="当前用户的随机状态"
    )

    ctime = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间", help_text="这条记录的创建时间"
    )

    @staticmethod
    @sync_to_async
    def add_or_update_async(user: User, state: str):
        TBChannelBindModel.objects.update_or_create(
            {"user": user, "state": state}, user=user
        )

    @staticmethod
    def get_user_by_state(state: str) -> Optional[User]:
        info = TBChannelBindModel.objects.filter(state=state).first()
        if info is None:
            return None
        return info.user

    def __str__(self) -> str:
        return f"{self.user}"
