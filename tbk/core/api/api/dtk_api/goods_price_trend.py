from typing import Optional

from dtk_api import DtkAsyncApi
from dtk_api.gen import GoodsPriceTrendResp, GoodsPriceTrendArgs
from fastapi import Body
from fastapi import Depends
from pydantic import Field
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkGoodsPriceTrendResponseModel(ResponseModel):
    data: Optional[GoodsPriceTrendResp] = Field(None, title="详细数据")


@app.post(
    "/dtk/goods_price_trend",
    tags=["大淘客"],
    summary="商品历史券后价",
    description="",
    response_model=DtkGoodsPriceTrendResponseModel,
)
async def dtk_goods_price_trend(
    args: GoodsPriceTrendArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkAsyncApi = Depends(get_dtk_async),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_price_trend(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
