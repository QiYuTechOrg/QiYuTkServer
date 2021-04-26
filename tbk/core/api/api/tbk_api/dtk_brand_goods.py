from django.http import HttpRequest

from core.forms.tbk import TbkBrandGoodsForm
from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/tbk/dtk/brand_goods",
    tags=["淘宝客"],
    summary="大淘客品牌商品列表",
)
async def tbk_dtk_brand_goods(
    request: HttpRequest, args: TbkBrandGoodsForm
) -> GenericItemListResponseModel:
    """
    获取淘宝客的单品详情
    """
    logger = get_logger()
    tbk = await get_dtk_std()

    @api_inner_wrapper(logger)
    async def inner():
        j = await tbk.get_brand_goods(args.brand_id, args.page_id)
        return ApiResp.from_data(j)

    return await inner
