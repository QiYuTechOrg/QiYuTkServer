from typing import Optional

from django.http import HttpRequest
from pydantic import Field

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
)
async def user_cancel(
    request: HttpRequest, g: UserTokenForm
) -> UserCancelResponseModel:
    logger = get_logger()

    @api_inner_wrapper(logger)
    async def inner():
        user = UserV2Logic(logger)
        ret = await user.cancel_user_account(g.token)
        return ApiResp.from_data(ret)

    return await inner
