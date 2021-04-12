from typing import Optional

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.dtk_api.gen import GoodsGetGoodsDetailsArgs, GoodsGetGoodsDetailsResp

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkGoodsDetailResponseModel(ResponseModel):
    data: Optional[GoodsGetGoodsDetailsResp] = Field(None, title="详细数据")


@app.post(
    "/dtk/goods_detail",
    tags=["大淘客"],
    summary="单品详情",
    description="",
)
async def dtk_goods_detail(
    request: HttpRequest, args: GoodsGetGoodsDetailsArgs
) -> DtkGoodsDetailResponseModel:
    logger = get_logger()
    dtk = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_get_goods_details(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
