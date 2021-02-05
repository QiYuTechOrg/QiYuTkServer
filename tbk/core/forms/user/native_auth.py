from pydantic import Field, BaseModel

__all__ = ["UserNativeAuthForm"]


class UserNativeAuthForm(BaseModel):
    """
    原生 账号/密码 认证
    """

    username: str = Field(..., title="账号", description="用户的奇遇淘客账号")
    password: str = Field(..., title="密码", description="用户的奇遇淘客密码")
