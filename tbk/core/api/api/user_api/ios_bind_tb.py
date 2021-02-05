"""
淘宝渠道 ID 绑定 for iOS
Android 使用的是回调的绑定方式
"""

from django.contrib.auth.models import User
from fastapi import Depends, Body
from pydantic import Field, BaseModel
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.logic import TaoBaoLogic
from core.resp.base import ResponseModel, ApiResp
from ...api import fields
from ...api.app import app
from ...api_utils import api_ensure_login


class TbBindResponseModel(ResponseModel):
    data: bool = Field(default=False, title="是否绑定了渠道 ID")


class TbBindForm(BaseModel):
    """
    绑定淘宝渠道ID的参数
    """

    code: str = Field(title="授权的 access code")
    token: str = fields.token


@app.post(
    "/user/bind",
    tags=["用户"],
    summary="iOS用户绑定淘宝渠道ID",
    response_model=TbBindResponseModel,
)
async def user_ios_bind_tb(
    g: TbBindForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
):
    """
    给指定的用户绑定渠道 ID 信息
    """

    @api_ensure_login(g.token, logger)
    async def inner(user: User):
        logic = TaoBaoLogic(logger)
        ret = await logic.ios_try_bind_v2(user, g.code)
        return ApiResp.from_data(ret)

    return await inner
