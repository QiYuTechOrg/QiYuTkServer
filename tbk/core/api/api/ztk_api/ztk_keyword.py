from typing import List, Optional

from fastapi import Depends
from pydantic import Field
from structlog.stdlib import BoundLogger
from ztk_api import ZTK

from core.logger import get_logger
from core.resp.base import ApiResp, ResponseModel
from core.vendor.ztk import get_ztk_api_v2
from ...api.app import app
from ...api_utils import api_inner_wrapper


class KeywordResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="热词/关键字")


@app.get(
    "/ztk/keyword",
    tags=["折淘客"],
    summary="关键词推荐",
    description="",
    response_model=KeywordResponseModel,
)
async def ztk_keyword(
    logger: BoundLogger = Depends(get_logger), ztk: ZTK = Depends(get_ztk_api_v2)
):
    @api_inner_wrapper(logger)
    async def inner():
        data = await ztk.keyword()
        return ApiResp(data=data).to_dict()

    return await inner
