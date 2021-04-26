from typing import Optional, List

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.dtk_api import DtkAsyncApi
from qiyu_api.dtk_api.gen import TbServiceGetBrandListArgs, TbServiceGetBrandListResp

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkBrandListResponseModel(ResponseModel):
    data: Optional[List[TbServiceGetBrandListResp]] = Field(None, title="详细数据")


@app.post(
    "/dtk/brand_list",
    tags=["大淘客"],
    summary="超值大牌",
    description="[大淘客品牌库文档](https://www.dataoke.com/pmc/api-d.html?id=17)",
)
async def dtk_tb_service_get_brand_list(
    request: HttpRequest, g: TbServiceGetBrandListArgs
) -> DtkBrandListResponseModel:
    logger = get_logger()

    dtk: DtkAsyncApi = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.tb_service_get_brand_list(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
