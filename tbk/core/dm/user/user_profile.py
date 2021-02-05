from typing import Optional

from pydantic import BaseModel, Field

from . import fields

__all__ = ["UserProfileDataModel"]


class UserProfileDataModel(BaseModel):
    mobile: str = fields.mobile
    tao_id: Optional[str] = fields.tao_id
    wx: Optional[str] = Field(None, title="微信")
    relation_id: Optional[str] = Field(None, title="淘宝渠道ID")
    ali_name: Optional[str] = Field(None, title="支付宝姓名")
    ali_account: Optional[str] = Field(None, title="支付宝账号")
