from typing import Optional, List

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.dtk_api import DtkAsyncApi
from qiyu_api.dtk_api.gen import GoodsSearchSuggestionArgs

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkSearchSuggestionResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="详细数据")


@app.post(
    "/dtk/search_suggestion",
    tags=["大淘客"],
    summary="搜索联想词",
    description="[搜索联想词文档](https://www.dataoke.com/pmc/api-d.html?id=18)",
    response_model=DtkSearchSuggestionResponseModel,
)
async def dtk_search_suggestion(request: HttpRequest, g: GoodsSearchSuggestionArgs):
    logger = get_logger()
    dtk: DtkAsyncApi = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_search_suggestion(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        ret_list = []
        for data in j:
            ret_list.append(data.kw)
        return ApiResp.from_data(ret_list)

    return await inner
