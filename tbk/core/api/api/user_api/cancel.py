from typing import Optional

from fastapi import Depends, Body
from pydantic import Field
from structlog.stdlib import BoundLogger

from core.forms import UserTokenForm
from core.logger import get_logger
from core.logic import UserV2Logic
from core.resp.base import ApiResp, ResponseModel
from ...api.app import app
from ...api_utils import api_inner_wrapper


class UserCancelResponseModel(ResponseModel):
    data: Optional[bool] = Field(None, title="是否已经注销")


@app.post(
    "/user/cancel",
    tags=["用户"],
    summary="用户注销",
    description="注销自己的用户",
    response_model=UserCancelResponseModel,
)
async def user_cancel(
    g: UserTokenForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
):
    @api_inner_wrapper(logger)
    async def inner():
        user = UserV2Logic(logger)
        ret = await user.cancel_user_account(g.token)
        return ApiResp.from_data(ret)

    return await inner
