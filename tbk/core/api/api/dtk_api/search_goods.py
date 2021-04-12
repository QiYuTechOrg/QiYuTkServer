from django.http import HttpRequest
from qiyu_api.dtk_api.gen import GoodsGetDtkSearchGoodsArgs

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/search_goods",
    tags=["大淘客"],
    summary="大淘客搜索",
    description="",
    response_model=GenericItemListResponseModel,
)
async def dtk_search_goods(request: HttpRequest, args: GoodsGetDtkSearchGoodsArgs):
    logger = get_logger()
    dtk = await get_dtk_std()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_get_dtk_search_goods(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
