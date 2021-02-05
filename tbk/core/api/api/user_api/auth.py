from typing import Optional

from fastapi import Depends, Body
from pydantic import Field
from structlog.stdlib import BoundLogger

from core.dm.user import UserNativeAuthDataModel
from core.forms.user import UserNativeAuthForm
from core.logger import get_logger
from core.logic import UserV2Logic
from core.resp.base import ResponseModel
from core.shared import AppErrno
from ...api.app import app


class UserAuthResponseModel(ResponseModel):
    data: Optional[UserNativeAuthDataModel] = Field(None, title="详细数据")


# 获取用户自身的状态信息
@app.post(
    "/user/auth",
    tags=["用户"],
    summary="用户认证息",
    description="用户登录",
    response_model=UserAuthResponseModel,
)
async def user_auth(
    g: UserNativeAuthForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
):
    ul = UserV2Logic(logger)
    token = await ul.auth(username=g.username, password=g.password)
    if token is None:
        return UserAuthResponseModel(
            errno=AppErrno.auth_failed, errmsg=str(AppErrno.auth_failed)
        )
    return UserAuthResponseModel(
        errno=AppErrno.success, errmsg="", data=UserNativeAuthDataModel(token=token)
    )
