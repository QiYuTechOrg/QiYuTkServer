from django_qiyu_utils import EnvHelper

__all__ = ["get_cb_url"]


def get_cb_url() -> str:
    """
    获取淘宝重新重定向的 地址
    :return:
    """
    return EnvHelper.get_from_env("ADMIN_HOST") + "/taobao/cb"
