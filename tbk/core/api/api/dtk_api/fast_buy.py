from django.http import HttpRequest
from qiyu_api.dtk_api.gen import CategoryDdqGoodsListArgs

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
)
async def dtk_fast_buy(
    request: HttpRequest, g: CategoryDdqGoodsListArgs
) -> GenericItemListResponseModel:
    logger = get_logger()
    dtk = await get_dtk_std()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.category_ddq_goods_list(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        out = j[0]
        return ApiResp.from_data(out)

    return await inner
