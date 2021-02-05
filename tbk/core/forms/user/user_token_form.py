from pydantic import BaseModel

from core.misc import AppFields

__all__ = ["UserTokenForm"]


class UserTokenForm(BaseModel):
    """
    用户 token 表单
    """

    token: str = AppFields.token
