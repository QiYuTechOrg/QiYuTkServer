from django.http import HttpRequest
from qiyu_api.dtk_api.gen import GoodsNineOpGoodsListArgs

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/goods_nine_op_goods_list",
    tags=["大淘客"],
    summary="9.9包邮",
    description="9.9包邮精选  文档: https://www.dataoke.com/pmc/api-d.html?id=15",
)
async def dtk_goods_nine_op_goods_list(
    request: HttpRequest, g: GoodsNineOpGoodsListArgs
) -> GenericItemListResponseModel:
    logger = get_logger()
    dtk = await get_dtk_std()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_nine_op_goods_list(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
