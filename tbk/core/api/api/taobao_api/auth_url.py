from typing import Optional

from django.http import HttpRequest
from pydantic import Field, BaseModel

from core.logger import get_logger
from core.logic import TaoBaoLogic
from core.resp.base import ResponseModel, ApiResp
from .. import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class AuthUrlDataModel(BaseModel):
    url: str = Field(..., title="要绑定的 URL")


class AuthUrlForm(BaseModel):
    token: str = fields.token


class TaoBaoAuthUrlResponseModel(ResponseModel):
    data: Optional[AuthUrlDataModel] = Field(None, title="详细数据")


@app.post(
    "/taobao/auth_url",
    tags=["淘宝"],
    summary="渠道ID绑定配置",
    description="返回绑定的渠道 ID URL, 授权直接用 showUrlPage 打开页面即可",
)
async def auth_url(request: HttpRequest, g: AuthUrlForm) -> TaoBaoAuthUrlResponseModel:
    logger = get_logger()

    @api_inner_wrapper(logger)
    async def inner():
        logic = TaoBaoLogic(logger)
        data = await logic.get_bind_channel_id_url(g.token)
        return ApiResp.from_data(data)

    return await inner
