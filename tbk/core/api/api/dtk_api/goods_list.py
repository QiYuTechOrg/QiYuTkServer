from dtk_api import DtkStdApi
from dtk_api.gen import GoodsGetGoodsListArgs
from fastapi import Body, Depends
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/goods_list",
    tags=["大淘客"],
    summary="商品列表",
    description="实际接口: https://www.dataoke.com/pmc/api-d.html?id=5",
    response_model=GenericItemListResponseModel,
)
async def dtk_goods_lists(
    args: GoodsGetGoodsListArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkStdApi = Depends(get_dtk_std),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_get_goods_list(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
