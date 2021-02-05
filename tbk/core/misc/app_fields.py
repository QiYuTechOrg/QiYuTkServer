from pydantic import Field

__all__ = ["AppFields"]


class AppFields(object):
    token = Field(..., title="认证令牌", description="用户登陆时获取的认证令牌 (aka: token)")
    test = Field(False, title="测试", description="内部使用")
    page = Field(1, title="第几页", description="")
