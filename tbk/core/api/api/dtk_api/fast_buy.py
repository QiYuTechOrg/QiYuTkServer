from dtk_api import DtkStdApi
from dtk_api.gen import CategoryDdqGoodsListArgs
from fastapi import Depends, Body
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/fast_buy",
    tags=["大淘客"],
    summary="快抢商品",
    description="[大淘客咚咚抢文档](https://www.dataoke.com/pmc/api-d.html?id=23)",
    response_model=GenericItemListResponseModel,
)
async def dtk_fast_buy(
    g: CategoryDdqGoodsListArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkStdApi = Depends(get_dtk_std),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.category_ddq_goods_list(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        out = j[0]
        return ApiResp.from_data(out)

    return await inner
