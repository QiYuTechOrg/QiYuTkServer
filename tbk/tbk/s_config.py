from typing import Awaitable

from asgiref.sync import sync_to_async
from constance import config

__all__ = ["SConfig"]


# noinspection PyPep8Naming
class MyMetaClass(type):
    @property
    def AliPid(cls):
        return config.AliPid

    @property
    def AliAppKey(cls):
        return config.AliAppKey

    @property
    def AliInviteCode(cls):
        return config.AliInviteCode

    @property
    def AliAppSecret(cls):
        return config.AliAppSecret

    ######################################
    # 大淘客配置
    # 折淘客配置
    @property
    def DTKAppKey(cls):
        return config.DTKAppKey

    @property
    def DTKAppSecret(cls):
        return config.DTKAppSecret

    ######################################
    # 折淘客配置
    @property
    def ZTKSid(cls):
        return config.ZTKSid

    @property
    def ZTKAppKey(cls):
        return config.ZTKAppKey


class SConfig(metaclass=MyMetaClass):
    """
    系统配置

    相关配置参见:
    settings 中的 CONSTANCE_CONFIG
    """

    # 阿里 app key 配置
    AliAppKey: str

    @staticmethod
    @sync_to_async
    def async_ali_app_key() -> Awaitable[str]:
        # noinspection PyTypeChecker
        return SConfig.AliAppKey

    # 阿里 app secret 配置
    AliAppSecret: str

    @staticmethod
    @sync_to_async
    def async_ali_app_secret() -> Awaitable[str]:
        # noinspection PyTypeChecker
        return SConfig.AliAppSecret

    # 渠道 ID 邀请码
    AliInviteCode: str

    @staticmethod
    @sync_to_async
    def async_ali_invite_code() -> str:
        return SConfig.AliInviteCode

    # 阿里 PID
    AliPid: str

    @staticmethod
    @sync_to_async
    def async_ali_pid():
        return SConfig.AliPid

    ####################################
    # 大淘客
    DTKAppKey: str

    @staticmethod
    @sync_to_async
    def async_dtk_app_key():
        return SConfig.DTKAppKey

    DTKAppSecret: str

    @staticmethod
    @sync_to_async
    def async_dtk_app_secret():
        return SConfig.DTKAppSecret

    ####################################
    # 折淘客
    # sid
    ZTKSid: str

    @staticmethod
    @sync_to_async
    def async_ztk_sid():
        return SConfig.ZTKSid

    # app key
    ZTKAppKey: str
    ####################################

    ####################################
    # WebHook 配置
    WEBHOOK_NEW_ORDER: str  # 新订单回调
    WEBHOOK_NEW_USER: str  # 新用户调
    WEBHOOK_NEW_BIND: str  # 渠道ID绑定

    ####################################
    # 网页端配置
    WEB_SHOW_COUPON: bool
