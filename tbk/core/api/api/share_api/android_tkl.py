"""
用户分享淘宝商品
"""
from django.http import HttpRequest

from core.forms import ShareItemTklForm
from core.logger import get_logger
from core.logic import ShareLogic
from core.resp import ShareItemTklResponseModel
from core.resp.base import ApiResp
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/share/android/relation_tkl",
    tags=["分享"],
    summary="Android 使用淘口令分享商品",
    description="用户通过淘口令分享指定的商品\n注意: 这个用户必须绑定渠道ID",
    response_model=ShareItemTklResponseModel,
)
async def share_android_relation_tkl(request: HttpRequest, g: ShareItemTklForm):
    logger = get_logger()

    @api_inner_wrapper(logger)
    async def inner():
        logic = ShareLogic(logger)
        tkl = await logic.share_item(g.item_id, g.token, False)
        logger.bind(tkl=tkl, item_id=g.item_id).info("create tkl")
        return ApiResp.from_data(tkl)

    return await inner
