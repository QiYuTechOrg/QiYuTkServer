from pydantic import BaseModel, Field

from core.misc import AppFields

__all__ = ["UserBindWxForm", "UserBindAliPayForm"]


class UserBindWxForm(BaseModel):
    """
    用户绑定微信表单
    """

    token: str = AppFields.token
    wx: str = Field(..., title="微信号码")


class UserBindAliPayForm(BaseModel):
    token: str = AppFields.token
    ali_name: str = Field(..., title="支付宝姓名")
    ali_account: str = Field(..., title="支付宝账号")
