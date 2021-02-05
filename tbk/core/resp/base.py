from dataclasses import dataclass
from typing import TypeVar, Optional, Generic

from pydantic import BaseModel, Field

from core.shared import AppErrno

T = TypeVar("T")

__all__ = ["ApiResp", "ResponseModel", "AppErrno"]


@dataclass
class ApiResp(Generic[T]):
    errno: AppErrno = AppErrno.success
    errmsg: str = "成功"
    data: Optional[T] = None

    @staticmethod
    def from_data(data: T) -> "ApiResp[T]":
        return ApiResp(data=data)

    @staticmethod
    def from_errno(errno: AppErrno, errmsg: Optional[str] = None) -> "ApiResp[int]":
        if errmsg is None:
            return ApiResp(errno=errno, errmsg=str(errno))
        else:
            return ApiResp(errno=errno, errmsg=errmsg)

    @staticmethod
    def system_error():
        return ApiResp.from_errno(AppErrno.system, "系统内部错误, 请联系网站管理员")

    def to_dict(self) -> dict:
        return {"errno": self.errno, "errmsg": self.errmsg, "data": self.data}


class ResponseModel(BaseModel):
    errno: AppErrno = Field(
        ...,
        title="错误码",
        description=""" 0 成功\n
 1 失败\n
 2 系统内部错误\n

10 无效的输入\n
11 认证失败\n

20 没有找到指定的内容\n
21 无效的 token  [客户端收到这个消息应该执行登出操作]\n
22 折淘客请求失败\n
23 用户不存在\n

30 没有发布历史\n

40 没有渠道 ID\n
41 没有找到指定的商品\n

""",
    )
    errmsg: str = Field(..., title="错误信息", description="详细的错误信息")
