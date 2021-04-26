from typing import List, Optional

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.ztk_api import SuggestArgs

from core.logger import get_logger
from core.resp.base import ApiResp, ResponseModel
from core.vendor.ztk import get_ztk_api_v2
from ...api.app import app
from ...api_utils import api_inner_wrapper


class SuggestResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="推荐词")


@app.get(
    "/ztk/suggest",
    tags=["折淘客"],
    summary="关键词推荐",
    description="",
)
async def ztk_suggest(request: HttpRequest, content: str) -> SuggestResponseModel:
    logger = get_logger()
    ztk = get_ztk_api_v2(logger)

    @api_inner_wrapper(logger)
    async def inner():
        args = SuggestArgs(content=content)
        j = await ztk.suggest(args)
        return ApiResp.from_data(j).to_dict()

    return await inner
