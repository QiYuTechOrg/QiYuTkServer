from typing import Optional, List

from pydantic import Field

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkTop100ResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="详细数据")


@app.get(
    "/dtk/top_100",
    tags=["大淘客"],
    summary="热搜记录",
    description="",
    response_model=DtkTop100ResponseModel,
)
async def dtk_top_100():
    logger = get_logger()
    dtk = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.category_get_top100()
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j.hotWords)

    return await inner
