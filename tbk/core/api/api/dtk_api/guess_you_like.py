from django.http import HttpRequest
from qiyu_api.dtk_api.gen import GoodsExplosiveGoodsListArgs

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/guess_you_like",
    tags=["大淘客"],
    summary="猜你喜欢",
    description="[每日爆品推荐](https://www.dataoke.com/pmc/api-d.html?id=34)",
    response_model=GenericItemListResponseModel,
)
async def dtk_guess_you_like(request: HttpRequest, g: GoodsExplosiveGoodsListArgs):
    logger = get_logger()
    dtk = await get_dtk_std()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_explosive_goods_list(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
