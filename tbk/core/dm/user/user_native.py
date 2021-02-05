from pydantic.main import BaseModel

from . import fields

__all__ = ["UserNativeAuthDataModel"]


class UserNativeAuthDataModel(BaseModel):
    """
    原生认证返回的数据
    """

    token: str = fields.token
