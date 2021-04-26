from typing import Optional

from django.http import HttpRequest
from pydantic import Field, BaseModel

from core.logger import get_logger
from core.logic import SysLogic
from core.resp.base import ResponseModel, ApiResp
from ...api.app import app
from ...api_utils import api_inner_wrapper


class SysConfigDataModel(BaseModel):
    pid: str = Field(..., title="淘宝 PID 配置")


class SysConfigResponseModel(ResponseModel):
    data: Optional[SysConfigDataModel] = Field(None, title="详细数据")


@app.get(
    "/sys/config",
    tags=["配置"],
    summary="系统配置",
    description="返回系统的配置",
)
async def sys_auth(request: HttpRequest) -> SysConfigResponseModel:
    logger = get_logger()

    @api_inner_wrapper(logger)
    async def inner():
        logic = SysLogic(logger)
        data = await logic.get_sys_config()
        return ApiResp.from_data(data)

    return await inner
