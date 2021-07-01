from django_qiyu_utils import EnvHelper

__all__ = ["CONSTANCE_BACKEND", "CONSTANCE_CONFIG", "CONSTANCE_CONFIG_FIELDSETS"]

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "AliAppKey": (
        EnvHelper.get_from_env("ALI_APP_KEY"),
        """APP Key 配置\n
在 淘宝开放平台的 控制台-应用管理-管理-概览 的APP证书中可以找到""",
        str,
    ),
    "AliAppSecret": (
        EnvHelper.get_from_env("ALI_APP_SECRET"),
        """APP Secret 配置\n
在 淘宝开放平台的 控制台-应用管理-管理-概览 的APP证书中可以找到""",
        str,
    ),
    "AliPid": (EnvHelper.get_from_env("ALI_PID"), "pid 配置", str),
    "AliInviteCode": (EnvHelper.get_from_env("ALI_INVITE_CODE"), "渠道ID邀请码", str),
    # 大淘客配置
    "DTKAppKey": (EnvHelper.get_from_env("DTK_APP_KEY"), "大淘客 APP Key", str),
    "DTKAppSecret": (EnvHelper.get_from_env("DTK_APP_SECRET"), "大淘客 App Secret", str),
    # 折淘客配置
    "ZTKSid": (EnvHelper.get_from_env("ZTK_SID"), "折淘客 sid", str),
    "ZTKAppKey": (EnvHelper.get_from_env("ZTK_APP_KEY"), "折淘客 App Key", str),
    # 其他配置
    "WEBHOOK_NEW_ORDER": (EnvHelper.get_from_env("WEBHOOK_NEW_ORDER"), "新订单的 WebHook", str),
    "WEBHOOK_NEW_USER": (EnvHelper.get_from_env("WEBHOOK_NEW_USER"), "新用户的 WebHook", str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "淘宝客": {
        "fields": ("AliPid", "AliAppKey", "AliAppSecret", "AliInviteCode"),
        "collapse": True,
    },
    "折淘客": {"fields": ("ZTKSid", "ZTKAppKey"), "collapse": True},
    "大淘客": {"fields": ("DTKAppKey", "DTKAppSecret"), "collapse": True},
    "WebHook": {"fields": ("WEBHOOK_NEW_ORDER", "WEBHOOK_NEW_USER"), "collapse": True},
}
