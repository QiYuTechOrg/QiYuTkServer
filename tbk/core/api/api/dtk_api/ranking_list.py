from fastapi import Depends, Body
from qiyu_api.dtk_api import DtkStdApi
from qiyu_api.dtk_api.gen import GoodsGetRankingListArgs
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/ranking_list",
    tags=["大淘客"],
    summary="各大榜单",
    description="[大淘客各大榜单接口](https://www.dataoke.com/pmc/api-d.html?id=6)",
    response_model=GenericItemListResponseModel,
)
async def dtk_ranking_list(
    args: GoodsGetRankingListArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkStdApi = Depends(get_dtk_std),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_get_ranking_list(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
