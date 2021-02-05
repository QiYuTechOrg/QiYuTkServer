from typing import Optional, Awaitable

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

__all__ = ["TBChannelIdModel"]


class TBChannelIdModel(models.Model):
    """
    淘宝渠道 ID 表

    这个表里面存储的是已经绑定 渠道 ID 的用户
    """

    class Meta(object):
        verbose_name = "渠道ID"
        verbose_name_plural = "渠道ID"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="那个用户的渠道ID"
    )

    # relation id 和 special id 的区别是:
    # relation id 可以分享 和 自购
    # special  id 只能用来自购

    # 有的用户可能没有 渠道关系 id
    relation_id = models.CharField(
        default=None,
        null=True,
        unique=True,
        max_length=255,
        verbose_name="渠道 ID",
        help_text="淘宝的关系 ID",
    )

    # 有的用户可能没有 会员运营 id
    special_id = models.CharField(
        default=None,
        null=True,
        unique=True,
        max_length=255,
        verbose_name="会员运营 ID",
        help_text="会员运营的 ID",
    )

    ctime = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间", help_text="用户绑定渠道 ID 的时间"
    )

    @staticmethod
    def get_by_relation_id(relation_id: int) -> "TBChannelIdModel":
        """
        根据渠道 ID 获取 绑定的对应关系
        :param relation_id:
        :return:
        :except `ObjectDoesNotExists`
        """
        return TBChannelIdModel.objects.get(relation_id=relation_id)

    @staticmethod
    def get_by_user(user: User) -> Optional["TBChannelIdModel"]:
        return TBChannelIdModel.objects.filter(user=user).first()

    @staticmethod
    @sync_to_async
    def get_by_user_async(user: User) -> Awaitable[Optional["TBChannelIdModel"]]:
        # noinspection PyTypeChecker
        return TBChannelIdModel.get_by_user(user)

    @staticmethod
    def create_or_update(
        user: User, relation_id: Optional[int], special_id: Optional[int]
    ):
        try:
            info: TBChannelIdModel = TBChannelIdModel.objects.get(user=user)
            if info.special_id is None and special_id is not None:
                info.special_id = special_id
            if info.relation_id is None and relation_id is not None:
                info.relation_id = relation_id
            info.save()
        except ObjectDoesNotExist:
            rid = None if relation_id is None else str(relation_id)
            sid = None if special_id is None else str(special_id)
            TBChannelIdModel.objects.create(user=user, relation_id=rid, special_id=sid)

    def __str__(self) -> str:
        return f"{self.user}({self.relation_id})"
