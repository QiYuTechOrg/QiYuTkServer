from typing import List, Optional

from django.http import HttpRequest
from pydantic import Field

from core.logger import get_logger
from core.resp.base import ApiResp, ResponseModel
from core.vendor.ztk import get_ztk_std_api
from ...api.app import app
from ...api_utils import api_inner_wrapper


class KeywordResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="热词/关键字")


@app.get(
    "/ztk/keyword",
    tags=["折淘客"],
    summary="关键词推荐",
    description="",
)
async def ztk_keyword(request: HttpRequest) -> KeywordResponseModel:
    logger = get_logger()
    ztk = await get_ztk_std_api(logger)

    @api_inner_wrapper(logger)
    async def inner():
        data = await ztk.keyword()
        return ApiResp(data=data).to_dict()

    return await inner
