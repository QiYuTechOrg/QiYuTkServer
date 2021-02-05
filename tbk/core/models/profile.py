from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    用户的 概述 信息
    """

    class Meta(object):
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
        help_text="用户的信息",
        editable=False,
    )

    # 昵称
    nickname = models.CharField(
        max_length=64, verbose_name="昵称", help_text="用户的昵称", editable=False
    )

    # 手机号
    # iOS 可以没有这个字段表示使用的是原生账号登陆
    mobile = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="手机号",
        help_text="用户的手机号",
        editable=False,
    )

    # 用户绑定的微信账号
    wx = models.CharField(
        max_length=255,
        null=True,
        default=None,
        verbose_name="微信",
        help_text="用户的微信号码",
        editable=False,
    )

    # 淘宝的 id
    tao_id = models.CharField(
        max_length=1024,
        default=None,
        null=True,
        verbose_name="淘宝 ID",
        help_text="当前绑定淘宝授权的 ID, 没有绑定的时候为空",
        editable=False,
    )

    test_account = models.BooleanField(
        default=False,
        verbose_name="测试账号",
        help_text="这个账号是否为测试账号, 后台管理对测试账号有更多的管理权限, 例如: 创建虚拟订单, 修改账户金额等",
    )

    def __str__(self) -> str:
        return self.mobile
