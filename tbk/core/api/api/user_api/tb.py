from typing import Optional

from fastapi import Depends, Body
from pydantic import Field
from structlog.stdlib import BoundLogger

from core.forms import UserTokenForm
from core.logger import get_logger
from core.logic import UserV2Logic
from core.resp.base import ResponseModel, ApiResp
from ...api.app import app
from ...api_utils import api_inner_wrapper


class UserTbResponseModel(ResponseModel):
    data: Optional[bool] = Field(None, title="是否绑定了淘宝")


@app.post(
    "/user/tb",
    tags=["用户"],
    summary="用户是否已经进行淘宝认证",
    description="用户是否已经进行淘宝认证",
    response_model=UserTbResponseModel,
)
async def user_tb(
    g: UserTokenForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
):
    @api_inner_wrapper(logger)
    async def inner():
        logic = UserV2Logic(logger)
        await logic.ensure_bind_tb(g.token)
        return ApiResp.from_data(True)

    return await inner
