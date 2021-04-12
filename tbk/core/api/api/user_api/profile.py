from typing import Optional

from django.contrib.auth.models import User
from django.http import HttpRequest
from pydantic import Field

from core.dm import UserProfileDataModel
from core.forms import UserTokenForm
from core.logger import get_logger
from core.logic import UserLogic
from core.resp.base import ResponseModel, ApiResp
from ...api.app import app
from ...api_utils import api_ensure_login


class UserProfileResponseModel(ResponseModel):
    data: Optional[UserProfileDataModel] = Field(None, title="详细数据")


# 获取用户自身的状态信息
@app.post(
    "/user/profile",
    tags=["用户"],
    summary="用户信息",
    description="获取用户自己的信息",
)
async def user_profile(
    request: HttpRequest, g: UserTokenForm
) -> UserProfileResponseModel:
    logger = get_logger()

    @api_ensure_login(g.token, logger)
    async def inner(user: User):
        ul = UserLogic(logger)
        data = await ul.profile(user=user)
        return ApiResp.from_data(data)

    return await inner
